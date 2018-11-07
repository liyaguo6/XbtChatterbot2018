# -*- coding: utf-8 -*-
'''
@auther: Li Yaguo
@summary: 预测输入问题是医疗问题还是非医疗问题，1代表医疗问题，0代表非医疗问题
'''
import jieba  #处理中文
import collections
import pickle
from setting import settings
from sklearn.naive_bayes import MultinomialNB  #多项式分类
import logging
jieba.setLogLevel(logging.INFO)

class Predict:
    def __init__(self,**kwargs):
        self.text = kwargs.get('text')
        self.predict_features = []
        with open(settings.TRAIN_FEATURES_WORDS, 'rb') as f:
            self.features_words = pickle.load(f)
        with open(settings.TRAIN_FEATURES, 'rb') as f:
            self.train_features = pickle.load(f)
            self.train_class = ['1','0']

    def text_processing(self, text):
        text_words_list = list(jieba.cut(text, cut_all=True))
        text_words_dict = dict(collections.Counter(text_words_list))
        self.predict_features.extend([text_words_dict[word] if word in text_words_dict else 0 for word in self.features_words])

    def start(self):
        self.text_processing(self.text)
        classifier = MultinomialNB().fit(self.train_features, self.train_class)
        predict_ret = classifier.predict_proba([self.predict_features])
        ret = classifier.predict([self.predict_features])[0]
        predict_acc = predict_ret.max()
        return ret,predict_acc

if __name__ == '__main__':
    text = '感冒'
    p = Predict(text=text)
    ret=p.start()
    print(int(ret[0]))
    print(float(ret[1]))