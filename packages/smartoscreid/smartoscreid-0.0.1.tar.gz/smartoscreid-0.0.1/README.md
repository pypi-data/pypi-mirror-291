# <div align="center">Peoplce Counting Project</div>

## Overview

The People Counting Project is designed to detect and count the number of people entering and exiting a specified area using computer vision techniques. This project can be used in various settings such as retail stores, offices, and events to monitor foot traffic and gather valuable data.

## Features

- **People Detection**: Detects people in a video feed or image using a deep learning model.
- **Bidirectional Counting**: Tracks and counts people entering and exiting a specific area.

- **Estimate person appear time**: Tracks and estimate time per person appear in video

## Installation

### Prerequisites

- Python 3.x (x >= 10)
- pip or pip3
- A GPU (optional but recommended for faster processing)


### Steps

1. **Clone the repository:**

    ```bash
    git clone gitlab_url 
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Download the pre-trained model (if applicable):**
    The model can download from model section



## Usage

```python 
from smartoscreid import PeopleCounting

# Your model path
model_path = 'smartoscreid/model/yolov8m.pt'

pc = PeopleCounting(model_path)

# List video from multiple camera
videos = ["input/Single1.mp4"]

pc.run(videos)
```

Result will generate in output folder

## <div align="center">Models</div>

YOLOv8 [Detect](https://docs.ultralytics.com/tasks/detect), [Track](https://docs.ultralytics.com/modes/track) mode is available for all Detect, Segment and Pose models.

All [Models](https://github.com/ultralytics/ultralytics/tree/main/ultralytics/cfg/models) download automatically from the latest Ultralytics [release](https://github.com/ultralytics/assets/releases) on first use.

<details open><summary>Detection (COCO)</summary>

See [Detection Docs](https://docs.ultralytics.com/tasks/detect/) for usage examples with these models trained on [COCO](https://docs.ultralytics.com/datasets/detect/coco/), which include 80 pre-trained classes.

| Model                                                                                | size<br><sup>(pixels) | mAP<sup>val<br>50-95 | Speed<br><sup>CPU ONNX<br>(ms) | Speed<br><sup>A100 TensorRT<br>(ms) | params<br><sup>(M) | FLOPs<br><sup>(B) |
| ------------------------------------------------------------------------------------ | --------------------- | -------------------- | ------------------------------ | ----------------------------------- | ------------------ | ----------------- |
| [YOLOv8n](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt) | 640                   | 37.3                 | 80.4                           | 0.99                                | 3.2                | 8.7               |
| [YOLOv8s](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s.pt) | 640                   | 44.9                 | 128.4                          | 1.20                                | 11.2               | 28.6              |
| [YOLOv8m](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8m.pt) | 640                   | 50.2                 | 234.7                          | 1.83                                | 25.9               | 78.9              |
| [YOLOv8l](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8l.pt) | 640                   | 52.9                 | 375.2                          | 2.39                                | 43.7               | 165.2             |
| [YOLOv8x](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x.pt) | 640                   | 53.9                 | 479.1                          | 3.53                                | 68.2               | 257.8             |


</details>


## <div align="center">Torchreid</div>
Torchreid is a library for deep-learning person re-identification, written in [PyTorch](https://pytorch.org/) and developed for our ICCV'19 project, [Omni-Scale Feature Learning for Person Re-Identification](https://arxiv.org/abs/1905.00953).

It features:

- Multi-GPU training
- Support both image- and video-reid
- End-to-end training and evaluation
- Incredibly easy preparation of reid datasets
- Multi-dataset training
- Cross-dataset evaluation
- Standard protocol used by most research papers
- Highly extensible (easy to add models, datasets, training methods, etc.)
- Implementations of state-of-the-art deep reid models
- Access to pretrained reid models
- Advanced training techniques
- Visualization tools (tensorboard, ranks, etc.)


Code: https://github.com/KaiyangZhou/deep-person-reid.

Documentation: https://kaiyangzhou.github.io/deep-person-reid/.

How-to instructions: https://kaiyangzhou.github.io/deep-person-reid/user_guide.

Model zoo: https://kaiyangzhou.github.io/deep-person-reid/MODEL_ZOO.

Tech report: https://arxiv.org/abs/1910.10093.

You can find some research projects that are built on top of Torchreid [here](https://github.com/KaiyangZhou/deep-person-reid/tree/master/projects).

## <div align="center">License</div>
This project is licensed under the MIT License - see the LICENSE file for details.