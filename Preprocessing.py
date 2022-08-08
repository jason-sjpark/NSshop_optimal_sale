# -*-coding cp949-*-
import csv
import pandas as pd
import numpy as np

#   1   ######################################      #일관성과 규칙이 보이지 않는 데이터 제거

df= pd.read_csv('./Preprocessing/원본/실적데이터.csv', encoding='cp949')
del df['마더코드']
del df['상품코드']

df.to_csv('./Preprocessing/1. 코드지우기.csv',encoding='cp949')
print("1 Finished")

#   2   ######################################      #노출시간이 빈칸이라면 같은 시간에 방송한 다른 제품의 노출시간을 보고 복사해 옴
f = open('./Preprocessing/1. 코드지우기.csv', 'r', encoding='cp949')
rdr1 = csv.reader(f)
w = open('./Preprocessing/2. 노출시간 빈칸채우기.csv', 'w', encoding='cp949', newline='')
wr = csv.writer(w)

for line1 in rdr1:
    if line1[2]=='':
        datetime = line1[1]
        foundtime = 20000
        s = open('./Preprocessing/1. 코드지우기.csv', 'r', encoding='cp949')
        rdr2 = csv.reader(s)
        for line2 in rdr2:
            if line2[1] == datetime:
                foundedtime = line2[2]
                break
        s.close()
        line1[2] = foundedtime
    wr.writerow(line1)

f.close()
w.close()


print("2 Finished")

#   3   ######################################                  ## '무형'의 데이터는 예측을 하지 않으므로 삭제한다.
f = open('./Preprocessing/2. 노출시간 빈칸채우기.csv', 'r', encoding='cp949')
rdr = csv.reader(f)
w = open('./Preprocessing/3. 실적데이터 무형 지우기.csv', 'w', encoding='cp949', newline='')
wr = csv.writer(w)

for line in rdr:
    if line[4] != '무형':
        wr.writerow(line)

f.close()
w.close()
print("3 Finished")

#   4   ######################################          ##판매 수량 데이터가 가치있을것이라 판단하여 취급액을 판매 단가로 나누어 판매수량을 도출
df= pd.read_csv('./Preprocessing/3. 실적데이터 무형 지우기.csv',thousands=',', encoding='cp949')
df['취급액'] = df['취급액'].fillna(value = 0)
df['취급액'] = pd.to_numeric(df['취급액'])
df['판매단가'] = pd.to_numeric(df['판매단가'])
df["판매수량"]=np.ceil(df["취급액"]/df["판매단가"]).astype(int)

df.to_csv('./Preprocessing/4. 실적데이터 판매수량 추가.csv',encoding='cp949')
print("4 Finished")

#   5   ######################################          ##날짜의 요일 주말, 평일 여부, 공휴일 여부 판별하여 데이터 생성
# 컬럼 정리
raw_sold = pd.read_csv("./Preprocessing/4. 실적데이터 판매수량 추가.csv", encoding='cp949')
sold_data=raw_sold
    # .drop(0).copy()
# 인덱스 정렬
col = []
for num, temp in enumerate(sold_data['노출(분)']):
    if pd.isna(temp) :
        col.append(col[num-1])
    else :
        col.append(temp)
sold_data['노출(분)']=col

# 무형의 것들은 제거
#sold_data=sold_data.dropna() 이미 무형제거 해서 주석처리함

# 요일 붙여주기
sold_data['방송일시']=pd.to_datetime(sold_data['방송일시'])
sold_data['요일']=sold_data['방송일시'].dt.day_name()

# 요일 바탕으로 휴일 붙여주기
sold_data['휴일'] = ["Yes" if (s=='Saturday')|(s=='Sunday') else "No" for s in sold_data['요일']]
# print(sold_data['방송일시'])

# 공휴일 붙여주기
holidays = ['2019-01-01','2019-02-04','2019-02-05','2019-02-06','2019-03-01','2019-05-06','2019-05-12','2019-06-06','2019-08-15','2019-09-12','2019-09-13','2019-09-14','2019-10-03','2019-10-09','2019-12-25','2020-01-01']
# print(holidays)

