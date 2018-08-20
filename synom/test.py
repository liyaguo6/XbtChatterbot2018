import re
with open("同义词.txt","r",encoding='gbk') as f:
   with open('new_synomys.txt','w',encoding='utf-8') as h:
    for line in f:
        if re.search('=',line):
            list1,list2 = line.split("=")
            l=list(list2.strip().split(" "))
            h.write("{}\t{}\n".format(l[0],l[1]))
