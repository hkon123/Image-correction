from ImageCorrect import LineDistort
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *
from ImageManipulation import Manipulation
from fourier2 import Fourier


fn = str(raw_input("File : "))
im = misc.imread(fn)
fim = im

fixed, shifts = LineDistort().correctHorizontal(im, roll = -20)
Nshifts = Manipulation().normalize(shifts, fixed.shape[1])
Ashifts = Manipulation().anchor(Nshifts)
Bshifts = Manipulation().normalize(Ashifts, fixed.shape[1])
#fixed2, shifts2 = LineDistort().correctHorizontal(im, pad = True)
fixed3 = LineDistort().adjustedCorrection(im, Bshifts)
fixed2 = LineDistort().adjustedCorrection(im, shifts)
fig, ax = plt.subplots(2,2)
ax[0,0].imshow(im,cmap=plt.cm.gray)
ax[0,1].imshow(fixed3,cmap=plt.cm.gray)
#ax[1,1].imshow(Fourier().trans(fixed3).imag,cmap=plt.cm.gray)
#ax[0,1].imshow(fixed3.real,cmap=plt.cm.gray)
ax[1,1].scatter(Bshifts, np.arange(0,len(Nshifts),1))
ax[1,0].scatter(shifts, np.arange(0,len(shifts),1))
#ax[1,0].scatter(Ashifts, np.arange(0,len(nShifts),1)[::-1])
plt.ylim(1400,-20)
plt.show()
'''
f = open('test.txt','w')
for i in range(fixed2.shape[0]):
    f.write("\n")
    for k in range(fixed2.shape[1]):
        f.write(str(fixed2[i,k]))
        f.write(" ")
'''
