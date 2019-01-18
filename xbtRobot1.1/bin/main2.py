from core import wav2pcm
import os, time
from core.MyRobert import bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.sound2wordXF import wordfromS     # 该文档使用讯飞api进行语音识别
import core.moni_record
import re
import random
from core.unknow_question_save import UnQuetion
from core.face_detcet import FaceRecon





class XbtBot:
    def __init__(self):
        self.words = None
        self.response = None
        self.results =None
        self.face_detect = FaceRecon('../database/haarcascades/haarcascade_frontalface_alt2.xml')
        t = MyThread(self.face_detect.imag_show)
        t.start()
        while 1:
            self.Flags = self.face_detect.is_face
            print(self.Flags)
            if self.Flags:
                self.run()
    #         else:
    #             self.Flags =False
    #             continue
    def voice2word(self):
        core.moni_record.monitor(settings.LISTEN_FILE)
        start1 = time.time()
        self.words = wordfromS(settings.LISTEN_FILE)  # 读取录音文件，通过讯飞API实现语音转写
        stop1 = time.time()
        print("讯飞API:%s" % (stop1 - start1))

    def think(self):
        start2 = time.time()
        chatterbot_respone = bot.get_response(self.words)
        response = chatterbot_respone
        print(response)
        t = MyThread(TuLin, args=(self.words,))
        t.setDaemon(True)
        t.start()
        if response !='False':
            self.response =response
            print("Mybot-{}".format(self.response))
        else:
            t.join()
            self.response = t.get_result()
            self.record()
            print("tulin-{}".format(self.response))

        stop2 = time.time()
        print("思考时间:%s" % (stop2 - start2))

    def record(self):
        s=UnQuetion.conndb()
        t1 = MyThread(s.dump, args=(self.words,))
        t1.start()


    def word2vice(self):
        start3 = time.time()
        tts_main(str(self.response))
        stop3 = time.time()
        wav2pcm.audio_play(settings.SPEACK_FILE)
        print("语音合成时间%s" % (stop3 - start3))
        # t1 = MyThread(wav2pcm.audio_play, args=(str(settings.SPEACK_FILE),))
        # wav2pcm.audio_play(settings.SPEACK_FILE)
        # t1.start()

    def run(self):
        try:
            self.voice2word()
            self.results = re.findall(r'(再见|goodbye|bye bye|拜拜|退出|再会|待会见|张总|李总|王总|赵总|刘总|马总)', self.words)
            if len(self.results) == 0:
                if self.words is not None:
                    self.think()
                    self.word2vice()
                    # else:
                    #     tts_main("好的，一会聊",settings.SPEACK_FILE)
                    #     wav2pcm.audio_play(settings.SPEACK_FILE)
                else:
                    tts_main("不好意思，您可以再说一遍吗？")
                    wav2pcm.audio_play(settings.SPEACK_FILE)

            elif [x for x in self.results if x in ["张总", "王总", "李总", "赵总", "刘总","马总"]]:
                words_list = ["欢迎领导莅临指导！", "欢迎领导来视察工作！", "领导辛苦了！", "请领导多多提出宝贵的意见！"]
                words_speak = random.choice(words_list)
                tts_main(words_speak)
                wav2pcm.audio_play(settings.SPEACK_FILE)

            else:
                tts_main("好的，再见，有什么事可以来找我哦！")
                wav2pcm.audio_play(settings.SPEACK_FILE)
        except:
            tts_main("抱歉，我好像没有明白你说了什么")
            wav2pcm.audio_play(settings.SPEACK_FILE)



if __name__ == '__main__':
    start = XbtBot()