#비교 위해 방송일시 date만 남겨서 문자열로 바꾸기
date=sold_data['방송일시'].dt.strftime("%Y-%m-%d")

#holidays랑 비교해서 공휴일 인지 아닌지 리스트로 내보내기
is_hol=[]
for i in date:
    if i in holidays:
        is_hol.append('Yes')
    else:
        is_hol.append('No')

#is_hol을 sold_data에 붙여주기
sold_data['공휴일']=is_hol
print(sold_data)

#csv로 내보내기
sold_data.to_csv('./Preprocessing/5. 실적데이터(휴일,공휴일 추가).csv',encoding='cp949')
print("5 Finished")

#   6   ######################################







print("6 Finished")


#   7 8 9   ######################################          ##각종 데이터 범주형 변환
train = pd.read_csv('./Preprocessing/5. 실적데이터(휴일,공휴일 추가).csv', encoding='cp949')

####################################################################
# 상품군 숫자형으로 변환 (가나다 순)
train['상품군'] = train['상품군'].map( {'가구': 0, '가전': 1, '건강기능': 2, '농수축': 3, '생활용품': 4, '속옷': 5, '의류': 6, '이미용': 7, '잡화': 8, '주방': 9, '침구': 10} ).astype(int)

####################################################################
# 노출시간 범주형으로 변환
for i in range(train.shape[0]):
    if (train.iloc[i]['노출(분)'] <= 10):
        train.loc[i, '노출(분)'] = 10
    elif (train.iloc[i]['노출(분)'] <= 20):
        train.loc[i, '노출(분)'] = 20
    elif (train.iloc[i]['노출(분)'] <= 30):
        train.loc[i, '노출(분)'] = 30
    elif (train.iloc[i]['노출(분)'] <= 40):
        train.loc[i, '노출(분)'] = 40
    else :
        train.loc[i, '노출(분)'] = 50

# 판매단가 범주형으로 변환

train['판매단가'] = pd.to_numeric(train['판매단가']) # int형으로 변환

for i in range(train.shape[0]):
    if (train.iloc[i]['판매단가'] <= 30900):
        train.loc[i, 'New판매단가'] = 1
    elif (train.iloc[i]['판매단가'] <= 35900):
        train.loc[i, 'New판매단가'] = 2
    elif (train.iloc[i]['판매단가'] <= 42000):
        train.loc[i, 'New판매단가'] = 3
    elif (train.iloc[i]['판매단가'] <= 48000):
        train.loc[i, 'New판매단가'] = 4
    elif (train.iloc[i]['판매단가'] <= 55600):
        train.loc[i, 'New판매단가'] = 5
    elif (train.iloc[i]['판매단가'] <= 60800):
        train.loc[i, 'New판매단가'] = 6
    elif (train.iloc[i]['판매단가'] <= 64800):
        train.loc[i, 'New판매단가'] = 7
    elif (train.iloc[i]['판매단가'] <= 73900):
        train.loc[i, 'New판매단가'] = 8
    elif (train.iloc[i]['판매단가'] <= 95200):
        train.loc[i, 'New판매단가'] = 9
    elif (train.iloc[i]['판매단가'] <= 147000):
        train.loc[i, 'New판매단가'] = 10
    elif (train.iloc[i]['판매단가'] <= 219000):
        train.loc[i, 'New판매단가'] = 11
    elif (train.iloc[i]['판매단가'] > 219000):
        train.loc[i, 'New판매단가'] = 12


# 판매 단가의 천의자리, 백의자리가 8 또는 9인 제품은 따로 라벨링하여 표시(취급액이 많기 때문에)
train['판매단가'] = train['판매단가'].astype(str) # str형으로 변환
for i in range(train.shape[0]):
    if (train.iloc[i]['판매단가'][-3] == '9'):
        train.loc[i, 'New판매단가'] = 0
    elif (train.iloc[i]['판매단가'][-3] == '8'):
        train.loc[i, 'New판매단가'] = 0
    elif (train.iloc[i]['판매단가'][-4] == '9'):
        train.loc[i, 'New판매단가'] = 0
    elif (train.iloc[i]['판매단가'][-4] == '8'):
        train.loc[i, 'New판매단가'] = 0


