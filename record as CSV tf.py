import sounddevice as sd
import numpy as np
# from scipy.io.wavfile import write
# from datetime import datetime, timedelta

import numpy as np
import tensorflow as tf
from os import makedirs

FRAME_RATE = 48000
FFT_SIZE = 2048
FRAME_STEP = 148
def fft(array):
#   array = array.astype(float)
  array = tf.signal.stft(array, frame_length=FFT_SIZE, frame_step=FRAME_STEP, window_fn=None)
  array = tf.abs(array)
  array = array[...,:256,:1024]
  return array.numpy()

import csv
def np2csv(nparray, fname):
    with open(fname, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(nparray)

def main():
    SECS = 1
    print('1sec per file.')
        
    CHANNELS = 1
    RATE = 48000
    CHUNK = SECS * RATE # RATE / number of updates per second
    csv_path = 'csvTF/'
    makedirs(csv_path, exist_ok=True)

    sd.default.samplerate = RATE
    sd.default.channels = CHANNELS

    csvCount = 0
    def save_recording(indata: np.ndarray, frames: int, t, status: sd.CallbackFlags):
        nonlocal csvCount
        # print(indata.dtype)
        indata = indata.reshape([-1])[-40000:]
        fft_indata = fft(indata)
        # print(fft_indata.shape)
        # fname = datetime.now().strftime("%Y-%m-%d__%Hh%Mm%Ss.wav")
        fname = f'{csv_path}{csvCount:06d}.csv'
        np2csv(fft_indata, fname)
        # write(filename, RATE, indata)
        print('Saved as '+fname)
        # print('Recording  ', end='', flush=True)
        csvCount+=1

    with sd.InputStream(blocksize=CHUNK, callback=save_recording, dtype=np.float32):
        while True:
            print('Enter q to quit.')
            print('Recording  ', end='', flush=True)
            userinput = input()
            if userinput == 'q':
                return

main()