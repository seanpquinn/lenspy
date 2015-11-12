#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import signal
import sys
import time

ocv_data_path = "/usr/share/opencv/"
ocv_cascade = "haarcascades/haarcascade_frontalface_default.xml"
fc = cv2.CascadeClassifier(ocv_data_path+ocv_cascade)

def sigterm_handler(signal, frame):
  print "Got SIGTERM, exiting."
  sys.exit(0)

def takePic():
  cp = cv2.VideoCapture(0)
  cp.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1024)
  cp.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
  ret, img = cp.read()
  cp.release()
  return ret, img

def findFaces(x):
  gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
  faces = fc.detectMultiScale(gray, 1.2, 2)
  retcode = 0
  if len(faces) > 0:
    retcode = 1
  return retcode,faces

def getFace(x,y):
  """Takes image array from takePic and array found from  findFaces
  and performs lensing on the largest face. Returns lensed image"""
  areas = y[:,2]*y[:,3]
  maxfc = np.argmax(areas)
  x0,y0,w = y[maxfc,0:3]
  w += 20
  return x0,y0,w,x

def lensImage(img,src,lens,xs,ys):
  """Lens image x using given parameters"""
  # edits image in place
  if (lens >= src):
    raise RuntimeError("lens: " + str(lens) + 
    " should not exceed source distance " + str(src))
  imageCopy = cv2.copyMakeBorder(img,0,0,0,0,cv2.BORDER_REPLICATE)
  height, width, colors = img.shape
  x, y = np.ogrid[0:height,0:width]
  #print "parameters are source: {0}, lens {1}, \
  #xSource {2}, ySource {3}".format(src, lens, xs, ys)
  dX = x - xs
  dY = y - ys
  R = dX*dX + dY*dY
  #shift = np.zeros_like(R)
  R[R==0]=1   #shut down the divide by 0 pixel, if any
  # less broken-line distortion seen w/25 than 10. 
  # Probably want to set a max on this
  # might be interesting to do a loop wherein lens is modified
  shift = (1.0- (src-lens)*src/lens/R/25.0) #might put a mass term in here
  dXshift = (dX*shift + xs).astype(int)
  dYshift = (dY*shift + ys).astype(int)
  # this seems to do the right thing, 
  #equivalent to +/- = height/width until in range
  dXshift %= height
  dYshift %= width
  img[x,y]=imageCopy[dXshift,dYshift]

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1024)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
while True:
  #rcode, new_img = takePic()
  rcode, new_img = cap.read()
  if rcode == False:
    continue #If image capture fails, take another
  rcode, faces_arr = findFaces(new_img)
  if rcode == 0:
    continue #No face found or other error, take new picture
  xx,yy,ww,face_img = getFace(new_img,faces_arr)
  print xx,yy,faces_arr
  cv2.rectangle(new_img, (xx, yy), (xx+ww, yy+ww), (0, 255, 0), 2)
  height, width, colors = new_img.shape
  xrand = np.random.randint(xx,xx+ww)
  yrand = np.random.randint(yy,yy+ww)
  source = 10*max(height,width)   #image Distance (in pixels)
  lens = source/2                 #distance to hole
  lensImage(new_img, source, lens, yrand, xrand)
  cv2.imshow("Lensed Me!", new_img)
  #cv2.waitKey(50)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  #time.sleep(0.2)
  #cv2.imwrite("JustLensed.jpg", face_img)
  #new_img[yy:yy+ww,xx:xx+ww] = face_img
  #cv2.imwrite("Orig+lens.jpg", new_img)
  #signal.signal(signal.SIGTERM, sigterm_handler)
cap.release()
cap.destroyAllWindows()
