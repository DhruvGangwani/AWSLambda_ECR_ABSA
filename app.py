from preprocessing.preprocessing import preprocess 
from preprocessing.get_nouns import get_noun
from preprocessing.word_similarity import get_similar_words
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, AutoModelForSequenceClassification
from transformers import pipeline
from get_sentiment import get_sentiment
from twitter.scrap_data import get_tweets
from credentials import consumer_key, consumer_secret, access_token, access_token_secret
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
    

qa_tokenizer = AutoTokenizer.from_pretrained("./models/qa_model")
qa_model = AutoModelForQuestionAnswering.from_pretrained("./models/qa_model")
qa_model = pipeline('question-answering', model=qa_model, tokenizer=qa_tokenizer)

sent_tokenizer = AutoTokenizer.from_pretrained("./models/sentiment_model")
sent_model = AutoModelForSequenceClassification.from_pretrained("./models/sentiment_model")
sent_model = pipeline('text-classification', model=sent_model, tokenizer=sent_tokenizer)

def compute(text, aspects):
	#preprocessing
	preprocess_text = preprocess(text)
	#get nouns
	noun_list = get_noun(preprocess_text)	
	#get alternative names of aspects
	aspect_classes = get_similar_words(noun_list, aspects)
	#get sentiment
	sentiment_result = get_sentiment(aspect_classes, text)
	return sentiment_result



def aspect_sentiment(aspects, hashtag):
	# request_content = requests.get_json()
	# aspects = request_content.get('aspects', None)
	# hashtag = request_content.get('hashtag', None)

	if not aspects or aspects == list() :
		return {'statusCode': 400, 'body': 'aspects not found in request'}

	if not hashtag or hashtag.strip() == '':
		return {'statusCode': 400, 'body': 'hashtag not found in request'}

	#extracts 50 tweets regarding the hashtag from twitter
	twitter_content = get_tweets(hashtag, consumer_key, consumer_secret, access_token, access_token_secret, tweet_count=50)
	aspect_score = {asp : {'positive': 0, 'negative': 0} for asp in aspects}
	
	if twitter_content.to_dict():
		for text in twitter_content['text']:
			sentiment_result = compute(text, aspects)
			for result in sentiment_result:
				score = sentiment_result[result]
				if score>0:
					aspect_score[result]['positive'] = aspect_score[result]['positive'] + score
				elif score<0:
					aspect_score[result]['negative'] = aspect_score[result]['negative'] - score
				else:
					pass
	else:
		return {'statusCode': 400, 'body': 'No twitter data scraped for this hashtag'}



	result_list = [[k, 'positive', v['positive']] for k,v in aspect_score.items()]
	result_list.extend([[k, 'negative', v['negative']] for k,v in aspect_score.items()])

	aspects_df = pd.DataFrame(result_list, columns= ['aspect', 'sentiment', 'score'])
	sns.barplot(x = 'aspect', y = 'score', hue='sentiment', data=aspects_df)
	plt.show()


# aspects = ['screen', 'battery', 'design', 'camera']
# hashtag = '#oneplus7pro'
# aspect_sentiment(aspects, hashtag)