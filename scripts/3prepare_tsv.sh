########################################################################################################
#Script that takes as an input a folder with the productivity measures ouput and it prepares  a tsv (one per language) with a summary of the measures (Taken from the *summary files) 
#This will be used for future processing
#for making graphs, clustering, etc.
#
#subword	prod	cum_freq	idiosincracy_index
#
#
####################################################################################################

input_folder=WPresults_productivity_udhr_intersection_wtok_1_10_1
output_folder=tsv
rm -rf ../outputs/"$input_folder"/"$output_folder"
mkdir ../outputs/"$input_folder"/"$output_folder"

cp ../outputs/"$input_folder"/*.summary ../outputs/"$input_folder"/"$output_folder"/

for f in `ls ../outputs/"$input_folder"/"$output_folder"/`;

do	
	echo "Processing $f"
	#Add a header:
        sed -i '1s/^/subword	prod	cum_freq	idiosincracy_index\n/' ../outputs/"$input_folder"/"$output_folder"/"$f"
	#We replace "subword:" from each row:
	sed -i 's/subword://g' ../outputs/"$input_folder"/"$output_folder"/"$f"
	
done

echo "DONE. See output in ../outputs/$input_folder/$output_folder"




