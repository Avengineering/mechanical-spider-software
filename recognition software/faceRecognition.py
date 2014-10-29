import numpy as np
import cv2

STANDARD_WIDTH = 92
STANDARD_HEIGHT = 112

if __name__=="__main__":
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')
    face_recognizer = cv2.createEigenFaceRecognizer()
    face_recognizer.load('./trainingData.yml')
    cam = cv2.VideoCapture(0)
    iteration = 0
    while True:
        _, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces_rect = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces_rect:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            face_roi = gray[y:y+h, x:x+w]
            face_roi_resized = cv2.resize(face_roi, (STANDARD_WIDTH, STANDARD_HEIGHT))
            label, confidence = face_recognizer.predict(face_roi_resized)
            if label == 0:
                text = "name: Baixiao confidence: {0}".format(confidence)
            else:
                text = "name: unknown"
            cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow('img', img)
        c = cv2.waitKey(1)
        if c & 0xFF == 27:
            break
        if c & 0xFF == ord('c'):
            cv2.imwrite("./image_{0}.jpg".format(iteration), img)
            iteration += 1
    cv2.destroyAllWindows()

