# 🚴‍♂️ Ride Your Bike

**A Multimodal Platform for Incentivized Urban Mobility through Gamified Biking**

---

## 📘 Abstract

This interdisciplinary project aims to develop a comprehensive system that incentivizes sustainable mobility through regular bike usage. The platform integrates a mobile application, web-based admin interface, GPS tracking, and AI-driven anti-cheating algorithms to offer a fair, transparent, and engaging user experience. Using gamification principles, real-time monitoring, and image recognition, the system provides tangible rewards for active commuting and fosters community participation. The system is designed to be scalable and integrable into smart city infrastructures, contributing to both environmental sustainability and public health initiatives.

---

## 🎯 Objectives

* **Encourage biking** through a structured reward system
* **Track and validate** user activity with real-time GPS and image recognition
* **Prevent fraudulent behavior** using data-driven anti-cheating mechanisms
* **Promote engagement** through rankings, events, and prizes
* **Generate insights** via personalized analytics and system-wide statistics

---

## 🧠 System Design Overview

The platform is composed of four core components:

### 1. **Mobile Application (React Native)**

* User account login
* Start/stop trip with real-time path tracking
* Display of speed, distance, and duration
* Pre-trip bike verification using image recognition
* Engagement with events and award systems
* Community integration through rankings

### 2. **Web Admin Dashboard (React.js)**

* Admin authentication
* Event creation and participant management
* Award and ranking configuration
* System-level trip monitoring
* User and data oversight

### 3. **Back-End (C#, Flask, PostgreSQL)**

* Secure API-based data exchange
* Centralized user and trip data repository
* Image processing service using pre-trained Mask R-CNN
* GPS path tracking and anti-cheating logic

### 4. **Anti-Cheating Algorithms**

* Speed spike detection using Haversine-based calculations
* Detection of non-biking behavior (e.g., vehicle trips)
* Use of Strava and OSM datasets for validation

---

## 🧪 Core Algorithms

### 📍 GPS Tracking & Validation

* **Input**: Timestamps, Latitude/Longitude, Speed
* **Output**: Trip log with verified metrics
* **Methods**: Haversine formula, time-delta computation
* **Threshold**: Trips exceeding 25 km/h flagged as suspicious

### 🖼️ Image-Based Bicycle Detection

* **Model**: Mask R-CNN (trained on COCO dataset)
* **Deployment**: Flask microservice for pre-trip validation
* **Precision**: 91% | **Recall**: 100% | **F2 Score**: 95%
* **Interface**: Defined bounding window for consistent input

---

## 📱 Mobile App Flow

1. User logs in
2. Verifies bike using camera
3. Starts GPS tracking
4. Monitored every 4 seconds for speed and movement
5. Notifications for inactivity or suspicious behavior
6. Trip ends manually or due to inactivity
7. Trip summary is shown with path map and statistics

---

## 🗂️ Project Structure

```bash
Incentives_bike_usage_Mobile_App/
├── __pycache__/                          # Python cache
├── faster_rcnn_resnet101_coco/          # Pre-trained image recognition model
├── src/
│   ├── app.py                            # App orchestrator
│   ├── Bike_Detector.py                  # Mask R-CNN detection pipeline
│   ├── GPS.py                            # GPS route tracking logic
│   ├── GPS_AC.py                         # Enhanced GPS tracking with anti-cheating
│   └── test.py                           # Validation and unit testing scripts
├── test/                                 # Sample inputs or logs
├── Dockerfile                            # Container configuration
├── .dockerignore                         # Docker exclusions
├── .gitattributes                        # Git metadata
├── .DS_Store                             # MacOS cache (to be ignored)
├── requirement.txt                       # Python dependencies
├── README.md                             # Project documentation
├── Presentation.pdf                      # Project presentation slides
└── Report.pdf                     # Full academic report
└── Web_Short_demo.mp4
└── APP_Short_Demo.mp4
```

---

## ⚙️ Setup & Requirements

**Minimum Requirements**

* Python 3.8+
* TensorFlow, NumPy, OpenCV, Flask
* PostgreSQL server
* React Native / React.js environments
* Docker (optional)

---

## 📊 System Evaluation

| Feature                  | Metric               | Result       |
| ------------------------ | -------------------- | ------------ |
| Image Detection          | F2 Score             | 95%          |
|                          | Precision            | 91%          |
|                          | Recall               | 100%         |
| GPS Accuracy             | Real-time Validation | Verified     |
| Anti-Cheating Evaluation | Vehicle Simulation   | Successful   |
| Usability Testing        | Participant Feedback | 27 responses |

---

## 🔮 Future Improvements

* Integrate **real-time traffic and bike lane data**
* Offer **merchant partnerships** for physical rewards
* Extend compatibility with **wearables and IoT**
* Deploy fully on **cloud platforms (e.g., AWS, Azure)**

---

## 📚 References

This project builds on academic and industrial insights in gamification, GPS systems, mobile application design, and AI-based object detection. Please refer to the Report for full literature review and reference list.

* [Mask R-CNN Paper](https://arxiv.org/abs/1703.06870)
* [COCO Dataset](https://cocodataset.org/)
* [React Native Docs](https://reactnative.dev/)
* [OpenStreetMap API](https://wiki.openstreetmap.org/wiki/API)