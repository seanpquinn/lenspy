#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import sys
import random       #for choosing location of hole
faceCascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")

def getBiggestFace():
    # returns image, face
    print "capturing from webcam"
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
         loop = True
         cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1024)
         cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
         while True:
            ret, image = cap.read()
            print "took a pic"
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2,2)
            print str(len(faces)) + " faces"
            if (len(faces) > 0): 
                biggest = 0
                for face in faces:
                    (i,j,w,h) = face 
                    if w*h > biggest:
                        biggest = w*h
                        biggestFace = face
                if biggest > 2500: 
                    cap.release()
                    return (image, biggestFace)
                    break
    else:
        return (False, False)
#imageCopy = cv2.copyMakeBorder(image,0,0,0,0,cv2.BORDER_REPLICATE)
#height, width, colors = image.shape

# identify faces
#faceCascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")


# seems to work for me if I don't have my glasses on, and is frontal
#if not loop: 
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
##faces = faceCascade.detectMultiScale(gray,
##                                     scaleFactor=1.1,
##                                     minNeighbors=5,
##                                     minSize=(50,50),
##                                     flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
#biggest = 2500 
#### change "magic numbers that work" to contstants
#biggestFace=(width/2 - 25 , height/2 - 25 , 50, 50)
#for face in faces:
#    print "found a face"
#    (i,j,w,h) = face
#    cv2.rectangle(imageCopy, (i, j), (i+w, j+h), (0, 255, 0), 2)
#    print w*h
#    if (w*h > biggest):
#        biggest = w*h
#        biggestFace = face


def lensImage(image, source, lens, xSource, ySource):
    # edits image in place
    if (lens >= source):
        raise RuntimeError("lens: " + str(lens) + " should not exceed source distance " + str(source))
    #xSource = (height-1)/2.0              #coords in plane of hole
    #ySource = (width-1)/2.0         #sticking it in the middle for now
    imageCopy = cv2.copyMakeBorder(image,0,0,0,0,cv2.BORDER_REPLICATE)
    height, width, colors = image.shape
    x, y = np.ogrid[0:height,0:width]
    print "parameters are source: {0}, lens {1}, xSource {2}, ySource {3}".format(source, lens, xSource, ySource)
    dX = x - xSource
    dY = y - ySource
    R = dX*dX + dY*dY
    #shift = np.zeros_like(R)
    R[R==0]=1   #shut down the divide by 0 pixel, if any
    # less broken-line distortion seen w/25 than 10. Probably want to set a max on this
    # might be interesting to do a loop wherein lens is modified
    shift = (1.0- (source-lens)*source/lens/R/25.0) #possibly put a mass term in here
    #dXshift = (dX*shift + xSource +0.5).astype(int)
    #dYshift = (dY*shift + ySource +0.5).astype(int)
    dXshift = (dX*shift + xSource).astype(int)
    dYshift = (dY*shift + ySource).astype(int)
    ## this seems to do the right thing, equivalent to +/- = height/width until in range
    dXshift %= height
    dYshift %= width
    ## doing a loop here since I don't know how to slice this right in numpy
    ## possible to subtract some things and only iterate over the pixels that matter?
    #for i in xrange(height):
    #    for j in xrange(width):
    #        image[i,j] = imageCopy[dXshift[i,j], dYshift[i,j]]
    #image = imageCopy[dXshift,dYshift]
    image[x,y]=imageCopy[dXshift,dYshift]
#source =  (biggest)**0.5*max(height,width)/(height+width)**0.5
while True:
    image, biggestFace = getBiggestFace()
    (xface, yface, wface, hface) = biggestFace
    cv2.rectangle(image, (xface, yface), (xface+wface, yface+hface), (0, 255, 0), 2)
    ySource = random.randint(xface, xface+wface)
    xSource = random.randint(yface, yface+hface)
    
    height, width, colors = image.shape
    source = 10*max(height,width)   #image Distance (in pixels)
    lens = source/2                 #distance to hole
    #lens = 5*max(height,width)      # 1/2 default source
    lensImage(image, source, lens, xSource, ySource)
    cv2.imshow("Lensed Me!", image)
    cv2.waitKey(10)
    cv2.imwrite("JustLensed.jpg", image)

