
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

base = pd.read_csv(r'split_datetime.csv', encoding='cp949')

base.drop(columns=['day','time','노출분','상품명','상품군','취급액'], inplace=True)

base.columns=['num','year','month','price','quantity']
print(base)

for i in range(base.shape[0]):
    if (base.iloc[i]['price'] <= 122000):
        base.loc[i, 'price'] = 0
    elif (base.iloc[i]['price'] <= 280000):
        base.loc[i, 'price'] = 1
    elif (base.iloc[i]['price'] <= 649000):
        base.loc[i, 'price'] = 2
    elif (base.iloc[i]['price'] <= 1239000):
        base.loc[i, 'price'] = 3
    elif (base.iloc[i]['price'] <= 1899000):
        base.loc[i, 'price'] = 4
    elif (base.iloc[i]['price'] <= 2690000):
        base.loc[i, 'price'] = 5
    elif (base.iloc[i]['price'] > 2690000):
        base.loc[i, 'price'] = 6



idx_nm1=base[(base['year']==2020) | (base['month']>1)].index #없앨거 지정
df1=base.drop(idx_nm1) #지정한거 drop

idx_nm2=base[(base['month']==1) | (base['month']>2)].index
df2=base.drop(idx_nm2)

idx_nm3=base[(base['month']<3) | (base['month']>3)].index
df3=base.drop(idx_nm3)

idx_nm4=base[(base['month']<4) | (base['month']>4)].index
df4=base.drop(idx_nm4)

idx_nm5=base[(base['month']<5) | (base['month']>5)].index
df5=base.drop(idx_nm5)

idx_nm6=base[(base['month']<6) | (base['month']>6)].index
df6=base.drop(idx_nm6)

idx_nm7=base[(base['month']<7) | (base['month']>7)].index
df7=base.drop(idx_nm7)

idx_nm8=base[(base['month']<8) | (base['month']>8)].index
df8=base.drop(idx_nm8)

idx_nm9=base[(base['month']<9) | (base['month']>9)].index
df9=base.drop(idx_nm9)

idx_nm10=base[(base['month']<10) | (base['month']>10)].index
df10=base.drop(idx_nm10)

idx_nm11=base[(base['month']<11) | (base['month']==12)].index
df11=base.drop(idx_nm11)

idx_nm12=base[base['month']<12].index
df12=base.drop(idx_nm12)

idx_nm_2020_1=base[base['year']==2019].index
df_2020_1=base.drop(idx_nm_2020_1)

# sns.boxplot(x="price",y="quantity",data=df1)
# plt.title("January boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df2)
# plt.title("February boxplot")
# plt.show()
#
# # sns.boxplot(x="price",y="quantity",data=df3)
# # plt.title("Marh boxplot")
# # plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df4)
# plt.title("April boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df5)
# plt.title("March boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df6)
# plt.title("June boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df7)
# plt.title("July boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df8)
# plt.title("August boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df9)
# plt.title("September boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df10)
# plt.title("October boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df11)
# plt.title("November boxplot")
# plt.show()
#
# sns.boxplot(x="price",y="quantity",data=df12)
# plt.title("December boxplot")
# plt.show()

sns.boxplot(x="price",y="quantity",data=df_2020_1)
plt.title("2020 January boxplot")
plt.show()


