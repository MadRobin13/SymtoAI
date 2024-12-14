# SymptoAI

SymptoAI is an AI-driven application designed to assist in medical diagnostics using speech and video processing. This project combines a deep learning model with a web-based frontend and REST API for efficient image-based diagnostic inference.

---

## Features

1. **AI-Powered Detection**
   - Uses a YOLO-based machine learning model to detect "malignant" objects in medical images.
   - Provides a classification result (malignant/not malignant).

2. **Web Frontend**
   - Allows users to upload and display Markdown files.
   - Simple, user-friendly interface for managing content.

3. **Backend API**
   - Flask-based REST API for processing and classifying uploaded images.
   - Secure file handling and inference.

4. **Client Integration**
   - Python script (`send.py`) for easy integration and testing of the API.

---

## Prerequisites
- Python 3.8 or higher
- `Flask`
- `ultralytics`
- `requests`

---

## Project Architecture

- **Frontend**: Displays content and manages file uploads.
- **Backend**: Provides REST API endpoints for inference.
- **Model**: YOLO model for detecting "malignant" objects.
- **Client**: A Python script to test API interactions.

---

## Future Enhancements

- Enhance the model to classify a wider range of medical conditions.
- Integrate a database for storing results and user data.


