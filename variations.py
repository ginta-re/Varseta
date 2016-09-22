# -*- coding: utf-8 -*-
from __future__ import division
import difflib
from operator import itemgetter
from itertools import groupby
import itertools
from bs4 import BeautifulSoup

class Variations:
    
    def __init__(self, utterances, similarity_value, ngram_mode, similarity_method):
        self.utterances = utterances
        self.chunklen = int(ngram_mode)
        self.similarity_value = float(similarity_value)
        self.similarity_method = similarity_method
        self._ngrams = self.find_ngrams() #chunks by 4 utterances
        self._overlaping_variations = []
        self.find_similar_utterances()
        self._variations = []
        self._variationsets = []

    
    def find_ngrams(self):
        #cut the bulk of text into ngram utterances, 2 for INCREMENTAL, 4 for ANCHOR
        return zip(*[self.utterances[i:] for i in range(self.chunklen)])
    
    def str_sim(self, s1, s2):
        # python diff-lib similarity
        return (difflib.SequenceMatcher(lambda x: x==' ',s1,s2)).ratio()

    def ldr_sim(self, s1, s2):
        #edit distance similarity adapted from en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
        s1 = ' ' + s1
        s2 = ' ' + s2
        d = {}
        S1 = len(s1)
        S2 = len(s2)
        for i in range(S1):
            d[i, 0] = i
        for j in range (S2):
            d[0, j] = j
        for j in range(1,S2):
            for i in range(1,S1):
                if s1[i] == s2[j]:
                    d[i, j] = d[i-1, j-1]
                else:
                    d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + 1)
        return 1-(d[S1-1, S2-1]/max(S1-1,S2-1))

    def find_similar_utterances(self):
        #finds 2gram or 4gram similar utterances according to EDR (edit distance) OR STR (diff-lib) similarity measure
        if self.similarity_method == "ldr":
            for pair in self._ngrams:
                try:
                    #ANCHOR for handiling 4gram stiching (1-2,1-3,1-4)
                    if self.ldr_sim(pair[0][2],pair[3][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1],pair[2],pair[3]])
                    elif self.ldr_sim(pair[0][2],pair[2][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1],pair[2]])
                    elif self.ldr_sim(pair[0][2],pair[1][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1]])
                except:
                    pass
                try:
                    #INCREMENTAL for handling 2gram stiching (1-2,2-3,3-4)
                    if len(pair) == 2 and self.ldr_sim(pair[0][2],pair[1][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1]])
                except:
                    pass
        if self.similarity_method == "str":
            for pair in self._ngrams:
                try:
                    #ANCHOR for handiling 4gram stiching (1-2,1-3,1-4)
                    if self.str_sim(pair[0][2],pair[3][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1],pair[2],pair[3]])
                    elif self.str_sim(pair[0][2],pair[2][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1],pair[2]])
                    elif self.str_sim(pair[0][2],pair[1][2]) > self.similarity_value:
                        self._overlaping_variations.append([pair[0],pair[1]])
                except:
                    pass
                try:
                    #INCREMENTAL for handling 2gram stiching (1-2,2-3,3-4)
                    if len(pair) == 2 and self.str_sim(pair[0][2],pair[1][2]) > self.similarity_value:
                            self._overlaping_variations.append([pair[0],pair[1]])
                except:
                    pass


    def mark_variation_sets(self):
        #removes 2-4gram overlaping repetitions and glues related ngrams into utterance sets
        clean_sets=[]
        for v in self._overlaping_variations:
            if len(clean_sets)==0:
                clean_sets.append(v)
            elif (not clean_sets[-1:][0][1:]==v) and (not clean_sets[-1:][0][2:]==v):
                clean_sets.append(v)
        for el in clean_sets:
            if not self._variations:
                self._variations.append(el)
            elif el[0] in self._variations[-1:][0]:
                temp=self._variations.pop()
                self._variations.append(list(map(itemgetter(0), groupby(temp+el))))
            else:
               self._variations.append(el)
        #removes duplicates at variation sets level
        for el in self._variations:
            el.sort()
            el = list(el for el,_ in itertools.groupby(el))
            self._variationsets.append(el)
        return self._variationsets


