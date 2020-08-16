import cv2
import numpy as np
import os
import sys

username = sys.argv[1]    

basedir = os.path.abspath(os.path.dirname(__file__))
os.mkdir(os.path.join(basedir, "static\\", username, ""))
folder_path = os.path.join(basedir, "static\\", username, "")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
count = 0
while True:
    ret, frame = cap.read()
    face_classifier = cv2.CascadeClassifier('attendance/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        extracter = None
    else:
        for(x,y,w,h) in faces:
            extracter = frame[y:y+h, x:x+w]
            break
    if extracter is not None:
        count+=1
        face = cv2.resize(extracter,(200,200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        file_name_path = folder_path + str(count) + '.jpg'
        print(file_name_path)
        cv2.imwrite(file_name_path,face)
        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Face Cropper',face)
    else:
        print("Face not Found")
        pass
    if cv2.waitKey(1)==13 or count==50:
        break
cap.release()
cv2.destroyAllWindows()
print('Collecting Samples Complete!!!')