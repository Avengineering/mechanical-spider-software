import getopt, sys
import numpy as np
import cv2

STANDARD_WIDTH = 92
STANDARD_HEIGHT = 112

if __name__=="__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:",'')
    except getopt.GetoptError:
        print "-i [input file]"
        exit(1)
    for opt, arg in opts:
        if opt == '-i':
            inputfile = arg
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    face_recognizer = cv2.createEigenFaceRecognizer()
    #face_recognizer.load('./trainingData.yml')
    iteration = 0
   
    img = cv2.imread(inputfile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces_rect = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces_rect:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        face_roi = gray[y:y+h, x:x+w]
        face_roi_resized = cv2.resize(face_roi, (STANDARD_WIDTH, STANDARD_HEIGHT))
        #label, confidence = face_recognizer.predict(face_roi_resized)
        #if label == 0:
            #text = "name: Baixiao confidence: {0}".format(confidence)
        #else:
            #text = "name: unknown"
        #cv2.putText(img, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.imshow('img', img)
    c = cv2.waitKey(0)

    cv2.destroyAllWindows()

