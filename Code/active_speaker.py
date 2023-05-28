import face_recognition
import cv2
import numpy as np
import math

print("Starting...")

cap = cv2.VideoCapture(0)

faces_cur_frame = []
face_encodings = []
faces = {}
encodings_cur_frame = []
face_landmarks = []
frame_count = 0
speaker_index = None
thresh = 20


def find_distance(landmarks):
    lst = []
    for k in range(len(landmarks)):
        p1 = landmarks[k]['top_lip']
        p2 = landmarks[k]['bottom_lip']
        x1, y1 = p1[10]
        x2, y2 = p1[9]
        x3, y3 = p1[8]
        x4, y4 = p2[8]
        x5, y5 = p2[9]
        x6, y6 = p2[10]
        dist = math.sqrt((x1-x4)**2 + (y1-y4)**2) + math.sqrt((x2-x5)**2 + (y2-y5)**2) + math.sqrt((x3-x6)**2 + (y3-y6)**2)
        lst.append(dist)
    return lst


while True:
    success, frame = cap.read()
    img = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    img = img[:, :, ::-1]

    frame_count += 1
    if frame_count == 10:
        process = True
        max_val = 21
        frame_count = 0
        print(faces)
    else:
        process = False
    
    faces_cur_frame = face_recognition.face_locations(img)
    encodings_cur_frame = face_recognition.face_encodings(img, faces_cur_frame)
    face_landmarks = face_recognition.face_landmarks(img)
    num_faces = len(encodings_cur_frame)
    dist_vals = find_distance(face_landmarks)

    if len(face_encodings) == 0:
        for i in range(num_faces):
            faces[i] = {"val": dist_vals[i]}

            face_encodings.append(encodings_cur_frame[i])
            print("faces added")

    else:
        for i, face_encoding, val, (top, right, bottom, left) in zip(range(num_faces), encodings_cur_frame, dist_vals, faces_cur_frame):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            area = (top-bottom)*(right-left)
            if val > 30:
                val /= 3

            if speaker_index == i:
                cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'speaking', (left + 6, bottom - 5), font, 0.5, (255, 255, 255), 2)

            if process and i == 0:
                speaker_index = None

            matches = face_recognition.compare_faces(face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                faces[best_match_index]["val"] += val

                if process:
                    if faces[best_match_index]["val"] > max_val:
                        speaker_index = i
                        max_val = faces[best_match_index]["val"]

                    faces[best_match_index]["val"] = 0

            else:
                if process:
                    faces[len(faces)] = {"val": 0}
                else:
                    faces[len(faces)] = {"val": val}
                face_encodings.append(face_encoding)
                print("face_added")

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print('Program Terminated')
