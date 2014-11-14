import cv2
import numpy as np
"""import video
import common
from common import getsize, draw_keypoints"""

class handTraker:
    def __init__(self):
        return
    def loadImg(self, img):
        self.image = img
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    def loadCascade(self, name):
        self.cascade = cv2.CascadeClassifier(name)
    
    def detectHands(self, scaleFactor, minNeighbour):
        self.handRect = self.cascade.detectMultiScale(self.gray, scaleFactor, minNeighbour)
        return self.handRect
        
        
        
    def SURF(self, HessianThreshold):
        self.surf = cv2.SURF(HessianThreshold)
        self.bf = cv2.BFMatcher()

    def detectAndCompute(self, image):
        return self.surf.detectAndCompute(image,None)

    def trainHandData(self, hand):
        self.trainKeypoints, self.descriptors = self.detectAndCompute(hand)

    def matchTrainData(self, kp, des, ratio):
        matches = self.bf.knnMatch(self.descriptors, des, k=2)
        self.goodMatches = []
        for m,n in matches:
            if m.distance < ratio*n.distance:
                self.goodMatches.append(m)
        return self.goodMatches
    def gettrainingData(self):
        return self.trainKeypoints, self.descriptors




if __name__=="__main__":
    tracker = handTraker()
    tracker.loadCascade('./cascade/aGest.xml')
    tracker.SURF(100)
    cam = cv2.VideoCapture(0)
    detectionMode = True
    while True:
        _,image = cam.read()
        copy = image.copy()
        
        if detectionMode:
            tracker.loadImg(image)
            hands = tracker.detectHands(1.1,5)
            goodHands = []
            for (x,y,w,h) in hands:
                if w > 90 and h > 90:
                    outsideOfFace = True
                    if outsideOfFace:
                        goodHands.append([x,y,w,h])
                        cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
                    break
            cv2.imshow('test', image)
        else:
            kp1, des1 = tracker.gettrainingData()
            kp2, des2 = tracker.detectAndCompute(image)
            matches = tracker.matchTrainData(kp2,des2,0.8)
            """for m in matches:
                cv2.circle(image, (int(kp2[m.queryIdx].pt[0]),int(kp2[m.queryIdx].pt[1])), 5, (0,255,0),2)"""
            for kp in kp2:
                cv2.circle(image, (int(kp.pt[0]),int(kp.pt[1])), 5, (0,255,0),2)
            cv2.imshow('test',image)
        

        c = cv2.waitKey(1)
        if c & 0xFF == ord('t') and detectionMode:
            for (x,y,w,h) in goodHands:
                trainingImg = copy[y:y+h,x:x+w]
                tracker.trainHandData(trainingImg)
                kps, des = tracker.gettrainingData()
                print len(kps)
                for kp in kps:
                    cv2.circle(image, (int(kp.pt[0]),int(kp.pt[1])), 5, (0,255,0),2)
                cv2.imshow('training image', trainingImg)
                detectionMode = False
                break
        if c & 0xFF == ord('d'):
            detectionMode = True
        if c & 0xFF == 27:
            break