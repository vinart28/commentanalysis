from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
# python -m dostoevsky download fasttext-social-network-model прописать в Shell для получения предобученной модели 


model = FastTextSocialNetworkModel(tokenizer=RegexTokenizer()) #происходит обучение модели на выборке


def sentimentAnalysis(commentsList):
  predictions = model.predict(commentsList, k = 2) 
  
  return predictions #возвращаем массив предсказаний 