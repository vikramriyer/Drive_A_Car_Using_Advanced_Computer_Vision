import pathlib, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

dir = pathlib.Path.cwd()
path = str(dir) + '/../camera_cal/'
for file in os.listdir(path):
    # Steps
    ## load image
    image = mpimg.imread(path + file)

    ## init
    objpoints = [] # 3D points in real world space
    imgpoints = [] # 2D points in img plane

    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

    ## convert to grayscale, cvt.BGR2GRAY (cv2.imread or glob) or cvt.RGB2GRAY (mpimg.imread)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ## find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (8,6), None)

    # if corners found
    if ret:
        imgpoints.append(corners)
        objpoints.append(objp)

        ## draw detected corners or an image
        image = cv2.drawChessboardCorners(image, (8,6), corners, ret)

        ## calibrate camera
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None)

        ## Undistort the image
        dst = cv2.undistort(img, mtx, dist, None, mtx)

'''
References to pathlib
https://realpython.com/python-pathlib/

'''
