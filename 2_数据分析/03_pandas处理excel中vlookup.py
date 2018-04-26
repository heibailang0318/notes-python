# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:34:53 2018
@author: lenovo
用pandas读取excel进行不同sheet间的vlookup，然后存储到新的excel
"""

import pandas as pd

# f1=pd.read_excel('file/数据.xlsx',sheetname='工作表1')
# f2=pd.read_excel('file/数据.xlsx',sheetname='工作表2')


f1=pd.read_excel('file/数据.xlsx',sheetname=0)    # 默认 0 开始
f2=pd.read_excel('file/数据.xlsx',sheetname=1)

# print(f1.head(2))   # 查看 前两行数据
# print(f1.columns)
# print(f1.ndim)

result=pd.merge(left=f1, right=f2, how='left', left_on='username', right_on='username', suffixes=('_f1','_f2')).fillna('')
# print(result)



writer = pd.ExcelWriter('file/数据2.xlsx')
result.to_excel(writer,'Sheet1',index ='False')
writer.save()