train.to_csv('./Preprocessing/7 8 9. 숫자형_범주형_변환.csv',encoding='cp949')
print("7 8 9 Finished")




#   10 11   ######################################

# 컬럼 정리
raw_sold = pd.read_csv("./Preprocessing/7 8 9. 숫자형_범주형_변환.csv", encoding='cp949')
sold_data = raw_sold
# print(sold_data['상품명'])
# .drop(['Unnamed: 0'],axis=1).copy()


#상품명에 남성, 남자라는 단어가 있고 상품군이 의류라면 0으로 라벨링
sold_data.loc[(sold_data['상품명'].str.contains('남성|남자')) & (sold_data['상품군']==6), "남여"] = 0
sold_data.loc[(sold_data['상품명'].str.contains('여성|여자')) & (sold_data['상품군']==6), "남여"] = 1
sold_data['남여'] = sold_data['남여'].fillna(value = 2)

# 무이자/일시불 붙여주기 (무이자=0, 일시불=1)
sold_data.loc[sold_data['상품명'].str.contains('무이자'), "무이자/일시불"] = 0
sold_data.loc[sold_data['상품명'].str.contains('일시불'), "무이자/일시불"] = 1
sold_data['무이자/일시불'] = sold_data['무이자/일시불'].fillna(value = 2)
# csv로 내보내기
sold_data.to_csv('./Preprocessing/10 11. 실적데이터(남여, 무이자일시불 구분).csv', encoding='cp949')
print("10 11 Finished")

#   12   ######################################

# 실적데이터 train으로 불러오기
train = pd.read_csv('./Preprocessing/10 11. 실적데이터(남여, 무이자일시불 구분).csv', encoding='cp949')
# 기상데이터 weather으로 불러오기
weather = pd.read_csv('./12. 기상_물가_데이터추가/일별_기상데이터.csv', encoding='cp949')

train = train.drop(['Unnamed: 0'],axis=1).copy()
train['남여'] = train['남여'].fillna(value = 2)

# train의 방송일시 컬럼 자료형 날짜형으로 변환
train['방송일시'] = pd.to_datetime(train['방송일시'], format='%Y-%m-%d %H:%M:%S', errors='raise')
# weather의 날짜 컬럼 자료형 날짜형으로 변환
weather['날짜'] = pd.to_datetime(weather['날짜'], format='%Y-%m-%d %H:%M:%S', errors='raise')

# train에 평균기온, 강수량 컬럼 추가 (기본값 0.0, double형)
train['최저기온'] = 0.0
train['최고기온'] = 0.0
train['평균기온'] = 0.0
train['강수량'] = 0.0
train['미세먼지농도'] = 0.0

k = 0
# 방송일시의 일에 맞는 기상데이터 넣어주기
for i in range(train.shape[0]):
    for j in range(k,weather.shape[0]):
        print(i, j)
        if (train.iloc[i]['방송일시'].date() == weather.iloc[j]['날짜'].date()):
            train.loc[i, '최저기온'] = weather.loc[j, '최저기온']
            train.loc[i, '최고기온'] = weather.loc[j, '최고기온']
            train.loc[i, '평균기온'] = weather.loc[j, '평균기온']
            train.loc[i, '강수량'] = weather.loc[j, '강수량']
            train.loc[i, '미세먼지농도'] = weather.loc[j, '미세먼지농도']
            k = j
            break

# 물가지수입력
# 소비자물가지수 CPI로 불러오기
CPI = pd.read_csv('./12. 기상_물가_데이터추가/월별_소비자물가지수.csv', encoding='cp949')

