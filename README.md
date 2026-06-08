🛡️ SecureLog
<div align="center">

AI-Powered Intelligent Log Analysis & Threat Detection System

Detect malicious activities, analyze system logs, identify anomalies, and generate security insights using Machine Learning and Artificial Intelligence.
</div>

📌 Overview

SecureLog is an intelligent cybersecurity platform that automatically analyzes system and application logs to identify suspicious activities, malware indicators, security threats, and anomalous behavior.

Traditional log analysis is time-consuming and requires expert knowledge. SecureLog leverages Machine Learning and AI-based classification models to automate threat detection and provide actionable security insights through an intuitive dashboard.

The platform assists:

Security Analysts
SOC Teams
IT Administrators
Organizations
Educational Institutions

in identifying potential threats hidden inside large volumes of log data.


🎯 Problem Statement

Modern systems generate thousands of log entries every day.

Manually reviewing these logs is:

❌ Time-consuming

❌ Error-prone

❌ Expensive

❌ Difficult to scale


SecureLog solves this problem by automatically:

Processing logs

Detecting malicious patterns

Identifying anomalies

Generating threat reports

Providing real-time insights


✨ Key Features
🔍 Log Analysis

Upload log files (.txt, .log)

Automatic preprocessing

Feature extraction

Pattern recognition


🤖 AI-Powered Threat Detection

TF-IDF Vectorization

Linear SVM Classification

Random Forest Classification

Ensemble Learning

Threat Prediction



🚨 Anomaly Detection

Detect:

Suspicious PowerShell commands

Credential dumping attempts

Malware indicators

Unauthorized access attempts

Command injection patterns

Abnormal user activities


📊 Interactive Dashboard

Threat statistics

Detection summaries

Security analytics

Visual reports

Real-time monitoring


👥 User Management

Secure Authentication

Login & Registration

Session Management

Role-Based Access


📑 Report Generation

Generate:

Security Reports

Threat Summaries

Incident Logs

Analysis Reports


🏗️ System Architecture
<img width="4057" height="327" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/f203f5e9-ebb9-4a40-89d4-9ba8a3242cb9" />


⚙️ Installation
1. Clone Repository: 
git clone https://github.com/YOUR_USERNAME/SecureLog.git

cd SecureLog

2. Create Virtual Environment: 
python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Linux / Mac:
source venv/bin/activate

3. Install Dependencies:
pip install -r requirements.txt

5. Train Model:
python train_model.py

7. Run Application:
python app.py

9. Open Browser:
http://127.0.0.1:5000


📈 Dataset

The model is trained on:

Genuine System Logs

Malicious Logs

PowerShell Attack Logs

Credential Dumping Logs

Malware Execution Logs

Security Event Logs


Dataset Categories:

Category	Label

Genuine Logs	0

Malicious Logs	1

🔬 Technologies Used

Technology	Purpose

Python	Backend

Flask	Web Framework

SQLite	Database

Scikit-Learn	Machine Learning

Pandas	Data Processing

NumPy	Numerical Computing

HTML/CSS	Frontend

JavaScript	Interactivity

Chart.js	Data Visualization


📊 Threat Detection Flow
<img width="1700" height="1198" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/fc6cf752-1d91-4133-a727-75070b5ef450" />


⭐ Support

If you found SecureLog useful:

⭐ Star the repository

🍴 Fork the project

🛡️ Contribute to improving cybersecurity research

<div align="center">
SecureLog — Making Log Analysis Smarter, Faster, and Safer
</div>
