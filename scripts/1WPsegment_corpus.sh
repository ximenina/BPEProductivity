########################################################################################################
#Script that segments (subword tokenizes) a corpus using WordPiece and a range of merges                                         #
#												       #
#Input: - A folder with a set of text files, ideally one language per file
#       - Range of BPE merges we want to apply
#
#Output: An output folder that contains (for each text file) the following output fileS:
# - .model
# - .freqs.tsv
# - .freqsprod.tsv files
#         
#How to run: ./segment_corpus.sh
####################################################################################################

# Declare input corpus and range of merges:
input_corpus=udhr_intersection_wtok #The input corpus folder with several text files (one per language). This must be a subfolder inside ../corpora/ (preferably a corpus that already went through the word tokenizer script)
declare -i init=1     #initial merge
declare -i final=200   #final merge
declare -i step=1     #Step size

outputfolder=WPsegmented_"$input_corpus"_"$init"_"$final"_"$step"  #The results will be stored in this folder (under ../corpora/)

rm -rf ../corpora/"$outputfolder"
mkdir ../corpora/
mkdir ../corpora/"$outputfolder"

for f in `ls ../corpora/"$input_corpus"/`; #For each language/file in the corpus folder

do	
	echo "Processing $f"
	mkdir ../corpora/"$outputfolder"/"$f"
	cat  ../corpora/"$input_corpus"/"$f" |sed 's/[.,"()?¿?¡!»«“”،/\]//g' |tr '[:upper:]' '[:lower:]' >  ../corpora/"$input_corpus"/"$f".tmp  #tmp file lowercased and filtered


	python3 wp_merges.py ../corpora/"$input_corpus"/"$f".tmp "$final"  #this script will output all the mdoels and files up to n merges in just one run
	#this script outputs: .model, .freqs.tsv, freqsprod.tsv for each merge (step 1, up to final)
	mv ../corpora/"$input_corpus"/"$f".tmp.*.model  ../corpora/"$outputfolder"/"$f"/
	mv ../corpora/"$input_corpus"/"$f".tmp.*.freqsprod.tsv  ../corpora/"$outputfolder"/"$f"/
	mv ../corpora/"$input_corpus"/"$f".tmp.*.freqs.tsv   ../corpora/"$outputfolder"/"$f"/
		
	#replace "tmp" on the filenames:
	#for x in ../corpora/"$outputfolder"/"$f"/*; do mv "$x" "$(echo "$x" | sed s/.tmp//)"; done
		
		
	
	rm ../corpora/"$input_corpus"/"$f".tmp #we erase the tmp processed text (lowercase, filtered)
	
	find ../corpora -type f -name "*.tmp.*"  | xargs -r rename "s/tmp.//"

	
	
done

	

echo "DONE. See output in ../corpora/$outputfolder"

