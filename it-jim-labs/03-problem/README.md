# Problem 3

To track the object (marker) on the video using two approaches:

1. tracking by detection using ORB features. You need to find homography and use it to draw a plane rectangle on the top of the marker so that it follows the orientation of the marker.
2. tracking using optical flow (Lucas-Kanade). In this case, you initialize the tracker using the ORB features like in the above solution, but after that, you update the positioning between the frames using optical flow. The output is to be drawn in the same way as in approach 1. But it will have different behavior.

**Output:** your code and two videos obtained using those two approaches.

## Project structure

```
03-problem
│   README.md
│   .gitignore
│
└───data (contains input data)
│   │   find_chocolate.mp4
│   │   marker.jpg
│   
└───output (contains an obtained videos)
│   │   01-task-solution.avi
│   │   02-task-solution.avi
│
└───src (contains source code )
│   config.py
│   01-task.py
│   02-task.py
```

## Task 1

+ Output video is in `output/`
+ [link](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/03-problem/output/01-task-solution.mp4)

## Task 2

+ Output video is in `output/`
+ [link](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/03-problem/output/02-task-solution.mp4)
