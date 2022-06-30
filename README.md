# Бот для анализа комментариев youtube роликов @commentanalysis
Код программы для чат-бота был написан в среде разработки https://replit.com/

#Установка и настройка#
1) для запуска приложения в личном боте, необходимо в main в строке bot = telebot.TeleBot("5298919963:AAGMVwkHc2kIwqhQRWs8k5gO1dUopZkoS74"), указать в "" token своего бота. 
2) для проведения корректного анализа комментариев библиотекой dostoevsky прописать в Shell для получения предобученной модели: python -m dostoevsky download fasttext-social-network-model 
3) если появляется ошибка "'TeleBot' object has no attribute 'message_handler'", прописать в Shell pip3 install --upgrade pyTelegramBotAPI

#Если возникнут ошибки при запуске программы с использованием токена личного бота, чтобы протестировать работу можно перейти по ссылке https://replit.com/@MariiaKotova/Python#getPlotImageFromPredictions.py, запустить http://joxi.ru/zANqRL9t1OV1g2, перейти  в чат-бот @commentanalysis и отправить боту команду /start
