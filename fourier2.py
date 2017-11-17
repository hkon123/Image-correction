from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *

'''
Class for doing Fourier manipulation of images
'''

class Fourier(object):

    #method takes an image as input, returns the fourier transformed image
    #fourier transformes the image by passing each row to the np.fft.fft method
    def trans(self, image):
        transformed = image[0]
        array = None
        for i in range(1,image.shape[0]):
            array = image[i]
            transformed = np.vstack((transformed, np.fft.fft(array)))
        return transformed

    #method that takes an image as input, returns the inverse fourier transform of that image
    #inverse fourier transformes the image by passing each row to the np.fft.ifft method
    def invTrans(self, image):

        transformed = image[0]
        array = None
        for i in range(1,image.shape[0]):
            array = image[i]
            transformed = np.vstack((transformed, np.fft.ifft(array)))
        return transformed

    #method that takes two arrays as input, conjugates one of them and multiplies them toghether
    # and returns the inverse fourier transform of the product
    def conMult(self, array1, array2):
        cArray1 = np.conjugate(array1)
        product = cArray1 * array2
        return np.fft.ifft(product)
