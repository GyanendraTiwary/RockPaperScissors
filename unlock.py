import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

def unlock():

    # taking input from the camera
    video_capture = cv2.VideoCapture(0)

    # loading and encoding photos

    harsh_img = face_recognition.load_image_file("photos/harsh.jpg")
    harsh_encoding  = face_recognition.face_encodings(harsh_img)[0]

    gyan_img = face_recognition.load_image_file("photos/gyan.jpg")
    gyan_encoding  = face_recognition.face_encodings(gyan_img)[0]

    known_face_encoding = [
        harsh_encoding,
        gyan_encoding
    ]

    known_face_names = [
        "Harsh",
        "Gyan"
    ]

    players = known_face_names.copy()

    face_locations = []
    face_encodings = []
    face_names = []

    s = True

    while True:
        # capturing the image
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25) #decreasing size
        # converting the opencv image to rgb format from bgr 
        rgb_small_frame = small_frame[:,:,::-1]

        name = ""
        #recognising faces
        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
        
        if name in known_face_names:
            video_capture.release()
            cv2.destroyAllWindows()
            return name
        else:
            print("Player not found!! press q to quit")
        
        cv2.imshow("Rock Paper Scissors", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            return "Q"
            




