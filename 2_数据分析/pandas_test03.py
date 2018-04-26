# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# # 离散化和面元划分
# ages=[20,22,25,27,21,23,37,37,61,45,41,32]
# bins=[18,25,35,60,100]
# cats=pd.cut(ages,bins)
# print cats
# print cats.codes

# # 根据最小值与最大值划分4组区间
# data=np.random.rand(20)
# print data.min(),data.max()
# print pd.cut(data,4,precision=2)  # 离散化函数

# 检测和过滤异常值
df1 = pd.DataFrame(np.random.randn(100,4))   # 创建随机 100*4 的数组
print df1.describe()

# col = df1[3]
# print col[np.abs(col)>3]    # 绝对值大小超过3的值

# # 返回一个由1和-1组成的数组
# print np.sign(df1)*3

# print df1[(np.abs(df1)>3).any(1)]   #绝对值大小超过3的任意行
# df1[np.abs(df1)>3] = np.sign(df1)*3