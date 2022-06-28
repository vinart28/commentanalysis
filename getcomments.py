import requests  # для api-запросов


tokenYoutube = "AIzaSyD7DOSK9XVtr1Bo0z3e3qO_Wr5RBbKj67U" 
URL = 'https://youtube.googleapis.com/youtube/v3/commentThreads'


def getComments(videoId, pageToken): 
  params = {'part': 'snippet,replies', 'videoId': videoId, 'key': tokenYoutube, 'maxResults': 100, 'pageToken': pageToken} # формируем переменную парамс - словарь, переменная с видео, кеу - токен ютуб, пейджтокен  

  response = requests.get(URL, params).json() #делаем запрос по апи ютуб и получаем в ответ данные в формате json 
  
  commentsList = [] #пустой массив 

  # Не вылетать если комментарии отключены !! https://www.youtube.com/watch?v=MUQ_YwX7zsQ 
  if 'pageInfo' not in response:
    return commentsList, None
    #проверяем есть у видео возможность оставлять комментарии. Если нет, возвращаем пустой массив, нон возвращается в качестве токена 

  # Не вылетать если нет комментариев !! https://www.youtube.com/watch?v=oU9jA2rN1w0&ab_channel=TheNotoriousNinjaduck
  if response['pageInfo']['totalResults'] == 0:
    return commentsList, None
     #проверяем есть у видео комментарии. Если нет, возвращаем пустой массив, нон возвращается в качестве токена
#проходим по комментариям и всем веткам к коментариям (обсуждениям) и добавляем данныем в массив 
  for item in response['items']:
    commentsList.append(f"{item['snippet']['topLevelComment']['snippet']['textOriginal']}")

    if 'replies' in item:
      replies = item['replies']['comments']
      for reply in replies:
        commentsList.append(f"{reply['snippet']['textOriginal']}")

  if 'nextPageToken' in response: #проверяем если есть токен следубщей страницы,позвращаем заполненный на предудущем шаге массив и пейдж токен. 
    return commentsList, response['nextPageToken']

  return commentsList, None #если пейдж токена нет, возрвращаем полученный заполненный массив на предыдущим шаге и нан вместо токена 