#Fix   re-order answe-red, pampe-red  
#read the model
#store per each merge the subwords that were merged  (separated by spaces)
#Go to segmented text of each merge to see the frequency of the subwords that were merged
#From the original text, extract the number of types (and frequency of these types) in which the merged subword appears

#original segmented: j@@ u@@ d@@ a
#We eliminate spaces: j@@u@@d@@a
#We search for the subwords, substitute </w> for end of the word

from collections import Counter
import sys
sys.stdout.reconfigure(encoding='utf-8')
import csv
import re

inputcorpus=sys.argv[1]   #WP MODEL (last line)     ab 	 ('a', '##b')
inputcorpus2=sys.argv[2]  #BPE freqsprod, e.g.,    T ##h ##i ##s	3

i=1


subwords=[]

####1. We read the BPE model  (actually the .sh scriot will only send the last line of the model)
with open(inputcorpus,'r', encoding="utf-8") as myfile: 
	content = myfile.readlines()
	for x in content:
		tmp=x.lower().split("\t")	
		subwords.append(tmp[1].strip())   #---> list of merged patterns: ['##y,', 'ab', '##fu']
			

#print(len(subwords))


###2. We read the freqsprod file   T ##h ##i ##s	3
words={}
with open(inputcorpus2,'r', encoding="utf-8") as myfile: 
	content = myfile.readlines()
	for x in content:
		tmp=x.lower().split("\t")
		words[tmp[0].strip()]= int(tmp[1])  #words[word]=freq

#print (words)

#import sys
#sys.exit()


##3. We start retrieving frequencies of merged patterns:

total_productivity=0
k=0;

#H ##o ##p ##e ##fu ##l ##l ##y,   We are going to find the words that contain ##fu (column 1 in .model) and extract the frequency

for wsub in subwords:
	k=k+1
	counter_words=0
	cumulative_freq=0
	# aabbbbaaabbbaaabb "aa" happens with kallalisut" How ti take into account this?  aa	-> aa@@l@@a@@j@@a@@n@@g@@i@@u@@p@@p@@aa@@t
	#If the subword it's at initial word position: (This is different than BPE, where there's distinction between final position and the rest)
	for w in words:
		exist_count = w.count(wsub)  #how many times does the word contain the subw
		#print(wsub, w, exist_count)
		if (exist_count>0): #at least one occurenceof the subw on the current w
			printing_list=[wsub, w, words[w]]
			print(*printing_list, sep='\t')	
			counter_words=counter_words+1
			cumulative_freq=cumulative_freq+words[w] #accumulated frequency of each type in which the subword appears

		

	productivity_index=cumulative_freq/counter_words #The higher the less productive
	total_productivity=total_productivity+productivity_index

	printing_list=["subword:"+wsub,counter_words, cumulative_freq, productivity_index]
	print(*printing_list, sep='\t')		
	
