from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
from math import *
from new import New

class Manipulation(object):

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

    def roll(self, image, value):
        return np.roll(image, value)

    def normalize(self, shifts, dimenshion):
        newShifts = []
        for i in shifts:
            newShifts.append(i)
        for i in range(len(newShifts)):
            if newShifts[i]>dimenshion/2:
                newShifts[i] = newShifts[i]-dimenshion
        return newShifts

    def anchor(self, shifts1):
        value = None
        shifts = []
        anchorPoints = np.empty((0,2), int)
        for i in shifts1:
            shifts.append(i)
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
                test = 0
                for h in range(0,len(anchorPoints[:,0])):
                    if anchorPoints[h,0] == i:
                        test+=1
                if test == 0:

                    continue
                for k in range(i+1,len(shifts)-1):
                    test = 0
                    for h in range(0,len(anchorPoints[:,0])):
                        if anchorPoints[h,0] == k:
                            test+=1
                    if shifts[k] == 0 and test != 0:
                        break
                    else:
                        for j in range(0,len(anchorPoints[:,0])):
                            #print(str(anchorPoints[j,0]) + " and " + str(i))
                            if anchorPoints[j,0] == i:
                                if shifts[k] == 0:
                                    value = True
                                shifts[k] = shifts[k] + -1*anchorPoints[j,1]
                                if value == True and shifts[k]>1:
                                    shifts[k] = shifts[k]
                                if value == True and shifts[k]<1:
                                    shifts[k] = shifts[k]
                                value = None
                                break
        return shifts


    def brute(self, image):
        newImage = New().new(image)
        for j in range(5):
            for i in range(newImage.shape[0]):
                for k in range(newImage.shape[1]-2):
                    if abs(int(newImage[i,k])-int(newImage[i,k+1]))>50:
                        if abs(int(newImage[i,k])-int(newImage[i,k+2]))<50:
                            newImage[i,k+1] = np.uint8((int(newImage[i,k]) + int(newImage[i,k+2]))/2)
        return newImage
