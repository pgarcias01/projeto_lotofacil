import requests
import zipfile
import pandas as pd
import lxml
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta

def download_db(date):

    url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'
    target_path = 'D_lotfac.zip'

    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()
    with zipfile.ZipFile(target_path) as zf:
        zf.extractall()



def work_in_db():
    fileHtml = 'd_lotfac.htm'

    f = open(fileHtml, 'r', encoding='latin-1')
    table = f.read()

    soup = BeautifulSoup(table, 'html.parser')
    table = soup.find(name='table')

    table_str = str(table)
    return table_str



