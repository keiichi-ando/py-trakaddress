import pandas as pd
import time

areas = ['hokkaidou', 'touhoku', 'kantou', 'koushinetsu', 'hokuriku', 'toukai', 'kansai', 'chugoku', 'shikoku', 'kyushu', 'okinawa']
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
    print(df.head())

    del _dfs

df = df.set_axis(['名前', '郵便番号', '住所', 'tel'], axis=1)
df = df.reset_index(drop=True)
print(df)