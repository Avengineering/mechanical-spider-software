import numpy as np
import cv2

if __name__=="__main__":
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
    cam = cv2.VideoCapture(0)
    iteration = 0;
    while True:
        _, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            print "here"
            face_roi = gray[y:y+h, x:x+w]
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)
        #break
        cv2.imshow('img', img)
        c = cv2.waitKey(1)
        if c & 0xFF == 27:
            break
        if c & 0xFF == ord('c'):
            fileName = "{0}.jpg".format(iteration)
            cv2.imwrite(fileName, face_roi)
            iteration = iteration+1
    cv2.destroyAllWindows()
