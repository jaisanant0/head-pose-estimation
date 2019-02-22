# Head-pose-estimation

It estimates the positon of head in real time using Dlib and OpenCV.

## Getting Started
Clone the repository and run head_pose.py

## Usage 
```
python3 head_pose.py
```

- It saves the output in current directory

## Assumptions

In computer vision, the pose of an object refers to its orientation and position with respect to a camera.

To calculate the 3D pose of an object in an image you need the following information :

1. **2D coordinates of a few points** : We need the 2D (x,y) coordinates of a few points in the image. In my case, I have choosen the corners of the eyes, the tip of the nose, corners of the mouth etc. with Dlib’s facial landmark detector.

2. **3D locations of the same points** : We also need the 3D location of the 2D feature points. A generic 3D model will be sufficient. We don’t need a full 3D model, just need the 3D locations of a few points in some arbitrary reference frame. I use the following points 
	a. Tip of the nose : ( 0.0, 0.0, 0.0)
	b. Chin : ( 0.0, -330.0, -65.0)
	c. Left corner of the left eye : (225.0, 170.0, -135.0)
	d. Right corner of the right eye : (-225.0, 170.0, -135.0)
	e. Left corner of the mouth : (150.0, -150.0, -125.0)
	f. Right corner of the mouth : (-150.0, -150.0, -125.0)

3. **Intrinsic parameters of the camera** : The camera is assumed to be calibrated. In other words, you need to know the focal length of the camera, the optical center in the image and the radial distortion parameters. So you need to [calibrate your camera](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html) or we can approximate the optical center by the center of the image, approximate the focal length by the width of the image in pixels and assume that radial distortion does not exist.

NOTE :
	I have used logitech c270 and hence provided the calibration coefficients.

