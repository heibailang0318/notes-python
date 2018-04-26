# coding=utf-8

import random


cnt=10	# 模拟次数
f_p=1/4		# 第一次概率
cas = [1,2]	# 行使权情况，1：假票放回，2：假票不放回

for i in range(cnt):
    rand=random.sample(cas, 1)  # 随机取一种情况
    if rand == [1]:  # 第一种情况下
        print(rand)

    else:
        print(rand)
