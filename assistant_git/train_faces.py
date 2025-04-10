import cv2
import numpy as np
import os

# Path to known faces directory
KNOWN_FACES_DIR = "./known_faces"

# Initialize face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load multiple images for training
known_faces = []
known_labels = []

for i, filename in enumerate(os.listdir(KNOWN_FACES_DIR)):
    img_path = os.path.join(KNOWN_FACES_DIR, filename)
    
    img = cv2.imread(img_path)
    if img is None:
        print(f"Skipping {filename}, unable to load image.")
        continue  # Skip if the image cannot be loaded

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    known_faces.append(gray)
    known_labels.append(0)  # Assign label '0' for authorized user

if not known_faces:
    print("No known faces found! Exiting.")
    exit()

# Train the recognizer
face_recognizer.train(known_faces, np.array(known_labels))

# Save trained model
face_recognizer.save("face_model.yml")
print("Training completed successfully! Model saved as face_model.yml")
