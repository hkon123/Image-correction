from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *
from fourier2 import Fourier
from ImageManipulation import Manipulation

'''
Class that fixes linear distorts of images
'''

class LineDistort(object):

    #method that takes an array as input and returns the index of the highest value in the array
    def maxima(self, array):
        test = array[0].real
        index = 0
        for i in range(1,len(array)-1):
            if array[i].real > test:
                test = array[i]
                index = i
        return index

    #method that takes an image, the fourier transform of that image and an index
    #uses the Fourier().conMult method to find the convolution graph of the fourier transform
    #of the ith and i-1th line in the image
    #then uses the maxima() method to find the peak
    #this is now the shift
    #it then returns the shifted ith line of the input image
    def shiftLine(self, transformed1, transformed2):
        #transformed = self.trans(image)
        shift = self.maxima(Fourier().conMult(transformed1,transformed2))
        return shift

    '''
    def correct(self, image):
        fixed = image[0]
        transformed = Fourier.trans(image)
        test = transformed[0]
        for i in range(1,image.shape[0]-1):
            fixed = np.vstack((fixed, self.shiftLine(image, transformed, i)))
        return fixed
    '''

    #method for correcting horizontally distorted images
    # image: image to be Corrected
    # pad: optional, how much padding to be added around the image (int)
    # removepad: optional, how many pixels to be removed from the image, left right top bottom(int)
    # roll: optional, how many pixels the image should be rolled left or right after the correction(-+int)
    # linePad : optional, does not work, dont use.
    #
    #returns the fixed image and an array of the shifts aplied to it
    def correctHorizontal(self, image, pad = False, removePad = False, roll = False, linePad = False):
        newImage = self.new(image) #creates a new identical image so the original isnt changed
        shifts = []
        if pad != False:   #adds padding using the Manipulation().addPad method
            newImage = Manipulation().addPad(newImage,pad)
        if removePad == True: #removes padding using the Manipulation().removePad2 method
            #newImage = self.removePad(newImage)
            newImage = Manipulation().removePad2(newImage)
        transformed = Fourier().trans(newImage) #creates a fourier transform of the original image
        #loop that loops through all the lines in the image and finds the shifts and applies them to the image
        for i in range(1,newImage.shape[0]-1):
            shift = self.shiftLine(np.fft.fft(newImage[i]),np.fft.fft(newImage[i-1]))
            shifts.append(shift)
            if linePad == True: #adds linepadding, does not work
                newImage[i] = Manipulation().addPad(newImage[i], shift)
            newImage[i] = np.roll(newImage[i], shift)
        if roll != False: #rolls the entire image isung the Manipulation().roll method
            newImage = Manipulation().roll(newImage, roll)
        return newImage, shifts

    #method for correcting horizontally distorted images
    #image: image to be Corrected
    #shifts: array of shifts to be aplied to the image
    #pad: optional, how much padding to be added around the image (int)

    #returns the image corrected using the given shifts
    def adjustedCorrection(self, image, shifts, pad = False):
        newImage = self.new(image) #creates a new identical image so the original isnt changed
        if pad == True: #adds padding around the image
            newImage =  Manipulation().addPad(newImage,pad)
            for i in range(pad+1,newImage.shape[0]-pad+1): #shifts the lines of the image using the given shifts
                newImage[i] = np.roll(newImage[i], shifts[i-pad+1])
        else:
            for i in range(1,newImage.shape[0]-1):  #shifts the lines of the image using the given shifts
                newImage[i] = np.roll(newImage[i], shifts[i-1])
        return newImage

    #method for correcting a vertically distorted images
    # takes an image as imput and returns the corrected image
    def correctVertical(self, image):
        newImage = self.new(image)
        for i in range(1,newImage.shape[0]-1):
            shift = self.maxima(Fourier().conMult(np.fft.fft(newImage[:,i]),np.fft.fft(newImage[:,i-1])))
            newImage[:,i] = np.roll(newImage[:,i], shift)
        return newImage

    #method that takes an image as input and returns an identical copy
    def new(self, image):
        new = image[0]
        for i in range(1, image.shape[0]-1):
            new = np.vstack((new, image[i]))
        return new