# train에 소비자물가지수 컬럼 추가 (기본값 0.0, double형)
train['소비자물가지수'] = 0.0

# 방송일시의 월에 맞는 소비자물가지수 넣어주기
for i in range(train.shape[0]):
    for j in range(1, 13):
        if (train.iloc[i]['방송일시'].month == j):
            train.loc[i, '소비자물가지수'] = CPI['소비자물가지수'][j - 1]
            break

train.to_csv('./Preprocessing/12. 기상_물가_데이터추가.csv', encoding='cp949')
print("12 Finished")

#   13   ###################################### #방송일시에서 시간만 추출후 치환
import pandas as pd

ts_day_idx = pd.date_range('00:00:00','23:50:00',freq='10T')
series_ts = pd.DataFrame(ts_day_idx, index=range(len(ts_day_idx)))
series_ts.columns = ['시각']
series_ts['시각인덱스'] = series_ts.index
series_ts['시각'] = series_ts['시각'].dt.strftime("%H:%M:%S")

train = pd.read_csv('./Preprocessing/12. 기상_물가_데이터추가.csv', header=0,encoding='cp949')
train = train.drop(['Unnamed: 0'],axis=1).copy()

train['방송일시'] = pd.to_datetime(train['방송일시'])
train['시각'] = train['방송일시'].dt.strftime("%H:%M:%S")
total=pd.merge(train,series_ts,on='시각',how='left')
total.to_csv('./Preprocessing/13. 시간추출, 치환.csv', encoding='cp949')

print("13 Finished")

#   14   ######################################
#상품명 텍스트 쪼개서 자주쓰이는 단어들로 사전을 만들고 각 제품을 라벨링


raw_sold = pd.read_csv("./Preprocessing/13. 시간추출, 치환.csv", encoding='cp949')
sold_data = raw_sold
# print(sold_data['상품명'])
# .drop(['Unnamed: 0'],axis=1).copy()

