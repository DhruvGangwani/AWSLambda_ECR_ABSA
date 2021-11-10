import spacy

nlp = spacy.load('en_core_web_md')

def get_similar_words(nouns, aspects):
	aspect_classes = {k: list() for k in aspects}
	for noun in nouns:
		scores = list()
		for aspect in aspects:
			aspect_token = nlp(aspect)
			noun_token = nlp(noun)
			similarity_score = aspect_token.similarity(noun_token)
			scores.append(similarity_score)
		index = scores.index(max(scores))
		aspect_name = aspects[index]
		
		if max(scores)>0.60:
			value = aspect_classes[aspect_name]
			value.append(noun)
			aspect_classes[aspect_name] = list(set(value))
			
		else:
			pass
	return aspect_classes	





# if __name__ == '__main__':
# 	nouns = ['screen', 'battery']
# 	aspects = ['display', 'battery', 'design', 'iphone13']
# 	result = get_similar_words(nouns, aspects)
# 	print(result)