from getcomments import getComments
from sentimentAnalysis import sentimentAnalysis
from getPlotImageFromPredictions import getPlotImageFromPredictions


COMMENTS_LIMIT = 30000 #переменная отображает, сколько комментариев мы готовы обработать. Для экономии времени бработки данных мы ограничили это число до 10к. Этих данных достаточно для получения результативного графика 


def handleVideoComments(videoId):
  pageToken = ''#API ютуб отдает 10000 коммментариев на странице, если их больше, он возвращает токен следующей страницы с комментариями. 
  predictions = [] # массив, в который мы будем "складывать" предсказания 
  
  while True:
      
    commentsList, pageToken = getComments(videoId, pageToken) #создаем переменную коментлист, сложим в нее комментарии после выполнения функции геткоментс, в пейдж токен получим токен если он будет
    
    if not commentsList: #если не будет коментов прерываем цикл, выдаем сообщение пользователю строка 28
      break
    
    predictions.extend(sentimentAnalysis(commentsList)) #если комментарии получены переходим к функции анализа. Результатом будет массив, полученный от фукции аналза данных (объедениение изначального пустого масиива и обработанного - функция экстенд. После кждой обработк данные в масиив будут дозаписываться)
    #print('пейдж токен: ', pageToken)
    if not pageToken:
      break #если нетпейдж токена выходим из цикла 

    if len(predictions) >= COMMENTS_LIMIT:
      break #если длина массива больше установленного лимита тоже выходим из цикла  

  if not predictions:
    return None, 'Видео не содержит комментариев.'
  
  return getPlotImageFromPredictions(predictions), None # возвращаем результ в виде картинки и нон вместо ошибки
