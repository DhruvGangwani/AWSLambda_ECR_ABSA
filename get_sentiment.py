
def get_sentiment(aspect_classes, text):
  sentiment_dict = {k:0 for k in aspect_classes}
  for aspect in aspect_classes:
    alt_names = aspect_classes[aspect]
    for name in alt_names:
      question = f'how is {name}'
      QA_input = {'question': question, 'context': text}
      qa_result = qa_model(QA_input)
      answer = qa_result['answer']

      #sentiment model 
      sent_result = sent_model(answer)    
      print(sent_result)
      sentiment = sent_result[0]['label']

      if sentiment == 'LABEL_0':
        sentiment, score = 'Negative', -1
      elif sentiment == 'LABEL_1':
        sentiment, score = 'Neutral', 0
      else:
        sentiment, score = 'Positive', 1
    
      value = sentiment_dict[aspect] + score
      sentiment_dict[aspect] = value
  return sentiment_dict

# if __name__ == '__main__':
# 	aspect_classes = {'display': ['screen'], 'battery': ['battery'], 'design': [], 'iphone13': []}
# 	text = 'screen is not good but battery performance is never good'
# 	result = get_sentiment(aspect_classes, text)
# 	print(result)
#       