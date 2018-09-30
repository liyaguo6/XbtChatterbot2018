from core import record
from core import wav2pcm
import os, time
from core.MyRobert import bot, MyThread
from core.TuLinRobert import TuLin
from core.speakout import tts_main
from setting import settings
from core.py_sdkXF import xf_text

if __name__ == '__main__':
    while True:
        try:
            start = time.time()
            record.rec(settings.LISTEN_FILE)  # 实现录音，将文件存储在1k.wav
            file = wav2pcm.wav_to_pcm(settings.LISTEN_FILE)  # 将wav格式的语音转化为pcm格式
            words = xf_text(file, 16000)  # 读取录音文件，通过讯飞API实现语音转写
            stop1 = time.time()
            print("讯飞API:%s" % (stop1 - start))
            chatterbot_respone = bot.get_response(words)
            t = MyThread(TuLin, args=(words,))
            t.setDaemon(True)
            t.start()
            if chatterbot_respone != "Tulin reply":
                response = chatterbot_respone
            else:
                t.join()
                response = t.get_result()
            stop2 = time.time()
            print("思考时间:%s" % (stop2 - stop1))
            tts_main(str(response))
            stop3 = time.time()
            print("语音合成时间%s" % (stop3 - stop2))
            print(stop3 - start)
            os.system("%s  %s" % (settings.PLAY_MEDIA, settings.SPEACK_FILE))
            if str(words) in ["再见，", "good bye，", "退出，"]:
                break
        except:
            tts_main("我好像没有明白你说了什么")
            os.system("%s  %s" % (settings.PLAY_MEDIA, settings.SPEACK_FILE))
            continue
