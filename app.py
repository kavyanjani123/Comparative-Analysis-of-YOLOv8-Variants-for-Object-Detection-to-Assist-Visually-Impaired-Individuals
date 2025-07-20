from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import numpy as np
import traceback

# Load your trained YOLO models
zebra_model = YOLO('models/zebracrossing_model.pt')  # Zebra Crossing model
traffic_sign_model = YOLO('models/trafficsign_model.pt')  # Traffic Sign model
vehicle_model = YOLO('models/vehicle_model.pt')  # Vehicle model

app = Flask(__name__)  # Correct initialization
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        image_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        # Ensure the image is loaded
        if img is None:
            return jsonify({'error': 'Failed to load image. Please try again.'})

        # First, perform prediction on Zebra Crossing model
        zebra_results = zebra_model(img)
        zebra_predictions = zebra_results[0].boxes  # Get predictions from Zebra Crossing model

        # Process Zebra Crossing predictions
        zebra_labels = zebra_predictions.cls.tolist()  # Class indices
        zebra_confidences = zebra_predictions.conf.tolist()  # Confidence scores
        zebra_bboxes = zebra_predictions.xyxy.tolist()  # Bounding box coordinates [x1, y1, x2, y2]

        # Second, perform prediction on Traffic Sign model
        traffic_sign_results = traffic_sign_model(img)
        traffic_sign_predictions = traffic_sign_results[0].boxes  # Get predictions from Traffic Sign model

        # Process Traffic Sign predictions
        traffic_sign_labels = traffic_sign_predictions.cls.tolist()  # Class indices
        traffic_sign_confidences = traffic_sign_predictions.conf.tolist()  # Confidence scores
        traffic_sign_bboxes = traffic_sign_predictions.xyxy.tolist()  # Bounding box coordinates [x1, y1, x2, y2]

        # Third, perform prediction on Vehicle model
        vehicle_results = vehicle_model(img)
        vehicle_predictions = vehicle_results[0].boxes  # Get predictions from Vehicle model

        # Process Vehicle predictions
        vehicle_labels = vehicle_predictions.cls.tolist()  # Class indices
        vehicle_confidences = vehicle_predictions.conf.tolist()  # Confidence scores
        vehicle_bboxes = vehicle_predictions.xyxy.tolist()  # Bounding box coordinates [x1, y1, x2, y2]

        # Define separate label mappings for each model
        zebra_label_map = {0: 'Zebra Crossing'}
        traffic_sign_label_map = {0: 'Stop Sign', 1: 'Yield Sign', 2: 'Speed Limit Sign', 3: 'Traffic Light'}
        vehicle_label_map = {0: 'Car', 1: 'Bus', 2: 'Truck', 3: 'Bicycle'}

        # Combine results from all three models
        all_predictions = []

        # Process Zebra Crossing predictions
        all_predictions.extend([
            {
                'label': zebra_label_map.get(int(label), 'Unknown'),
                'confidence': confidence,
                'bbox': bbox
            }
            for label, confidence, bbox in zip(zebra_labels, zebra_confidences, zebra_bboxes)
        ])

        # Process Traffic Sign predictions
        all_predictions.extend([
            {
                'label': traffic_sign_label_map.get(int(label), 'Unknown'),
                'confidence': confidence,
                'bbox': bbox
            }
            for label, confidence, bbox in zip(traffic_sign_labels, traffic_sign_confidences, traffic_sign_bboxes)
        ])

        # Process Vehicle predictions
        all_predictions.extend([
            {
                'label': vehicle_label_map.get(int(label), 'Unknown'),
                'confidence': confidence,
                'bbox': bbox
            }
            for label, confidence, bbox in zip(vehicle_labels, vehicle_confidences, vehicle_bboxes)
        ])

        return jsonify(all_predictions)  # Return all predictions as a JSON response

    except Exception as e:
        # Log the error and stack trace for better debugging
        print("Error during prediction:", str(e))
        traceback.print_exc()  # Prints detailed stack trace in the console
        return jsonify({'error': 'An error occurred during prediction. Please try again.'})

if __name__ == "__main__":  # Correct initialization
    app.run(host="0.0.0.0", port=5000)
