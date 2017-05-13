# -*- coding: utf-8 -*-
from __future__ import division
import difflib
from operator import itemgetter
from itertools import groupby
import itertools
from bs4 import BeautifulSoup

class Variations:
    
    def __init__(self, utterances, similarity_value, ngram_mode, similarity_method):
		# list of utterances: [[start_time, end_time, utterance_transcription], [start_time, end_time, utterance_transcription],...]
        self.utterances = utterances
        # comparison modes:
        # 2 => Incremental
        # 4 => Anchor
        self.comparison_mode = int(ngram_mode)
        self.similarity_value = float(similarity_value)
        self.similarity_method = similarity_method
        # collects all the variationsets
        self._variationsets = []
        self.find_variationsets()



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


	 #extracts variation sets based on ANCHOR or INCREMENTAL comparison according to EDR (edit distance) OR STR (diff-lib) similarity measure 
	 # returns: [[utterance, utterance, utterance], [utterance, utterance], ...]
	 # a single utterance consisting of: [start_time, end_time, utterance_transcription]
    def find_variationsets(self):
		print self.utterances, len(self.utterances)
		threshold = 0
		# previous and current utterance will be compared
		previous_utterance = ""
		current_utterance = ""
		
		# the current variation set is cumulated in here
		variationset = []
		
		
		if self.similarity_method == "ldr":
			#TODO replace numbers by string representaion of comparison method
			# Extract INCREMENTAL
			if self.comparison_mode == 2:
				for index, utt in enumerate(self.utterances):
					#intitalization
					if index == 0:
						previous_utterance = utt
						
					else:
						current_utterance = utt
	
						
						# create new variation set
						# previous_utterance[2] --> only look at transcription
						if self.ldr_sim(previous_utterance[2], current_utterance[2]) > self.similarity_value and variationset == []:
							variationset.append(previous_utterance)
							variationset.append(current_utterance)
							previous_utterance = current_utterance
						
						# extend variation set
						elif self.ldr_sim(previous_utterance[2], current_utterance[2]) > self.similarity_value and variationset != []:
							variationset.append(current_utterance)
							previous_utterance = current_utterance
							
							
						# we've either reached an interjection or an end of a variation set
						elif self.ldr_sim(previous_utterance[2], current_utterance[2]) <= self.similarity_value and variationset != []:
							
							# look ahead two if there are utterances that belong again to the varset
							if threshold == 0 and index < len(self.utterances)-2 and (self.ldr_sim(previous_utterance[2], self.utterances[index+1][2]) > self.similarity_value or self.ldr_sim(previous_utterance[2], self.utterances[index+2][2]) > self.similarity_value):
								threshold +=1
								variationset.append(current_utterance)
							
							# look ahead only one
							# if threshold is still 0 but only one utterance left or if threshold == 1	
							elif (threshold == 0 or threshold == 1) and  index < len(self.utterances)-1 and (self.ldr_sim(previous_utterance[2], self.utterances[index+1][2]) > self.similarity_value):
								threshold += 1
								variationset.append(current_utterance)
							
							# this is the end of the variation set and/or the end of the file
							else:
								threshold = 0
								self._variationsets.append(variationset)
								variationset = []
								previous_utterance = current_utterance
									
									

						
						#just read the next line
						# TODO change into a else statement	
						elif self.ldr_sim(previous_utterance[2], current_utterance[2]) <= self.similarity_value and variationset == []:
							previous_utterance = current_utterance
							
						else:
							print "This case shouldn't be happening, something went wrong"
						
						#if it's the last utterance, add any left variation sets
						if index == len(self.utterances)-1:
							self._variationsets.append(variationset)

							
			# ANCHOR		
			elif self.comparison_mode == 4:
				for index, utt in enumerate(self.utterances):
					#intitalization
					if index == 0:
						previous_utterance = utt
					
					else:
						current_utterance = utt
						
						# new variation set
						if self.ldr_sim(previous_utterance[2], current_utterance[2]) > self.similarity_value and variationset == []:
							variationset.append(previous_utterance)
							variationset.append(current_utterance)
							
						#extend variation set
						elif self.ldr_sim(previous_utterance[2], current_utterance[2]) > self.similarity_value and variationset != []:
							variationset.append(current_utterance)
							
							
						# interjection reached
						elif self.ldr_sim(previous_utterance[2], current_utterance[2]) <= self.similarity_value and variationset != []:
							
							# look ahead two if there are utterances that belong again to the varset
							if threshold == 0 and index < len(self.utterances)-2 and (self.ldr_sim(previous_utterance[2], self.utterances[index+1][2]) > self.similarity_value or self.ldr_sim(previous_utterance[2], self.utterances[index+2][2]) > self.similarity_value):
								threshold +=1
								variationset.append(current_utterance)
								
							# look ahead only one
							# if threshold is still 0 but only one utterance left or if threshold == 1
							elif (threshold == 0 or threshold == 1) and index < len(self.utterances)-1 and (self.ldr_sim(previous_utterance[2], self.utterances[index+1][2]) > self.similarity_value):
								threshold += 1
								variationset.append(current_utterance)
								
			
									
							# this is the end of the variation set and/or the end of the file
							else:
								threshold = 0
								self._variationsets.append(variationset)
								variationset = []
								previous_utterance = current_utterance
								
						
						#just read the next line
						# TODO change into a else statement	
						elif self.ldr_sim(previous_utterance[2], current_utterance[2]) <= self.similarity_value and variationset == []:
							previous_utterance = current_utterance

						else:
							print "This case shouldn't be happening, something went wrong"	
						
						#if it's the last utterance, add any left variation sets
						if index == len(self.utterances)-1:
							self._variationsets.append(variationset)						
								
								
							
						
							
							



    def mark_variation_sets(self):
        return self._variationsets



		
		
		
		
		
		
		
		
		
		
		