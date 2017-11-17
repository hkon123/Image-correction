from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *
from new import New

'''
Class for manipulating an image
'''

class Manipulation(object):

    #method for adding padding to all 4 sides of an image using np.lib.pad
    #takes an image and an amount of pad and returns the new image
    def addPad(self, image, pad):
        return np.lib.pad(image,((pad,pad),(pad,pad)),'constant', constant_values=(255, 255))

    #method for adding padding to the two horizadtal sides of the image using np.lib.pad
    #takes an image and an amount of pad and returns the new image
    def pad(self, image):
        for i in range(image.shape[0]):
            image[i] = np.lib.pad(image[i],(30,30),'constant', constant_values=(255, 255))
        return image

    #method for removing ekstra pad from images
    #takes an image and returns the same image with 45 lines removed from all 4 sides
    def removePad2(self, image):
        for i in range(45):
            image = np.delete(image, (0), axis= 0)
            image = np.delete(image, (-1), axis= 0)
            image = np.delete(image, (0), axis= 1)
            image = np.delete(image, (-1), axis= 1)
        return image

    #method for rolling an entire images
    #takes an image and an amount of roll and returns the image rolled
    def roll(self, image, value):
        return np.roll(image, value)

    #method for normalizing shifts around zero so the shifts are from (-dimenshion/2,dimenshion/2)
    #insted of (0,dimenshion)
    #takes an array of shifts and the dimension of the image as raw_input
    #returns the normalized shifts
    def normalize(self, shifts, dimenshion):
        newShifts = []
        for i in shifts:
            newShifts.append(i)
        for i in range(len(newShifts)):
            if newShifts[i]>dimenshion/2:
                newShifts[i] = newShifts[i]-dimenshion
        return newShifts

    #method for anchoring all the lines in the image that are already alligned by changing their
    #shifts to 0 and moving all the other shifts relative to this
    #takes an array of shifts as input and returns an array of anchored shifts
    def anchor(self, shifts1):
        shifts = []
        anchorPoints = np.empty((0,2), int) # creates an array to hold the shifts that needs to be changed to zero
        for i in shifts1:                   #and how much they are moved
            shifts.append(i) # creates a new identical list of shifts as to not change the original
        i=0
        while i< len(shifts)-2: #finds the shifts that will be anchored to zero by testing if 3 or more shifts in a row
            if shifts[i] == shifts[i+1] and shifts[i] == shifts[i+2]: #are equal
                anchorPoints = np.append(anchorPoints,np.array([[i,shifts[i]]]), axis = 0)
                anchorPoints = np.append(anchorPoints,np.array([[i+1,shifts[i+1]]]), axis = 0)
                anchorPoints = np.append(anchorPoints,np.array([[i+2,shifts[i+1]]]), axis = 0)
            i+=1
        for i in anchorPoints[:,0]: #changes the value of the shifts that passed the last test to zero
            shifts[i] = 0
        #loop to move the shifts that are not zero relative to the ones that are now zero
        for i in range(len(shifts)):
            if shifts[i] == 0:                                     #"if the current shift is now zero(ie an anchorpoint) then"
                test = 0                                            # test value needed to check if a shift was zero before the shifts were anchored but should not be anchored
                for h in range(0,len(anchorPoints[:,0])):           #loop through all the indexes of the anchorpoints
                    if anchorPoints[h,0] == i:                      #if the index of shift is not found within the list of anchorpoints test will equal zero
                        test+=1
                if test == 0:                                       #if test is zero that means that the current shift is not an anchorpoint, so continue
                    continue
                for k in range(i+1,len(shifts)-1):                  #loops through the shifts after the current anchorpoint
                    test = 0
                    for h in range(0,len(anchorPoints[:,0])):        #same test as before to see if the next shift is zero, but not an anchorpoint
                        if anchorPoints[h,0] == k:
                            test+=1
                    if shifts[k] == 0 and test != 0:                  #if the next shift is an anchor point then break
                        break
                    else:                                              #if it is not an anchorpoint it is moved by the same amount as the anchorpoint was moved
                        for j in range(0,len(anchorPoints[:,0])):       #when it was moved to zero
                            if anchorPoints[j,0] == i:
                                shifts[k] = shifts[k] + -1*anchorPoints[j,1]
                                break
        return shifts

'''
    def brute(self, image):
        newImage = New().new(image)
        for j in range(5):
            for i in range(newImage.shape[0]):
                for k in range(newImage.shape[1]-2):
                    if abs(int(newImage[i,k])-int(newImage[i,k+1]))>50:
                        if abs(int(newImage[i,k])-int(newImage[i,k+2]))<50:
                            newImage[i,k+1] = np.uint8((int(newImage[i,k]) + int(newImage[i,k+2]))/2)
        return newImage
'''
