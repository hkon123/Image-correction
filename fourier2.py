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
