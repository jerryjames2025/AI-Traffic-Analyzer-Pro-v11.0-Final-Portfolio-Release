# AI-Traffic-Analyzer-Pro-v11.0-Final-Portfolio-Release

# 🚦 AI Traffic Analyzer Pro

AI Traffic Analyzer Pro is a computer vision and AI-powered traffic video analytics platform.  
It detects and tracks vehicles from uploaded traffic videos, estimates vehicle speed, identifies overspeed violations, generates analytics dashboards, creates violation challans, and provides an AI assistant for querying vehicle data.

---

## 📌 Project Overview

This project is built using:

- OpenCV
- YOLOv8
- ByteTrack
- Streamlit
- Plotly
- ReportLab
- Ollama LLM integration
- Python

The system allows users to upload a traffic video, process it using object detection and tracking, and analyze vehicle movement, speed, violations, and reports through an interactive dashboard.

---

## ✨ Key Features

### 🎥 Video Upload and Processing

- Upload traffic videos directly from the dashboard
- Process videos using YOLOv8
- Track vehicles using ByteTrack
- Generate processed output video
- Show live processing progress

### 🚗 Vehicle Detection and Tracking

- Detect cars, motorcycles, buses, and trucks
- Assign unique vehicle IDs
- Track vehicle movement across frames
- Save best vehicle image
- Store vehicle details in JSON and CSV

### ⚡ Speed Estimation

- Estimate vehicle speed using pixel movement
- Track current speed, average speed, and maximum speed
- Maintain speed history for each vehicle

### 🚨 Violation Detection

- Detect overspeed vehicles
- Store violation image evidence
- Estimate fine amount
- Provide penalty category
- Suggest license/legal action
- Generate downloadable violation challan PDF

### 🔢 Number Plate Ready System

- Number plate detection-ready structure
- Plate image field
- Plate confidence field
- Plate-aware dashboard and AI assistant
- Future support for EasyOCR/Tesseract OCR

### 📊 Analytics Dashboard

- Vehicle count summary
- Vehicle type distribution
- Speed distribution
- Average speed by vehicle type
- Detection confidence analysis
- Fastest vehicle table
- Overspeed vehicle table

### 🤖 AI Assistant

The AI assistant can answer questions such as:

- Show overspeed vehicles
- Show fastest vehicles
- Show trucks
- Show cars
- Show vehicles with number plates
- Show vehicles without number plates
- Show vehicle 5
- Give session summary

### 📄 Reports

- AI traffic report
- Markdown report download
- PDF report download
- Vehicle PDF report
- Violation challan PDF

---

## 🗂 Project Structure

```text
AI-Traffic-Analyzer/
│
├── app.py
├── config.py
├── tracker.py
├── counter.py
├── analytics.py
├── visualization.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── speed_estimator.py
│   ├── vehicle_manager.py
│   ├── violation_manager.py
│   ├── exporter.py
│   ├── session_manager.py
│   └── number_plate_detector.py
│
├── models/
│   └── vehicle.py
│
├── dashboard/
│   ├── app.py
│   ├── sidebar.py
│   ├── views/
│   │   ├── upload_video.py
│   │   ├── vehicle_gallery.py
│   │   ├── vehicle_details.py
│   │   ├── violations.py
│   │   ├── analytics.py
│   │   ├── reports.py
│   │   ├── ai_assistant.py
│   │   └── settings.py
│   │
│   ├── utils/
│   │   ├── data_loader.py
│   │   ├── session_loader.py
│   │   ├── session_browser.py
│   │   ├── analytics.py
│   │   ├── report_pdf.py
│   │   ├── report_generator.py
│   │   ├── ai_report.py
│   │   └── ollama_client.py
│   │
│   └── components/
│       └── metrics.py
│
├── sessions/
├── uploaded_videos/
└── outputs/

ng to complete
Open Dashboard, Gallery, Violations, Analytics, Reports, or AI Assistant
