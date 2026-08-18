# SewerVision AI
### AI-Powered Sewer CCTV Inspection & Unauthorized Pipe Detection

> A deep learning and computer vision system for detecting pipe connections in sewer CCTV imagery and supporting automated infrastructure inspection.

---

## 🚀 Overview

**SewerVision AI** is a computer vision project designed to assist in the inspection of sewer infrastructure using deep learning-based object detection.

The system analyzes sewer CCTV imagery and identifies relevant pipe structures that may require further inspection. By applying automated image analysis, the project aims to reduce the effort involved in manually reviewing large volumes of sewer inspection imagery.

The project combines:

- Deep Learning
- YOLO-based Object Detection
- Computer Vision
- OpenCV
- Python
- Roboflow dataset preparation
- Image and video inference

The system was developed as part of research into the automated detection of unauthorized wastewater pipe connections in sewer systems.

---

## 🎯 Problem Statement

Sewer infrastructure is commonly inspected using CCTV cameras. Inspectors must manually examine captured images or video to identify pipe connections and other structural abnormalities.

This process can be:

- Time-consuming
- Repetitive
- Dependent on manual visual inspection
- Difficult under poor image-quality conditions
- Challenging when large amounts of CCTV footage are generated

SewerVision AI explores an automated computer vision approach to assist inspectors by identifying relevant pipe structures within sewer CCTV imagery.

---

## 💡 Proposed Solution

The project uses a deep learning-based object detection pipeline to analyze sewer CCTV images.

### Processing Pipeline

Sewer CCTV Images
        ↓
Dataset Preparation
        ↓
Image Preprocessing
        ↓
Object Annotation
        ↓
YOLO Model
        ↓
Model Training
        ↓
Prediction
        ↓
Confidence Filtering
        ↓
Detection Visualization

The system can process both individual images and video input through dedicated Python inference scripts.

---

## 🧠 AI / Computer Vision Approach

The project uses a YOLO-based object detection approach.

Instead of simply classifying an entire image, object detection allows the system to identify the location of relevant structures using bounding boxes.

A typical prediction contains:

- Detected object
- Bounding box coordinates
- Confidence score

This makes the output more useful for visual inspection because the detected region can be directly highlighted in the CCTV frame.

---

## 📊 Dataset

The project uses the **Sewer CCTV** dataset exported from Roboflow.

### Dataset Information

| Property | Details |
|---|---|
| Dataset | Sewer CCTV |
| Images | 2,000 |
| Image Size | 640 × 640 |
| Dataset Platform | Roboflow |
| Annotation Format | Folder-based dataset |
| Augmentation | None |
| Preprocessing | Auto-orientation + resize |

The dataset metadata states that the images were exported from Roboflow on **June 20, 2024**. 

The dataset is organized into training, validation and testing data.

```text
dataset/
├── train/
├── valid/
└── test/
SewerVision-AI/
│
├── train/
│   └── Training dataset
│
├── valid/
│   └── Validation dataset
│
├── test/
│   └── Testing dataset
│
├── check.py
│   └── Dataset / image checking utilities
│
├── interface2.py
│   └── Application interface
│
├── predict_pipesimage.py
│   └── Image-based pipe detection
│
├── pedict_pipesvideo.py
│   └── Video-based pipe detection
│
├── pipe.yaml
│   └── Dataset configuration
│
├── Requirements.txt
│   └── Python dependencies
│
├── .env.example
│   └── Example environment configuration
│
└── README.md
