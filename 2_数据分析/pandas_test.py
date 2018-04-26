# coding=utf-8
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

print '---------------------------------------Series---------------------------------------'
# Series 类似于一维数组对象，由一组数据以及一组与之相关的数组标签（即索引）组成，左边索引，右边值
obj1 = Series([4, 7, -5, 3])                            # 默认
print 'obj1:\n', obj1
print 'obj1.index:', obj1.index
print 'obj1.values:', obj1.values

obj2 = Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])  # 指定索引
print 'obj2:\n', obj2
print 'obj2(元素>3)的值:\n', obj2[obj2 > 3]  # 获取元素大于3的值

dic1 = {'name': 'wangjing', 'sex': 'man', 'age': '31', 'address': 'BJ'}
dic2 = {"name": "zhangnan", "sex": "woman", "age": "15", "address": "BJ"}
obj3 = Series(dic1)  # 可以直接将字典转换Series
obj4 = Series(dic2)
print 'obj3:\n', obj3
print 'obj4:\n', obj4

print '数据检测：\n', pd.isnull(obj3)  # isnull,notnull
print '\n', pd.notnull(obj3)
print 'obj3自带的isnull：\n', obj3.isnull()

print '---------------------------------------DataFrame---------------------------------------'
# DataFrame
# 是一个表格型的数据结构，它含有一组有序的列，每组可以是不同的值类型（数值，字符串，布尔值），有行索引，也有列索引，相当于Series组成的字典
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame1 = DataFrame(data)
frame1['newcol1'] = 5  # 新加列
frame1['newcol2'] = np.arange(5)  # 新加列
val = Series([-1.2, -1.5, -1.7])
frame1['newcol3'] = val  # 匹配不到的赋值会默认填写 NaN
print 'frame1:\n', frame1['state']
print 'frame1:\n', frame1  # 自动加索引
print 'pop:\n', 'pop' in frame1.columns  # DataFrame 列判断
del frame1['newcol1']  # 删除指定列
print 'frame1:\n', frame1
print 'frame1的矩阵:\n', frame1.values
print 'frame1的转置:\n', frame1.T

frame2 = Series(range(3), index=['a', 'b', 'c'])
index1 = frame2.index
print 'index:\n', index1  # index 对象不可修改
print 'index:\n', index1[1:]
# Series 的index重排
print 'frame2.reindex:\n', frame2.reindex(['a', 'b', 'c', 'd', 'e'])
# 设置默认值
print 'frame2.reindex默认值0:\n', frame2.reindex(['a', 'b', 'c', 'd', 'e'], fill_value=0)

index2 = pd.Index(np.arange(3))
frame3 = Series([1.5, -2.7, 0], index=index2)
print 'frame3:\n', frame3
print 'frame3.index is index2:\n', frame3.index is index2

frame4 = Series(['11fv', 'vvvb', 'zzz'], index=[0, 2, 4])
print 'frame4:\n', frame4
# reindex向前填充
print 'frame4.reindex向前填充：\n', frame4.reindex(range(5), method='ffill')

frame5_1 = DataFrame(np.arange(9).reshape(
    3, 3), index=['a', 'c', 'd'], columns=['Ohio', 'Texas', 'California'])
print 'frame5_1:\n', frame5_1
frame5_2 = frame5_1.reindex(['a', 'b', 'c', 'd', 'e', 'f'], fill_value=0)
print 'frame5_2:\n', frame5_2
states = ['T', 'W',  'California']
# frame5_3 = frame5_1.reindex(index=['a', 'b', 'c'], columns=states, method='ffill')
# print 'frame5_3:\n', frame5_3
