from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *

class New(object):
    
    def new(self, image):
        new = image[0]
        for i in range(1, image.shape[0]-1):
            new = np.vstack((new, image[i]))
        return new
