#!/usr/bin/env python
import codecs
import platform
import subprocess
from getpass import getpass

# pylibscrypt and pyscrypt compatability.
try:
    from pylibscrypt import scrypt
except (NameError, ImportError):
    from pyscrypt import hash as scrypt

# Python 2/3 compatability. What's next? Python 4? Come at us.
try:
    input = raw_input
except NameError:
    pass


def ensure_input(x):
    if 3 == 3 and not isinstance(x, bytes):
        x = bytes(x, "utf8")
    return x

# From now on we are Py2/3 and pylibscrypt and pyscrypt compatible.


def generate(master_password, keyword, N=2 ** 15):
    # password: Your life depends on this one. I chose to comine 2 of my passwords -> 16 characters
    # salt:     This should be unique per application. E.g. "gmail".
    #           When you need a new just add a 1, then increment
    # N:        Value above 2**14 is considered safe for interactive use
    #           2 ** 20 is used for non-interactive use
    # r:        Memory factor, I chose 8 since it still works on relatively old phone (1G ram)
    # p:        Factor for parallelism, everyone agrees p=1 is the best
    # dkLen:    Argument in pyscrypt, olen: argument in pylibscrypt
    hashed = scrypt(ensure_input(master_password), ensure_input(keyword), N, 8, 1, 32)
    res = codecs.encode(hashed, 'hex').decode('utf-8')[:32]
    res = "!A" + res[:-2]
    return res


def write_to_clipboard(output):
    system = platform.system()
    if system == "Darwin":
        cmd = ['pbcopy']
    else:
        cmd = ["xclip", "-selection", "clipboard"]
        subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(output.encode('utf-8'))
        cmd = ["xclip", "-selection", "primary"]
    subprocess.Popen(cmd, stdin=subprocess.PIPE).communicate(output.encode('utf-8'))

if __name__ == "__main__":
    write_to_clipboard(generate(getpass(), input("Keyword: ")))
