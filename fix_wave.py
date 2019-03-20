
import os
import wave
wav_dir = 'wav'

new_dir = 'wav_new'
wave_list = os.listdir(wav_dir)
for w in wave_list:
    wave_path = os.path.join(wav_dir, w)
    wf = wave.open(wave_path, 'rb')
    pa = wf.getparams()
    nchannels, sampwidth, framerate, nframes = pa[:4]
    data = wf.readframes(nframes)
    wf.close()

    new_path = os.path.join(new_dir, w)
    f = wave.open(new_path, "wb")
    f.setnchannels(nchannels)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)
    f.writeframes(data)
    f.close()

