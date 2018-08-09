# pyrec.py 文件内容
import pyaudio
import wave
from io import BytesIO

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
RECORD_SECONDS = 5


def rec(file_name):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音,请说话......")

    frames = []

    count = 0
    while count < RECORD_SECONDS * 10:  # 控制录音时间
        string_audio_data = stream.read(CHUNK)
        frames.append(string_audio_data)
        count += 1
    print("录音结束!")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))


if __name__ == '__main__':
    print(rec("test.wav"))
    # with wave.open(r"D:\MyProj\Company\XbtChatterbot2018\database\listen\1kXF.wav", "rb") as wf:
    #     params = wf.getparams()
    #     nchannels, sampwidth, framerate, nframes = params[:4]
    #     import numpy as np
    #
    #     str_data = wf.readframes(nframes)
    #     wave_data = np.fromstring(str_data, dtype=np.short)
    #
    #     wave_data.shape = -1, 2
    #     wave_data = wave_data.T
    #     print(len(wave_data[0]))
    #     time = np.arange(0, nframes / 2) * (1.0 / framerate)
    #     print(time)
    #     import pylab as pl
    #
    #     # 绘制波形
    #     pl.subplot(211)
    #     pl.plot(time, wave_data[0])
    #     pl.show()
    # with open(r"D:\MyProj\Company\XbtChatterbot2018\database\listen\1kXF.pcm", "rb") as f:
    #     data = f.read()
    #     print(data)
