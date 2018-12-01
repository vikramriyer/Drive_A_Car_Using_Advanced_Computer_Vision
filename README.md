## Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

In this project, our goal is to write a software pipeline to identify the lane boundaries in a video like shown below in the gif.

![](project_video_lane.gif)

## Administrative Stuff
- All the code for the pipeline is present in [P2.ipynb](P2.ipynb) file. If you prefer watching on the browser, I suggest checking the html [(P2.html)](P2.html) version of the same notebook.
- The project video is named [project_video_output.mp4](https://youtu.be/izcRpUbAXnk).


Steps in the Pipeline
---

- Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
- Apply a distortion correction to raw images.
- Use color transforms to create a thresholded binary image.
- Apply a perspective transform to rectify binary image ("birds-eye view").
- Detect lane pixels and fit to find the lane boundary.
- Determine the curvature of the lane and vehicle position with respect to center.
- Warp the detected lane boundaries back onto the original image.
- Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

Let's look at each of the points mentioned above in detail and how we got to display lane lines on the project video.

## Camera Calibration

We begin by calibrating the camera. The cameras that we use tend to generate some sort of distortions to the original images depending on a lot of factors thus deforming the shapes. However, the deformity caused can be eliminated by performing some operations with the help of constants which are a matrix and some coefficients.

It turns out that the deformities are constant and hence the above method works well.

![](rubric_images/calibration2.jpg)
![](rubric_images/calibration3.jpg)

## Color Spaces and Gradients

**HLS**
![](rubric_images/HLS.png)

**LUV**
![](rubric_images/LUV.png)

**HSV**
![](rubric_images/HSV.png)

## Undistortion
![](rubric_images/distorted_undistorted_train.png)
![](rubric_images/distorted_undistorted_valid.png)

## Perspective Transform
![](rubric_images/perspective_transform.png)

## Fit lines sliding window algo
![](rubric_images/plot_line_window1.png)
![](rubric_images/plot_line_window2.png)

## Drawing Lane Lines
![](rubric_images/lane_drawn_roc_offset_straight_lines2.jpg)
