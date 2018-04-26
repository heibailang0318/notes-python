# coding=utf-8
# 不引用则不显示图形
import numpy as np

# Series([4, 5, 7]).plot()
# plt.show()
#print '---------------------------------------numpy------------------------------------------'
#data1 = np.random.randint(-11, high=15, size=(2, 3))  # 半开半闭区间 high不指定时候默认第一个为最大值
#print 'data1:\n',data1
#print '数组形状: \n', data1.shape
#print '数组的维数（即数组轴的个数）：\n', data1.ndim
#print '数组元素的总个数：\n', data1.size
#print '数组元素的类型：\n', data1.dtype

data2 = np.zeros((5, 2))
print 'data2: \n', data2

arr1 = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)  # 以list或tuple变量为参数产生一维数组
print 'arr1:\n', arr1

data3 = np.empty((8, 4))
for i in range(8):
    data3[i] = i
print 'data3: \n', data3

data4 = np.arange(4).reshape(2, 2)  # 生成一个0到16之内的2行8列数组
print 'data4:\n', data4
print 'data4的转置:\n', data4.T  # 特殊的T属性
print 'data4的转置*data4计算：\n', np.dot(data4.T, data4)  # 矩阵转置与矩阵相乘
print 'data4的和axis=0:\n',data4.sum(axis=0)            #axis代表轴，2维数组，2个轴，axis=0则先算最外面，等于几就先抵消第几个中括号
print 'data4的和axis=1:\n',data4.sum(axis=1)            #axis代表轴，2维数组，2个轴，axis=1则先算最
print 'data4的算数平均数:\n',data4.mean()
print 'data4的0轴的差:\n', np.apply_along_axis(np.diff,0,data4)                           # 指定轴上，按指定的函数进行操作
print 'data4的1轴的差:\n', np.apply_along_axis(np.diff,1,data4)                           # 指定轴上，按指定的函数进行操作

data5 = np.arange(16).reshape((2, 2, 4))
print 'data5:\n', data5
print 'data5的转置:\n', data5.transpose((2, 1, 0))  # ？未懂
print 'data5的矩阵判断:\n', np.where(data5 > 5, -1, data5)  # 矩阵判断

data6 = np.random.randn(5, 4)
print 'data6:\n',data6

data7 = np.arange(6).reshape(3,2)
data8 = np.arange(8).reshape(2,4)
print 'data7:\n',data7
print 'data8:\n',data8
print 'data7与data8的矩阵相乘:\n', data7.dot(data8)               # 相当于np.dot(data7,data8)


data9=np.arange(10)                         # 1 维数组
print 'data9:\n',type(data9)
data10=np.arange(12).reshape(3,4)           # 2 维数组
print 'data10:\n',data10
data11 = range(10)
print 'data11:\n',type(data11)              # range返回的是list，arange返回的是ndarray类型

print '对角矩阵:\n',np.eye(3,k=2,dtype=int)      # 对角矩阵，k用于控制对角线
print '1 矩阵：\n',np.ones((3,3),dtype=float)      # 创建单位矩阵
print '合并数组1：\n',np.vstack((np.eye(3,k=2,dtype=int),np.ones((3,3),dtype=float)))
print '合并数组2：\n',np.hstack((np.eye(3,k=2,dtype=int),np.ones((3,3),dtype=float)))

