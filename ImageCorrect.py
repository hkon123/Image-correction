from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *
from fourier2 import Fourier
from ImageManipulation import Manipulation


class LineDistort(object):

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
        shift = self.maxima(Fourier().conMult(transformed[i],transformed[i-1]))
        return np.roll(image[i], shift)


    def correct(self, image):
        fixed = image[0]
        transformed = Fourier.trans(image)
        test = transformed[0]
        for i in range(1,image.shape[0]-1):
            fixed = np.vstack((fixed, self.shiftLine(image, transformed, i)))
        return fixed

    def correctHorizontal(self, image, pad = False, removePad = False, roll = False, linePad = False):
        newImage = self.new(image)
        shifts = []
        if pad == True:
            newImage = np.lib.pad(newImage,((300,300),(300,300)),'constant', constant_values=(255, 255))
        if removePad == True:
            #newImage = self.removePad(newImage)
            newImage = Manipulation().removePad2(newImage)
        transformed = Fourier().trans(newImage)
        for i in range(1,newImage.shape[0]-1):
            shift = self.maxima(Fourier().conMult(np.fft.fft(newImage[i]),np.fft.fft(newImage[i-1])))
            shifts.append(shift)
            if linePad == True:
                newImage[i] = Manipulation().addPad(newImage[i], shift)
            newImage[i] = np.roll(newImage[i], shift)
        if roll != False:
            newImage = Manipulation().roll(newImage, roll)
        return newImage, shifts

    def adjustedCorrection(self, image, shifts, pad = False):
        newImage = self.new(image)
        if pad == True:
            newImage = np.lib.pad(newImage,((300,300),(300,300)),'constant', constant_values=(255, 255))
            for i in range(301,newImage.shape[0]-301):
                newImage[i] = np.roll(newImage[i], shifts[i-301])
        else:
            for i in range(1,newImage.shape[0]-1):
                newImage[i] = np.roll(newImage[i], shifts[i-1])
        return newImage

    def correctVertical(self, image):
        newImage = self.new(image)
        for i in range(1,newImage.shape[0]-1):
            shift = self.maxima(Fourier().conMult(np.fft.fft(newImage[:,i]),np.fft.fft(newImage[:,i-1])))
            newImage[:,i] = np.roll(newImage[:,i], shift)
        return newImage

    def new(self, image):
        new = image[0]
        for i in range(1, image.shape[0]-1):
            new = np.vstack((new, image[i]))
        return new
