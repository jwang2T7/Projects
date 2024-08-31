

import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# To use a video file instead of a camera, replace '0' with the video file path
cap = cv2.VideoCapture(0)
face_found=0
face_not_found=0

while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        face_found+=1
    else:
        face_not_found+=1

    if face_found+face_not_found>20:
        if face_found>face_not_found:
            print("Face detected")
        else:
            print("Face not detected")
        face_found=0
        face_not_found=0
    



    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()

import face_recognition
import os
import cv2
import numpy as np

# Path to the directory containing user images
user_images_directory = "/Users/jimwang/Desktop/FaceVerification"

# Load user images and generate embeddings
def load_user_embeddings(directory):
    database = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Extract user ID or name from the filename
            user_id = os.path.splitext(filename)[0]
            # Generate embedding for the user image
            image_path = os.path.join(directory, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                # Assuming the first encoding is the user's encoding
                database.append((user_id, face_encodings[0]))
    return database

# Load the face embeddings database
database = load_user_embeddings(user_images_directory)

# Your existing code for facial recognition with modifications for dynamic database use
cap = cv2.VideoCapture(0)  # Adjust the device index as needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color
    rgb_frame = frame[:, :, ::-1]

    # Attempt to find faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        # Initialize variables
        matches = face_recognition.compare_faces([db_embedding for (_, db_embedding) in database], face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance([db_embedding for (_, db_embedding) in database], face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = database[best_match_index][0]

        # Display the name of the best match below the face
        y = face_locations[0][0] - 10 if face_locations[0][0] - 10 > 10 else face_locations[0][0] + 10
        cv2.rectangle(frame, (face_locations[0][3], face_locations[0][0]), (face_locations[0][1], face_locations[0][2]), (0, 0, 255), 2)
        cv2.putText(frame, name, (face_locations[0][3], y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all active windows
#cap.release()
#cv2.destroyAllWindows()

import face_recognition
import cv2
import numpy as np
import time
import os
import pytz
from datetime import datetime

# Initialize the camera
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variable to hold the timestamp when the last face image was saved
last_save_time = time.time()
face_save_interval = 5  # Interval between face saves (in seconds)

# Directory to save face images
save_directory = "FaceImages"
os.makedirs(save_directory, exist_ok=True)
face_id = 0
toronto_tz = pytz.timezone('America/Toronto')
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Get the current time
    current_time = time.time()

    # Check if it's time to save a new face
    if current_time - last_save_time >= face_save_interval:
        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(frame)

        # If faces are detected, save the first one
        if face_locations:
            # Update the last saved time
            last_save_time = current_time

            # Increment the face ID
            face_id += 1

            toronto_time = datetime.now(toronto_tz)

            # Format the timestamp for the filename
            timestamp = toronto_time.strftime('%B %d, %Y -> %I hours %M minutes %S seconds').lower()

            # Save the image of the face to a file
            top, right, bottom, left = face_locations[0]
            face_image = frame[top:bottom, left:right]
            save_path = os.path.join(save_directory, f"Face_{timestamp}.jpg")
            cv2.imwrite(save_path, face_image)
            print(f"Saved face_{face_id}.jpg")

    # Display the resulting frame
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display
    cv2.imshow('img', img)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()

