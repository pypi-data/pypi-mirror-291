# Web scraper looking for data on the web for a certain paper


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from EcoOpen.utils.keywords import keywords
import os
import requests
from pathlib import Path

urls = [
    'https://link.springer.com/article/10.1007/s10886-017-0919-8',
    "https://link.springer.com/article/10.1007/s10886-018-0942-4",
    "https://doi.org/10.1073/pnas.1211733109",
    "http://dx.doi.org/10.3955/046.091.0105",
    "https://doi.org/10.1016/j.scitotenv.2013.10.121",
    "https://doi.org/10.1111/nph.14333"
    ]

filetypes = [
    "csv", "xlsx", "xls", "txt", "pdf", "zip",
    "tar.gz", "tar", "gz", "json", "xml", "docx",
    "doc", "ods", "odt", "pptx", "ppt", "png", "jpg",]

exclude = []
for i in filetypes:
    exclude.append(i.lower()+".")

def find_data_web(doi):
    url = "https://doi.org/" + doi
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    real_url = driver.current_url
    print(real_url)
    domain = real_url.split('/')[2]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    supplementary_files = []
    closed_article_snippets = [
        "buy article",
        "access the full article",
        "purchase pdf",
    ]
    # check if the article is closed
    if any(snippet in str(soup).lower() for snippet in closed_article_snippets):
        print("You need to buy the article to access the data.")
    # specific for PNAS
    elif "suppl_file" in str(soup).lower():
        # find the link to the supplementary file
        links = soup.find_all('a')
        for link in links:
            try:
                if "suppl_file" in link.get('href'):
                    # print("There is a supplementary file")
                    supplementary_files.append(link.get('href'))
                    # print(link.get('href'))
            except TypeError:
                pass
    for i in keywords["repositories"]:
        links = soup.find_all('a')
        for link in links:
            try:
                if i in link.get('href'):
                    # print("There is a supplementary file")
                    supplementary_files.append(link.get('href'))
                    # print(link.get('href'))
            except TypeError:
                pass
    return supplementary_files

def get_data_from_link(link, output_dir="examples/data"):
    output_dir = Path(os.path.expanduser(output_dir))
    output_dir = output_dir.absolute()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(link)
    wait = WebDriverWait(driver, 3)
    real_url = driver.current_url
    # print(real_url)
    domain = real_url.split('/')[2]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    files = []
    for i in filetypes:
        filename = ""
        links = soup.find_all('a')
        for link in links:
            try:
                if "."+i in link.get('href'):
                    # print("There is a file")
                    l = link.get('href')
                    if "http" not in l:
                        l = "https://"+domain + l
                    files.append(l)
                    # print(link.get('href'))
            except TypeError:
                pass
    # close the browser
    driver.close()
    # download the files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in files:
        # print(i)
        response = requests.get(i, timeout=2)
        response.raise_for_status()
        filename = i.split('/')[-1]
        if "?" in filename:
            filename = filename.split("?")[0]
        if filename != "":
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(response.content)
    return files

if __name__ == '__main__':
    doi = "10.1016/j.tpb.2012.08.002"
    doi = "10.3390/microorganisms10091765"
    data_links = find_data(doi)
    print(get_data_from_repo(data_links[0]))

