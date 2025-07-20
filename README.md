# Comparative Analysis of YOLOv8 Variants for Object Detection to Assist Visually Impaired Individuals

## 📌 Project Overview
This project presents a comparative evaluation of various YOLOv8 object detection models (`YOLOv8s`, `YOLOv8m`, `YOLOv8l`, and `YOLOv8x`) to aid visually impaired individuals in recognizing real-world objects such as:
- Zebra crossings 🦓
- Traffic signs 🚦
- Vehicles 🚗

The objective is to determine the most suitable YOLOv8 variant for **real-time assistive applications** based on metrics such as **precision**, **recall**, **mAP**.

---

## 🎯 Objectives
- Compare different YOLOv8 models (`s`, `m`, `l`, `x`) on assistive datasets
- Evaluate each variant using:
  - Accuracy
  - Precision & Recall
  - mAP@0.5 and mAP@0.5:0.95
- Select the best model for real-time deployment scenarios

---

## 🧠 Methodology

### 📥 Dataset Collection
- Datasets were collected from open-source platforms for:
  - Zebra crossings
  - Vehicles (cars, buses, bikes, etc.)
  - Traffic signs (Stop, Yield, Traffic Light, etc.)
- Annotated in YOLO format (`class x_center y_center width height`)

### ⚙️ Training Details
- Platform: Google Colab / Local GPU
- Framework: [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- Parameters:
  - Image size: 640x640
  - Optimizer: SGD/Adam
  - Epochs: 50–100
  - Batch Size: 16

### 📈 Evaluation Metrics
- **Precision**
- **Recall**
- **mAP@0.5**
- **mAP@0.5:0.95**
- **Inference Time** (measured per image)

---

## 📊 Results

| Model     | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | Inference Time |
|-----------|-----------|--------|---------|--------------|----------------|
| YOLOv8s   | xx%       | xx%    | xx%     | xx%          | ✅ Fastest     |
| YOLOv8m   | ✅ Best   | ✅     | ✅      | ✅           | ⚖️ Balanced    |
| YOLOv8l   | High      | High   | High    | High         | Slower         |
| YOLOv8x   | Slightly Better | ✅ Highest | ✅ Highest | ✅ Highest   | 🐢 Slowest     |

*(Replace xx% with actual results)*

---

## 📷 Visual Results
> Sample outputs with bounding boxes from each model are available in the `runs/detect/` folder and inside the report.

---

## 🤖 Flask API
The project includes a **Flask-based backend API** (`app.py`) to:
- Accept uploaded images via POST
- Run predictions using all 3 trained YOLO models
- Return JSON output with bounding boxes and labels

### ▶️ Run the server:
```bash
pip install -r requirements.txt
python app.py
