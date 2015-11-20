# -*- coding: utf-8 -*-
import cv2
import numpy as np
import signal
import sys
import time

imgdir="/home/sqnn/lensface/"
face_data = "data/haarcascade_frontalface_default.xml"
fc = cv2.CascadeClassifier(face_data)

try:
  pattern=sys.argv[1] #Hole motion taken from input argument
except:
  print "Please enter mode"
  sys.exit(1)

if "circ" in pattern:
  def lensfunction(xx,ww,yy,kk):
    xc = xx+ww/2+60*np.cos(kk/5.)
    yc = yy+ww/2+80*np.sin(kk/5.)
    return xc,yc
elif "lem" in pattern:
  def lensfunction(xx,ww,yy,kk):
    radius = ww/2*abs(np.cos(kk/5.))
    xc = xx+ww/2+radius*np.cos(kk/5.)
    yc = yy+ww/2+radius*np.sin(kk/5.)
    return xc,yc
elif "rand" in pattern:
  def lensfunction(xx,ww,yy,kk):
    xc = np.random.randint(xx,xx+ww)
    yc = np.random.randint(yy,yy+ww)
    return xc,yc
elif "lissajous" in pattern:
  def lensfunction(xx,ww,yy,kk):
    xc = xx+ww/2+60*np.cos(kk/2.)
    yc = yy+ww/2+80*np.sin(kk/5.)
    return xc,yc
elif "cray" in pattern:
  def lensfunction(xx,ww,yy,kk):
    xc=xx+ww/2+70*(np.cos(kk)-np.cos(80*kk)**3)
    yc=xx+ww/2+80*(np.sin(kk)-np.sin(80*kk)**3)
    return xc,yc
elif "hypotrochoid" in pattern:
  def lensfunction(xx,ww,yy,kk):
    xc=xx+ww/2+60*np.cos(kk)+20*np.cos(-0.25*kk)
    yc=xx+ww/2+80*np.sin(kk)-20*np.sin(-0.25*kk)
    return xc,yc
else:
  raise SyntaxError("Missing/bad argument. Availabe modes are [circ,lem,rand]. Run as: python lenspy.py mode")
  sys.exit(1)

#these are sizes we ask from camera and how we set default
#lens and source plane distance parameters
HEIGHT=840
WIDTH=840

def takePic():
  """Useage: takePic()

Parameters
----------
None

Returns
----------
ret : int
	Return code from cv2.VideoCapture
img : 2d numpy array
	Pixel values for image data"""
  cp = cv2.VideoCapture(0)
  cp.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,HEIGHT)
  cp.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,WIDTH)
  ret, img = cp.read()
  cp.release()
  return ret, img

def findFaces(x):
  """Useage: findFaces(x)

Parameters
----------
x : 2d array of floats. 
	Image data from cv2 capture

Returns
----------
retcode : int
  Return code from cv2.VideoCapture
faces : 2d numpy array
	Array containing coordinates of recognized faces"""

  gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
  faces = fc.detectMultiScale(gray, 1.2, 2)
  retcode = 0
  if len(faces) > 0:
    retcode = 1
  return retcode,faces

def getFace(x,y):
  """Useage: getFacee(x,y)

Parameters
----------
x,y : 2d array of floats. 
  Image data from cv2 capture

Returns
----------
x0 : int
	x coordinate at the center of face
y0 : int
	y coordinate at center of face
w : int
	width of recognized face
x : 2d numpy array
  Array containing pixel data for image"""
  areas = y[:,2]*y[:,3]
  maxfc = np.argmax(areas)
  x0,y0,w = y[maxfc,0:3]
  w += 20
  return x0,y0,w,x

def lensImage(img,src,lens,xs,ys):
  """Useage: lensImage(img,src,lens,xs,ys)
  lens a 2d numpy array in place using a given source distance src and 
  black hole coordinate (xs,ys).

Parameters
----------
img : 2d array of floats. 
  Image data from cv2 capture
src : float
  Distance to source (pixels)
lens : float
  GR lens parameters
xs,ys : int
  pixel coordinates of black hold location

Returns
----------
None"""
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
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,HEIGHT)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,WIDTH)
kk = 0
while True:
  rcode, new_img = cap.read()
  rcode, faces_arr = findFaces(new_img)
  if rcode == 0:
    continue #No face found or other error, take new picture
  xx,yy,ww,face_img = getFace(new_img,faces_arr)
  #cv2.rectangle(new_img, (xx, yy), (xx+ww, yy+ww), (0, 255, 0), 2)
  height, width, colors = new_img.shape
  xc,yc=lensfunction(xx,ww,yy,kk)
  area_ratio = float(ww*ww)/HEIGHT/WIDTH
  source = 10*max(HEIGHT,WIDTH)   #image Distance (in pixels)
  #lens = source/2                 #distance to hole
  #print "area_ratio=" + str(area_ratio)
  # area ratio ranges from about .003 to .04 typically
  # dont want lens image to go negative
  lens = max((8.0 - 70*area_ratio)*source/9, source/9.0)
  lensImage(new_img, source, lens, yc, xc)
  cv2.imshow("Lensed Me!", new_img)
  cv2.moveWindow("Lensed Me!",1020,140)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  sec=time.strftime("%S",time.localtime())
  if sec=='30' or sec=='0':
    filename=time.strftime("%H%M%S%Y",time.localtime())
    cv2.imwrite(imgdir+filename+".png",new_img)
  kk+=1
cap.release()
cap.destroyAllWindows()
