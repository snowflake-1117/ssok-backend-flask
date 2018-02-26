from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from sklearn import model_selection, metrics
import os, glob, json
import csv
import numpy as np
import json

root_dir = "./data/"
dic_file = root_dir + "/word-dic.json"

word_dic = json.load(open(dic_file))
max_words = word_dic["_MAX"]

# get numbers of class by counting files
files = glob.glob(root_dir + "*.wakati", recursive=True)
nb_classes = len(files)-1
print("nb_classes:",nb_classes)

batch_size = 64
nb_epoch = 20

# MLP 모델 생성하기 --- (※1)
def build_model():
    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy'])
    return model


# 데이터 읽어 들이기--- (※2)
data = json.load(open("./data/train_data.json"))
X = data["X"] # 텍스트를 나타내는 데이터
Y = data["Y"] # 카테고리 데이터

# 학습하기 --- (※3)
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
Y_train = np_utils.to_categorical(Y, nb_classes)
print("train:",len(X),len(Y))
model = KerasClassifier(
    build_fn=build_model,
    nb_epoch=nb_epoch,
    batch_size=batch_size)
model.fit(np.array(X),np.array(Y))


# 예측하기 --- (※4)
# 데이터 읽어 들이기--- (※5)
data = json.load(open("./data/train_data.json"))
X = data["X"] # 텍스트를 나타내는 데이터
Y = data["Y"] # 카테고리 데이터
predicts = model.predict(np.array(X))
print("predict:",len(np.array(X)))

ac_score = metrics.accuracy_score(Y, predicts)
cl_report = metrics.classification_report(Y, predicts)
print("정답률 =", ac_score)
print("리포트 =\n", cl_report)

# decode the prediction
print('Predicted:')
category_names = ["affair", "event", "recruit", "scholarship", "student"]
with open('mlp3-classifier.csv',"w",encoding="utf8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Division'])
    for position, predict in enumerate(predicts):
        Y_predicted = category_names.__getitem__(predict)
        filewriter.writerow([Y_predicted])
print("end")