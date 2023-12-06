##   How to run: python3 wp_merges.py file number_of_merges
# It returns 3 files per each merge: *.freqs.tsv, *.freqsprod.tsv, *.model
#
#  freqs.tsv =  Frequency distribution of the vocabulary at each merge
#   freqsprod.tsv = frequency distribution of the words at each merge. 
#  model = The symbols that were merged at each merge operation. 
################################################################################################

# Inspired by the code in:  https://huggingface.co/learn/nlp-course/chapter6/6?fw=pt


from collections import defaultdict
import sys
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding='utf-8')


arguments=sys.argv

with open(arguments[1], encoding='utf-8') as file:  #Reading training textfile
	corpus = [line.rstrip() for line in file]


merges=arguments[2]

word_freqs = defaultdict(int)

for text in corpus:
	for word in text.split():
		
		word_freqs[word] += 1

#print(word_freqs)


alphabet = []
for word in word_freqs.keys():
	if word[0] not in alphabet:
		alphabet.append(word[0])
	for letter in word[1:]:
		if f"##{letter}" not in alphabet:
			alphabet.append(f"##{letter}")


#print(alphabet)

vocab = alphabet.copy()

splits = {
	word: [c if i == 0 else f"##{c}" for i, c in enumerate(word)]
	for word in word_freqs.keys()
}


def compute_pair_scores(splits):
	letter_freqs = defaultdict(int)
	pair_freqs = defaultdict(int)
	for word, freq in word_freqs.items():
		split = splits[word]
		if len(split) == 1:
			letter_freqs[split[0]] += freq
			continue
		for i in range(len(split) - 1):
			pair = (split[i], split[i + 1])
			letter_freqs[split[i]] += freq
			pair_freqs[pair] += freq
		letter_freqs[split[-1]] += freq

	scores = {
		pair: freq / (letter_freqs[pair[0]] * letter_freqs[pair[1]])
		for pair, freq in pair_freqs.items()
	}
	return scores






def merge_pair(a, b, splits):
	for word in word_freqs:
		split = splits[word]
		if len(split) == 1:
			continue
		i = 0
		while i < len(split) - 1:
			if split[i] == a and split[i + 1] == b:
				merge = a + b[2:] if b.startswith("##") else a + b
				split = split[:i] + [merge] + split[i + 2 :]
			else:
				i += 1
		splits[word] = split
	return splits

#splits = merge_pair("a", "##b", splits)
#print(splits["about"])

def encode_word(word):
	tokens = []
	while len(word) > 0:
		i = len(word)
		while i > 0 and word[:i] not in vocab:
			i -= 1
		if i == 0:
			return ["[UNK]"]
		tokens.append(word[:i])
		word = word[i:]
		if len(word) > 0:
			word = f"##{word}"
	return tokens


#merges = 30
for i in range(int(merges)):
	#Storing outputs:
	filemerges = open(arguments[1]+"."+str(i+1)+".model", "w", encoding='utf-8')
	filefreqs= open(arguments[1]+"."+str(i+1)+".freqs.tsv", "w", encoding='utf-8')
	filefreqsprod= open(arguments[1]+"."+str(i+1)+".freqsprod.tsv", "w", encoding='utf-8')

	scores = compute_pair_scores(splits)
	best_pair, max_score = "", None
	for pair, score in scores.items():
		if max_score is None or max_score < score:
			best_pair = pair
			max_score = score
	splits = merge_pair(*best_pair, splits)
	new_token = (
		best_pair[0] + best_pair[1][2:]
		if best_pair[1].startswith("##")
		else best_pair[0] + best_pair[1]
	)
	print((i+1),"\t", new_token, "\t", best_pair, file=filemerges)   #printing example:  ab ('a', '##b') #filenames start with 1 as the first merging index.
	#printing_line=str(i)+"\t"+ new_token+ "\t"+ best_pair	
	#filemerges.write(printing_line) #print example:  ab ('a', '##b')
	
	vocab.append(new_token)   #each new_token is a merge of symbols that is added to the original vocabulary (comprised by chars and subwords)


	#Read the corpus and encode word by word:
	words=[]
	subwords=[]

	for text in corpus:
		sentence=[]
		for word in text.split():
			segmented_word=encode_word(word)
			words.append(" ".join(segmented_word)) #for obtaining the counts for freqsprod.tsv
			for subw in segmented_word:
				subwords.append(subw) #for obtaining the counts for freqs.tsv		
		
			sentence.append(" ".join(encode_word(word)))	#encode_word returns an array, we convert it to a string
		#print(" ".join(sentence))

	frequencywords=Counter(words)
	#We print Frequencies:
	for value, key in sorted([(j,i) for i,j in frequencywords.items()], reverse=True):
		if (key != ""):
			filefreqsprod.write(str(key)+ '\t'+str(value)+'\n')
			#print (str(key)+ '\t'+str(value)+'\n')


	frequencysubwords=Counter(subwords)
	#We print Frequencies:
	for value, key in sorted([(j,i) for i,j in frequencysubwords.items()], reverse=True):
		if (key != ""):
			filefreqs.write(str(key)+ '\t'+str(value)+'\n')
			#print (str(key)+ '\t'+str(value)+'\n')

	#print(words)
	#print(subwords)

	filemerges.close()
	filefreqs.close()
	filefreqsprod.close()


