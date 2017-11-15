from scipy import misc      # Import misc
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

    def correctHorizontal(self, image, pad = False, removePad = False, roll = False):
        newImage = self.new(image)
        if pad == True:
            newImage = np.lib.pad(newImage,((50,50),(50,50)),'constant', constant_values=(255, 255))
        if removePad == True:
            #newImage = self.removePad(newImage)
            newImage = self.removePad2(newImage)
        transformed = self.trans(newImage)
        for i in range(1,newImage.shape[0]-1):
            shift = self.maxima(self.conMult(np.fft.fft(newImage[i]),np.fft.fft(newImage[i-1])))
            newImage[i] = np.roll(newImage[i], shift)
        if roll == True:
            newImage = self.roll(newImage)
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

fn = str(raw_input("File : "))
im = misc.imread(fn)
fim = im

fixed = Fourier().correctHorizontal(im, roll = True)
fixed2 = Fourier().correctHorizontal(im, pad = True)
fixed3 = Fourier().correctHorizontal(fixed2, removePad = True)
fig, ax = plt.subplots(2,2)
ax[0,0].imshow(im,cmap=plt.cm.gray)
ax[0,1].imshow(fixed.real,cmap=plt.cm.gray)
ax[1,0].imshow(fixed2.real,cmap=plt.cm.gray)
ax[1,1].imshow(fixed3.real,cmap=plt.cm.gray)
plt.show()
#for i in range(0,trans.shape[0]):
#    prod = Fourier().conMult(trans[i],trans[i+1])
#    print(Fourier().minima(prod))
#    fig,ax = plt.subplots(2,1)
#    ax[0].scatter(prod.real,prod.imag)
#    ax[1].plot(np.arange(0-trans.shape[1]/2, 0 +trans.shape[1]/2, 1), prod.real,)
#    plt.show()
'''np.array_equal(image[i], np.zeros(len(image[i])))'''
