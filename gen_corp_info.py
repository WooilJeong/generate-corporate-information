import sys
import requests
import pandas as pd

def get_info(corpNo):
    url = "https://www.kreport.co.kr/api/v1/ss/getSearchList"

    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    data = {
      "cmQuery": corpNo,
      "cmQueryOption": "",
      "cmCollection": "",
      "cmPageNo": 1,
      "cmSortField": "",
      "cmSortOption": 1,
      "cmRowCountPerPage": 0,
      "pdNm": "",
      "sidoNmList": [],
      "estbDtSt": "",
      "estbDtEd": "",
      "enpSzeList": [],
      "enpIpoList": [],
      "enpFcdList": [],
      "bzcCd": "",
      "bzcNm": "",
      "ksic10BzcCd": "",
      "asetTSum": "",
      "capital": "",
      "sam": "",
      "loginTf": 'false'
    }
    res = requests.post(url, headers=headers, json=data)
    df = pd.DataFrame(res.json()['data']['searchRslDtoList'])
    df['query'] = corpNo
    newCols = list(df.columns[-1:]) + list(df.columns[:-1])
    df = df[newCols]
    return df

def generate_excel_file(file_path, export_path):
    raw = pd.read_excel(file_path, dtype=str)
    df = pd.DataFrame()
    for idx, row in raw.iterrows():
        print(row['사업자번호'])
        sub = get_info(row['사업자번호'])
        df = pd.concat([df,sub], axis=0, ignore_index=True)
    df.to_excel(export_path, index=False, encoding='CP949')


arg1 = sys.argv[1]
arg2 = sys.argv[2]

generate_excel_file(arg1, arg2)