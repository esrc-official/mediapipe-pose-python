# MediaPipe Pose for Python

[![Platform](https://img.shields.io/badge/platform-desktop-orange.svg)](https://github.com/esrc-official/mediapipe-pose-python)
[![Languages](https://img.shields.io/badge/language-python-orange.svg)](https://github.com/esrc-official/mediapipe-pose-python)
[![Apache License](https://img.shields.io/badge/license-Apache-brightgreen.svg)](https://github.com/esrc-official/mediapipe-pose-python/blob/master/LICENSE.md)

<br />

## Introduction
This project is to estimate skeletons and to analyze angles from the videos using MediaPipe Pose solution.

<br />

## Requirements
The requirements for this project are:
- Python 3.9.0
- Mediapipe >=0.8.11

<br />

## Installation

### Step 1: Clone this repository and move directory
You can **clone** the project from the [repository](https://github.com/esrc-official/mediapipe-pose-python).

```
// Clone this repository
git clone git@github.com:esrc-official/mediapipe-pose-python.git

// Move to the sample
cd mediapipe-pose-python

// Install third-party libraries (default)
pip install -r requirements.txt
// Install third-party libraries (macos m1)
pip install -r requirements_m1.txt
```

### Step 2: Install third-party libraries
Please install third-party libraries using [requirements.txt](https://github.com/esrc-official/mediapipe-pose-python/blob/master/requirements.txt).
If your environment is macos m1, you can use [requirements_m1.txt](https://github.com/esrc-official/mediapipe-pose-python/blob/master/requirements_m1.txt).

```
// Install third-party libraries (default)
pip install -r requirements.txt

// Install third-party libraries (macos m1)
pip install -r requirements_m1.txt
```

### Step 3: Set configs for yours custom
You should change the project directory on `configs/customized_basic_mediapipe_pose_test.yaml`.


![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/config_example.png)

### Step 4: Copy dataset
Please copy dataset on `dataset/pose/videos`.
If you change the directory or video extension, please set `configs/dataset_module/pose_custom_dataset.yaml`.

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/dataset_directory.png)

<br />

## Run project
You can run project by executing python or script.

```
// Use python directly
python main.py

// Use script
source scripts/main.sh
```

Then, the results are saved on `logs/${now:%Y-%m-%d}/${now:%H-%M-%S}`.

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/result_example.png)

<br />

## Package structure

project tree

├─configs  
│  ├─architecture_module
│  ├─dataset_module  
│  ├─hydra  
│  ├─logger
├─datasets
│  ├─pose
├─logs  
├─scripts
└─src  
    ├─architecture_modules  
    │  └─models  
    ├─dataset_modules  
    │  └─datasets  
    ├─engine  
    └─utils  