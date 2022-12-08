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

### Step 3: Set configs for your custom
You should change the project directory on `configs/customized_basic_mediapipe_pose_test.yaml`.

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/config_example.png)

### Step 4: Copy dataset
Please copy dataset on `dataset/pose/videos`.
If you change the directory or video extension, please set `configs/dataset_module/pose_custom_dataset.yaml`.

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/dataset_directory.png)

### (Optional) Step 5: Set configs for your custom dataset
You can change configs on `configs/dataset_module/pose_custom_dataset.yaml` for your custom dataset.
For example, you can set the value of `flip_x` to `True` if you want to flip the image vertically. 

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/dataset_module_configs.png)

### (Optional) Step 6: Set configs for your custom model
You can change configs on `configs/architecture_module/mp_pose_archimodule.yaml` for your custom model.
For example, you can set the value of `relative_coordinate` to `False` if you want to extract the landmarks on absolute coordinates.
<b>Note that only 2d landmarks can be extracted in the absolute coordinates, whereas 3d landmarks can be extracted in the relative coordinates.</b>

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/dataset_module_configs.png)


<br />

## Run project
You can run project by executing python or script.

```
// Use python directly
python main.py

// Use script
source scripts/main.sh
```

Then, the results are saved on `logs/`.

![img](https://github.com/esrc-official/mediapipe-pose-python/blob/master/assets/log_example.png)

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
├─src  
    ├─architecture_modules   
    │  └─models   
    ├─dataset_modules    
    │  └─datasets   
    ├─engine   
    └─utils   