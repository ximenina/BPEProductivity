#########################################################################################################
#Script for caculating TTR statistics at differentlevels (word level and character ngrams)	        #
#Input: A directory with text files						                	#	
#Output: A tsv file with the statistics (each file per line)						#
#Example: python3 general_TTR.py toycorpus/								#
########################################################################################################

import os
import sys
from re import sub
import numpy as np
from collections import defaultdict, Counter
#from nltk.util import ngrams
from random import sample
from itertools import chain
import pandas as pd
#import seaborn as sb

import sklearn

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 6]


############################################################################


directory=sys.argv[1]  #tsv directory 
all_files = os.listdir(directory)

#outputname=directory[:-1]+'_ttr_analysis.tsv'
#outputfile = open(outputname,'a')
#outputfile.write('Corpus\tTTR\tTypes\tTokens\tTTR_trigrams\ttrigrams_types\ttrigrams_tokens\tTTR_unigrams\tunigrams_types\tunigrams_tokens:\n')

merges = pd.read_csv('merges0to350.csv',  sep='\t')
for n in all_files:
	inputcorpus=directory+n
	data = pd.read_csv(inputcorpus,  sep='\t')
	print ("Processing"+n)

	fileparts=n.split(".")
	#outputplot=fileparts[0]+".merges.png"
	outputplot=fileparts[0]+".png"

	
	fig = plt.figure(figsize=(20, 10))
	#fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	xs = data['word_types']
	ys = data['cum_freq']
	zs = data['idiosincracy_index']


	ax.set_xlabel('Num. of types that contain the subword')
	ax.set_ylabel('Cum. freq')
	ax.set_zlabel('Idiosincracy_index')

	img=ax.scatter(xs, ys, zs, s=50, alpha=0.6, edgecolors='w')
	#img=ax.scatter(xs, ys, zs, s=50, c=merges)
	#fig.colorbar(img)
	plt.savefig(outputplot)


  


#outputfile.close()

