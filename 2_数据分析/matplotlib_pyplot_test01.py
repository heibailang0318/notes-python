# coding=utf-8
import matplotlib.pyplot as pl 
import numpy as np
pl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
pl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
#pl.style.use('ggplot')          # plot style一个子模块使用 风格
#print(pl.style.available)       # 查看所有风格实例 

################################### plot(*args, **kwargs)#####################################
#'''
#    plot(*args, **kwargs)	Plot lines and/or markers to the Axes.
#
#plot(y)           # plot y using x as index array 0..N-1
#若A为向量，则绘图时以序号为横坐标，序号对应的值为纵坐标；
#plot(y, 'r+')     # ditto, but with red plusses
#plot(x, y)        # plot x and y using default line style and color
#plot(x, y, 'bo')  # plot x and y using blue circle markers
#'''
##############################################################################################
'''
pl.figure()
pl.plot([1,2,3,4])    # 以y为坐标，x默认0..n-1的点的图, default line

pl.figure()
pl.plot([1,2,3,4], 'r+')    # 以y为坐标，x默认0..n-1的点的图，指定颜色, default line 点
 
pl.figure()
pl.plot([1,2,3,4],[80,7,6,5])   # default line

pl.figure()
pl.plot([1,2,3,4],[80,7,6,5],'r+')  #default 点 
''' 



'''
pl.figure()         # 创建一个画板
#设置坐标轴名称
pl.title('中文')
pl.xlabel('x轴')     # 指定x坐标名
pl.ylabel('y轴')     # 指定y坐标名  

pl.grid(color='b', linestyle='-.', linewidth=0.5)   # 指定背景格颜色
#pl.axis([0,6,0,20])     # 指定 x 轴显示区域为 0-6，y 轴为 0-20

t = np.arange(0., 5., 0.2)
pl.plot(t, t, 'r--', 
         t, t**2, 'bs', 
         t, t**3, 'g^')
''' 

''' # test01
X = np.linspace(-np.pi, np.pi, 256,endpoint=True)   # 等分 -π 到 π 256份，endpoint表示包含256闭区间，（π-（-π））/256
#print (X)
C,S = np.cos(X),np.sin(X)
#pl.plot(X)      # 打印X，x轴由X的序列展示，y由X的向量值展示， 索引x轴有256个

#pl.figure()
#pl.plot(C)      # x：c的个数256，y：c的具体向量值
#pl.plot(S)

pl.figure()
pl.plot(X,C)    # x:X向量{-π，π}，y:C的具体向量值
pl.plot(X,S)
''' 
# test02
# 创建一个 8 * 6 点（point）的图，并设置分辨率为 80
pl.figure(figsize=(10,6), dpi=80)

# 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块 ,
pl.subplot(1,1,1)
'''# 第一个图
#pl.subplot(2,2,1)
#pl.plot(X,X**2)

# 绘制第2个图
#pl.subplot(2,2,2)
#pl.plot(X)

# 绘制第3个图
#pl.subplot(2,1,2)       # 第三个图占用了2*2的下面的所有
#pl.plot(X**2,X) 
'''
X = np.linspace(-np.pi, np.pi, 256,endpoint=True) 
C,S = np.cos(X), np.sin(X)

# 绘制余弦曲线，使用蓝色的、连续的、宽度为 1 （像素）的线条
pl.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
pl.plot(X, S, color="red",  linewidth=2.5, linestyle="-", label="sine")
pl.legend(loc='upper left')
pl
# 设置横轴的上下限
#pl.xlim(X.min(), X.max())
#pl.ylim(-1.01,1.01)

xmin ,xmax = X.min(), X.max()
ymin, ymax = C.min(), C.max()

dx = (xmax - xmin) * 0.2
dy = (ymax - ymin) * 0.2

pl.xlim(xmin - dx, xmax + dx)
pl.ylim(ymin - dy, ymax + dy)
 
# 设置横轴记号
#pl.xticks(np.linspace(-4,4,9,endpoint=True))     # 等差数列以-4开始，4结束，个数是9   an=a1+(n-1)*d
#pl.yticks(np.linspace(-1,1,5,endpoint=True))

#pl.xticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi])
#pl.yticks([-1,0,1])

# 精确标记轴记号       LaTeX
pl.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
pl.yticks([-1, 0, +1], [r'$-1$', r'$0$', r'$+1$'])

'''# 坐标轴
ax = pl.gca() 
print(type(pl.gca()))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
'''
 
# 以分辨率 72 来保存图片
#pl.savefig("exercice_2.png",dpi=72)



pl.show()



