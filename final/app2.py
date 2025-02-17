import cv2
import face_recognition
import pickle
from picamera2 import Picamera2
import numpy as np
import threading
import serial
from pyfingerprint.pyfingerprint import PyFingerprint
import time

# Global flags for verification
face_matched = False
rfid_matched = False
fingerprint_matched = False

VALID_RFID = "CARD ID: 3660550963"  # Replace with the valid RFID code

# Load known faces and their names
try:
    with open("face_encodings.pkl", "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)
except FileNotFoundError:
    print("Error: 'face_encodings.pkl' not found. Ensure it exists.")
    exit()

def verify_rfid():
    global rfid_matched
    port = '/dev/ttyACM0'  # Change this if needed
    baudrate = 9600

    try:
        print("Opening Serial Connection for RFID...")
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Initial wait for serial to stabilize

        print("Waiting for RFID input (20 sec)...")
        start_time = time.time()  # Start timing

        while time.time() - start_time < 20:  # Wait for 20 seconds
            rfid_data = ser.readline().decode().strip()
            if rfid_data:
                print(f"RFID Data Received: {rfid_data}")
                if rfid_data == VALID_RFID:
                    rfid_matched = True
                    print("RFID Matched!")
                    return True
                else:
                    print("RFID Did Not Match!")

        print("RFID Timeout: No card detected within 20 seconds.")

    except Exception as e:
        print("RFID Error:", e)

    return False

def verify_face():
    global face_matched
    picam2 = Picamera2()
    picam2.start()

    print("Initializing Camera for Face Detection...")
    time.sleep(2)  # Wait for the camera to initialize

    start_time = time.time()  # Start timing
    face_matched = False

    while time.time() - start_time < 10:  # Camera checks for 10 seconds
        frame = picam2.capture_array()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                if True in matches:
                    face_matched = True
                    print("Face Matched!")
                    return True  # Exit and approve once face is matched

    print("Face Did Not Match within 10 seconds!")
    return False

def verify_fingerprint():
    global fingerprint_matched
    try:
        print("Initializing Fingerprint Sensor...")
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            print("Fingerprint sensor password verification failed!")
            return False

        print("Place finger...")
        while not f.readImage():
            pass

        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            fingerprint_matched = True
            print("Fingerprint Matched!")
            return True
        else:
            print("Fingerprint Did Not Match!")

    except Exception as e:
        print("Fingerprint Error:", e)

    return False

def process_payment(payment_option, amount):
    print(f"Processing payment via {payment_option} for amount {amount}")

    # Step 1: Ensure that the face is successfully detected first
    print("Starting face verification...")
    if not verify_face():
        print("Face verification failed. Aborting payment.")
        return False
    
    # Step 2: After face detection, proceed with selected payment option (RFID or fingerprint)
    if payment_option == 'rfid':
        print("Calling verify_rfid()...")
        return verify_rfid()
    elif payment_option == 'fingerprint':
        print("Calling verify_fingerprint()...")
        return verify_fingerprint()
    
    print("Invalid payment option!")
    return False