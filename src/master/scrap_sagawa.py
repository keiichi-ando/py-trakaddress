from os import path
import pandas as pd
import time
import csv
import requests
from lxml import html


offices = []
_outfile = path.join(path.dirname(__file__), '../../data/ts_sagawa.csv')

for i in range(1, 18):
    
    time.sleep(2)
    # 1-18
    _url = f'https://www2.sagawa-exp.co.jp/company/branch/list/?sub_b_id={i}'
    _res = requests.get(_url)
    _res.encoding = _res.apparent_encoding

    dom = html.fromstring(_res.text)

    for dl in dom.xpath('//dl'):
        dl_text = html.tostring(dl)

        _office = html.fromstring(dl_text).xpath('//span[@class="name01"]')
        if (_office):
            _addr = html.fromstring(dl_text).xpath(
                '//ul[@class="list_officeInfo01"]/li[1]')
            _addr = _addr[0].text.split('　')
            print(_office[0].text, _addr[0], _addr[1])

            offices.append([_office[0].text, _addr[0], _addr[1]])

    print(_url)

df = pd.DataFrame(offices, columns=['名前', '郵便番号', '住所'])
df['名前'] = df['名前'].str.replace('営業所', '').str.replace('支店', '')
df['郵便番号'] = df['郵便番号'].str.replace('〒', '')

print(df)

df.to_csv(_outfile, index=False, quoting=csv.QUOTE_NONNUMERIC)
