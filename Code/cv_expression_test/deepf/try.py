# import the required modules
import cv2
#import matplotlib.pyplot as plt
from deepface import DeepFace
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    try:
        result = DeepFace.analyze(img,actions=['emotion'])
        face_detector = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(img, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_img = gray_img[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_img, (48, 48)), -1), 0)

            # predict the emotions
            cv2.putText(img, result[0]['dominant_emotion'], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        #print(result[0]['dominant_emotion'])
    except Exception:
        time.sleep(0)
    cv2.imshow('Emotion Detection', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()


