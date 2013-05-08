from __future__ import division
from cv import *
import os


def capture_frame():
    """Capture frame from webcam, convert to grayscale, flip, and smooth."""
    global wc
    global fm
    global inputframe

    CvtColor(QueryFrame(wc), inputframe, CV_RGB2GRAY)
    Flip(inputframe, flipMode=fm)
    Smooth(inputframe, inputframe, CV_MEDIAN)

    return inputframe


def hybrid_process(hybframe):
    """Process frame using a gradient-Laplacian hybrid."""
    global summation

    hybgrad = gradient_process(hybframe)
    hyblap = laplacian_process(hybframe)

    Add(hybgrad, hyblap, summation)

    return summation


def gradient_process(gradframe):
    """Process frame using only a gradient."""
    global gradscaled

    Resize(gradframe, gradscaled)

    return GetMat(gradscaled)


def laplacian_process(lapframe):
    """Process frame using only a Laplacian."""
    global th
    global clr
    global edges
    global ldeg
    global lapscaled
 
    Threshold(lapframe, lapframe, th, clr, CV_THRESH_BINARY)
    Laplace(lapframe, edges, ldeg)
    Convert(edges, lapframe)
    Resize(lapframe, lapscaled)

    return GetMat(lapscaled)


def print_output(printmat):
    """Print the image as a string of ASCII characters"""
    printed = ''
    for y in range(printmat.height):
        printed = printed + ' ' * int((terminalwidth - dw) / 2)
        for x in range(printmat.width):
            printed = printed + asciiGroup[int(-1 + len(
                asciiGroup) - ((printmat[y, x] * len(asciiGroup)) // 256))]
        printed = printed + '\n' * (y != (printmat.height - 1))

    os.system('clear')
    print(printed)


def run(gradient, laplacian):
    """Capture and process feed from webcam"""
    initialize()

    while True:
        rawframe = capture_frame()

        if gradient and laplacian:
            printed = hybrid_process(rawframe)
        elif gradient:
            printed = gradient_process(rawframe)
        elif laplacian:
            printed = laplacian_process(rawframe)
        else:
            return

        print_output(printed)
        WaitKey(1)


def initialize():
    """Initialize settings and images"""
    global wc
    global asciiGroup
    global fm
    global th
    global clr
    global ldeg
    global quadwidth
    global dqw
    global terminalwidth
    global dw
    global scaledsize
    global inputframe
    global gradscaled
    global edges
    global lapscaled
    global gradscaled
    global summation


    # Settings for frame capture
    wc = CaptureFromCAM(0)
    asciiGroup = "####**oahbpqwmzcunxrt-+~<>:,^`...     "
    windowsize = GetSize(QueryFrame(wc))
    hght = windowsize[1]
    wdth = windowsize[0]
    flipMode = 1
    fm = flipMode

    # Settings for Threshold()
    threshold = 100
    th = threshold
    color = 255
    clr = color

    # Setting for Laplace()
    laplaceDegree = 7
    ldeg = laplaceDegree

    # Settings for sizing (for fullscreened terminal on 1600x900 screen)
    terminalwidth = 304
    desiredwidth = 222
    dw = desiredwidth
    scaledsize = (dw, int(dw / 2 * hght // wdth))

    # Initialize OpenCV images
    inputframe = CreateImage(windowsize, 8, 1)
    edges = CreateImage(windowsize, IPL_DEPTH_16S, 1)
    hybscaled = CreateImage(scaledsize, 8, 1)
    gradscaled = CreateImage(scaledsize, 8, 1)
    lapscaled = CreateImage(scaledsize, 8, 1)
    summation = CreateMat(scaledsize[1], scaledsize[0], CV_8UC1)

if __name__ == '__main__':
    run(gradient=True, laplacian=True)
