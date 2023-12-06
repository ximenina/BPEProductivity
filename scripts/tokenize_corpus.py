###Script for (word) tokenizing a text using Polyglot library ##

from collections import Counter
import sys
sys.stdout.reconfigure(encoding='utf-8')
import csv
import re
from polyglot.text import Text

inputcorpus=sys.argv[1]  


with open(inputcorpus,'r', encoding="utf-8") as myfile: 
	content = myfile.readlines()
	for x in content: #We tokenize line by line using polyglot
		text = Text(x)  ##Polyglot object
		try:
			tokenized_words=text.words  #Polyglot (orthographic word boundaries)
		except:
			tokenized_words=sample_text.split() #In case there's an error in polyglot, we split just by whitespace 
			

		
		print(*tokenized_words, sep=' ')
