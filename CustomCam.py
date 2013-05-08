from __future__ import division
from cv import *
from time import time
import os
import customconvolve as cc


def run():
	wc = CaptureFromCAM(0)
	asciiGroup = "#*oahbpqwmzcunxrt-+~<>:,^`. "
	asciiGroup = "##########**********oahkbdpqwmzcvunxrjft|?-+~<>!:,^`'...    "[::-1]
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
		# asciiGroup = "#*oahbpqwmzcunxrt-+~<>:,^`. "
		CvtColor(QueryFrame(wc),frame,CV_RGB2GRAY)
		Flip(frame,flipMode=fm)

		Resize(frame,scaled) 
		printed=''
		for y in range(scaled.height):
			printed = printed + ' '*int((304-dw)/2)
			for x in range(scaled.width):
				printed = printed + asciiGroup[int(len(asciiGroup) - (scaled[y,x] * len(asciiGroup))//256 - 1)]
			printed = printed + '\n'*(y!=scaled.height-1)

		#insert magic edge detect here
		frame = cc.convolve(frame,'uberlaplace')
		Resize(frame,scaled)

		#asciiGroup = asciiGroup[::-1]
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