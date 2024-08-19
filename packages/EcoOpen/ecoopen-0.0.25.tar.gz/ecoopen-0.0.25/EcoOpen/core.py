from habanero import Crossref
import numpy as np
import re
from tqdm import tqdm
import pandas as pd
import itertools
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import pathlib
from time import sleep
from tika import parser
from pprint import pprint
from tqdm import tqdm
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from EcoOpen.inference import get_inference
from EcoOpen.utils.keywords import keywords
from EcoOpen.data_download import *


def find_papers(query="", doi=[], number_of_papers=100, start_year=2010, end_year=datetime.now().year+1, sort="relevance", order="desc"):
    number_of_papers = int(number_of_papers)
    cr = Crossref()
    if query != "":
        papers = cr.works(query=query, limit=number_of_papers, filter = {'from-pub-date': str(start_year), 'until-pub-date': str(end_year)}, sort=sort)
    elif doi != []:
        cr = Crossref()
        papers = cr.works(ids=doi)
    else:
        raise ValueError("Please provide a keyword, doi, title or author")
    
    dataframe = {
        "doi":[],
        "title":[],
        "authors":[],
        "published":[],
        "link":[],
    }   
    
    if type(papers) == dict:
    
        for paper in papers["message"]["items"]:
            # fill the dataframe. if the certain key is not present add empty string
            try:
                dataframe["doi"].append(paper["DOI"])
            except KeyError:
                dataframe["doi"].append("")
            try:
                dataframe["title"].append(paper["title"][0])
            except KeyError:
                dataframe["title"].append("")
            try:
                authors = ""
                for author in paper["author"]:
                    authors += author["given"] + " " + author["family"] + ", "
                authors = authors[:-2]
            
                dataframe["authors"].append(authors)
            except KeyError:
                dataframe["authors"].append("")
            try:
                dataframe["published"].append(paper["published"]["date-parts"][0])
            except KeyError:
                dataframe["published"].append("")
            try:
                dataframe["link"].append(paper["link"][0]["URL"])
            except KeyError:
                dataframe["link"].append("")
    elif type(papers) == list:
        for p in papers:
            # fill the dataframe. if the certain key is not present add empty string
            
            paper = p["message"]
            try:
                dataframe["doi"].append(paper["DOI"])
            except KeyError:
                dataframe["doi"].append("")
            try:
                dataframe["title"].append(paper["title"][0])
            except KeyError:
                dataframe["title"].append("")
            try:
                authors = ""
                for author in paper["author"]:
                    authors += author["given"] + " " + author["family"] + ", "
                authors = authors[:-2]
            
                dataframe["authors"].append(authors)
            except KeyError:
                dataframe["authors"].append("")
            try:
                dataframe["published"].append(paper["published"]["date-parts"][0])
            except KeyError:
                dataframe["published"].append("")
            try:
                dataframe["link"].append(paper["link"][0]["URL"])
            except KeyError:
                dataframe["link"].append
    
    return pd.DataFrame(dataframe)
    # return papers
    
def get_journal_info(journal_name):
    cr = Crossref()
    journal = cr.journals(query=journal_name)
    return journal

def get_paper_by_keyword(keyword):
    cr = Crossref()
    papers = cr.works(query=keyword)
    return papers

