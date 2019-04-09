import mwclient
from threading import Thread
import os
import shelve
import math
import re

def base_builder():
    filepath = 'Nouns8.txt'
    db = 'noun_stems'
    theads_num = 20
    threads = []
    global templates
    templates = {}
    site = mwclient.Site('ru.wiktionary.org')

    with open(filepath, 'r', encoding='utf-8') as nounsfile:
        allnouns = [line.split('\n') for line in nounsfile.readlines()]


    list_length = round(len(allnouns)/threads_num)
    for i in range(threads_num):
        yield gen_word_list(allnouns[i * list_length: (i + 1) * list_length])

    for n in noun_lists:
        thr = Thread(target=parse_pages, args=(n, site,))
        threads.append(thr)
        thr.start()

    for thr in threads:
        thr.join()

    with shelve.open(db, writeback=True) as db:
        for stem, dic in templates.items():
            db[stem] = dic

def gen_word_list(wordlist):

    for word in wordlist:
        yield word

def parse_pages(wordlist, site):
    
    for word in words:
       
        try:
            curpage = site.Pages[word]
            curtext = curpage.text(section=2).split("{{")
        except:
            print(word)
            continue

        for piece in curtext:
       
            if (piece.startswith('сущ ru') or piece.startswith('Фам')):
                
                piece.replace('\n', '').split('|')
                template = piece[0]
                
                for i, line in enumerate(piece):
                    if line.startswith("основа"):
                        stem_name, stem = parsing(line)
                       
                        if stem and stem_name:
                            templates.setdefault(stem.lower(), {}).setdefault((template, stem_name), set()).add(word.lower())

            else:
                continue

def parsing(line):
  
    stem_name, stem = stem_line.split('=')
    crap = [' ', '[', ']', '{', '}', '\u0301', '\u0300', '\ufeff']

    for eachcrap in crap:
        stem = stem.replace(eachcrap, '')

    return stem_name, stem


if __name__ == "__main__":
    main()





                        
