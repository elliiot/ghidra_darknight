#!/usr/bin/env python3

# usage: path to _code_browser.tcd (in your home directory)

import sys


if __name__ == "__main__":
    code_browser_tcd = sys.argv[1]

    with open(code_browser_tcd, "r") as fd:
        content = fd.read()
        content_orig = content
        
    inp = open("darknight", "r")

    while 1:
        conf_name = inp.readline()
        if not conf_name:
            break

        i = content.find(conf_name)
        if i == -1:
            print("error: can't find", conf_name)
            break

        j_beg = content.find("<", i + len(conf_name))
        j_end = content.find("/>", j_beg) + 2

        color = inp.readline().strip()
        content = content[:j_beg] + color + content[j_end:]

    # content = content.replace("\n", "\r\n")

    with open(code_browser_tcd + ".bak", "w+") as fd:
        fd.write(content_orig)
        print("old file copied to", code_browser_tcd + ".bak")

    with open(code_browser_tcd, "w+") as fd:
        fd.write(content)
        print("colors set !")
