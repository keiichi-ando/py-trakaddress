import requests
import lxml.html
from bs4 import BeautifulSoup as bs
import time

time.sleep(1)
res = requests.get('https://www2.sagawa-exp.co.jp/company/branch/list/?sub_b_id=17') # 1-18

soup = bs(res.content, 'lxml')
dls = soup.find_all('dl')
offices = []

for dl in dls:
    dt = html.fromstring(str(dl))

    ad = ((dt.xpath('//ul/li[1]')[0]).text).split('　')[1] # [0] zip7, [1] address
    offices.append ( [(dt.xpath('//span[@class="name01"]')[0]).text.replace('営業所',''), ad] )

df = pd.DataFrame(offices, columns=['名前','住所'])

print(df)