import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [10, 6]
base = pd.read_csv(r'./실적데이터(휴일, 공휴일 추가)/실적데이터(휴일,공휴일 추가).csv', encoding='cp949')
base.drop(columns=['num','요일','노출(분)','마더코드','상품코드','상품명','상품군','판매단가','휴일','공휴일'], inplace=True)
base['방송일시'] = pd.to_datetime(base['방송일시'], format='%Y-%m-%d %H:%M:%S', errors='raise')

time_grouped = base.groupby([base['방송일시'].dt.time])
time_grouped.sum().reset_index().to_csv('time_grouped.csv')