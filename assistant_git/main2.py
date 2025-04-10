import cv2
import numpy as np
import os
import subprocess

# Load trained recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("face_model.yml")  # Load the trained model

# Initialize webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def authenticate_face():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print("No face detected. Access denied.")
            break  # Exit immediately after one attempt

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            label, confidence = face_recognizer.predict(roi_gray)

            print(f"Confidence: {confidence}")  # Debugging

            # **Corrected Authentication Logic**
            if confidence < 50:  # Lower confidence means a better match
                print("Authentication successful! Welcome.")
                color = (0, 255, 0)  # Green for success
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.imshow("Face Authentication", frame)
                cv2.waitKey(2000)  # Show success for 2 seconds
                cap.release()
                cv2.destroyAllWindows()
                return True
            else:
                print("Face not recognized. Access denied.")
                color = (0, 0, 255)  # Red for failure
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.imshow("Face Authentication", frame)
                cv2.waitKey(2000)  # Show failure for 2 seconds
                break  # Exit immediately after one failed attempt

        break  # Exit loop after first attempt

    cap.release()
    cv2.destroyAllWindows()
    return False

