import re
import json
from concurrent.futures import  ThreadPoolExecutor
# list3 =[]
# with open("同义词.txt","r",encoding='gbk') as f:
#    with open('new_synomys.json','w',encoding='utf-8') as h:
#     for line in f:
#         if re.search('=',line):
#             list1,list2 = line.split("=")
#             l=list(list2.strip().split(" "))
#             list3.append([l[0],l[1]])
#     h.write(json.dumps(list3))

def load_data():
    with open("new_synomys.json", 'r') as load_f:
        for line in json.load(load_f):
            sign= yield line
            if sign == 'stop':
                break

def task():
    load_data1 = load_data()
    for k in load_data1:
        try:
            print(k)
            if k == ['匹夫', '个人']:
                load_data1.send('stop')
        except:
            break

if __name__ == '__main__':
    # pool = ThreadPoolExecutor(20)
    for i in range(3):
        task()
    # pool.shutdown()  # join结束

# try:
#     print(next(load_data))
#     print(next(load_data))
#     load_data.send('stop')
# except StopIteration:
#     print(12)

# next(load_data)

d= {1:[23,45]}
print(type(d.values()))