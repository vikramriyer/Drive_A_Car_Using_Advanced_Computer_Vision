import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2, glob, math

# 1. One time calibration process
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# Make a list of calibration images
images = glob.glob('camera_cal/calibration*.jpg')
cols = 2
rows = math.ceil(len(images)/cols)

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6), None)

    # If found, add object points, image points
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (9,6), corners, ret)
        plt.figure(figsize=(15,9))
        plt.imshow(img)
        cv2.waitKey(500)
cv2.destroyAllWindows()

img = cv2.cvtColor(cv2.imread("camera_cal/calibration1.jpg"), cv2.COLOR_BGR2RGB)
img_size = (img.shape[1], img.shape[0])
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

def undistort_image(img, mtx, dist):

    dist = cv2.undistort(img, mtx, dist, None, mtx)
    return dist

# Nothing uptil here needs change

def warp(img):

    src = np.float32([[(180,720), (560,460), (740,460), (1200,720)]])
    dest = np.float32([[(100,720), (0,0), (1300,0), (1200,720)]])
    M = cv2.getPerspectiveTransform(src, dest)
    MInv = cv2.getPerspectiveTransform(dest, src)
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    return warped, MInv

def binarize(b, thresh=(210, 255)):

    binary = np.zeros_like(b)
    binary[(b >= thresh[0]) & (b <= thresh[1])] = 1
    return binary

def combine_thresholds(binary_1, binary_2):

    combined_binary = np.zeros_like(binary_1)
    combined_binary[(binary_1 == 1) | (binary_2 == 1)] = 1
    return combined_binary

def threshold_image(img, s_thresh, v_thresh):

    s = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)[:,:,2]
    v = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]
    s_b = binarize(s, s_thresh)
    v_b = binarize(v, v_thresh)
    combined = combine_thresholds(s_b, v_b)
    return s_b

def pipeline(img):

    s_thresh, v_thresh = (200,240), (230,255)
    try:
        undist_img = undistort_image(img, mtx, dist)
    except:
        undist_img = img
    warped, MInv = warp(undist_img)
    binary_warped = threshold_image(warped, s_thresh, v_thresh)

    return binary_warped, MInv

class Line:
    pass

def video_pipeline():

    # read the video, prepare a file to write the output video
    cap = cv2.VideoCapture("project_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    # read the frames one by one and call the image pipeline to get the binary warped image
    while True:

        # read the current frame and convert to RGB
        _, frame = cap.read()

        # do the processing
        binary_warped, MInv = pipeline(frame)

        # draw the lines and polygon

        # stack the warped image together so can be combined with original frame
        # out_img = np.dstack((warped, warped, warped)) * 255

        # get the unwarped image
        # unwarped = warpPerspective(out_img, MInv, img_size, flags=cv2.INTER_LINEAR)

        # combine the unwarped image to original frame
        # result = cv2.addWeighted(frame, 1, unwarped, 0.3, 0)

        # write to the output video
        # out.write(result)

        # display the video
        cv2.imshow('frame', binary_warped)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

video_pipeline()