# 무이자/일시불 붙여주기 (무이자=0, 일시불=1)
sold_data.loc[sold_data['상품명'].str.contains('TV'), "New상품명"] = 1
sold_data.loc[sold_data['상품명'].str.contains('쿠쿠전기밥솥'), "New상품명"] = 2
sold_data.loc[sold_data['상품명'].str.contains('침대'), "New상품명"] = 3
sold_data.loc[sold_data['상품명'].str.contains('압력밥솥'), "New상품명"] = 4
sold_data.loc[sold_data['상품명'].str.contains('유로탑'), "New상품명"] = 5
sold_data.loc[sold_data['상품명'].str.contains('드로즈'), "New상품명"] = 6
sold_data.loc[sold_data['상품명'].str.contains('에어컨'), "New상품명"] = 7
sold_data.loc[sold_data['상품명'].str.contains('소파'), "New상품명"] = 8
sold_data.loc[sold_data['상품명'].str.contains('냉장고'), "New상품명"] = 9
sold_data.loc[sold_data['상품명'].str.contains('세탁기'), "New상품명"] = 10
sold_data.loc[sold_data['상품명'].str.contains('침구세트'), "New상품명"] = 11
sold_data.loc[sold_data['상품명'].str.contains('가스레인지'), "New상품명"] = 12
sold_data.loc[sold_data['상품명'].str.contains('노트북'), "New상품명"] = 13
sold_data.loc[sold_data['상품명'].str.contains('분쇄믹서기'), "New상품명"] = 14
sold_data.loc[sold_data['상품명'].str.contains('온수매트'), "New상품명"] = 15
sold_data.loc[sold_data['상품명'].str.contains('브라팬티'), "New상품명"] = 16
sold_data.loc[sold_data['상품명'].str.contains('안동간고등어'), "New상품명"] = 17
sold_data.loc[sold_data['상품명'].str.contains('LED침대'), "New상품명"] = 18
sold_data.loc[sold_data['상품명'].str.contains('트렁크'), "New상품명"] = 19
sold_data.loc[sold_data['상품명'].str.contains('캐리어'), "New상품명"] = 20
sold_data.loc[sold_data['상품명'].str.contains('에어프라이어'), "New상품명"] = 21
sold_data.loc[sold_data['상품명'].str.contains('벽걸이에어컨'), "New상품명"] = 22
sold_data.loc[sold_data['상품명'].str.contains('비데'), "New상품명"] = 23
sold_data.loc[sold_data['상품명'].str.contains('냄비세트'), "New상품명"] = 24
sold_data.loc[sold_data['상품명'].str.contains('데님팬츠'), "New상품명"] = 25
sold_data.loc[sold_data['상품명'].str.contains('소곱창전골'), "New상품명"] = 26
sold_data.loc[sold_data['상품명'].str.contains('선글라스'), "New상품명"] = 27
sold_data.loc[sold_data['상품명'].str.contains('크로스백'), "New상품명"] = 28
sold_data.loc[sold_data['상품명'].str.contains('숄더백'), "New상품명"] = 29
sold_data.loc[sold_data['상품명'].str.contains('토트백'), "New상품명"] = 30
sold_data.loc[sold_data['상품명'].str.contains('손질갑오징어'), "New상품명"] = 31
sold_data.loc[sold_data['상품명'].str.contains('생유산균골드'), "New상품명"] = 32
sold_data.loc[sold_data['상품명'].str.contains('다이아몬드'), "New상품명"] = 33
sold_data.loc[sold_data['상품명'].str.contains('롱코트'), "New상품명"] = 34
sold_data.loc[sold_data['상품명'].str.contains('밍크'), "New상품명"] = 35
sold_data.loc[sold_data['상품명'].str.contains('니트'), "New상품명"] = 36
sold_data.loc[sold_data['상품명'].str.contains('팔찌'), "New상품명"] = 37
sold_data.loc[sold_data['상품명'].str.contains('모시떡'), "New상품명"] = 38
sold_data.loc[sold_data['상품명'].str.contains('쌀'), "New상품명"] = 39
sold_data.loc[sold_data['상품명'].str.contains('가스와이드그릴'), "New상품명"] = 40
sold_data.loc[sold_data['상품명'].str.contains('프라이팬'), "New상품명"] = 41
sold_data.loc[sold_data['상품명'].str.contains('팬츠'), "New상품명"] = 42
sold_data.loc[sold_data['상품명'].str.contains('목걸이'), "New상품명"] = 43
sold_data.loc[sold_data['상품명'].str.contains('패딩'), "New상품명"] = 44
sold_data.loc[sold_data['상품명'].str.contains('무선청소기'), "New상품명"] = 45
sold_data.loc[sold_data['상품명'].str.contains('티셔츠'), "New상품명"] = 46
sold_data.loc[sold_data['상품명'].str.contains('녹용도가니탕'), "New상품명"] = 47
sold_data.loc[sold_data['상품명'].str.contains('손질문어'), "New상품명"] = 48
sold_data.loc[sold_data['상품명'].str.contains('순금'), "New상품명"] = 49
sold_data.loc[sold_data['상품명'].str.contains('포기김치'), "New상품명"] = 50
sold_data.loc[sold_data['상품명'].str.contains('롱드로즈'), "New상품명"] = 51
sold_data.loc[sold_data['상품명'].str.contains('후라이팬'), "New상품명"] = 52
sold_data.loc[sold_data['상품명'].str.contains('런닝'), "New상품명"] = 53
sold_data.loc[sold_data['상품명'].str.contains('언더셔츠'), "New상품명"] = 54
sold_data.loc[sold_data['상품명'].str.contains('통오징어'), "New상품명"] = 55
sold_data.loc[sold_data['상품명'].str.contains('사첼백'), "New상품명"] = 56
sold_data.loc[sold_data['상품명'].str.contains('두유48팩'), "New상품명"] = 57
sold_data.loc[sold_data['상품명'].str.contains('락앤락'), "New상품명"] = 58
sold_data.loc[sold_data['상품명'].str.contains('전기밥솥'), "New상품명"] = 59
sold_data.loc[sold_data['상품명'].str.contains('전자레인지'), "New상품명"] = 60
sold_data.loc[sold_data['상품명'].str.contains('쥐포'), "New상품명"] = 61
sold_data.loc[sold_data['상품명'].str.contains('레깅스'), "New상품명"] = 62
sold_data.loc[sold_data['상품명'].str.contains('석류'), "New상품명"] = 63
sold_data.loc[sold_data['상품명'].str.contains('원피스'), "New상품명"] = 64
sold_data.loc[sold_data['상품명'].str.contains('브라'), "New상품명"] = 65
sold_data.loc[sold_data['상품명'].str.contains('브라탑'), "New상품명"] = 66
sold_data.loc[sold_data['상품명'].str.contains('코트'), "New상품명"] = 67
sold_data.loc[sold_data['상품명'].str.contains('샌들'), "New상품명"] = 68
sold_data.loc[sold_data['상품명'].str.contains('온열매트'), "New상품명"] = 69
sold_data.loc[sold_data['상품명'].str.contains('치마레깅스'), "New상품명"] = 70
sold_data.loc[sold_data['상품명'].str.contains('갓김치3kg+총각김치3kg'), "New상품명"] = 71
sold_data.loc[sold_data['상품명'].str.contains('항균도마'), "New상품명"] = 72
sold_data.loc[sold_data['상품명'].str.contains('핸드백'), "New상품명"] = 73
sold_data.loc[sold_data['상품명'].str.contains('리빙박스'), "New상품명"] = 74
sold_data.loc[sold_data['상품명'].str.contains('반지'), "New상품명"] = 75
sold_data.loc[sold_data['상품명'].str.contains('햅쌀'), "New상품명"] = 76
sold_data.loc[sold_data['상품명'].str.contains('루테인'), "New상품명"] = 77
sold_data.loc[sold_data['상품명'].str.contains('넥센타이어'), "New상품명"] = 78
sold_data.loc[sold_data['상품명'].str.contains('자켓'), "New상품명"] = 79
sold_data.loc[sold_data['상품명'].str.contains('예초기'), "New상품명"] = 80
sold_data.loc[sold_data['상품명'].str.contains('백팩'), "New상품명"] = 81
sold_data.loc[sold_data['상품명'].str.contains('갈비탕'), "New상품명"] = 82
sold_data.loc[sold_data['상품명'].str.contains('손질갈치'), "New상품명"] = 83
sold_data.loc[sold_data['상품명'].str.contains('베스트'), "New상품명"] = 84
sold_data.loc[sold_data['상품명'].str.contains('브라세트'), "New상품명"] = 85
sold_data.loc[sold_data['상품명'].str.contains('밴딩팬츠'), "New상품명"] = 86
sold_data.loc[sold_data['상품명'].str.contains('남성기초세트'), "New상품명"] = 87
sold_data.loc[sold_data['상품명'].str.contains('동태포'), "New상품명"] = 88
sold_data.loc[sold_data['상품명'].str.contains('행주티슈'), "New상품명"] = 89
sold_data.loc[sold_data['상품명'].str.contains('손질새우'), "New상품명"] = 90
sold_data.loc[sold_data['상품명'].str.contains('여행가방'), "New상품명"] = 91
sold_data.loc[sold_data['상품명'].str.contains('스니커즈'), "New상품명"] = 92
sold_data.loc[sold_data['상품명'].str.contains('손질왕꼬막'), "New상품명"] = 93
sold_data.loc[sold_data['상품명'].str.contains('백김치'), "New상품명"] = 94
sold_data.loc[sold_data['상품명'].str.contains('러닝화'), "New상품명"] = 95
sold_data.loc[sold_data['상품명'].str.contains('청소기'), "New상품명"] = 96
sold_data.loc[sold_data['상품명'].str.contains('물걸레'), "New상품명"] = 97
sold_data.loc[sold_data['상품명'].str.contains('갑오징어'), "New상품명"] = 98
sold_data.loc[sold_data['상품명'].str.contains('후드코트'), "New상품명"] = 99
sold_data.loc[sold_data['상품명'].str.contains('워킹화'), "New상품명"] = 100
sold_data.loc[sold_data['상품명'].str.contains('브라캡'), "New상품명"] = 101
sold_data.loc[sold_data['상품명'].str.contains('손질꽃게'), "New상품명"] = 102
sold_data.loc[sold_data['상품명'].str.contains('서랍장'), "New상품명"] = 103
sold_data.loc[sold_data['상품명'].str.contains('꽃게'), "New상품명"] = 104
sold_data.loc[sold_data['상품명'].str.contains('코르셋'), "New상품명"] = 105
sold_data.loc[sold_data['상품명'].str.contains('젤네일스트립'), "New상품명"] = 106
sold_data.loc[sold_data['상품명'].str.contains('다이아'), "New상품명"] = 107
sold_data.loc[sold_data['상품명'].str.contains('LA갈비'), "New상품명"] = 108
sold_data.loc[sold_data['상품명'].str.contains('옷걸이'), "New상품명"] = 109
sold_data.loc[sold_data['상품명'].str.contains('릴렉스팬츠'), "New상품명"] = 110
sold_data.loc[sold_data['상품명'].str.contains('카페트'), "New상품명"] = 111
sold_data.loc[sold_data['상품명'].str.contains('매트릭스'), "New상품명"] = 112
sold_data.loc[sold_data['상품명'].str.contains('트렌치코트'), "New상품명"] = 113
sold_data.loc[sold_data['상품명'].str.contains('반팔'), "New상품명"] = 114
sold_data.loc[sold_data['상품명'].str.contains('공기청정기'), "New상품명"] = 115
sold_data.loc[sold_data['상품명'].str.contains('로봇청소기'), "New상품명"] = 116
sold_data.loc[sold_data['상품명'].str.contains('롱패딩'), "New상품명"] = 117
sold_data.loc[sold_data['상품명'].str.contains('바다장어'), "New상품명"] = 118
sold_data.loc[sold_data['상품명'].str.contains('패션밍크'), "New상품명"] = 119

