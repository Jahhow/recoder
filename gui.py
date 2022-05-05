import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import tensorflow as tf
import sounddevice as sd
from plt_chinese import plt

THRESHOLD = 11.785

if __name__ == '__main__':
    app = QApplication(sys.argv)

def smooth(arr, factor=2**-2, startvalue=None):
    if startvalue is None:
        r=[arr[0]]
        last=arr[0]
        arr=arr[1:]
    else:
        r=[]
        last=startvalue
    for a in arr:
        diff=a-last
        diff*=factor
        newA=last+diff
        last=newA
        r.append(newA)
    return r

FRAME_RATE = 10000
FFT_SIZE = 2048
FRAME_STEP = 2048-1892
from scipy.signal import stft

def fft(array):
  f, t, array = stft(array, fs=FRAME_RATE, nperseg=FFT_SIZE, noverlap=1892, padded=False)
  array = np.abs(array).transpose()
  array = array[...,:256,:1024, np.newaxis]
  return array

class WorkThread(QThread):
    onUpdateScoresResult = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        model = tf.keras.models.load_model('model/0429.h5')

        SECS = 4


        CHANNELS = 1
        RATE = 10000
        CHUNK_SECS = 0.25
        CHUNK = int(CHUNK_SECS * RATE) # RATE / number of updates per second

        sd.default.samplerate = RATE
        sd.default.channels = CHANNELS

        wave = np.array([], dtype=np.float32)
        def process_recording(indata: np.ndarray, frames: int, t, status: sd.CallbackFlags):
            nonlocal wave
            indata = indata.reshape([-1])
            wave = np.concatenate([wave, indata])

            if len(wave)<40000:
                return

            wave = wave[-40000:]
            
            fft_indata = fft(wave)
            fft_indata = fft_indata[np.newaxis,...]
            # print('fft_indata.shape',fft_indata.shape)

            y = model.predict(fft_indata)
            # print('y.shape',y.shape)
            y = y[0,0]
            # print(type(y), y)
            self.onUpdateScoresResult.emit((y,))
            # print(fft_indata.shape)

        with sd.InputStream(blocksize=CHUNK, callback=process_recording, dtype=np.float32):
            while True:
                self.sleep(2147483647)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.setWindowTitle('中鋼 AI 異常偵測')
        # self.setupUi(self)
        # self.resize(WINDOW_SIZE)

        self.textlabel: QLabel
        # self.textlabel.setText('異常偵測')

        # Actions
        # self.actionEncoder.triggered.connect(
        #     self.on_actionEncoder)

        # Buttons
        self.pushButton: QPushButton
        # self.updatePlayButtonIcon()
        self.pushButton.clicked.connect(self.onPushButtonClick)

        # setFocus to receive keypress
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.onInitScoresResult()

        # Thread --------------------------------------------------------
        self.initThread = WorkThread()
        self.initThread.onUpdateScoresResult.connect(self.onUpdateScoresResult)
        self.initThread.start()

        self._bgcolor = QColor(240,240,240)
        self.targetColor = QColor(240,240,240)

    @pyqtProperty(QColor)
    def bgcolor(self):
        return self._bgcolor
    @bgcolor.setter
    def bgcolor(self, color:QColor):
        # self.setStyleSheet(f'background-color: rgb({color.red}, {color.green}, {color.blue});')
        self.setStyleSheet(f'background-color: rgb({color.red()}, {color.green()}, {color.blue()});')
        # self.setStyleSheet(f'background-color: rgb(0, 255, 255);')
        self._bgcolor = color
                         
    def onInitScoresResult(self):
        self.smoothDiffs=[]
        # stepXticks=1
        TITLE = '聲波異常偵測'
        self.textlabel.setText(TITLE)

        plt.ion()
        self.fig = plt.figure(dpi=100, figsize=(10,3), facecolor='w')
        self.ax = self.fig.add_subplot()
        self.ax.set_title(TITLE)
        self.pltdata, = self.ax.plot([], [], label='預測之轉速與實際轉速之差異')
        # self.ax.set_ylabel('異常值')
        # self.ax.set_xticks(xticks[0][::stepXticks], xticks[1][::stepXticks], rotation=90)
        self.ax.legend()
        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.fig.show()

    def onUpdateScoresResult(self, r):
        y, = r

        smoothDiffs = self.smoothDiffs
        if len(smoothDiffs) == 0:
            smoothDiffs.append(y)
        else:
            last = smoothDiffs[-1]
            diff = y-last
            smoothDiffs.append(last+diff*2**-2)
        self.pltdata.set_data(np.arange(len(smoothDiffs)), smoothDiffs)
        ydelta = max(smoothDiffs) - min(smoothDiffs)
        self.ax.set_ylim(min(smoothDiffs)-ydelta*.05, max(smoothDiffs)+ydelta*.05)
        xdelta = len(smoothDiffs)
        self.ax.set_xlim(0-xdelta*.05, xdelta-1+xdelta*.05)
        # self.ax.autoscale()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # self.fig.show()

        if y>THRESHOLD:
            # self.setStyleSheet("background-color: red;")
            self.animateBgcolorTo(QColor(240, 70, 70))
            self.textlabel.setText('異常')
        else:
            # self.setStyleSheet("background-color: none;")
            self.animateBgcolorTo(QColor(240, 240, 240))
            self.textlabel.setText('正常')

    def animateBgcolorTo(self,targetColor):
        if self.targetColor != targetColor:
            self.targetColor = targetColor
            
            self.animation = QPropertyAnimation(self, b'bgcolor')
            self.animation.setDuration(150)
            # self.animation.setStartValue(self.bgcolor)
            self.animation.setEndValue(targetColor)
            self.animation.start()

    def onPushButtonClick(self):
        self.fig.show()

if __name__ == '__main__':
    def main():
        window = MainWindow()
        window.showMaximized()
        # animation = QPropertyAnimation(window, b'bgcolor')
        # animation.setDuration(1000)
        # animation.setStartValue(window.bgcolor)
        # animation.setEndValue(QColor(240,70,70))
        # animation.start()
        app.exec()

    main()