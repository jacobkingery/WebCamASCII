from __future__ import division
from cv import *
from time import time
import os

def run():
	wc = CaptureFromCAM(0)	#selects the first camera found
	asciiGroup = "#*oahbpqwmzcunxrt-+~<>:,^`. "		#ASCII characters used to represent image
	windowsize = GetSize(QueryFrame(wc))	#Finding image size
	hght = windowsize[1]
	wdth = windowsize[0]
	flipMode = 1 	#Mirror web cam image
	fm = flipMode
	threshold = 100		#Threshold for Threshold()
	th = threshold
	color = 255		#Color for Threshold()
	clr = color
	laplaceDegree = 3		#Degree of Lapaciation
	ldeg = laplaceDegree
	desiredwidth = 225		#Desired width of output
	dw = desiredwidth
	scaledsize = (dw, int(dw * .5 * hght // wdth))		#Scaled size based on desired width

	frame = CreateImage(windowsize, 8, 1)		#Creating frame image
	edges = CreateImage(windowsize, IPL_DEPTH_16S, 1)		#Creating edges image
	scaled = CreateImage(scaledsize, 8, 1)		#Creating scaled image

	while True:
		CvtColor(QueryFrame(wc),frame,CV_RGB2GRAY)		#Capturing a frame from the web cam and converting it to grayscale
		Flip(frame,flipMode=fm)		#Flipping image so that it is mirrored
		Smooth(frame,frame,CV_MEDIAN)		#Smoothing image to reduce noise

		'''Comment lines 34-40 and 50-57 and uncomment lines 60-65 to go back to just gradient/lapacian without the overlay'''
		Resize(frame,scaled) 		#Resizing image to desired size
		printed=''
		for y in range(scaled.height):
			printed = printed + ' '*int((304-dw)/2)		#Centering output in terminal window of width 304
			for x in range(scaled.width):
				printed = printed + asciiGroup[int(len(asciiGroup) - (scaled[y,x] * len(asciiGroup))//256 - 1)]		#Adding next character
			printed = printed + '\n'*(y!=scaled.height-1)		#Adding newline for each row


		Threshold(frame,frame,th,clr,CV_THRESH_BINARY)		#Creating black and white image
		Laplace(frame,edges,ldeg)		#Doing Laplacian on image
		Convert(edges,frame)		

		Resize(frame,scaled)		#Resizing image to desired size

		pixelnum = 0
		for y in range(scaled.height):
			pixelnum += int((304-dw)/2)
			for x in range(scaled.width):
				pixelnum += 1
				if scaled[y,x] != 0:
					printed = printed[:pixelnum-1] + asciiGroup[0] + (printed[pixelnum:]*(pixelnum!=len(printed)-1))		#Replacing character from gradient with # if it is present in edge-detected image
			pixelnum += 1*(y!=(scaled.height-1))


		# printed=''
		# for y in range(scaled.height):
		# 	printed = printed + ' '*int((304-dw)/2)
		# 	for x in range(scaled.width):
		# 		printed = printed + asciiGroup[int(len(asciiGroup) - (scaled[y,x] * len(asciiGroup))//256 - 1)]
		# 	printed = printed + '\n'*(y!=scaled.height-1)

		os.system('clear')		#Clearing terminal
		print(printed)		#Printing string of ASCII characters
		WaitKey(1)

if __name__=='__main__':
	run()