def get_papers(journal_list="available_journals.csv"):
    df = pd.read_csv(journal_list, index_col=0)
    df = df.dropna()
    df = df.reset_index()
    # print(df)

    for i in range(200, len(df)):
        # i = 101
        journal_title = df["Title"][i]
        expected_papers = df["Number of papers since 2010"][i]
        issn = df["ISSN"][i]
        issn = issn.replace("'", "")
        issn = issn.replace("[", "").replace("]", "")
        issn = issn.replace(" ", "").split(",")

        print(issn)

        noffsets=1
        if expected_papers/1000 >=1:
            noffsets = expected_papers//1000
        # jinfo = get_papers(issn)
        cr = Crossref()
        print(f"Searching for papers in {journal_title} since 01-01-2010")
        for iss in issn:
            jinfo = cr.journals(
                ids=issn,
                works=True,
                sort="published",
                order="asc",
                cursor="*",
                cursor_max=int(expected_papers),
                filter = {'from-pub-date': '2010-01-01'},
                progress_bar = True,
                limit=1000)

            print(type(jinfo))
            print(iss)

            if type(jinfo) == dict:
                items = jinfo["message"]["items"]
                if len(items) > 0:
                    break
            else:
                print(sum(len(z["message"]["items"]) for z in jinfo))

                items = [z["message"]["items"] for z in jinfo]
                items = list(itertools.chain.from_iterable(items))

        papers = {}

        keys = [
            "title",
            "published",
            "DOI",
            "type",
            #"abstract",
            "link",
            "is-referenced-by-count",
            "publisher",
            "author" # TODO: format
        ]
        for key in keys:
            papers[key] = []
        n=1
        for item in items:
            for key in keys:
                try:
                    value = item[key]
                    if key=="title":
                        value = value[0]
                    elif key in ("published", "issued"):
                        value = value["date-parts"][0]
                        if len(value) == 3:
                            value = f"{value[0]}-{value[1]}-{value[2]}"
                        elif len(value) == 2:
                            value = f"{value[0]}-{value[1]}"
                        else:
                            value = f"{value[0]}"
                    elif key == "link":
                        for v in value:
                            # print(v["URL"])
                            if "xml" not in v["URL"]:
                                value = v["URL"]
                            if "pdf" in v["URL"]:
                                value = v["URL"]
                                break
                            else:
                                value="no link"

                    if key == "author":
                        author_string=""
                        for a in value:
                            author_string+=a["given"] + " "
                            author_string+=a["family"]
                            if a["affiliation"] != []:
                                author_string+=" (" + str(a["affiliation"][0]["name"]) + "),"                    
                        value= author_string

                    papers[key].append(value)
                except KeyError:
                    # print(f"KeyError: {key}")
                    if key == "link":
                        key="URL"
                        try:
                            papers["link"].append(item[key])
                        except KeyError:
                            papers[key].append("")
                    else:
                        papers[key].append("")

            #print([item[k] for k in keys])

        jdf = pd.DataFrame(papers)
        jj = journal_title.replace(" ", "_")
        idx_ = i+1
        jdf.to_csv(f"data/papers/{idx_:03d}_{jj}.csv", sep=",", quoting=2)

    return "done!"


def custom_tokenizer(text):
    pattern = r"(?u)\b\w\w+\b[!]*"
    return re.findall(pattern, text) 

