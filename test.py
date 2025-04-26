import cv2
import numpy as np
import pickle
import os
import csv
import time
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch

# ----------- Utility Functions ------------
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def load_data():
    with open('data/names.pkl', 'rb') as name_file:
        labels = pickle.load(name_file)
    with open('data/faces_data.pkl', 'rb') as face_file:
        faces = pickle.load(face_file)
    
    min_len = min(faces.shape[0], len(labels))
    return faces[:min_len], labels[:min_len]

def save_attendance(name, time_str, csv_path):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['NAME', 'TIME'])
        writer.writerow([name, time_str])

# ----------- Load Training Data and Train Model ------------
faces_data, labels = load_data()
print(f"Loaded faces: {faces_data.shape}, Labels: {len(labels)}")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(faces_data, labels)

# ----------- Initialize System ------------
video = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
background_img = cv2.imread('background.jpg')

if background_img is None:
    print("Error: Background image not found.")
    exit()

# Position on background where the webcam frame will appear
overlay_x, overlay_y = 55, 162

# ----------- Main Loop ------------
while True:
    ret, frame = video.read()
    if not ret:
        print("Error reading video frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    attendance_data = None

    for (x, y, w, h) in faces:
        face_crop = frame[y:y+h, x:x+w]
        resized_face = cv2.resize(face_crop, (50, 50)).flatten().reshape(1, -1)

        name = knn.predict(resized_face)[0]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, name, (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        timestamp = datetime.now().strftime("%H:%M:%S")
        attendance_data = (name, timestamp)

    # Resize frame to fit dynamically into background
    bg_copy = background_img.copy()
    bg_height, bg_width = bg_copy.shape[:2]
    max_h = bg_height - overlay_y
    max_w = bg_width - overlay_x

    # Resize camera frame
    resized_frame = cv2.resize(frame, (max_w, max_h))
    bg_copy[overlay_y:overlay_y + max_h, overlay_x:overlay_x + max_w] = resized_frame

    # Show the combined view
    cv2.imshow("Face Recognition Attendance System", bg_copy)

    key = cv2.waitKey(1)
    if key == ord('o') and attendance_data:
        date_str = datetime.now().strftime("%d-%m-%Y")
        csv_file = f"Attendance/Attendance_{date_str}.csv"
        save_attendance(attendance_data[0], attendance_data[1], csv_file)
        speak("Attendance Taken.")
    elif key == ord('q'):
        break

# ----------- Cleanup ------------
video.release()
cv2.destroyAllWindows()
