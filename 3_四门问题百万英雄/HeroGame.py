# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 23:11:01 2018

@author: Administrator


理论推导：
情况1：
    拿到真票的概率是1/4，因为主持人拿到假票这个事件对我先拿真票的事件概率不影响

情况2：
    主持人知道真假的情况下：
    我第一次拿到真，则重选肯定拿到假，即(1/4)*0
    我第一次拿到假，概率是3/4, 主持人从假票池中取走一张，相当于我跟主持共消耗掉2张假票，剩下两张票中肯定有一张真票
    ，第二次拿真的概率是1/2，则最终我获得真票的概率是:(1/4)*0+(3/4)*(1/2) = 3/8

    主持人不知真假随意选：
    贝叶斯公式计算：
        我选择了A票，主持人选了B票，
        P(A)表示A票为真的概率
        P(A¯)表示A票为假的概率
        P(B¯|A)表示若A为真票，则B一定假票的概率
        P(B¯|A¯)表示若A为假票，那么B为假票的概率
        P(A|B¯)表示B为假票，A为真票的概率
 
        P(A)=1/4	
        P(A¯)=3/4		
        P(B¯|A)=1	
        P(B¯|A¯)=2/3
        
        所以：
        P(A|B¯)=(P(B¯|A)*P(A)) / (P(B¯|A)*P(A)+P(B¯|A¯)*P(A¯))
        =(1*1/4) / (1*(1/4) + (2/3)*(3/4))
        =(1/4) / (1/4+1/2)
        =(1/4) / (3/4)
        =1/3

"""


import random

def HeroGameCase1(): 
    tickets = ['假','假','假','真']    # 初始化票,0表示假票，1表示真票
    random.shuffle(tickets)    # 打乱4张票的真假顺序
#    print('票列表：',tickets)  
    # 我从4张票中选1张票
    choice = random.randint(0, len(tickets)-1) 

    return tickets[choice]


	# 主持人知道真假，故意选假，且 不是我选择的票，剩下的票中，主持任意选一张票
def HeroGameCase2_1(): 
    tickets = ['假','假','假','真']    # 初始化票,0表示假票，1表示真票
    random.shuffle(tickets)    # 打乱4张票的真假顺序
#    print('票列表：',tickets) 
    
    # 我从4张票中选1张票
    choice = random.randint(0, len(tickets)-1) 
#    print('我选的序号：', choice)           # 我选的序号
#    print('我选的序号的票：', tickets[choice])  # 我选的序号的票是真还是假
     
    tmp=[]  # 收集主持人的假票池的序号
    for i in range(len(tickets)):
        if tickets[i] != '真' and i != choice: 
            tmp.append(i)         
            
#    print('主持人选择序号范围：',tmp)
    random.shuffle(tmp) # 打乱主持人选票池的票序 
    # 主持人从假票池里剔除一张票
    zchoice= random.sample(tmp,1)[0]         # 重新选择1张票的序号
#    print('主持人选的序号：', zchoice)           # 主持人选的序号
#    print('主持人的序号的票：', tickets[zchoice])  # 主持人选的序号的票是真还是假
    
    tmp2 = []   # 我重新选择的池子
    for i in range(len(tickets)-1):   # 收集我重新选择的池子
        if i != zchoice and i != choice:
            tmp2.append(i) 
    
    # 如果我第1次选了真，则剩下的都是假，我重新选择肯定是假，否则再去判断
    if tickets[choice] == '真':
        return '假'
    else:
#        print('我重新选择的序号范围：',tmp2)
        random.shuffle(tmp2) # 打乱我重新选票池的票序
        rechoice= random.sample(tmp2,1)[0]  # 重新选择1张票的序号
#        print('我重新选择的序号：',rechoice)
#        print('我重新选择的序号的票：',tickets[rechoice])
        return tickets[rechoice]


	# 主持人不知道真假，且 不是我选择的票，剩下的票中，主持随机选一张票
def HeroGameCase2_2(): 
    tickets = ['假','假','假','真']    # 初始化票,0表示假票，1表示真票
    random.shuffle(tickets)    # 打乱4张票的真假顺序
#    print('票列表：',tickets) 
    
    # 我从4张票中选1张票
    choice = random.randint(0, len(tickets)-1) 
#    print('我选的序号：', choice)           # 我选的序号
#    print('我选的序号的票：', tickets[choice])  # 我选的序号的票是真还是假
    
    tmp=[]  # 收集主持人的假票池的序号
    for i in range(len(tickets)):
        if i != choice:     # 剔除我第1次选的票 
            tmp.append(i)
            
#    print('主持人选择序号范围：',tmp)
    random.shuffle(tmp) # 打乱主持人选票池的票序
    # 主持人从票池里剔除1张票
    zchoice= random.sample(tmp,1)[0]         # 重新选择1张票的序号
#    print('主持人选的序号：', zchoice)           # 主持人选的序号
#    print('主持人的序号的票：', tickets[zchoice])  # 主持人选的序号的票是真还是假
 
    
    tmp2 = []   # 我重新选择的池子
    for i in range(len(tickets)-1):   # 收集我重新选择的池子
        if i != zchoice and i != choice:
            tmp2.append(i)
    
    
    
    # 如果我第1次选了真，则我重新选择肯定是假
    if tickets[choice] == '真':
        return '假'
    elif tickets[zchoice] == '真':   # 如果我第1次选的是假，主持人选择的是真，则我重选肯定是假,这种情况样本不计算，因为游戏结束
        return '不计算'
    else:
#        print('我重新选择的序号范围：',tmp2)
        random.shuffle(tmp2) # 打乱我重新选票池的票序
        rechoice= random.sample(tmp2,1)[0]  # 重新选择1张票的序号
#        print('我重新选择的序号：',rechoice)
#        print('我重新选择的序号的票：',tickets[rechoice])
        return tickets[rechoice]

if __name__ == '__main__':
    n=10000 
    # 情况1
    t1=f1=0
    for i in range(n):
        x = HeroGameCase1()
        if x == '真':
            t1 = t1+1
        else:
            f1 = f1+1
    print('\n情况1：  真票数:%s, 假票数:%s, 真票概率：%f' %(t1,f1,t1/n))
    
    # 情况2
    t2=f2=0
    for i in range(n):
        x = HeroGameCase2_1()
        if x == '真':
            t2 = t2+1
        else:
            f2 = f2+1
    print('\n情况2_1：真票数:%s, 假票数:%s, 真票概率：%f' %(t2,f2, t2/n))
    
     # 情况2_2
    t3=f3=nl=0
    for i in range(n):
        x = HeroGameCase2_2()
        if x == '真':
            t3 = t3+1
        elif x == '假':
            f3 = f3+1
        else:
            nl = nl+1
    print('\n情况2_2：真票数:%s, 假票数:%s, 不计算数：%s, 真票概率：%f' %(t3,f3,nl, t3/(n-nl)))
     
     
#     HeroGameCase2_2()