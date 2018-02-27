from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from keras import backend as K
from pymysql import ProgrammingError
from db_manager import DBManager
from get_original_line import get_original_line
import glob, json
import numpy as np


root_dir = "./data/snowe/"
dic_file = root_dir + "/word-dic.json"

word_dic = json.load(open(dic_file))
max_words = word_dic["_MAX"]
MODEL = 'classifier-model.h5py'

# get numbers of class by counting files
files = glob.glob(root_dir + "*.wakati", recursive=True)
nb_classes = len(files) - 1
print("nb_classes:", nb_classes)
batch_size = 64
nb_epoch = 10


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


data = json.load(open(root_dir + "train_data.json"))
X = data["X"]  # 텍스트를 나타내는 데이터
Y = data["Y"]  # 카테고리 데이터
Y_train = np_utils.to_categorical(Y, nb_classes)
print("train:", len(X), len(Y))

# if model already exist, use modelCheckpoint for kerasClassifier
try:
    check = ModelCheckpoint(MODEL, monitor='val_loss', save_best_only=False)
    callbacks_list = [check]
    model = KerasClassifier(build_fn=build_model, nb_epoch=nb_epoch, batch_size=batch_size)
    model.fit(np.array(X), np.array(Y_train), callbacks=callbacks_list)
except OSError:
    model = KerasClassifier(
        build_fn=build_model,
        nb_epoch=nb_epoch,
        batch_size=batch_size)
    model.fit(np.array(X), np.array(Y_train))

data = json.load(open(root_dir + "/test_data.json"))
X = data["X"]
Y = data["Y"]
predicts = model.predict(np.array(X))

model.model.save(MODEL)
del model

# decode the prediction
category_names = ["학사", "행사", "모집", "장학", "학생"]
for position, predict in enumerate(predicts):
    try:
        Y_predicted = category_names.__getitem__(predict)
        DBManager.updateAt(get_original_line(root_dir + "/gongji.txt", position), Y_predicted)
    except ProgrammingError:
        # the line is not in table
        pass

K.clear_session()
print("end")
