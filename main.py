#!/usr/bin/env python3

import sys
import src.settings
from src.master.address import AddressUtil
from src.master.address import AddressParser
from model.address import Address


if __name__ == "__main__":
    args = sys.argv

    if (len(args) > 1):
        if (args[1] == "getzip"):
            _util = AddressUtil()
            _util.getzip()
            # _util.zip_extract('/home/ando/python/address/src/master/../../data/ken_all.zip')
        else:
            _parser = AddressParser()
            _myad = Address(args[1])
            _myad = _parser.parse(_myad)

            print(_myad.full, chr(9), _myad.pref, chr(9), _myad.city, chr(9), _myad.town)

