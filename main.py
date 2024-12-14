from flask import Flask, request, jsonify
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename

# Initialize the Flask app
app = Flask(__name__)

# Path to your trained model
model = YOLO('best.pt')  # Replace with the path to your trained model

# Set up a folder to save uploaded images
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for uploaded images
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to check if the image contains a malignant object
def is_malignant(image_path):
    results = model(image_path)  # Perform inference
    detected_objects = results[0].boxes  # Get detected objects

    # Check if any detected object is malignant (class_id == 0.0)
    for obj in detected_objects:
        class_id = obj.cls[0].item()  # Get class ID
        if class_id == 0.0:  # Assuming 0.0 corresponds to malignant class
            return True
    return False

# Endpoint for image upload and inference
@app.route('/predict', methods=['POST'])
def predict():
    # Check if the request has a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # If the file has an allowed extension, save it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Check if the image is malignant
        if is_malignant(filepath):
            return jsonify({'result': 'malignant'}), 200
        else:
            return jsonify({'result': 'not malignant'}), 200

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
