from core import wav2pcm
import os, time
from core.MyRobert import bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.sound2wordXF import wordfromS     # 该文档使用讯飞api进行语音识别
import core.moni_record
from core import vad_speakout
import re
import random
import multiprocessing
from classfication.predict import Predict

class XbtBot:
    def __init__(self):
        self.words = None
        self.response = None
        self.results =None
        self.classes =None
        self.accuracy = None


    def voice2word(self):
        core.moni_record.monitor(settings.LISTEN_FILE)
        start1 = time.time()
        self.words = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
        stop1 = time.time()
        print("讯飞API:%s" % (stop1 - start1))

    def think(self):
        start2 = time.time()
        self.text_classfi()
        if self.classes and self.accuracy>=0.66:
            chatterbot_respone = bot.get_response(self.words)
            response = chatterbot_respone
            print(response)
            if response !='False':
                print("Mybot-{}-{}-{}".format(self.classes, self.accuracy,response))
                self.response =response
            else:
                print("human-{}-{}-{}".format(self.classes, self.accuracy,response))
                self.response = '您说的问题我还没有明白，请寻求人工服务小姐姐帮忙！'
        else:
            self.response = TuLin(self.words)
            print("tulin-{}-{}-{}".format(self.classes, self.accuracy,self.response))

        stop2 = time.time()
        print("思考时间:%s" % (stop2 - start2))


    def text_classfi(self):
        p = Predict(text=self.words)
        ret_class = p.start()
        self.classes = int(ret_class[0])
        self.accuracy = float(ret_class[1])



    def word2vice(self):
        start3 = time.time()

        tts_main(str(self.response),settings.SPEACK_FILE)

        stop3 = time.time()
        print("语音合成时间%s" % (stop3 - start3))
        self.tts_qps(str(self.response))
        # t1 = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()

    def tts_qps(self,respond_words):
        result_list = vad_speakout.text_vad(respond_words)

        make_wave = multiprocessing.Process(target=vad_speakout.make_data,
                                            args=(vad_speakout.queue, result_list,))  # 生成数据进程
        read_wave = multiprocessing.Process(target=vad_speakout.handle_data,
                                            args=(vad_speakout.queue, vad_speakout.lock))
        read_wave.daemon = True  # 设为守护线程

        make_wave.start()
        read_wave.start()

        make_wave.join()
        print('Ended!')

    def run(self):
        while True:
            try:
                self.voice2word()
                self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见|张总|李总|王总|赵总|刘总|领导|主任)', self.words)
                if len(self.results) == 0:
                    if self.words is not None:
                        self.think()
                        self.word2vice()
                    else:
                        tts_main("不好意思，您可以再说一遍吗？",settings.SPEACK_FILE)
                        wav2pcm.audio_play(settings.SPEACK_FILE)

                elif [x for x in self.results if x in ["张总", "王总", "李总", "赵总", "刘总",'领导','主任']]:
                    words_list = ["欢迎领导莅临指导！", "欢迎领导来视察工作！", "领导辛苦了！", "请领导多多提出宝贵的意见！"]
                    words_speak = random.choice(words_list)
                    tts_main(words_speak,settings.SPEACK_FILE)
                    wav2pcm.audio_play(settings.SPEACK_FILE)

                else:
                    tts_main("好的，再见，有什么事可以来找我哦！",settings.SPEACK_FILE)
                    wav2pcm.audio_play(settings.SPEACK_FILE)
                    break
            except:
                tts_main("抱歉，我好像没有明白你说了什么",settings.SPEACK_FILE)
                wav2pcm.audio_play(settings.SPEACK_FILE)
                continue


if __name__ == '__main__':
    start = XbtBot()
    start.run()