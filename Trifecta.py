from __future__ import division
from cv import *
import os


def capture_frame():
    """Capture frame from webcam, convert to grayscale, flip, and smooth."""
    CvtColor(QueryFrame(wc), inputframe, CV_RGB2GRAY)
    Flip(inputframe, flipMode=fm)
    Smooth(inputframe, inputframe, CV_MEDIAN)

    return inputframe


def hybrid_process(hybframe):
    """Process frame using a gradient-Laplacian hybrid."""
    hybprinted = gradient_process(hybframe)

    Threshold(hybframe, hybframe, th, clr, CV_THRESH_BINARY)
    Laplace(hybframe, edges, ldeg)
    Convert(edges, hybframe)
    Resize(hybframe, scaled)

    pixelnum = 0
    for y in range(scaled.height):
        pixelnum += int((terminalwidth - dw) / 2)
        for x in range(scaled.width):
            pixelnum += 1
            if scaled[y, x] != 0:
                hybprinted = (hybprinted[:pixelnum - 1] + asciiGroup[0] + (
                    hybprinted[pixelnum:] * (pixelnum != len(hybprinted) - 1)))
        pixelnum += 1 * (y != (scaled.height - 1))

    return hybprinted


def gradient_process(gradframe):
    """Process frame using only a gradient."""
    Resize(gradframe, scaled)

    printed = ''
    for y in range(scaled.height):
        printed = printed + ' ' * int((terminalwidth - dw) / 2)
        for x in range(scaled.width):
            printed = printed + asciiGroup[int(-1 + len(
                asciiGroup) - ((scaled[y, x] * len(asciiGroup)) // 256))]
        printed = printed + '\n' * (y != scaled.height - 1)

    return printed


def laplacian_process(lapframe):
    """Process frame using only a Laplacian."""
    Threshold(lapframe, lapframe, th, clr, CV_THRESH_BINARY)
    Laplace(lapframe, edges, ldeg)
    Convert(edges, lapframe)
    Resize(lapframe, scaled)

    printed = ''
    for y in range(scaled.height):
        printed = printed + ' ' * int((terminalwidth - dw) / 2)
        for x in range(scaled.width):
            printed = printed + asciiGroup[int(-1 + len(
                asciiGroup) - ((scaled[y, x] * len(asciiGroup)) // 256))]
        printed = printed + '\n' * (y != scaled.height - 1)

    return printed


def all_process(rawframe):
    """Process frame all three ways."""
    Copy(rawframe, gradframe)
    Copy(rawframe, lapframe)
    Copy(rawframe, hybframe)
    gradientprinted = gradient_process(gradframe).split('\n')
    laplacianprinted = laplacian_process(lapframe).split('\n')
    hybridprinted = hybrid_process(hybframe).split('\n')

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


def run():
    """Capture and process feed from webcam"""
    # while True:
    from time import time
    starttime = time()
    for x in range(100):
        rawframe = capture_frame()

        printed = all_process(rawframe)

        os.system('clear')
        print(printed)
        WaitKey(1)
    print(time() - starttime)


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
    rawframe = CreateImage(windowsize, 8, 1)
    gradframe = CreateImage(windowsize, 8, 1)
    lapframe = CreateImage(windowsize, 8, 1)
    hybframe = CreateImage(windowsize, 8, 1)
    edges = CreateImage(windowsize, IPL_DEPTH_16S, 1)
    scaled = CreateImage(scaledsize, 8, 1)

    run()
