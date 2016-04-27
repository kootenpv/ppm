#!/usr/bin/env python
import codecs
from getpass import getpass

import pyscrypt

try:
    input = raw_input
except NameError:
    pass


def generate(master_password, keyword, cost=2048, oLen=32):
    hashed = pyscrypt.hash(
        password=master_password.encode(),
        salt=keyword.encode(),
        N=cost,
        r=1,
        p=1,
        dkLen=32
    )
    tmp = codecs.encode(hashed, 'hex').decode('utf-8')[0:oLen]
    tmp = "!A" + tmp[:-2]
    return tmp

if __name__ == "__main__":
    master_password = getpass()
    while True:
        print(generate(master_password, input("Keyword: ")))
