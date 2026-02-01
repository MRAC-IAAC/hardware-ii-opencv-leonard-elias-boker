## Hardware II – Object Detection Assignment

This repository contains my submission for the **Hardware II** course assignment.

The project focuses on training and evaluating an object detection model using **computer vision techniques**.  
A single object class (**cup**) was selected to keep the scope focused and to allow a clear evaluation of the full workflow.

### Workflow Overview
- Selection of an object class (cup)
- Dataset preparation and annotation using **Roboflow**
- Dataset versioning, preprocessing, and augmentation
- Training of an object detection model (YOLO-based)
- Evaluation using standard metrics (mAP, precision, recall)

### Tools & Technologies
- Roboflow (dataset management, training, evaluation)
- YOLO-based object detection model
- Python / OpenCV (contextual relation to course content)
- GitHub for documentation and submission

### Dataset
- Total images: 375  
- Train / Validation / Test split: 80% / 13% / 7%
- Preprocessing: auto-orient, resize to 256×256
- Augmentation: horizontal flip

### Notes
The repository documents the complete process from dataset preparation to model training and evaluation.  
All files and links included here represent the final state of the assignment submission.

---

**Student:** Leonard Elias Böker  
**Course:** Hardware II  
**Institution:** IAAC


### HARDWARE-II - Open CV

## Link Miro Board
https://miro.com/app/board/uXjVGLZ_DpM=/

## Chat Hpt Link
https://chatgpt.com/share/69765339-e290-800f-979d-8a61548d622a

## System Disription

This project explores a vision-based robotic interaction system usng two camera inputs, computer vision, and ROS to control a UR10 robotic arm.
One camera observes the workspace from above and uses OpenCV with ArUco markers to detect and localize objects (cubes) and predefined target positions within a calibrated coordinate system.
A second camera captures human hand gestures, which are interpreted using MediaPipe to extract user intent, such as selecting an object or defining a target position.

Both vision streams are processed independently and communicated through ROS nodes, allowing modular data exchange between perception, decision-making, and robot control.
Based on the detected workspace state and the interpreted gesture input, a task planner generates a pick-and-place command for the robot.
The UR10 robot then executes the movement, autonomously picking up a cube from its current location and placing it at the specified target position.

## System Architektur
<img width="2960" height="926" alt="Screenshot 2026-01-25 183243" src="https://github.com/user-attachments/assets/b0ac6556-8a4e-41d3-bba3-1970a53d6516" />
