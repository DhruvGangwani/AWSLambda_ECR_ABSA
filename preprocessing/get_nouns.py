import nltk

def get_noun(lines):
	tokenized = nltk.word_tokenize(lines)
	nouns = set([word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN')])
	return nouns

# if __name__ == '__main__':
# 	lines = 'battery is not up to the mark but on the other hand screen is good'
# 	result = get_noun(lines)
# 	print(result)