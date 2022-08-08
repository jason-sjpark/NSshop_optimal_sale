import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
train = pd.read_csv('./Preprocessing/15_1. 최종train.csv', encoding='cp949')
test = pd.read_csv('./Preprocessing/15_2. 최종test.csv', encoding='cp949')

X_train = train.drop(columns=['Unnamed: 0','방송일시','상품명','요일','휴일','공휴일','시각','취급액']).copy()
Y_train = train['취급액']
X_test  = test.drop(columns=['Unnamed: 0','방송일시','상품명','요일','휴일','공휴일','시각','취급액']).copy()
print(X_train.shape, Y_train.shape, X_test.shape)

logreg = RandomForestClassifier()
logreg.fit(X_train, Y_train)
Y_pred = logreg.predict(X_test)

test['취급액2'] = Y_pred
test.to_csv('submission.csv', index = False)