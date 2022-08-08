# import the necessary dependencies
import tensorflow as tf
from matplotlib import pyplot, font_manager
from tensorflow import keras
import numpy as np
import pandas as pd
from keras import losses
from sklearn.preprocessing import MinMaxScaler

# import the data
from tensorflow.python.keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint

# 3. 한글폰트를 설정(한글을 사용한다면 반드시해야 함)
from matplotlib import rc

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
# 맥OS인 경우 위 두 줄을 입력하지 말고 아래 코드를 입력하세요
# rc('font', family='AppleGothic')
pyplot.rcParams['axes.unicode_minus'] = False

train = pd.read_csv('./Preprocessing/15_1. 최종train.csv', encoding='cp949')
test = pd.read_csv('./Preprocessing/15_2. 최종test.csv', encoding='cp949')
print(train.head())
print(train.columns)
print(train.shape)
print(test.head())
print(test.columns)
print(test.shape)

# _data = every attribute except for the sale price
# _target = the sale price(예측하고 싶은 요소)
train_data = train.drop(columns=['Unnamed: 0','방송일시','상품명','요일','휴일','공휴일','시각','취급액']).copy()
train_target = train[['취급액']]
print(train_data.columns)
print(train_data.shape)
print(train_target.shape)

test_data = test.drop(columns=['Unnamed: 0','방송일시','상품명','요일','휴일','공휴일','시각','취급액']).copy()
test_target = test[['취급액']]
print(test_data.columns)
print(test_data.shape)
print(test_target.shape)

# 정규화
mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std

# build the model
model = tf.keras.models.Sequential()

# fit the model
# keras.layers.Dense(출력값의 크기, 활성화 함수, 입력값의 모양(배열의 차원))
# Q : 활성화 함수 relu 적합한 것인가?
# Q : 다른 파라미터는?
model.add(tf.keras.layers.Dense(50, activation='sigmoid', input_shape=(train_data.shape[1],)))
# 모델은 (*, 8) 형태의 배열을 인풋으로 받고 - input_shape(2차원 이상일떄)
# (*, 16) 형태의 배열을 출력합니다 - dense              input_dim : 인풋shape에 차원이 하나만 있는경우ex)배열인경우
# 첫 번째 레이어 이후에는,
# 인풋의 크기를 특정하지 않아도 됩니다:
model.add(tf.keras.layers.Dense(25, activation='relu'))

model.add(tf.keras.layers.Dense(1)) # sales price 값 하나만 출력
model.compile(optimizer='adam', loss='mean_absolute_percentage_error', metrics=['mean_absolute_percentage_error'])
# from tensorflow.keras.optimizers import SGD
# model.compile(optimizer=SGD(lr=0.2), loss=losses.mean_absolute_percentage_error, metrics=['accuracy'])

# 무조건 Epoch을 많이 돌린 후, 더 이상 성능의 발전이 없을 경우 중단 > GPU power 절약, overfitting 방지
# patience 는 성능이 증가하지 않는 epoch 을 몇 번이나 허용할 것인가를 정의한다. partience 는 다소 주관적인 기준이다. 사용한 데이터와 모델의 설계에 따라 최적의 값이 바뀔 수 있다.
early_stopping = EarlyStopping(monitor='val_mean_absolute_percentage_error',patience=10, mode='min', verbose=1)
mc = ModelCheckpoint('best_model.h5', monitor='val_mean_absolute_percentage_error', mode='min', save_best_only=True)

#학습시키기 (traindata(X,Y)에 대해서만..)
history = model.fit(train_data, train_target, epochs=300, validation_split=0.2, callbacks=[early_stopping, mc], batch_size= 3000)

pyplot.subplot(211)
pyplot.plot(history.history['mean_absolute_percentage_error'])
pyplot.plot(history.history['val_mean_absolute_percentage_error'])
pyplot.title('model mean_absolute_percentage_error')
pyplot.ylabel('mean_absolute_percentage_error')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'test'], loc='upper left')

pyplot.subplot(212)
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'test'], loc='upper left')
pyplot.show()

test_target_hat = model.predict(test_data)
print(test_target)
print(test_target_hat)
pyplot.subplot(211)
pyplot.plot(test_target_hat, label='추정치')
pyplot.legend()

pyplot.subplot(212)
pyplot.plot(test_target, label='실제값')

pyplot.legend()
pyplot.show()


# # 값 넣고 예측해보기 (true value of this house = $208500)
# test = pd.read_csv('test데이터',encoding='cp949')
# X_test = df.drop(columns=['취급액','Unnamed: 0','시각인덱스']).copy()
# Y_test = df[['취급액']]
# test_data = np.array([2003,   854, 1710, 2, 1, 3, 8, 2008])
# print(model.predict(X_test.reshape(,16), batch_size=1)) #16열로 바꾸기

# save this model
model.save('saved_model.h5')
#
# recover the model
# old_model = keras.models.load_model('saved_model.h5')
#