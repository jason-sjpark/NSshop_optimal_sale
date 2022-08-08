import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [10, 6]
base = pd.read_csv(r'./실적데이터(휴일, 공휴일 추가)/실적데이터(휴일,공휴일 추가).csv', encoding='cp949')
base.drop(columns=['방송일시','노출(분)','마더코드','상품코드','상품명','상품군','판매단가','휴일','공휴일'], inplace=True)
sns.boxplot(x="요일",y=" 취급액 ",data=base)
plt.show()