import pandas as pd
import matplotlib
matplotlib.use('Agg') # переключает серверную часть на «agg», чтобы Matplotlib не пытался отрисовать график в окне.
import matplotlib.pyplot as plt
import io


COLORS ={'neutral':'#87CEFA','negative':'#f25e66','positive':'#98FB98','skip':'#CCCCFF','speech':'#ffcf48'} #указываем цвет длякаждого типа комента 


def preparePredictions(allPredictions):
  # из двух характеристик выбираем одну, с наибольшим значением
  preparedPredictions = []
  for prediction in allPredictions:
    keyWithMaxValue = max(prediction, key=prediction.get)
    preparedPredictions.append({ keyWithMaxValue: prediction[keyWithMaxValue] })
  return preparedPredictions


def getPlotImageFromPredictions(predictions):
  df = pd.DataFrame(preparePredictions(predictions)) #создаем дата фрейм из обоботанных даныых в функции
  buffer = io.BytesIO()
  figure = df.count().plot.bar(color=[COLORS[column] for column in df.columns.values], edgecolor='black',fontsize=14, title='Количество оценок').get_figure() #строимграфик 
  figure.tight_layout()  # Добавляем layout, чтобы не обрезалась картинка.
  figure.savefig(buffer, format='jpg') #сохраняем график в формате
  plt.close(figure)
  buffer.seek(0)
  pic = io.BufferedReader(buffer)
  return pic #возвращаем картинку с графиком. 