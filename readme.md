# Garbage Detection System using YOLOv8

A Python-based object detection system that uses YOLOv11s to identify and classify garbage in images and videos. This is an experimental project designed for learning and testing computer vision techniques.

## Features

- Real-time garbage detection using YOLOv8 architecture
- Support for multiple input sources (images, videos, folders, USB camera, Raspberry Pi camera)
- Adjustable confidence threshold for detections
- Custom resolution settings for display and recording
- Video recording capability for live detection sessions
- FPS monitoring for performance tracking
- Bounding box visualization with class labels and confidence scores

## Project Structure

```
moonshoot/
├── calling.py              # Main detection script
├── best.pt                 # Trained YOLOv8 model weights (not included)
├── readme.md               # Project documentation
└── env/                    # Virtual environment (excluded from repo)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Required Dependencies

Install all required packages using pip:

```powershell
pip install ultralytics opencv-python numpy
```

For Raspberry Pi camera support (optional):

```powershell
pip install picamera2
```

### Quick Setup

```powershell
# Clone the repository
git clone https://github.com/aarvo09/garbage-detector-py.git
cd garbage-detector-py

# Create virtual environment (recommended)
python -m venv env
.\env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac

# Install dependencies
pip install ultralytics opencv-python numpy

# Add your trained model file (best.pt) to the project directory

# Run detection
python calling.py --model best.pt --source <your_image_or_video>
```

## Usage

### Basic Command

```powershell
python calling.py --model <path_to_model> --source <path_to_source>
```

### Examples

**Single Image Detection:**
```powershell
python calling.py --model best.pt --source test.jpg
```

**Folder of Images:**
```powershell
python calling.py --model best.pt --source ./test_images/
```

**Video File:**
```powershell
python calling.py --model best.pt --source video.mp4
```

**USB Camera (Live Detection):**
```powershell
python calling.py --model best.pt --source usb0
```

**With Custom Threshold and Resolution:**
```powershell
python calling.py --model best.pt --source video.mp4 --thresh 0.6 --resolution 640x480
```

**Recording Video Output:**
```powershell
python calling.py --model best.pt --source usb0 --resolution 1280x720 --record
```

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--model` | Yes | - | Path to the trained YOLOv11s model file (.pt) |
| `--source` | Yes | - | Input source: image file, video file, folder path, or "usb0" for camera |
| `--thresh` | No | 0.5 | Confidence threshold for detections (0.0 to 1.0) |
| `--resolution` | No | None | Display resolution as WIDTHxHEIGHT (e.g., 640x480, 1280x720) |
| `--record` | No | False | Enable video recording (requires --resolution, only works with video/USB sources) |

### Supported File Formats

- **Images:** .jpg, .jpeg, .png, .bmp (case-insensitive)
- **Videos:** .avi, .mov, .mp4, .mkv, .wmv

### Controls

- Press **'q'** to quit the detection window during video/camera processing

## Known Limitations

This is an early-stage experimental project only for learning  with several known issues:

- **Low Model Accuracy:** The current model has limited detection accuracy and may produce false positives/negatives
- **Small Dataset:** Training was performed on a small, imbalanced dataset
- **Poor Generalization:** Model may not perform well on diverse or real-world scenarios
- **Data Quality Issues:** Insufficient data preprocessing and augmentation
- **Not Production-Ready:** This system is NOT suitable for real-world deployment or commercial use

## Project Status

 **EXPERIMENTAL PROJECT - FOR LEARNING PURPOSES ONLY**

This project is in early development and serves as a learning exercise in computer vision and object detection. The current implementation has significant limitations and should be used only for educational and experimental purposes.

**This project is not actively maintained and no future improvements are planned.**

**Not recommended for:**
- Production environments
- Critical applications
- Real-world garbage management systems
- Commercial deployment

## License

This project is open-source and available for educational purposes.

## Acknowledgments

- YOLOv11s by Ultralytics
- OpenCV community
- Python computer vision ecosystem
