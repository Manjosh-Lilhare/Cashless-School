##Cashless School Management System##

Overview

Traditional cash-based transactions in schools are time-consuming, non-transparent, and do not encourage healthy habits or positive behavior. The existing solutions fail to integrate all stakeholders into a unified platform. This project introduces a digital, point-based economy where students use points instead of cash for school purchases.

Features

Point System: Parents deposit money into a student’s digital wallet, and points can be used for canteen, books, transport, and other services.

Secure Payments: Transactions are verified via Face ID and RFID tap cards. Lost cards can be blocked via an app.

Mobile & Web App: Allows students, parents, and administrators to track spending, achievements, and rankings.

Gamification & Motivation: Bonus points are awarded for academic and extracurricular performance, fostering a competitive environment.

Real-Time Analytics: Spending insights and dietary tracking for parents and administrators.

Scalable & Affordable: Cost-effective installation, ensuring accessibility for schools.

Technologies Used

Hardware Requirements

Raspberry Pi 5 – Main processing unit.

Raspberry Pi Pico + RFID Module – Student card-based transactions.

Fingerprint Sensor (TTL) – Biometric authentication.

School Server or Cloud Storage – Transaction and student data storage.

Network Router & Internet Connection – Syncing transactions with the backend.

Software Requirements

Operating System: Raspberry Pi OS (RPi 5), MicroPython (Pico)

Database: MySQL for transaction storage

Backend: Flask (Python) for API handling

Frontend: HTML/CSS/JavaScript for mobile and web interfaces

Authentication: Auth0 for secure logins

Cloud Services: AWS/GCP/Azure for storage and remote access

RFID Library: MFRC522 or similar for card reading

Fingerprint Authentication: Adafruit-Fingerprint Library (TTL sensors)

Setup Instructions

Clone the repository:

git clone https://github.com/your-repo/cashless-school.git
cd cashless-school

Install dependencies:

pip install flask mysql-connector-python

Run the Flask backend:

python app.py

Open the web app in your browser:

http://127.0.0.1:5000

Block Diagram / Flow Chart

Add your block diagram or flow chart here

Future Enhancements

Integration with a payment gateway.

AI-driven spending analysis.

Expansion to universities and corporate environments.

Contributors

Nishant Gakare

Ishan Pote

Aryan Thawkar

Manjosh Lilhare

Team CixCodeCrushers

References

RFID: A Technical Overview

Secure Mobile Payment Systems

Face Recognition System

MFRC522 RFID Module with Raspberry Pi Pico

FTDI Cable and Adapter Pinout
