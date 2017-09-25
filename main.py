# -*- coding: utf-8 -*-
import sys
import codecs
import variations
import utterances
import evaluation


if __name__ == '__main__':
    
    if len(sys.argv) != 6:
        sys.exit("Usage: python main.py filedir golddir similarity ngramsLen method...")

    u = utterances.Utterances(sys.argv[1], sys.argv[2])
    v = variations.Variations(u._utterances, sys.argv[3], sys.argv[4], sys.argv[5])
    varset = v.mark_variation_sets()

    utterances_in_varset = 0
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    for number, el in enumerate(varset):
        a,b,c = zip(*(el))
        utterances_in_varset += len(c)
        print "\n", number
        for ut in el:
            print ut[0], ut[1], ut[2]
    print "\nSTATS of MARKED VARIATION SETS in Files from: ", sys.argv[1]
    print "\nnumber of utterances: ", len(u._utterances)
    print "number of variation sets: ", len(varset)
    print "number of utterances in variation sets: ", utterances_in_varset
    gold_utterances = u._goldutterances
    gu_length = 0
    # get the total amount of utterances in variation sets
    for u in gold_utterances:
	gu_length += len(u)
    print "\n\nnumber of gold utterances: ", gu_length

    e = evaluation.Evaluation(varset,gold_utterances)
