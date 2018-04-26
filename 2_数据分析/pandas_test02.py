# coding=utf-8
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
#print '-------------------------df---------------------------------------'
#df = pd.read_csv('D:/pandas_test03.csv', header=0)
#print df.head(2)
#
#
#df.columns = ['a', 'b', 'c', 'd']   # 更改列名
#print df.head(5)
#
#print len(df)
#
#pd.options.display.float_format = '{:,.3f}'.format      # 一些基本的统计信息
#print df.describe()
#print df['b']
#print '-------'
#print df[(df.b<1000)& (df.c>100)]       #过滤


print '================================df2================================'
df2 = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
                   'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female'],
                    'city':['BJ','TJ','BJ','BJ','SH'],
                    'type':['A','A','A','B','A']
                    })
#print '\n行索引:\n',df2.index
#print '\n列索引:\n',df2.columns
#print '\n列数据类型:\n',df2.dtypes
print '\ndf2:\n',df2
print df2.groupby(['sex','city','type']).mean()     # mean 求平均
# print df2.groupby(['sex','city','type']).mean().unstack()   # 将最内层索引转置打平到列
# print df2.groupby(['sex'])[['total_bill']].mean()       #选取一个或一组列
print df2.groupby(['sex']).agg(['mean','sum','min','max'])
print df2.groupby(['sex']).mean()
print df2.groupby(['sex']).agg([('tip','mean'),('total_bill','sum')])

# print '========select======='
# print '\nloc，基于列label，可选取特定行（根据行index）:\n',df2.loc[1:3, ['total_bill', 'tip']]
# print '\nloc，基于列label，可选取特定行（根据行index）:\n',df2.loc[1:3, 'tip': 'total_bill']
# print '\nloc，基于列label，可选取特定行（根据行index）:\n',df2.loc[1:3, 'tip': 'total_bill']
# print '\niloc，基于行/列的position:\n',df2.iloc[1:3, [1, 2]]
# print '\niloc，基于行/列的position:\n',df2.iloc[1:3, 1: 3]
# print '\nat，根据指定行index及列label，速度比loc快，快速定位DataFrame的元素:\n',df2.at[3, 'tip']
# print '\niat，与at类似，不同的是根据position来定位的(具体下标从0开始):\n',df2.iat[3, 1]
# print '\nix，为loc与iloc的混合体，既支持label也支持position:'
# print df2.ix[1:3, [1, 2]]
# print df2.ix[1:3, ['total_bill', 'tip']]
# print df2[1: 3]
# print df2[['total_bill', 'tip']]

#print '========where======='
#print 'Pandas实现where filter，较为常用的办法为df[df[colunm] boolean expr]:'
#print df2[df2['sex'] == 'Female']       #获取性别是Female的行
#print df2[df2['total_bill'] > 20]       #获取金额大于20的行
#print df2.query('total_bill > 20')      #获取金额大于20的行
#
#print '在where子句中常常会搭配and, or, in, not关键词，Pandas中也有对应的实现：'
## and
#print df2[(df2['sex'] == 'Female') & (df2['total_bill'] > 20)]
## or
#print df2[(df2['sex'] == 'Female') | (df2['total_bill'] > 20)]
## in
#print df2[df2['total_bill'].isin([21.01, 23.68, 24.59])]
## not
#print df2[-(df2['sex'] == 'Male')]
#print df2[-df2['total_bill'].isin([21.01, 23.68, 24.59])]
#print '对where条件筛选后只有一行的dataframe取其中某一列的值，其两种实现方式如下：'
#total = df2.loc[df2['tip'] == 1.66, 'total_bill'].values[0]
#print total

#print '========distinct======='
#print df2.drop_duplicates(subset=['sex'], keep='first', inplace=True)   #   ######?

#print '========group======='
#print df2.groupby('sex').size()
#print df2.groupby('sex').count()
#print df2.groupby('sex')['tip'].count()
#print 
##对于多合计函数:select sex, max(tip), sum(total_bill) as total from tips_tb group by sex;
#print df2.groupby('sex').agg({'tip': np.max, 'total_bill': np.sum})         # 使用 numpy库的函数
#print
## count(distinct **)
#print df2.groupby('tip').agg({'sex': pd.Series.nunique})

#print '========as======='
##SQL中使用as修改列的别名，Pandas也支持这种修改： 
#df2.rename(columns={'total_bill': 'total', 'tip': 'pit', 'sex': 'xes'}, inplace=True)
#print df2

#print '========join======='
##第一种方法是按DataFrame的index进行join的，而第二种方法才是按on指定的列做join。Pandas满足left、right、inner、full outer四种join方式。
## 1.
#df.join(df2, how='left'...)
#
## 2.
#pd.merge(df1, df2, how='left', left_on='app', right_on='app')

#print '========order======='
#print df2.sort_values(['total_bill', 'tip'], ascending=[True, False])   #按字段排序

# print '========top======='
# print df2.nlargest(3, columns=['total_bill'])
#select a.sex, a.tip
#from tips_tb a
#where (
#    select count(*)
#    from tips_tb b
#    where b.sex = a.sex and b.tip > a.tip
#) < 2
#order by a.sex, a.tip desc;
# 1.
#print df2.assign(rn=df2.sort_values(['total_bill'], ascending=False)
#          .groupby('sex')
#          .cumcount()+1)\
#    .query('rn < 3')\
#    .sort_values(['sex', 'rn'])
#    
## 2.
#print df2.assign(rn=df2.groupby('sex')['total_bill']
#          .rank(method='first', ascending=False)) \
#    .query('rn < 3') \
#    .sort_values(['sex', 'rn']) 

# print '========replace======='
# # overall replace
# df2.replace(to_replace='Female', value='Sansa', inplace=True)
# # dict replace
# df2.replace({'sex': {'Female': 'Sansa', 'Male': 'Leone'}}, inplace=True)
# # replace on where condition
# df2.loc[df2.sex == 'Male', 'sex'] = 'Leone'
#
# print df2

























