import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import os

face_classifier = cv2.CascadeClassifier('C:/Users/aashi/PycharmProjects/try1/haarcascade_frontalface_default.xml')
basedir = os.path.abspath(os.path.dirname(__file__))
a = {}
for username in os.listdir(os.path.join(basedir,"static\\", "")):
    data_path = os.path.join(basedir, 'static\\', username, "")
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    Training_Data, Labels = [], []

    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    a[username]=model
    print("Model Training Complete of ", username)


def face_detector(img, size = 0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        return img,[]

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))

    return img,roi

count = 0
attender = {}
for username in a.keys():
    attender[username] = 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    user = {}
    ret, frame = cap.read()
    image, face = face_detector(frame)
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        for username, model in a.items():
            result = model.predict(face)
            if result[1] < 500:
                confidence = int(100*(1-(result[1])/300))
                user[username] = confidence
        for j in user.keys():
            if user[j] == max(list(user.values())):
                attendee = j
                cv2.putText(image, j, (250, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        attender[attendee] += 1
        for username, record in attender.items():
            if attender[username] == 10:
                person = username
                print(username, ' done')
        try:
            with open('attendance/username.txt', 'w') as f:
                f.write(person)
            break
        except:
            pass
        display_string = str(h_confidence)+'% Confidence of user'
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)
        cv2.imshow('Face Cropper', image)
    except:
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Face Cropper', image)
        pass

    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()