def gather_journal_info(list_of_journals, path_to_save=None):
    ISSNs = []
    titles = []
    query = []
    available = []
    dois = []
    number_of_papers_since_2010 = []
    journals = tqdm(list_of_journals, colour="green")

    for i in journals:
        jinfo = get_journal_info(i)

        if jinfo['message']["total-results"] > 0:

            # find item wit the most similar title
            # finding the right journal
            # in majority of cases the idx of the most similar journal title
            # will be 0, however sometimes API returns more popular journal
            # title as the first choice therefore an similarity checks between
            # query and result needs to be performed
            titles_ = [j["title"] for j in jinfo["message"]["items"]]
            qq = i
            vectorizer = TfidfVectorizer(
                tokenizer=custom_tokenizer, token_pattern=None)
            combined_list = titles_ + [qq]
            tfidf_matrix = vectorizer.fit_transform(combined_list)
            # print(tfidf_matrix)
            cosine_sim = cosine_similarity(
                tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

            idx = cosine_sim.argmax()
            # sanity check
            # if idx!=0:
            #     print(titles_)
            #     print(cosine_sim)
            ### idx points to the most similiar title
            
            available.append(1)
            ISSNs.append(jinfo['message']['items'][idx]['ISSN'])
            titles.append(jinfo['message']['items'][idx]['title'])
            
            npapers = 0
            dj = jinfo[
                "message"
                ]["items"][idx]["breakdowns"]["dois-by-issued-year"]
            for year in dj:
                if int(year[0]) >= 2010:
                    npapers += year[1]
            number_of_papers_since_2010.append(npapers)
            # print(
            #     i, "|",
            #     jinfo['message']["total-results"], "|",
            #     npapers, "|",
            #     titles[-1], "|",
            #     idx)
            res = jinfo['message']["total-results"]
            journals.set_description(
                f"{i} | {res} | {npapers} | {titles[-1]} | {idx}"
                )

        else:
            available.append(0)
            ISSNs.append("")
            titles.append("")
            number_of_papers_since_2010.append("")
            # print(
            #     i,
            #     jinfo['message']["total-results"]
            #     )
            journals.set_description(f"{i} | no result found")
        query.append(i)

    df = pd.DataFrame({
        "Journal query": query,
        "Title": titles,
        "ISSN": ISSNs,
        "Available": available,
        "Number of papers since 2010": number_of_papers_since_2010
    })
    # drop duplicate rows
    # df.drop_duplicates()
    if path_to_save:
        df.to_csv(path_to_save)
    return df

def download_paper(doi, output_dir):
    output_dir = Path(os.path.expanduser(output_dir))
    output_dir = output_dir.absolute()
    print(output_dir)
    cr = Crossref()
    doi = doi
    paper = cr.works(ids=doi)

    # print(paper)
    try:
        title = paper["message"]["title"][0]
    except KeyError:
        title = ""

    if "link" in paper["message"]:
        download_link = paper["message"]["link"][0]["URL"]
    elif "URL" in paper["message"]:
        download_link = paper["message"]["URL"]
        download_link = find_pdf(download_link)
    else:
        print("No download link found")
        download_link = ""

    print(download_link)
    if not os.path.exists(output_dir):
        os.system(f"mkdir {output_dir}")

    existing_papers = list(Path(f"{output_dir}").glob("**/*.pdf"))

    if "pdf" in download_link:
        os.system(f"wget --trust-server-names -O {output_dir}/{title.replace(' ', '_').replace('.', '_')}.pdf  {download_link}")
        new_path = f'{output_dir}/{title.replace(" ", "_").replace(".","_")}.pdf'
    else:
        os.system(f"python -m PyPaperBot --doi='{doi}' --dwn-dir='{output_dir}'")
        try:
            os.remove(f"{output_dir}/bibtex.bib")
            result = pd.read_csv(f"{output_dir}/result.csv")
            new_path = f'{output_dir}/{result["PDF Name"][0]}'
            # rename the downloaded file
            new_path = new_path.replace(" ", "_")
            os.rename(f"{output_dir}/{result['PDF Name'][0]}", new_path)
            os.remove(f"{output_dir}/result.csv")

        except FileNotFoundError:
            pass

    all_papers = list(Path(f"{output_dir}").glob("**/*.pdf"))
    if Path(new_path).exists():
        # get path to the downloaded file that was not present before
        print("Download successful")
        return new_path
    else:
        print("Download failed")
        return None

def find_pdf(url):
    # Requests URL and get response object
    response = requests.get(url)
    # print(response.url)

    # Parse text obtained
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlinks present on webpage
    links = soup.find_all('a')

    i = 0

    # From all links check for pdf link and
    # if present download file
    the_link = ""
    for link in links:
        if ('pdf' in link.get('href', [])):
            i += 1
            # print(link.get('href', []))
            the_link = link.get('href', [])
            break
    return "http://"+urlparse(response.url).netloc+the_link
        
def download_papers(dois, output_dir):
    download_results = {"doi":[], "path": [], "result":[]}
    for doi in dois:
        result = download_paper(doi, output_dir)
        if result != None:
            download_results["doi"].append(doi)
            download_results["path"].append(result)
            download_results["result"].append("Success")
        else:
            download_results["doi"].append(doi)
            download_results["path"].append("Download failed")
            download_results["result"].append("Failed")
            
    return pd.DataFrame(download_results)

def inference_cleanup(inference):
    new_inference = []
    for i in inference:
        i_=[i[0]]
        if "yes" in i[1][0].lower():
            i_.append("yes")
        elif "no" in i[1][0].lower():
            i_.append("no")

        if "yes" in i[1][1].lower():
            i_.append("yes")
        elif "no" in i[1][1].lower():
            i_.append("no")

        new_inference.append(i_)
    return new_inference


def find_dataAI(path):
    inference = AnalyzePDF_AI(path)
    indices = find_supplementary_data_sentence_AI(inference)
    data_links = []
    dataframe = {
        "data_links": [],
        "inference": []
    }
    if indices != []:
        for i in indices:
            # detect http links
            link = re.findall(r'(https?://\S+)', inference[i][0])
            if link != []:
                data_links.append(link)

        dataframe["data_links"] = data_links
        dataframe["inference"] = inference[i]
        
        
        return 
    
    else:
        print("No supplementary data found or data reference found in this paper")
        return None

def find_supplementary_data_sentence_AI(inference):
    indices = []
    for idx, i in enumerate(inference):
        if "yes" in i[2].lower():
            indices.append(idx)
    return indices

def ReadPDF(filepath):
    # parse PDF using 
    raw = parser.from_file(filepath)
    return raw["content"].replace("\n", "")

def ReadPDFs(filepaths):
    # if filepaths is a dataframe extract filepaths
    if type(filepaths) == pd.core.frame.DataFrame:
        filepaths = filepaths["path"].tolist()
    raws = []
    for file in filepaths:
        if type(file) == pathlib.PosixPath:
            file = str(file)
        raw = ReadPDF(file)
        raws.append(raw)
    return raws

def AnalyzePDF_AI(filepath):
    raw = ReadPDF(filepath)
    # split text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', raw)
    # pprint(sentences)

    # split raw into paragraphs made from 5 sentences
    paragraphs = []
    for i in range(0, len(sentences), 3):
        paragraph = " ".join(sentences[i:i+5])
        paragraphs.append(paragraph)

    # get inference
    inference = []
    for i in tqdm(paragraphs):
        inf = get_inference(i)
        # print("Sentece", i)
        # print("Inference", inf)
        inference.append([i, inf])

    inference = inference_cleanup(inference)
    
    return inference


def FindOpenData(dois, output_dir):
    """Prototype function to find open data in scientific papers"""
    # download the papers
    download_results = download_papers(dois, "examples")
    # download the supplementary data
    supplementary_files = []
    for doi in dois:
        links = find_data(doi)
        print(links)
      
        
def find_das(sentences):
    """Find data availability sentences in the text"""
    das_keywords = keywords["data_availability"]
    das_sentences = [sentence for sentence in sentences if any(kw.lower() in sentence.lower() for kw in das_keywords)]
    return das_sentences

def find_keywords(sentences):
    """find keywords in sentences"""
    detected = []
    kw = keywords.copy()
    kw.pop("data_availability")
    for k in kw.keys():
        kk = kw[k]
        for sentence in sentences:
            if any(kw.lower() in sentence.lower() for kw in kk):
                detected.append(sentence)

    return detected

def find_dataKW(path):
    """Find data keywords in the text"""
    raw = ReadPDF(path)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', raw)
    das_sentences = find_das(sentences)
    keyword_sentences = find_keywords(sentences)
    
    
    # detect links in the sentences
    data_links = []
    for sentence in keyword_sentences:
        link = re.findall(r'(https?://\S+)', sentence)
        if link != []:
            data_links.append(link)
    
    # clean the links
    dl = []
    for i in data_links:
        for j in i:
            # split merged links
            if len(j.split("http")) > 2:
                for k in j.split("http"):
                    if k != "":
                        dl.append("http"+k)
            else:
                dl.append(j)
    # clean special non standard url characters
    dl = [i.replace(")", "").replace("]", "").replace("}", "") for i in dl]
    dl = [i.replace("(", "").replace("[", "").replace("{", "") for i in dl]
    dl = [i.replace(";", "").replace(",", "") for i in dl]
    return das_sentences, dl
        


if __name__ == "__main__":
    # print(get_journal_info("Nature"))
    # print(get_paper_by_keyword("climate change"))
    # print(get_papers())
    # print(gather_journal_info(["Nature", "Science"]))
    # download_paper("10.3390/microorganisms10091765", "examples")
    # print(
        # download_papers(
        # ["10.1016/j.tpb.2012.08.002", "10.3390/microorganisms10091765"],
        # "examples")
    # )

    # example for reading PDF
    # raw = ReadPDF(
        # "examples/Stage_and_age_structured_Aedes_vexans_and_Culex_pipiens__Diptera__Culicidae__climate-dependent_matrix_population_model.pdf"
    # )
    # String of the content of the PDF
    # example_pdfs = list(pathlib.Path("examples").glob("*.pdf"))
    # raws = ReadPDFs(list(pathlib.Path("examples").glob("*.pdf")))   
    # print(raw)
    # example for analyzing PDF
    # inference = AnalyzePDF_AI(raws[1])
    # find_supplementary_data_sentence_AI(inference)
    # keywords = AnalyzePDF_keywords(raw)

    papers = find_papers("Hackenberger")
    
    
    
    papers

