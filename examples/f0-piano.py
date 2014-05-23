import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hamming, triang, blackman, blackmanharris
from scipy.fftpack import fft, ifft, fftshift
import math
import sys, os, functools, time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../software/models/'))

import utilFunctions as UF
import stft as STFT
import harmonicModel as HM
import sineModel as SM

(fs, x) = UF.wavread('../sounds/piano.wav')
w = np.blackman(1501)
N = 2048
t = -90
minf0 = 100
maxf0 = 300
f0et = 1
maxnpeaksTwm = 4
H = 128
x1 = x[1.5*fs:1.8*fs]

plt.figure(1, figsize=(9, 7))
mX, pX = STFT.stftAnal(x, fs, w, N, H)
f0 = HM.f0Twm(x, fs, w, N, H, t, minf0, maxf0, f0et)
f0 = UF.cleaningTrack(f0, 5)
yf0 = SM.sinewaveSynth(f0, np.array([0.4]), H, fs)
UF.play(yf0,fs)
f0[f0==0] = np.nan
maxplotfreq = 800.0
numFrames = int(f0.size)
frmTime = H*np.arange(numFrames)/float(fs)                             
binFreq = fs*np.arange(N*maxplotfreq/fs)/N                        
plt.pcolormesh(frmTime, binFreq, np.transpose(mX[:,:N*maxplotfreq/fs+1]))
plt.autoscale(tight=True)
plt.plot(frmTime, f0, linewidth=2, color='k')
plt.autoscale(tight=True)
plt.title('mX + f0 (piano.wav), TWM')

plt.tight_layout()
plt.show()
