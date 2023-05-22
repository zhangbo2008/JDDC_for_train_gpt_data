#=========对京东数据进行刷成gpt多轮数据格式.里面数据会有一些错误, 手动改了一点点,因为实在太多了12W行......
import pandas as pd

with open('data/chat.txt') as f:
    t=f.readlines()


import re
save=[]
for i in t[1:]:
    i=re.sub('\t+','\t',i)
    session_id,user_id,waiter_send,is_transfer,is_repeat,content=[k.replace('\n','').replace('\t','') for k in i.split('\t',5) if k] # split 设置一下最大分割数量为5即可!!!!!!!!!陈宫分成六分.
    save.append([session_id,waiter_send,content])
#========先对于每一个用户的句子进行合并
save2=[]
waiter_send='0'
content=''
for dex,i in enumerate(save):
    if i[1]!=waiter_send:
        save2.append([session_id,waiter_send,content])
        session_id=i[0]
        waiter_send=i[1]
        content=i[2]
    else:
        session_id=i[0]
        waiter_send=i[1]
        content+=i[2]
    if dex==len(save)-1:
        save2.append([session_id,waiter_send,content]) #12W句子.

#=========session用来进行history的处理:
save3=[]
tmpsession=save2[0][0]
tmp={}
old_session=-1
for i in range(0,len(save2),2 ):
    tmp={}#=======每次重新创立字典不然里面走地址.
    if save2[i][0]!=old_session:#新建的session
        session_first_id=i #记录session开始的id
        old_session=save2[i][0]
    tmp['prompt']=save2[i][2]
    tmp['response']=save2[i+1][2]
    ttt=[]
    a=[]
    b=[]
    for j in range(session_first_id,i,2):
        a.append(save2[j][2])
    for j in range(session_first_id+1,i,2):
        b.append(save2[j][2])
    tmp['history']=list(zip(a,b))
    save3.append(tmp)
print(1)
    
import json
with open('extract_train.json', 'w') as f:
   f.write(json.dumps(save3, indent=4,ensure_ascii=False))

