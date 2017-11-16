from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *


class Fourier(object):

    def trans(self, image):
        transformed = image[0]
        array = None
        for i in range(1,image.shape[0]):
            array = image[i]
            transformed = np.vstack((transformed, np.fft.fft(array)))
        return transformed

    def invTrans(self, image):

        transformed = image[0]
        array = None
        for i in range(1,image.shape[0]):
            array = image[i]
            transformed = np.vstack((transformed, np.fft.ifft(array)))
        return transformed

    def conMult(self, array1, array2):
        cArray1 = np.conjugate(array1)
        product = cArray1 * array2
        return np.fft.ifft(product)

    def maxima(self, array):
        test = array[0].real
        index = 0
        for i in range(1,len(array)-1):
            if array[i].real > test:
                test = array[i]
                index = i
        return index

    def shiftLine(self, image, transformed, i):
        #transformed = self.trans(image)
        shift = self.maxima(self.conMult(transformed[i],transformed[i-1]))
        return np.roll(image[i], shift)


    def correct(self, image):
        fixed = image[0]
        transformed = self.trans(image)
        test = transformed[0]
        for i in range(1,image.shape[0]-1):
            fixed = np.vstack((fixed, self.shiftLine(image, transformed, i)))
        return fixed

    def correctHorizontal(self, image, pad = False, removePad = False, roll = False, linePad = False):
        newImage = self.new(image)
        shifts = []
        if pad == True:
            newImage = np.lib.pad(newImage,((50,50),(50,50)),'constant', constant_values=(255, 255))
        if removePad == True:
            #newImage = self.removePad(newImage)
            newImage = self.removePad2(newImage)
        transformed = self.trans(newImage)
        for i in range(1,newImage.shape[0]-1):
            shift = self.maxima(self.conMult(np.fft.fft(newImage[i]),np.fft.fft(newImage[i-1])))
            shifts.append(shift)
            if linePad == True:
                newImage[i] = self.addPad(newImage[i], shift)
            newImage[i] = np.roll(newImage[i], shift)
        if roll == True:
            newImage = self.roll(newImage)
        return newImage, shifts

    def adjustedCorrection(self, image, shifts, pad = False):
        newImage = self.new(image)
        if pad == True:
            newImage = np.lib.pad(newImage,((170,170),(170,170)),'constant', constant_values=(255, 255))
            for i in range(171,newImage.shape[0]-171):
                newImage[i] = np.roll(newImage[i], shifts[i-171])
        else:
            for i in range(1,newImage.shape[0]-1):
                newImage[i] = np.roll(newImage[i], shifts[i-1])
        return newImage

    def correctVertical(self, image):
        newImage = self.new(image)
        for i in range(1,newImage.shape[0]-1):
            shift = self.maxima(self.conMult(np.fft.fft(newImage[:,i]),np.fft.fft(newImage[:,i-1])))
            newImage[:,i] = np.roll(newImage[:,i], shift)
        return newImage

    def new(self, image):
        new = image[0]
        for i in range(1, image.shape[0]-1):
            new = np.vstack((new, image[i]))
        return new

    def addPad(self, line, pad):
        return np.lib.pad(line,(pad,pad),'constant', constant_values=(0,0))

    def pad(self, image):
        for i in range(image.shape[0]):
            image[i] = np.lib.pad(image[i],(30,30),'constant', constant_values=(0, 0))
        return image

    def removePad(self, image):
        i = 0
        while i < image.shape[0]:
            if np.array_equal(image[i], np.zeros(len(image[i]))) == True:
                image = np.delete(image, (i), axis= 0)
            else:
                i+=1
        i = 0
        while i < image.shape[1]:
            if np.array_equal(image[:,i], np.zeros(len(image[:,i]))) == True:
                image = np.delete(image, (i), axis = 1)
            else:
                i+=1
        return image

    def removePad2(self, image):
        for i in range(45):
            image = np.delete(image, (0), axis= 0)
            image = np.delete(image, (-1), axis= 0)
            image = np.delete(image, (0), axis= 1)
            image = np.delete(image, (-1), axis= 1)
        return image

    def roll(self, image):
        return np.roll(image, 12)

    def normalize(self, shifts, dimenshion):
        for i in range(len(shifts)):
            if shifts[i]>dimenshion/2:
                shifts[i] = shifts[i]-dimenshion
        return shifts

    def anchor(self, shifts1):
        shifts = []
        anchorPoints = np.empty((0,2), int)
        anchor = 57
        for i in shifts1:
            shifts.append(i)
        '''
        i=0
        while i< len(shifts)-2:
            if shifts[i] == shifts[i+1] and shifts[i] == shifts[i+2]:
                anchor = shifts[i]
                break
            i+=1
        '''
        i=0
        while i< len(shifts)-2:
            if shifts[i] == shifts[i+1] and shifts[i] == shifts[i+2]:
                anchorPoints = np.append(anchorPoints,np.array([[i,shifts[i]]]), axis = 0)
                anchorPoints = np.append(anchorPoints,np.array([[i+1,shifts[i+1]]]), axis = 0)
                anchorPoints = np.append(anchorPoints,np.array([[i+2,shifts[i+1]]]), axis = 0)
            i+=1
        for i in anchorPoints[:,0]:
            shifts[i] = 0

        for i in range(len(shifts)):
            if shifts[i] == 0:
                for k in range(i+1,len(shifts)-1):
                    if shifts[k] ==0:
                        break
                    else:
                        for j in range(0,len(anchorPoints[:,0])):
                            #print(str(anchorPoints[j,0]) + " and " + str(i))
                            if anchorPoints[j,0] == i:
                                shifts[k] = shifts[k] + -1*anchorPoints[j,1]
                                break
        return shifts




fn = str(raw_input("File : "))
im = misc.imread(fn)
fim = im
print(im)
fixed, shifts = Fourier().correctHorizontal(im)
#fixed2, shifts2 = Fourier().correctHorizontal(fixed)
#fixed3 = Fourier().correctHorizontal(fixed2, removePad = True)
nShifts = Fourier().normalize(shifts, fixed.shape[0])
#nShifts2 = Fourier().normalize(shifts2, fixed.shape[0])
Ashifts = Fourier().anchor(nShifts)
fixed2 = Fourier().adjustedCorrection(im, shifts, pad = True)
fixed3 = Fourier().adjustedCorrection(im, Ashifts)
fig, ax = plt.subplots(2,2)
ax[0,0].imshow(im,cmap=plt.cm.gray)
ax[0,1].imshow(fixed.real,cmap=plt.cm.gray)
#ax[1,0].imshow(fixed2.real,cmap=plt.cm.gray)
ax[1,1].imshow(fixed3.real,cmap=plt.cm.gray)
ax[1,0].scatter(Ashifts, np.arange(0,len(Ashifts),1)[::-1])
#ax[0,1].scatter(nShifts, np.arange(0,len(nShifts),1)[::-1])
#ax[1,1].scatter(Fourier().normalize(shifts2, fixed.shape[0]), np.arange(0,len(shifts2),1))
plt.show()
#for i in range(0,trans.shape[0]):
#    prod = Fourier().conMult(trans[i],trans[i+1])
#    print(Fourier().minima(prod))
#    fig,ax = plt.subplots(2,1)
#    ax[0].scatter(prod.real,prod.imag)
#    ax[1].plot(np.arange(0-trans.shape[1]/2, 0 +trans.shape[1]/2, 1), prod.real,)
#    plt.show()
'''np.array_equal(image[i], np.zeros(len(image[i])))'''
