# -*- coding: utf-8 -*-
import numpy as np

print '---------------------------------------data1------------------------------------------'
data1 = np.arange(6)
print 'data1:\n',data1
print 'ndim:',data1.ndim
print 'shape:',data1.shape

print '---------------------------------------data2------------------------------------------'
data2 = np.arange(10).reshape(2,5)
print 'data2:\n',data2
print 'ndim:',data2.ndim
print 'shape:',data2.shape