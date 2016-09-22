# -*- coding: utf-8 -*-
import glob
import codecs
from bs4 import BeautifulSoup


class Utterances:
    
    def __init__(self, filedir, golddir):
        self._utterances = []
        self._goldutterances = []
        self._read_files(filedir)
        self._read_gold(golddir)
    
    def _read_files(self, filedir):
        for filename in glob.glob(filedir+"/*.txt"):
            for line in codecs.open(filename, "r", "utf-8").readlines():
                self._read_sentence(line)

    def _read_gold(self, golddir):
        for filename in glob.glob(golddir+"/*.txt"):
            soup = BeautifulSoup(codecs.open(filename, "r", "utf-8").read(), "html.parser")
            for link in soup.find_all('set'):
                tag_link=str(link).split("\n")
                for el in tag_link:
                    if "<set" in el or "</set>" in el:
                        tag_link.remove(el)
                untag_link=[]
                for el in tag_link:
                    e=el.split("\t")
                    untag_link.append([e[0].decode('utf-8'), e[1].decode('utf-8'), e[3].decode('utf-8')])
                self._goldutterances.append(untag_link)
    
    def _read_sentence(self, line):
        tokens = line.strip().split()
        if tokens:
            self._utterances.append([tokens[0].decode('utf-8'), tokens[1].decode('utf-8'), " ".join(tokens[3:])])
                                    
                                    
    