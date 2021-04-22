from os import path
import pandas as pd
import time
import csv

_outfile = path.join(path.dirname(__file__), '../../data/ts_fukutsu.csv')

areas = ['hokkaidou', 'touhoku', 'kantou', 'koushinetsu', 'hokuriku',
         'toukai', 'kansai', 'chugoku', 'shikoku', 'kyushu', 'okinawa']
# areas = ['hokkaidou', 'touhoku'] #, 'kantou', 'koushinetsu', 'hokuriku', 'toukai', 'kansai', 'chugoku', 'shikoku', 'kyushu', 'okinawa']
df = pd.DataFrame()

for area in areas:

    time.sleep(3)

    url = f'https://corp.fukutsu.co.jp/company/base/branch/{area}.html'
    _dfs = pd.read_html(url)

    for _df in _dfs:
        if df.empty:
            df = _df
        else:
            df = df.append(_df)

    print(url)
    del _dfs

df = df.set_axis(['名前', '郵便番号', '住所', 'tel'], axis=1)
df = df.reset_index(drop = True)

# normalize
df['名前'] = df['名前'].str.replace('営業所', '').str.replace('支店','')
df['郵便番号'] = df['郵便番号'].str.replace('〒', '')
df['tel'] = df['tel'].str.replace('（', '-').str.replace('）', '-')

print(df)

df.to_csv(_outfile, index=False, quoting=csv.QUOTE_NONNUMERIC)
