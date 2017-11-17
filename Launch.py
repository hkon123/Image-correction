from ImageCorrect import LineDistort
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *
from ImageManipulation import Manipulation
from fourier2 import Fourier

'''
Class to call the methods from the other classes and set up the plots
'''

class Launch(object):

    def __init__(self):
        fn = str(raw_input("File : ")) #reads in a pgm file
        im = misc.imread(fn) #creates an array of of the uint8 values in the image

        fixed, shifts = LineDistort().correctHorizontal(im, roll = -20) #gives a fixed image with roll added
        Nshifts = Manipulation().normalize(shifts, fixed.shape[1])  #Normalizes the shifts from the first immage correction
        Ashifts = Manipulation().anchor(Nshifts) #anchors all the points that does not need to be moved at zero and moves the shifts around them
        Bshifts = Manipulation().normalize(Ashifts, fixed.shape[1]) #renormalizes the shifts
        fixed3 = LineDistort().adjustedCorrection(im, Bshifts) # corrects the original image using the anchored and normalized shifts
        fixed2, shifts2 = LineDistort().correctHorizontal(im, pad = 100) # corrects the original image using original mehtod, but adds whitespace around the image
        #fixed4 , shifts4 = LineDistort().correctHorizontal(im)
        #fixed2 = LineDistort().adjustedCorrection(im, shifts)


        #plotting of all the images
        fig, ax = plt.subplots(2,2)
        ax[0,0].imshow(im,cmap=plt.cm.gray)
        ax[1,1].imshow(fixed3,cmap=plt.cm.gray)
        ax[1,0].imshow(fixed2,cmap=plt.cm.gray)
        ax[0,1].imshow(fixed.real,cmap=plt.cm.gray)
        ax[0,0].set_title("Original")
        ax[0,1].set_title("Corrected using given method, added image roll")
        ax[1,0].set_title("Corrected using given method, added whitespace around image")
        ax[1,1].set_title("corrected by normalizing shifts and anchoring non corrupted lines")

        plt.show()

        #plotting of the shift graphs
        fig, ax = plt.subplots(2,2)
        ax[0,0].imshow(im,cmap=plt.cm.gray)
        ax[0,1].imshow(fixed3,cmap=plt.cm.gray)
        ax[1,1].scatter(Bshifts, np.arange(0,len(Nshifts),1))
        ax[1,0].scatter(shifts, np.arange(0,len(shifts),1))
        ax[0,0].set_title("Original")
        ax[0,1].set_title("corrected by normalizing shifts and anchoring non corrupted lines")
        ax[1,0].set_title("line shift vs pixel before normalising and anchoring")
        ax[1,1].set_title("line shift vs pixel after normalizing and anchoring")


        plt.show()
