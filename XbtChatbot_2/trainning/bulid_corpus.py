# -*- coding: utf-8 -*-
'''
@auther: Li Yaguo
@summary: 用于训练chatterbot文件
'''

from chatterbot.trainers import ChatterBotCorpusTrainer
import os,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# corpus_file = os.path.join(BASE_DIR,"database/jsonfile/test.json")
corpus_file = os.path.join(BASE_DIR,'trainning\\test.json')
from core.MyRobert import bot

bot.set_trainer(ChatterBotCorpusTrainer)

# 使用中文语料库训练它
# if __name__ == '__main__':

    # bot.train([
    #     "你认为什么时间戒烟是最好的？",
    #     "戒烟越早越好什么时候戒烟都为时不晚。",
    #      "成人的腋下体温为多少摄氏度？",
    #      "36℃—37℃。"
    # ])


def load_json_file(file):
    list1 = []
    list1.append(["你叫什么名字？","我是新巴特的Ohboy!"])
    data_dict = dict(conversations=list1)
    with open(file, 'w') as f:
        import json
        f.write(json.dumps(data_dict))


if __name__ == '__main__':
      # load_json_file("test.json")
      # bot.train("./test.json")
      # bot.train(corpus_file)
     response = bot.get_response("吸烟的危害是什么")
     print(response)