from __future__ import division
from cv import *
from time import time
import os

def run():
	wc = CaptureFromCAM(0)
	asciiGroup = "#*oahbpqwmzcunxrt-+~<>:,^`. "
	windowsize = GetSize(QueryFrame(wc))
	hght = windowsize[1]
	wdth = windowsize[0]
	flipMode = 1
	fm = flipMode
	threshold = 100
	th = threshold
	color = 255
	clr = color
	laplaceDegree = 7
	ldeg = laplaceDegree
	desiredwidth = 225
	dw = desiredwidth
	scaledsize = (dw, int(dw * .5 * hght // wdth))

	frame = CreateImage(windowsize, 8, 1)
	edges = CreateImage(windowsize, IPL_DEPTH_16S, 1)
	scaled = CreateImage(scaledsize, 8, 1)

	while True:
		CvtColor(QueryFrame(wc),frame,CV_RGB2GRAY)
		Flip(frame,flipMode=fm)
		Smooth(frame,frame,CV_MEDIAN)

		'''Comment lines 34-40 and 50-57 and uncomment lines 60-65 to go back to just gradient/lapacian without the overlay'''
		Resize(frame,scaled) 
		printed=''
		for y in range(scaled.height):
			printed = printed + ' '*int((304-dw)/2)
			for x in range(scaled.width):
				printed = printed + asciiGroup[int(len(asciiGroup) - (scaled[y,x] * len(asciiGroup))//256 - 1)]
			printed = printed + '\n'*(y!=scaled.height-1)


		# EqualizeHist(frame,frame)
		Threshold(frame,frame,th,clr,CV_THRESH_BINARY)
		Laplace(frame,edges,ldeg)
		Convert(edges,frame)

		Resize(frame,scaled)

		pixelnum = 0
		for y in range(scaled.height):
			pixelnum += int((304-dw)/2)
			for x in range(scaled.width):
				pixelnum += 1
				if scaled[y,x] != 0:
					printed = printed[:pixelnum-1] + asciiGroup[0] + (printed[pixelnum:]*(pixelnum!=len(printed)-1))
			pixelnum += 1*(y!=(scaled.height-1))


		# printed=''
		# for y in range(scaled.height):
		# 	printed = printed + ' '*int((304-dw)/2)
		# 	for x in range(scaled.width):
		# 		printed = printed + asciiGroup[int(len(asciiGroup) - (scaled[y,x] * len(asciiGroup))//256 - 1)]
		# 	printed = printed + '\n'*(y!=scaled.height-1)

		os.system('clear')
		print(printed)
		WaitKey(1)

if __name__=='__main__':
	run()