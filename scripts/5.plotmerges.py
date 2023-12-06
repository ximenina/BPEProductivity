#############################################################################################################################################################################
#Script for generating 3D plots of BPE merges per each language.                                                                                                            #
#The colors of data points are a visual cue for the merge operation (i.e. from 1 to 200) at which the respective subword was created.				            #
#INPUT: A folder with TSV files containing the summary of the BPE productivity measures (one per language). Each TSV file should contain the following header:              #
#subword	prod	cum_freq	idiosincracy_index													    #	
#OUTPUT: A folder with .png plots (one plot per language).														    #
#Example of how to run: python3 plotmerges.py ../results/corpusPBC_summary_tsv/	200 					             					    #	
#############################################################################################################################################################################

import os
import sys
from re import sub
import numpy as np
from collections import defaultdict, Counter
#from nltk.util import ngrams
from random import sample
from itertools import chain
import pandas as pd


import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 6]
font = {
        
        'size'   : 14}
#'weight' : 'bold',
plt.rc('font', **font)




############################################################################


directory=sys.argv[1]  #tsv directory
merges=int(sys.argv[2])  #merges

try: 
    output=directory+"../plots"
    os.mkdir(output) 
except OSError as error: 
    print("Output directory already exists") 

#import sys
#sys.exit()


all_files = os.listdir(directory)

merges=list(range(1, merges+1)) #merges that we are going to analyze (fixed to the first 200)


for n in all_files:
	inputcorpus=directory+n
	data = pd.read_csv(inputcorpus,  sep='\t')
	print ("Processing"+n)

	fileparts=n.split(".")

	outputplot=fileparts[0]+".png"  #Output file where the plot is going to be saved

	
	fig = plt.figure(figsize=(20, 10))
	
	ax = fig.add_subplot(111, projection='3d')

	
        #3D plot:
	xs = data['prod']
	ys = data['cum_freq']
	zs = data['idiosincracy_index']
	cs=merges # For coloring the datapoints

	ax.set_xlabel('|W|(productivity)', labelpad=6, fontweight='bold')
	ax.set_ylabel('C. freq',labelpad=6, fontweight='bold')
	ax.set_zlabel('Idiosyncrasy',labelpad=3, fontweight='bold')

	img=ax.scatter(xs, ys, zs, s=50, c=cs, cmap='brg_r')


	fig.colorbar(img)
	plt.savefig(output+"/"+outputplot)




