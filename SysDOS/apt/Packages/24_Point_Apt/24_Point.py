# -*- coding: utf-8 -*-
"""
Create on Mon Mar 11 19:32:25 2024
@author: fangg
"""
import random
import re

sum = []
flag = True

while flag:
    am = random.randint(1, 20)
    bm = random.randint(1, 20)
    cm = random.randint(1, 20)
    dm = random.randint(1, 20)
    op = ["+", "-", "*", "/"]
    for i in range(len(op)):
        for j in range(len(op)):
            for k in range(len(op)):
                sum.append(eval(str(am) + op[i] + str(bm) + op[j] + str(cm) + op[k] + str(dm)))

    if 24 in sum:
        flag = False

print("我们来玩24点游戏吧！")

flag1 = True
while flag1:
    inputNum = [am, bm, cm, dm]
    print(f"你抽到的数字分别是：{am},{bm},{cm},{dm}!")
    i = input("请输入你的答案，×用*表示，÷用/表示：")
    s = re.split(r'\W+', i)
    nlength = 4
    for ss in s:
        if int(ss) in inputNum and len(s) == nlength:
            flag1 = False
            inputNum.remove(int(ss))
        elif int(ss) not in inputNum and len(s) != nlength:
            flag1 = True
            print('你输入的数字及数字个数不对，请重新输入！')
            break
        elif int(ss) not in inputNum and len(s) == nlength:
            flag1 = True
            print('你输入的数字不对，请重新输入！')
            break
        elif int(ss) in inputNum and len(s) != nlength:
            flag1 = True
            print('你输入的数字个数不对，请重新输入！')
            break
    if flag1 == False:
        if eval(i) == 24:
            print('你成功了~~~')
            break
        else:
            print('答案不等于 24！')
            flag1 = True