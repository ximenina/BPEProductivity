#######################################################################################
#Script for word-level tokenizing corpora. It requires Polyglot library.
#
# How to run: ./0wordtokenize_corpus.sh
# You must declare first the input corpus folder that you want to process.
########################################################################################

input_corpus=udhr_intersection #The input corpora folder with several text files (one per language). This must be a subfolder inside ../corpora/


outputfolder="$input_corpus"_wtok  #The results will be stored in the ../corpora/ folder
0
rm -rf ../corpora/"$outputfolder"
mkdir ../corpora/"$outputfolder"

for f in `ls ../corpora/"$input_corpus"/`; #For each language/file in the corpus folder

do	
	echo "Processing $f"
	python3 tokenize_corpus.py ../corpora/"$input_corpus"/"$f" > ../corpora/"$outputfolder"/"$f"
	

	
	
done

echo "DONE. See output in ../corpora/$outputfolder"

