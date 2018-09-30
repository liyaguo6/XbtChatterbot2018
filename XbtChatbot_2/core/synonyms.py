# -*- coding: utf-8 -*-
'''
@auther: Li Yaguo
@summary: 同义词替换，生成同义句
'''
from core.MyRobert import bot
from synom.synonyms_replace import SynonymsReplacer
from setting.settings import *
from concurrent.futures import ThreadPoolExecutor
import random


class Synons:
    def __init__(self, words):
        self.result = set()
        self.words = words

    def replace(self):
        if len(self.words) >= 1:
            s = SynonymsReplacer(SYNO_FILES)
            result = s.get_syno_sents_list(self.words)
            return result
        else:
            print("没有声音")

    def chatbot_responae(self, response_obj):
        response = response_obj.result()
        if response != 'Tulin reply':
            self.result.add(response)

    def search(self):
        result = self.replace()
        if len(result) > 1:
            pool = ThreadPoolExecutor(len(result) - 1)
            for word in result[1:]:
                # 开启线程池，同时去数据库查询
                pool.submit(bot.get_response, word).add_done_callback(self.chatbot_responae)
            pool.shutdown()
        else:
            print("没有声音1")


def sy(words):
    s = Synons(words)
    s.search()
    result = list(s.result)
    if result == []:
        return None
    else:
        rd_result = random.choice(list(s.result))
        return rd_result
