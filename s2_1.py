# -*- coding: utf-8 -*-
"""S2_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1muADcaTeBYqKZ-7upLF7_1B6zSMc8tqL

Zadaniem sieci jest przypisanie etykiety do odpowiedniego obrazka z liczbą.

Dokumentacja gotowego badania: *https://keras.io/api/datasets/mnist/*

images=x, labels=y

####***1.Import bibliotek***
"""

import keras
from keras.datasets import mnist #gotowy zbiór danych z tego badania
import matplotlib.pyplot as plt #wizualizacje
from keras import models, layers #sieci neuronowe
from keras.utils import to_categorical #kategoryzacja
import numpy as np #działania na wektorach

"""####***2.Przygotowanie danych***"""

#Podział zbioru danych na zbiór uczący i testowy (według gotowego podziału z dokumentacji)

(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

#Przegląd danych

print(train_labels) #labels - jakie etykiety są przypisane kolejno w zbiorze
print(train_images.shape) #images - ile jest obrazków w zbiorze, rozmiar obrazków w pikselach
print(test_images.shape)
plt.imshow(train_images[47],cmap=plt.cm.binary) #funkcja do drukowania obrazków
print(train_labels[47])

"""####***3.Budowa i uczenie sieci***"""

#Budowa sieci

network = models.Sequential()

#warstwa wejściowa (256 neuronów, funkcja aktywacji: relu, rozmiar 28*28 bo tyle pikseli ma jedno zdjęcie)

network.add(layers.Dense(256,activation='relu',input_shape=(28*28,)))
#można zmieniać liczbę warstw, funkcj, żeby zoptymalizować wynik

#warstwa wyjściowa 10 neuronów bo mamy 10 cyfr które możemy przypasować do zdjęć

network.add(layers.Dense(10,activation='sigmoid',input_shape=(28*28,)))

network.summary()

p#kompilowanie sieci (podajemy jaką metodą będzie uczona)

network.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])
print(train_labels[0])

#kategoryzacja danych

train_labels=to_categorical(train_labels)
test_labels=to_categorical(test_labels)
print(train_labels[0])

#normalizacja danych wejściowych (żeby szybciej działała sieć)

print(train_images[0]) #wyświetla piksele obrazka, chcemy przeskalować na przedział 0-1
train_images=train_images.reshape((60000,28*28)) #niby mamy podany rozmiar ale przekształcamy na 28*28 na wszelki wypadek
test_images=test_images.reshape((10000,28*28))
train_images=train_images.astype('float32')/255 #dzielimy przez 255 bo wiemy że 255 to maks a chcemy liczby z przedziału 0-1
test_images=test_images.astype('float32')/255
print(train_images[0])

#uczenie sieci

network.fit(train_images,train_labels,epochs=5, batch_size=128)
#epochs - liczba przejść przez zbiór uczący, które model ma wykonać podczas uczenia
#batch_size - rozmiar partii danych, który jest używany podczas jednej iteracji przez proces uczenia

"""####***4.Ocena jakości klasyfikacji***"""

#sprawdzenie wyników na zbiorze testowym (czy nie przeuczyliśmy sieci)

test_loss, test_acc = network.evaluate(test_images, test_labels)
print(test_loss) # to samo bez zaokrągleń
print(test_acc)

#sprawdzamy na losowym zdjęciu

(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data() #dzielimy zbiór jeszcze raz bo znormalizowaliśmy piksele i wyświetlenie obrazka nie jest możliwe
img=test_images[410]
plt.imshow(img)
print(test_labels[410])

network.save('rozpoznawanie.cyfr.model')
new_model=kerasmodels.load_model('rozpoznawanie.cyfr.model')

#normalizujemy nasze losowo wybrane zdjęcie

img=img.reshape((28*28))
img=img.astype('float32')/255

#sprawdzamy wynik dla tego obrazka

result=new_model.predict(np.array([img]))
print(result)
print(np.argmax(result)) #etykieta = numer pozycji dla której wartość jest największa