#!/usr/bin/env python
import codecs
import platform
import subprocess
from getpass import getpass

import pylibscrypt


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


def generate(master_password, keyword, cost=2 ** 20, oLen=32):
    hashed = pylibscrypt.scrypt(password=bytes(master_password, "utf8"),
                                salt=bytes(keyword, "utf8"),
                                N=cost,
                                r=8,
                                p=1,
                                olen=oLen)
    res = codecs.encode(hashed, 'hex').decode('utf-8')[:oLen]
    res = "!A" + res[:-2]
    return res

if __name__ == "__main__":
    write_to_clipboard(generate(getpass(), input("Keyword: ")))
