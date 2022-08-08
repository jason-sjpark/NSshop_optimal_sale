import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [10, 6]
base = pd.read_csv(r'./실적데이터(휴일, 공휴일 추가)/실적데이터(휴일,공휴일 추가).csv', encoding='cp949')
base.drop(columns=['num','요일','노출(분)','마더코드','상품코드','상품명','방송일시','판매단가','휴일','공휴일'], inplace=True)

time_grouped = base.groupby(base['상품군'])
time_grouped.sum().reset_index().to_csv('type_grouped.csv')