sold_data['New상품명'] = sold_data['New상품명'].fillna(value = 0)

sold_data.loc[sold_data['공휴일'].str.contains('Yes'), "공휴일 여부"] = 1
sold_data.loc[sold_data['공휴일'].str.contains('No'), "공휴일 여부"] = 0
sold_data.loc[sold_data['휴일'].str.contains('Yes'), "휴일 여부"] = 1
sold_data.loc[sold_data['휴일'].str.contains('No'), "휴일 여부"] = 0
sold_data.loc[sold_data['요일'].str.contains('Monday'), "New요일"] = 0
sold_data.loc[sold_data['요일'].str.contains('Tuesday'), "New요일"] = 1
sold_data.loc[sold_data['요일'].str.contains('Wednesday'), "New요일"] = 2
sold_data.loc[sold_data['요일'].str.contains('Thursday'), "New요일"] = 3
sold_data.loc[sold_data['요일'].str.contains('Friday'), "New요일"] = 4
sold_data.loc[sold_data['요일'].str.contains('Saturday'), "New요일"] = 5
sold_data.loc[sold_data['요일'].str.contains('Sunday'), "New요일"] = 6

# csv로 내보내기
sold_data.to_csv('./Preprocessing/14. 상품명 치환.csv', encoding='cp949')

print("14 Finished")

# 15   ######################################

# from sklearn.model_selection import train_test_split
#
# df = pd.read_csv("./Preprocessing/14. 상품명 치환.csv", sep=",", encoding='cp949')
# train, test = train_test_split(df, test_size=0.4)
#
# train.to_csv('./Preprocessing/15_1. 최종train.csv', encoding='cp949')
# test.to_csv('./Preprocessing/15_2. 최종test.csv', encoding='cp949')
# print("15 Finished")
