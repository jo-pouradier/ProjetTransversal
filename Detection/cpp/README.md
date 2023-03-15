# First install opencv and opencv_contrib on your system (build from source or use brew)

## Find your opencv folder with lib and include folders

command to build:
```
g++ fromChatGpt.cpp -o detection.o -I/usr/local/Cellar/opencv/4.7.0_2/include/opencv4 -L/usr/local/Cellar/opencv/4.7.0_2/lib -std=c++17 -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect  -lopencv_flann
```
-lopencv_contrib
-lopencv_legacy