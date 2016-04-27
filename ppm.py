#!/usr/bin/env python
import codecs
import platform
import subprocess
from getpass import getpass

import pyscrypt

try:
    input = raw_input
except NameError:
    pass


def write_to_clipboard(output):
    system = platform.system()
    if system == "Darwin":
        cmd = ['pbcopy']
    else:
        cmd = ["xclip", "-selection", "clipboard"]
        subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(output.encode('utf-8'))
        cmd = ["xclip", "-selection", "primary"]
    subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(output.encode('utf-8'))


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
    write_to_clipboard(generate(getpass(), input("Keyword: ")))
