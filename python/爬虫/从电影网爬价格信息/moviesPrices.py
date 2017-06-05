# -*- coding: utf-8 -*-

import urllib
import sys

def main():
    if len(sys.argv) > 1:
        html = getHtml(sys.argv[1])
    print html

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

if __name__ == "__main__":
    main()