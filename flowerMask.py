#Create a mask for the flower task consisting of random 10x10 pixels generated from the flower stimuli

""" 
flowerMask.py
Creates a mask consisting of numPixelxnumPixel pixel squares randomly selected from the flower images
Flower image dimensions: [x][y][R,G,B,a] where x = y = 800 and a is an alpha value (set to opaque [255] for this)
Flower starts at x/y = 190 and goes to x/y = 610 (roughly), but sweet spot is from 250 to 550 (IMO)
"""
#%%
import numpy as np
import scipy as sp
import math
from skimage import data #probably don't need
from skimage import io
import os
import shutil
import matplotlib.pyplot as plt
import random as rdm
from datetime import datetime

def fileParams():
    """ Delivers a list of five parameters with the following properties:
                a is 1:9 (inc)
                b is 1 or 9
                c is 1 or 9
                d is 1 or 9
         and    e is 1:5 (inc) 
        flower image files always take the form 'flower1_abcd_e.png'"""
    oneNine = (1,9) #list to randomly choose a parameter from 
    a = np.random.randint(1,10)
    b = rdm.choice(oneNine)
    c = rdm.choice(oneNine)
    d = rdm.choice(oneNine)
    e = np.random.randint(1,6)
    paramList = (a,b,c,d,e)
    return paramList

def getRandomFlower(paramList, dirPath):
    """Returns a random flower file from the images folder in the working directory"""
    #  create string for file name
    randFlowerFile = "flower1_" + str(paramList[0]) + str(paramList[1]) + str(paramList[2]) + str(paramList[3]) + "_" + str(paramList[4]) + ".png"
    # load file into an array
    randFlower = io.imread(dirPath+"/images/"+randFlowerFile)
    return randFlower

def getRandomChunk(xCentre, yCentre, rad, numPixels):
    """ Returns x and y dims from circle at centre of image w radius rad. 
        Upper edge boundaries for each dimension are reduced by numPixels."""
    # choose random section from array from circle of radius rad positioned at centre of image
    x = np.random.randint(xCentre-rad, xCentre-numPixels+rad) #Second value shifted to the right by pixels because edges
    # y values are constrained by x using circle equation (r^2 = (x-a)^2+(y-b)^2)
    y1 = int(-1 * math.sqrt(rad**2-(x-xCentre)**2)+yCentre) #lower (top) bound of y
    y2 = int(math.sqrt(rad**2-(x-xCentre)**2)+yCentre-numPixels) #Upper (bottom) bound of y; again, -pixels because edges
    if y1 < y2: #if x is at an extreme (xCentre +/- rad), y1 will be greater than y2 because of -pixels; this checks and accounts for that
        y = np.random.randint(y1,y2)
    else:
        y = int((y1+y2)/2)
    dims = (x,y)
    return dims

#Variables
numPixels = 25 #The size of the pixel chunks
dimMask = 800 #The dimensions of the mask image (square for now cuz it's late)
dirPath = os.getcwd()
rad = 150
#define an empty array to store the mask as it's being built
blankImg = np.empty((dimMask,dimMask,4),np.uint8)
#get centre of image (where flower is positioned)
xCentre = int(blankImg.shape[0]/2)
yCentre = int(blankImg.shape[1]/2)

''' Loop to fill blank image with random flower chunks, looks gross but it's just getting the 
    x and y dims of the image and splitting it into numPixels-sized chunks '''
for i in range(int(blankImg.shape[0]/numPixels)):
    for j in range(int(blankImg.shape[1]/numPixels)):
        # generate file parameter values
        paramList = fileParams()
        # get random flower
        randomFlower = getRandomFlower(paramList, dirPath)
        # get x and y dims
        x, y = getRandomChunk(xCentre, yCentre, rad, numPixels)
        # save a numPixels x numPixels sized chunk from this location into chunk of blank image file
        for a in range(i*numPixels,i*numPixels+numPixels):
            for b in range(j*numPixels,j*numPixels+numPixels):
                blankImg[a][b]=randomFlower[x+(a%numPixels)][y+(b%numPixels)]
                blankImg[a][b][3] = 255 # Make image opaque

#Save time-stamped image
now = datetime.now() # current date and time
date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
newFileName = dirPath + "/masks/mask_" + date_time + ".png"
io.imsave(newFileName, blankImg)
