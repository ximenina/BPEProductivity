########################################################################################################
#Script that takes as an input a segmented corpus using BPE: it takes the model, and previously generated frequency files.
#It calculates measures of productivity, idiosyncrasy and cumulative frequency of subwods.
#You must declare the input corpus folder and the location of the segmented BPE version
#How to run: ./2BPEproductivity_merges.sh
####################################################################################################

# Declare input corpus, segmented corpus and range of merges:
input_corpus=udhr_intersection_wtok  #The input corpus folder with several text files (one per language). This must be a subfolder inside ../corpora/ 
segmented_corpus=BPEsegmented_udhr_intersection_wtok_0_200_1  #The folder that contains the segmented version of the input corpus, must be inside ../corpora/
declare -i init=1     #From which merge
declare -i final=10  #To which merge
declare -i step=1


outputfolder=BPEresults_productivity_"$input_corpus"_"$init"_"$final"_"$step"

rm -rf ../outputs/"$outputfolder"
mkdir ../outputs/"$outputfolder"


for f in `ls ../corpora/"$input_corpus"/`; #For each language/file in the corpus folder
do
echo "Processing $f"	
	for ((i=init; i<=final; i=i+step));
	do
		
		#obtain last line of the model
		tail -1 ../corpora/"$segmented_corpus"/"$f"/"$f"."$i".model >model.tmp
		
		#run script (for calculating measures) with the model last line and the segmentd frequencies at that merge
		python3 productivity.py model.tmp  ../corpora/"$segmented_corpus"/"$f"/"$f"."$i".txt.freqsprod.tsv >> ../outputs/"$outputfolder/$f.detailed"


	done
		#Filter only the summary of subwords:
		cat ../outputs/"$outputfolder/$f.detailed"| grep "subword:" >> ../outputs/"$outputfolder/$f.summary"
	
	
done

rm model.tmp

echo "DONE. See output in ../output/$outputfolder"

