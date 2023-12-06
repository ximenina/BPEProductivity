########################################################################################################
#Script that segments (subword tokenizes) a corpus using BPE and a range of merges                                         #
#												       #
#Input: - A folder with a set of text files, ideally one language per file
#       - Range of BPE merges we want to apply
#
#Output: An output folder that contains (for each text file) the following output fileS:
# - .model
# - .freqs.tsv (frequency distribution of the subwords vocabulary at each merge)
# - .freqsprod.tsv files  (frequecy distribution of the words at each merge) 
#
#         
#How to run: ./segment_corpus.sh
####################################################################################################

# Declare input corpus and range of merges:
input_corpus=udhr_intersection_wtok #The input corpus folder with several text files (one per language). This must be a subfolder inside ../corpora/
declare -i init=0     #initial merge
declare -i final=200   #final merge
declare -i step=1     #Step size

outputfolder=BPEsegmented_"$input_corpus"_"$init"_"$final"_"$step"  #The results will be stored in this folder (under ../corpora/)

rm -rf ../corpora/"$outputfolder"
mkdir ../corpora/
mkdir ../corpora/"$outputfolder"

for f in `ls ../corpora/"$input_corpus"/`; #For each language/file in the corpus folder

do	
	echo "Processing $f"
	mkdir ../corpora/"$outputfolder"/"$f"

	#For each merge:
	for ((i=init; i<=final; i=i+step)); 
	do
		#We learn the BPE model (lower case and filter some general punctuation marks):
		cat  ../corpora/"$input_corpus"/"$f" |sed 's/[.,"()?¿?¡!»«“”،/\]//g' |tr '[:upper:]' '[:lower:]'| subword-nmt learn-bpe -s "$i" >../corpora/"$outputfolder"/"$f"/"$f"."$i".model
		
		
		#We apply it:
		cat  ../corpora/"$input_corpus"/"$f" |sed 's/[.,"()?¿?¡!»«“”،/\]//g' |tr '[:upper:]' '[:lower:]'| subword-nmt apply-bpe -c ../corpora/"$outputfolder"/"$f"/"$f"."$i".model > ../corpora/"$outputfolder"/"$f"/"$f"."$i".txt
		

		#We calculate frequencies of each tokenized file:	
		python3 freq.py ../corpora/"$outputfolder"/"$f"/"$f"."$i".txt  #outputs:.freqs.tsv

                # We replace "@@ " for "@@" (in place), and then we calculate productivy measures for the subwords in each tokenized file 
		sed -i 's/@@ /@@/g' ../corpora/"$outputfolder"/"$f"/"$f"."$i".txt
		python3 freq_productivity.py ../corpora/"$outputfolder"/"$f"/"$f"."$i".txt  # (outputs: .freqsprod.tsv)

		#We erase the segmented version of the corpus (*.txt) to free space. We only keep the model, the frequency and productivity measures of the BPE subwords:
		rm ../corpora/"$outputfolder"/"$f"/"$f"."$i".txt
		
		
	done
	
	
	
done

echo "DONE. See output in ../corpora/$outputfolder"

