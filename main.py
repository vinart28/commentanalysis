import telebot
from pytube import extract  # для получения id видео из ссылки
import sqlite3
#from dostoevsky.tokenization import RegexTokenizer
#from dostoevsky.models import FastTextSocialNetworkModel

from handleVideoComments import handleVideoComments



bot = telebot.TeleBot("5298919963:AAGMVwkHc2kIwqhQRWs8k5gO1dUopZkoS74")

dbConnection = sqlite3.connect('history.db', check_same_thread=False)
dbCursor = dbConnection.cursor()
dbCursor.execute('''CREATE TABLE IF NOT EXISTS urls_history (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, user_id, url TEXT)''')  # можно еще колонку с датой date TEXT
dbConnection.commit()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Привет {message.chat.first_name}. Пришли мне ссылку на YouTube-видео")
    


@bot.message_handler(commands=['history'])
def history_message(message):
  result = ''
  urls = dbCursor.execute(f'SELECT DISTINCT url FROM urls_history WHERE user_id == {message.chat.id};')
  
  for index, url in enumerate(urls):
    result += f'{index+1}. {url[0]}\n'

  if len(result) == 0:
    bot.send_message(message.chat.id, 'Ссылок ещё не было 🤔')
    return    
    
  if len(result) > 4096: 
    for x in range(0, len(result), 4096):
      bot.send_message(message.chat.id, result[x:x+4096], disable_web_page_preview=True)
  else:
    bot.send_message(message.chat.id, result, disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def catch_message(message):
  
  urls = [possiblyLink for possiblyLink in message.text.split() if 'youtu.be/' in possiblyLink.lower() or 'youtube.com/' in possiblyLink.lower()] #

  if not urls:
    bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуй, пожалуйста, другую ссылку.')
    return
# если массив возможных ссылок пустой, то вдаем сообщени об ошибке 
  
    # если массив не пустой, то переходим в цикл 
  
  for url in urls:
   
    try:
      videoId = extract.video_id(url) #пробуем извлечь id из элемента массива - ссылки, если это не удается сделать, то срабатывает exept, если id корректный, то мы записываем его в переменную videoId
    except:
      bot.send_message(message.chat.id, f'URL: {url}\n\nЧто-то пошло не так. Попробуй, пожалуйста, другую ссылку.', disable_web_page_preview=True)
      continue
      
    bot.send_message(message.chat.id, 'Подождите немного, мы обрабатываем данные')
    
    dbCursor.execute('INSERT INTO urls_history VALUES(?, ?, ?);', [None, message.chat.id, url])
    dbConnection.commit() #записываем информацию в базу данных 
  
    plotImage, errorMessage = handleVideoComments(videoId) #передаем переменную видеоid в функцию, получаем картинку либо сообщение об ошибке
    
    if errorMessage: #проверяем есть ли сообщение об ошибке да выдаем сообщение , нет - спасибо получите график 
      bot.send_message(message.chat.id, f'URL: {url}\n\n{errorMessage}', disable_web_page_preview=True)
      continue

    bot.send_photo(message.chat.id, plotImage, caption=f'URL: {url}')# если не вылетили в предудыщем блоке то выдаем картинку с подписью !)))))) за подпись отвечает параметр капшн 

bot.polling()


# Если появляется ошибка "'TeleBot' object has no attribute 'message_handler'", прописать в Shell pip3 install --upgrade pyTelegramBotAPI
# Айдишники для тестов: https://www.youtube.com/watch?v=AR6ovvs6Ihg (очень много комментариев), https://www.youtube.com/watch?v=6ayq4-YtfEs (мало комментариев)

bot.infinity_polling()

  
