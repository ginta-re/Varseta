# -*- coding: utf-8 -*-

class Evaluation:
    
    def __init__(self, variation_sets, gold_sets):
        self.variation_sets = variation_sets
        self.gold_sets = gold_sets
        self.strict_evaluate()
        self.fuzzy_evaluate()

    def strict_evaluate(self):
        tp=0
        for elem in self.gold_sets:
            try:
                if elem in self.variation_sets:
                    tp+=1
            except:
                pass
        fp=(len(self.variation_sets))-tp
        fn=(len(self.gold_sets))-tp
        p=float(tp/(tp+fp+0.0001))
        r=float(tp/(tp+fn+0.0001))
        f=float(2*(p*r)/(p+r+0.0001))
        print "\n", "EVALUATION AGAINS THE GOLD STANDARD"
        print "\n", "true positives:",tp, ", false positives:", fp, ", false negavites:", fn, "from a total of ", len(self.gold_sets), "GOLD variation sets \n"
        print "Strict match Precision = \t", p
        print "Strict match Recall = \t", r
        print "Strict match F-score = \t", f
    
    
    def fuzzy_evaluate(self):
        pp=0
        l=len(self.variation_sets)
        for elem in self.gold_sets:
            try:
                if elem in self.variation_sets:
                    pp+=1
                    self.variation_sets.remove(elem)
                else:
                    for s in self.variation_sets:
                        if elem[0] in s:
                            pp+=1
                            self.variation_sets.remove(s)
                            break
            except:
                pass
        fp=l-pp
        fn=len(self.gold_sets)-pp
        p=float(pp/(pp+fp+0.0001))
        r=float(pp/(pp+fn+0.0001))
        f=float(2*(p*r)/(p+r+0.0001))
        print "\n", "true positives:",pp, ", false positives:", fp, ", false negavites:", fn, "from a total of ", len(self.gold_sets), "GOLD variation sets \n"
        print "Fuzzy match  Precision = \t", p
        print "Fuzzy match Recall = \t", r
        print "Fuzzy match F-score = \t", f

