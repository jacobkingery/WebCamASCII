import cv
from time import time
import numpy as np
#from random_kernel import random_kernel

# Returns a CvMat object equivalent to entered list matrix
def giveMeCV(l):
	r = cv.CreateMat(len(l),len(l[0]),1)
	for i in range(len(l)):
		for j in range(len(l[0])):
			cv.SetND(r,(i,j),l[i][j])
	return r

# Example Kernels for Testing

sobel = giveMeCV([[-1, 0, 1],
			  	  [-2, 0, 2],
			   	  [-1, 0, 1]])
test = np.matrix([[-1, 0, 1],
				  [-2, 0, 2],
			   	  [-1, 0, 1]])
test = np.transpose(test)
sobelT = giveMeCV(test.tolist())

laplace = giveMeCV([[-1,-1,-1],
					[-1, 8,-1],
					[-1,-1,-1]])

uberlaplace = giveMeCV([[-1,-1,-1,-1,-1],
						[-1,-1,-1,-1,-1],
						[-1,-1,24,-1,-1],
						[-1,-1,-1,-1,-1],
						[-1,-1,-1,-1,-1]])

def run():
	# SETUP VARIABLES

	wc = cv.CaptureFromCAM(0)
	cv.NamedWindow('Camera',cv.CV_WINDOW_AUTOSIZE)
	dur = 20 # approximate duration in seconds

	# Applied Kernel
	kernel = laplace

	start = time() # for framerate checking (usu. ~30)
	for i in range(dur*30):

		# Capture Frame from Webcam
		frame = cv.QueryFrame(wc)
		# Apply Kernel Filter
		#kernel = giveMeCV(random_kernel(3,1,0)) # Uncomment for random kernel
		cv.Filter2D(frame, frame, kernel)
		# Mirror Image
		cv.Flip(frame,flipMode=1)

		# Display transformed image
		cv.ShowImage('Camera',frame)
		cv.WaitKey(1)
	# Frame Rate

	print(dur/(time()-start))

def get_kernel(s):
	if s=='sobel':
		return sobel
	elif s=='sobelT':
		return sobelT
	elif s=='laplace':
		return laplace
	elif s=='uberlaplace':
		return uberlaplace
	else:
		return laplace

def convolve(frame, k_name): # Maybe also take kernels
	kernel = get_kernel(k_name)
	cv.Filter2D(frame,frame,kernel)
	return frame

if __name__=='__main__':
	run()