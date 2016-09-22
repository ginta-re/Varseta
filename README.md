# Varseta
A python script for extracting Variation sets from child directed speech (CDS) data.


# Data format

Files should be prepared in a simple .txt format. 4 tab-separated columns. Child directed speech data example:
```
193.99	  194.71	0.720	Goddag goddag
196.88	  197.8		0.920	Goddag goddag
199.97    200.786   0.816   Säger Siffun
201.327	  203.17	1.843	Goddag goddag säger Siffun goddag goddag
204.36    205.24	0.880	#LL !
207.80    209.409	1.609	Han säger #LL på riktigt
210.213	  212.54    2.327	Ja han är snäll hårig som katten
215.079	  215.766	0.687	Var den läskig ?
216.924	  217.64    0.716	Den här är gladare
```

Where:
- First column is the beginning time of the utterance.
- Second column is  the end time of the utterance.
- Third column is the length of the utterance (optional, can be replaced with other data, see below).
- Forth column is the transcription of the utterance.

Here is alternative example of a 4-column data file, extracted from the CHILDES corpus:
```
14	14	*MOT:		skal jeg sætte den fast.
16	16	*MOT:		hvor skal badeværelset være.
18	18	*MOT:		har du tænkt på det.
19	19	*MOT:		skal vi sætte det derind.
23	23	*MOT:		du skal.
26	26	*MOT:		hov.
27	27	*MOT:		det var jo skuffer.
28	28	*MOT:		hvis du vender den om på den anden led Anne.
29	29	*MOT:		så kan du se så er den meget nemmere.
30	30	*MOT:		og trække den ud.
35	35	*MOT:		prøv at se her.
36	36	*MOT:		det er sådan en .
```
Where:
- First column is the beginning time of the utterance. If times are not available, one can use simple integers to mark the utterance number.
- Second column is  the end time of the utterance. If times are not available, one can use simple integers to mark the utterance number.
- Third column marks the author of the direct speech, e.g. ‘*MOT:’.
- Forth column is the transcription of the utterance.

# Script usage

In order to mark the variation sets for any language:
```
python main.py testing/test_data/NOSET/2/ dummy/evaluation_data/GOLD/2/ 0.6 4 str
```
You will need 5 arguments:

1. a path to the folder with your 4-column-formatted .txt files
2. a path to the folder with equivalent annotated files. If you have no annotated data, use a dummy folder path.
3. a similarity value, anything between 0.01 and 0.99
4. a number for marking strategy: use 4 for ANCHOR and 2 for INCREMENTAL
5. a code for string similarity method: use str for python’s diff-lib or ldr for edit distance

some examples:
```
python main.py DATA/Childes/plain/Afrikaans/3 DATA/Childes/GOLD/ 0.6 4 str

python main.py DATA/Swedish_MINGLE_dataset/plain/1 DATA/Swedish_MINGLE_dataset/GOLD/1 0.6 4 ldr

python main.py DATA/Swedish_MINGLE_dataset/plain/1 DATA/Swedish_MINGLE_dataset/GOLD/1 0.51 2 str
```

If you want to find the number of exact repetitions, you can use INCREMENTAL strategy (2) and 0.99 similarity value, for instance:

```
python main.py DATA/Childes/plain/Welsh/3 DATA/Childes/GOLD/ 0.99 2 str
```

To redirect standard output to a file use > operator:

```
python main.py DATA/Swedish_MINGLE_dataset/plain/2 DATA/Swedish_MINGLE_dataset/GOLD/2 0.6 2 ldr > Swe2_06_2_ldr.txt
```

# Cite this work

[Wirén, M., Nilsson Björkenstam, K., Grigonytė, G. and Cortes, E.E., 2016. Longitudinal Studies of Variation Sets in Child-directed Speech. In The 54th Annual Meeting of the Association for Computational Linguistics, Berlin, Germany, August 11, 2016 (pp. 44-52). Association for Computational Linguistics.](https://aclweb.org/anthology/W/W16/W16-1907.pdf)
