from __future__ import division
from cv import *
import os


def capture_frame():
    """Capture a frame from the webcam, convert to grayscale, flip, and smooth."""
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


def all_process(rawframe):
    """Process frame all three ways."""
    global gradframe
    global lapframe
    global hybframe
    global quadwidth
    global dqw
    global terminalwidth
    global dw

    Copy(rawframe, gradframe)
    Copy(rawframe, lapframe)
    Copy(rawframe, hybframe)
    gradientprinted = print_output(gradient_process(gradframe)).split('\n')
    laplacianprinted = print_output(laplacian_process(lapframe)).split('\n')
    hybridprinted = print_output(hybrid_process(hybframe)).split('\n')

    printed = ''
    for y in range(len(gradientprinted)):
        gradienttrimmed = gradientprinted[y][(int((
            terminalwidth - dw) / 2) - int((quadwidth - dqw) / 2)):]
        printed = printed + gradienttrimmed + laplacianprinted[y] + '\n'
    for y in range(len(hybridprinted)):
        printed = printed + ' ' * (int((
            terminalwidth - dqw) / 2) - int((terminalwidth - dw) / 2))
        printed = printed + hybridprinted[
            y] + '\n' * (y != (len(hybridprinted) - 1))

    return printed


def print_output(printmat):
    """Print the image as a string of ASCII characters."""
    global terminalwidth
    global dw
    global asciiGroup

    printed = ''
    for y in range(printmat.height):
        printed = printed + ' ' * int((terminalwidth - dw) / 2)
        for x in range(printmat.width):
            printed = printed + asciiGroup[int(-1 + len(
                asciiGroup) - ((printmat[y, x] * len(asciiGroup)) // 256))]
        printed = printed + '\n' * (y != (printmat.height - 1))

    return printed


def run():
    """Capture and process feed from webcam."""
    while True:
        rawframe = capture_frame()

        printed = all_process(rawframe)

        os.system('clear')
        print(printed)
        WaitKey(1)


if __name__ == '__main__':
    # Settings for frame capture
    wc = CaptureFromCAM(0)
    asciiGroup = "#*oahbpqwmzcunxrt-+~<>:,^`. "
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

    # Settings for sizing
    quadwidth = 152
    desiredquadwidth = 110
    dqw = desiredquadwidth
    terminalwidth = 304
    desiredwidth = 222
    dw = desiredwidth
    scaledsize = (dqw, int(dqw / 2 * hght // wdth))

    # Initialize OpenCV images
    inputframe = CreateImage(windowsize, 8, 1)
    gradframe = CreateImage(windowsize, 8, 1)
    lapframe = CreateImage(windowsize, 8, 1)
    hybframe = CreateImage(windowsize, 8, 1)
    edges = CreateImage(windowsize, IPL_DEPTH_16S, 1)
    scaled = CreateImage(scaledsize, 8, 1)
    gradscaled = CreateImage(scaledsize, 8, 1)
    lapscaled = CreateImage(scaledsize, 8, 1)
    summation = CreateMat(scaledsize[1], scaledsize[0], CV_8UC1)


    run()
