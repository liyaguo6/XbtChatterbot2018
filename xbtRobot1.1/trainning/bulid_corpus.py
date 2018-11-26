from chatterbot.trainers import ChatterBotCorpusTrainer
import os,sys,re
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# corpus_file = os.path.join(BASE_DIR,"database/jsonfile/test.json")
corpus_file = os.path.join(BASE_DIR,'trainning\\test2.json')
# from core.MyRobert import bot

from chatterbot import ChatBot


bot = ChatBot("Terminal",
              storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
              logic_adapters=[
                  {'import_path': "chatterbot.logic.BestMatch"},
              ],
              filters=[
                  'chatterbot.filters.RepetitiveResponseFilter'
              ],
              # trainer='chatterbot.trainers.ListTrainer',
              input_adapter="chatterbot.input.VariableInputTypeAdapter",
              output_adapter="chatterbot.output.OutputAdapter",
              database_uri="mongodb://localhost:27017/",
              database="xbt",
              read_only=True,
              trainer='chatterbot.trainers.ListTrainer'
              )
# bot.set_trainer(ChatterBotCorpusTrainer)



# 使用中文语料库训练它
# if __name__ == '__main__':
#     bot.train([
#         "这是医院领导来视察。",
#         "欢迎领导莅临指导",
#         "这是指南针科创园的马总",
#             "领导辛苦了",
#     ])


def load_json_file(save_mode="1"):
    list1 = []
    if save_mode == '1':
        with open('original_data_re.txt','r',encoding='utf-8') as h:
            lines = h.readlines()
            for line in lines:
                if line != "\n" :
                    line=re.sub(r"\ufeffquestion:  |answer:  |答:|question:  ","",line.strip())
                    list1.append(line)
#     else:
#         data_dict = dict(conversations=list1)
#         with open(file, 'w') as f:
#             import json
#             f.write(json.dumps(data_dict))
    return list1
def load_csv_file(file):
    ret_list=load_json_file()
    answer = []
    question = []
    for index,item  in enumerate(ret_list):
        if index%2==0:
            answer.append(item)
        else:
            question.append(item)
    import pandas as pd
    df = pd.DataFrame({'answer':answer,'question':question})
    print(df)
    df.to_csv(file,encoding='gbk')

if __name__ == '__main__':
#     ret=load_json_file("test1.json")
    # bot.train("./test.json")
    # bot.train("./my_export.json")
    # bot.train(ret)
    # response = bot.get_response("安徽指南针科创园简介？")
    # print(response)
    load_csv_file('test215.csv')