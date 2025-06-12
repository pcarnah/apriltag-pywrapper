# apriltag-pywrapper
Pip installable python wrapping using the python wrapping provided by the original AprilTag library.

AprilTag 3
==========
AprilTag is a visual fiducial system popular in robotics research. This repository contains the most recent version of AprilTag, AprilTag 3, which includes a faster (>2x) detector, improved detection rate on small tags, flexible tag layouts, and pose estimation. AprilTag consists of a small C library with minimal dependencies.

Papers
======
AprilTag is the subject of the following papers.

[AprilTag: A robust and flexible visual fiducial system](https://april.eecs.umich.edu/papers/details.php?name=olson2011tags)

[AprilTag 2: Efficient and robust fiducial detection](https://april.eecs.umich.edu/papers/details.php?name=wang2016iros)

[Flexible Layouts for Fiducial Tags](https://april.eecs.umich.edu/papers/details.php?name=krogius2019iros)

Install
=======

Tested on Windows and Linux

To install directly from GitHub:
```
pip install git+https://github.com/pcarnah/apriltag-pywrapper.git
```

Usage
=====

## Choosing a Tag Family
For the vast majority of applications, the tagStandard41h12 family will be the correct choice. You can find the images for the tags in the [apriltag-imgs repo](https://github.com/AprilRobotics/apriltag-imgs). Scale up the images in your favorite editor and print them out.

Some heuristics for when to choose other tag families:
1. If you need more tags, use tagStandard52h13
2. If you need to maximize the use of space on a small circular object, use tagCircle49h12 (or tagCircle21h7).
3. If you want to make a recursive tag use tagCustom48h12.
4. If you want compatibility with the ArUcO detector use tag36h11

If none of these fit your needs, generate your own custom tag family [here](https://github.com/AprilRobotics/apriltag-generation).

## Getting Started with the Detector
### Python

    import cv2
    import numpy as np
    from apriltag import AprilTagDetector

    imagepath = 'test.jpg'
    image = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
    detector = AprilTagDetector(family='tagStandard52h13',
                               threads=4,
                               decimate=1.0,
                               blur=0.25,
                               sharpen=0.25)

    detections = detector.detect(image)


Each detection is returned as a dictionary:

```
{
  'hamming': 0,
  'margin': 26.071725845336914,
  'id': 0,
  'center': array([542.78599907, 418.26722263]),
  'lb-rb-rt-lt': array([[530.70965576, 443.665802  ],
         [564.809021  , 431.85003662],
         [554.27758789, 394.09848022],
         [520.16308594, 404.31442261]])
}
```

## Tuning the Detector Parameters
Explanation of available options:
The constructor takes a number of arguments:

- family: a string for the tag type we're detecting. This argument is required.
  If an invalid string is given, the known list of tag families will be
  reported. At the time of this writing the known families are:

  - "tag36h11"
  - "tag25h9"
  - "tag16h5"
  - "tagCircle21h7"
  - "tagCircle49h12"
  - "tagStandard41h12"
  - "tagStandard52h13"
  - "tagCustom48h12"

All the other arguments are optional:

- threads: how many threads the detector should use. Default is 1

- maxhamming: max number of corrected bits. Larger values guzzle RAM. Default is
  1

- decimate: detection of quads can be done on a lower-resolution image,
  improving speed at a cost of pose accuracy and a slight decrease in detection
  rate. Decoding the binary payload is still done at full resolution. Default is 1.0

- blur: What Gaussian blur should be applied to the segmented image (used for
  quad detection?) Parameter is the standard deviation in pixels. Very noisy
  images benefit from non-zero values (e.g. 0.8). Default is 0.0
  
- sharpen: How much sharpening should be done to decoded images. This can help
  decode small tags but may or may not help in odd lighting conditions or
  low light conditions. Default is 0.25.

- refine_edges: When non-zero, the edges of the each quad are adjusted to "snap
  to" strong gradients nearby. This is useful when decimation is employed, as it
  can increase the quality of the initial quad estimate substantially. Generally
  recommended to be on. Very computationally inexpensive. Option is ignored if
  decimate == 1. Default is True

- debug: When non-zero, write a variety of debugging images to the current
  working directory at various stages through the detection process. (Somewhat
  slow). Default is False

The detect() method takes a single argument: an image array

### Increasing speed.
Increasing the quad_decimate parameter will increase the speed of the detector at the cost of detection distance.  If you have extra cpu cores to throw at the problem then you can increase nthreads. If your image is somewhat noisy, increasing the quad_sigma parameter can increase speed.

### Increasing detection distance.
First choose an example image and run the detector with debug=1 to generate the debug images. These show the detector's output at each step in the detection pipeline.
If the border of your tag is not being detected as a quadrilateral, decrease quad_decimate (all the way to 1 if necessary).
If the border of the tag is detected then experiment with changing decode_sharpening.

## Pose Estimation.
This wrapper does not contain ApirlTag's PoseEstimator. Pose estimation can be done using OpenCV via the PnP solver. The detector follows the ApirlTag convention of reporting 
