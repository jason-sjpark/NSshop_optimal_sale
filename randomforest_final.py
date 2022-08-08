import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager
from matplotlib import rc
import pickle

# 한글사용위한 코드
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# 전처리 완료한 실적데이터를 train으로 받아옴
train = pd.read_csv('14. 상품명 치환.csv', encoding='cp949')
# 실적데이터와 같은 방법으로 전처리 완료한 예측데이터 test로 받아옴
test = pd.read_csv('.\Preprocessing\예측데이터 최종.csv', encoding='cp949')

# 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처
mpl.rcParams['axes.unicode_minus'] = False

# warnings 무시
import warnings
warnings.filterwarnings('ignore')

# train데이터의 방송일시(날짜)에서 month, day, hour, minute, 요일 컬럼 만들어줌
train['방송일시']=pd.to_datetime(train['방송일시'])
train["month"] = train["방송일시"].dt.month
train["day"] = train["방송일시"].dt.day
train["hour"] = train["방송일시"].dt.hour
train["minute"] = train["방송일시"].dt.minute
train["dayofweek"] = train["방송일시"].dt.dayofweek

# 직관적으로 1억 이천 이상의 취급액을 가진 것들이 이상치라고 판단, 제거해줌
idx_nm_1 = train[(train['취급액'] >= 120000000)].index
train = train.drop(idx_nm_1)

# test데이터의 방송일시(날짜)에서 month, day, hour, minute, 요일 컬럼 만들어줌
test['방송일시']=pd.to_datetime(test['방송일시'])
test["month"] = test["방송일시"].dt.month
test["day"] = test["방송일시"].dt.day
test["hour"] = test["방송일시"].dt.hour
test["minute"] = test["방송일시"].dt.minute
test["dayofweek"] = test["방송일시"].dt.dayofweek

# 범주형으로 만들어줄 컬럼 지정 (이 컬럼들은 train데이터 안에 있는 컬럼들)
categorical_feature_names1 = [
                              "노출(분)",
                              "상품군",
                             "남여",
                             "New판매단가",
                             "무이자/일시불",
                             "시각인덱스",
                             "New상품명",
                              "공휴일 여부",
                             "휴일 여부",
                             'dayofweek',
                             "month",
                             "day",
                             "hour",#필수
                             "minute"#필수
                             ]
# test데이터에서 범주형으로 만들어줄 컬럼 지정 (이 컬럼들은 test데이터에 있는 컬럼들)
categorical_feature_names2 = [
                              "노출(분)",
                              "상품군", #필수
                             "남여",
                             "New판매단가",
                             "무이자/일시불",
                             "시각인덱스", #필수
                             "New상품명",
                              # "공휴일 여부",
                             # "휴일 여부",
                             'dayofweek',
                             "month",
                             "day",
                             "hour",#필수
                             "minute"#필수
                             ]

# 위의 컬럼들 범주형으로 변환
for var in categorical_feature_names1:
    train[var] = train[var].astype("category")
for var in categorical_feature_names2:
    test[var] = test[var].astype("category")

# 컬럼들 중 시행착오를 거쳐 최상의 성능을 보이는 조합의 컬럼들만 사용
feature_names = [
                 "노출(분)",
                  "상품군",
                   "판매단가",
                  "남여",
                 "New판매단가",
                   "무이자/일시불",
                 # "최저기온",
                 # "최고기온",
                 # "평균기온",
                 # "강수량",
                 #  "미세먼지농도",
                 # "소비자물가지수",
                  "시각인덱스",
                   "New상품명",
                #  "공휴일 여부",
                #  "휴일 여부",
                # "dayofweek",
                 "month",
                # "day",
                # "hour",
                #  "minute"
                 ]

# train, test에서 필요한 컬럼들만 사용해서 취급액을 예측할 X값들 지정
X_train = train[feature_names]
X_test = test[feature_names]

# X값들을 활용하여 값을 예측해줄 '취급액'컬럼 분리
y_train = train["취급액"]

from sklearn.metrics import make_scorer

def rmsle(predicted_values, actual_values):
    # 넘파이로 배열 형태로 바꿔준다.
    predicted_values = np.array(predicted_values)
    actual_values = np.array(actual_values)

    # 예측값과 실제 값에 1을 더하고 로그를 씌워준다.
    log_predict = np.log(predicted_values + 1)
    log_actual = np.log(actual_values + 1)

    # 위에서 계산한 예측값에서 실제값을 빼주고 제곱을 해준다.
    difference = log_predict - log_actual
    # difference = (log_predict - log_actual) ** 2
    difference = np.square(difference)

    # 평균을 낸다.
    mean_difference = difference.mean()

    # 다시 루트를 씌운다.
    score = np.sqrt(mean_difference)

    return score

rmsle_scorer = make_scorer(rmsle)

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

from sklearn.ensemble import RandomForestRegressor

max_depth_list = []

#회귀랜덤포레스트 모델 기본값 사용
model = RandomForestRegressor(n_estimators=100,
                              n_jobs=-1,
                              random_state=0)

# 실적데이터에 대해서 모델을 학습시킴
model.fit(X_train, y_train)

# 학습시킨 모델로 예측데이터 취급액 예측해줌 (predictions)
predictions = model.predict(X_test)
predictions=pd.DataFrame(predictions)
print(predictions)
print(predictions.shape)

# 예측데이터에 새로운 컬럼으로 예측한 취급액 추가해줌
test["New취급액"] = predictions

# 예측한 취급액 시각화
ax = predictions.plot(kind='bar', title='예측 취급액', figsize=(12, 4), legend=True, fontsize=12)
ax.set_xlabel('취급액', fontsize=12)          # x축 정보 표시
ax.set_ylabel('비율', fontsize=12)     # y축 정보 표시
plt.show()

# 예측한 취급액 덧붙인 예측데이터 파일을 '결과1'이라는 이름으로 저장
test.to_csv('결과1.csv',encoding='cp949')


