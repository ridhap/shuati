#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

# Quick leetcode scraper
#
# Generate the source file of the question and pre-fixed head comment
# 
# Usage: scraper.py [leetcode question url] [extension]
#
# Example: scraper.py http://.... .c

from bs4 import BeautifulSoup
import requests
import sys
import re
import validators
import operator
import os

if __name__ == "__main__":

    script, url, extension = sys.argv

    if not validators.url(url):
        print("Please enter a valid url!")
        sys.exit()
        
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    # produce the directory name based upon leetcode question title
    # 
    title_corp = soup.find_all("div", class_="question-title")
    title_raw = title_corp[0].h3.get_text()
    title_lines = title_raw.split('\n')
    title_lines = list(filter(operator.methodcaller('strip'), title_lines)) 
    title_rdy = title_lines[0].lstrip(' ').replace(".", "-").split(' ')
    title = "".join(title_rdy)

    # create the directory
    #
    path = "./leetcode/" + title
    if not os.path.isdir(path):
        os.mkdir(path)

    # produce file name
    #
    pat = re.compile(r"^(\d+)-")
    m = re.search(pat, title)
    filename=title[:m.start()] + title[m.end():]
    filename=filename[0].lower() + filename[1:]

    target = open(path+"/"+filename+extension, "w")

    # Fetch the question describtion
    #
    letters = soup.find_all("div", class_="question-content")
    rawText = letters[0].get_text()
    lines = rawText.split('\n')
    lines = list(filter(None, lines)) 

    # Construct the header comment of the file
    #
    target.write("/*          \n")
    target.write(" * [Source] \n")
    target.write(" *          \n")
    target.write(" * " + url + "\n")
    target.write(" *          \n")
    target.write(" * [Problem Description]\n");
    target.write(" *          \n")

    for line in lines:
        if "Subscribe" not in line:
            if "click" in line:
                pass
            else:
                # Remove CLR, "\n" if appears
                line = line.replace("\r", "").replace("\n", "")
                target.write(" * " + line + "\n") 
        else:
            break
    target.write(" *          \n")
    target.write(" * [Comments]\n");
    target.write(" *          \n")
    target.write(" *          \n")
    target.write(" *          \n")    
    target.write(" * [Companies]\n");
    target.write(" */          \n")
    target.write("\n\n")
    
    target.close()
