

import requests
import zipfile
import os
import pandas as pd
import csv
import re
from functools import reduce

# @see https://biz.kkc.co.jp/software/geo/addressmatch/function/
# @see https://yamagata.int21h.jp/tool/testdata/


class AddressUtil:

    def get_datapath(self):
        return os.path.join(os.path.dirname(__file__), '../../data')

    def getzip(self):
        """ 日本郵便のHPから小書きのzipファイルを取得して解凍

        Args:

        Return:
            bool : 処理成否

        """

        _url = os.environ['URL_JPZIP']
        _tofile = os.path.join(self.get_datapath(), _url.split("/")[-1])
        # _data
        _r = requests.get(_url, stream=True)
        with open(_tofile, 'wb') as _f:
            for _chunk in _r.iter_content(chunk_size=1024):
                if _chunk:
                    _f.write(_chunk)
                    _f.flush()

            print('{} is downloaded.'.format(_tofile))
            self.zip_extract(_tofile)
            self.to_jis_master(_tofile)

            return _tofile

        return False  # 失敗

    def zip_extract(self, filename):
        """ファイル名を指定して zip ファイルを解凍する

        Args:
            filename (str): zipファイル名

        Return:
            viod

        """
        _zipfile = zipfile.ZipFile(filename)
        _zipfile.extractall(self.get_datapath())

    def to_jis_master(self, filename):
        """ ken_all.csvをjisx0401, jisx0402のデータ変換

        Args:
            filename (str): KEN_ALL.CSV フルパス

        Return:
            void

        """
        _tofile = os.path.join(self.get_datapath(), 'jisx0402.csv')

        _columns = ["jisx", "oldzip", "zip7", "pref_kana", "city_kana", "town_kana", "pref", "city",
                    "town", "flug_de", "flug_aza", "flug_choume", "flug_dupa", "flug_update", "flug_comment"]
        _dtypes = {"jisx": 'object', "oldzip": 'object', "zip7": 'object', "pref_kana": 'object', "city_kana": 'object', "town_kana": 'object', "pref": 'object', "city": 'object',
                   "town": 'object', "flug_de": 'uint8', "flug_aza": 'uint8', "flug_choume": 'uint8', "flug_dupa": 'uint8', "flug_update": 'uint8', "flug_comment": 'uint8'}

        df = pd.read_csv(filename, encoding='cp932',
                         header=None, names=_columns, dtype=_dtypes)
        df = df.drop(['oldzip', 'pref_kana', 'city_kana', 'town_kana', "flug_de",
                     "flug_aza", "flug_choume", "flug_dupa", "flug_update", "flug_comment"], axis=1)

        # DataFrameGroupBy => DataFrameに変換するためにreset_index()を使用する
        _df = df.groupby(['jisx', 'pref', 'city'],
                         as_index=False).sum().reset_index()

        _df[['jisx', 'pref', 'city']].to_csv(
            _tofile, index=False, quoting=csv.QUOTE_NONNUMERIC)


class AddressParser:
    _myad = None

    def __init__(self):
        pass

    def parse(self, address):
        """ 住所パーサー

        Args:
            adderss (model.Address): アドレスモデル
        Return 
            model.Address

        """
        self._myad = address
        self.normalize()
        self.address_parse()
        return self._myad

    def normalize(self):
        """ 住所文字列正規化

        Args:

        Return 
            void

        """
        self._myad.full = self._myad.full.translate(str.maketrans(
            {chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

    def address_parse(self):
        """ 住所文字列 分割 full => pref city town extra1 extra2

        Args:

        Return 
            void

        """
        _pat = '(...??[都道府県])*((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下>松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.*)'
        _add = re.split(_pat, self._myad.full)

        if(len(_add) > 3):
            self._myad.pref = _add[1]
            self._myad.city = _add[2]
            self._myad.town = _add[3]

            if self._myad.pref == None and self._myad.city != None:
                if (re.search('^(和歌山|鹿児島)市', self._myad.city)):
                    self._myad.pref = self._myad.city[0:3] + '県'
                elif (re.search('^(京都|大阪)市', self._myad.city)):
                    self._myad.pref = self._myad.city[0:2] + '府'
                elif (re.search('^(青森|秋田|山形|福島|栃木|千葉|新潟|富山|福井|山梨|長野|岐阜|静岡|奈良|鳥取|岡山|広島|山口|徳島|高知|福岡|佐賀|長崎|熊本|大分|宮崎|沖縄)市', self._myad.city)):
                    self._myad.pref = self._myad.city[0:2] + '市'

            self.normalizeJou()
            self.parseFloor()

    def normalizeJou(self):
        """ 町域正規化（〜条）

        Args:

        Return 
            void

        """

        if (self._myad.town == ""):
            return

        _pat = '([東西南北])([0-9]+)(条)'
        _result1 = re.search(_pat, self._myad.town)
        if (_result1 != None):
            # convert number to kanji
            d = {'10': '十', '20': '二十', '30': '三十', '1': '一', '2': '二', '3': '三',
                 '4': '四', ' 5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}
            _f = reduce(lambda x, y: x.replace(
                y, d[y]), d, _result1.group(2))
            if (len(_f) == 2 and not re.match('.十', _f)):
                _f = f'{_f[0]}十{_f[1]}'
            # replace
            self._myad.town = re.sub(_pat, r'\1' + _f + r'\3', self._myad.town)

    def parseFloor(self):
        """ 町域分割 部屋番号など

        Args:

        Return 
            void

        """

        if (self._myad.town == ""):
            return

        _pat = '(.*)([0-9〇一-十]+(棟|号棟|F|階|号室))(.*)'
        _result1 = re.match(_pat, self._myad.town)
        if (_result1 != None):
            self._myad.town = _result1.group(1)
            self._myad.extra1 = _result1.group(2)
            self._myad.extra2 = _result1.group(4)
