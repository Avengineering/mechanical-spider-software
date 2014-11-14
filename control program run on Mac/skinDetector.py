import cv2
import numpy as np

class skinDetector:
    def __init__(self):
        self.kernel = np.ones((5,5),np.uint8)
    def parameters(self, Ymin, Ymax, Crmin, Crmax, Cbmin, Cbmax):
        self.Ymin = Ymin
        self.Ymax = Ymax
        self.Crmin = Crmin
        self.Crmax = Crmax
        self.Cbmin = Cbmin
        self.Cbmax = Cbmax
        self.lower_threshold = np.array([Ymin, Crmin, Cbmin])
        self.upper_threshold = np.array([Ymax, Crmax, Cbmax])
    def loadImg(self, img):
        self.image = img;
        self.YCrCbimg = cv2.cvtColor(self.image, cv2.COLOR_BGR2YCR_CB)
    def getMask(self):
        raw_mask = cv2.inRange(self.YCrCbimg, self.lower_threshold, self.upper_threshold)
        mask = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, self.kernel)
        return mask
    def kernel(self,x,y):
        self.kernel = np.ones((x,y), np.uint8)
    
    def loadCascade(self, name):
        self.cascade = cv2.CascadeClassifier(name)
    def detectMultiScale(self, img, scaleFactor, minNeighbour):
        copy = img.copy()
        if len(copy.shape) == 3:
            copy = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
        return self.cascade.detectMultiScale(copy, scaleFactor, minNeighbour)


"""if __name__=="__main__":
    Ymin = 10
    Ymax = 255
    Crmin = 133
    Crmax = 173
    Cbmin = 77
    Cbmax = 127
    
    def CrminChange(value):
        Crmin = value
        tracker.parameters(Ymin, Ymax, Crmin, Crmax, Cbmin, Cbmax)
    def CrmaxChange(value):
        Crmax = value
        tracker.parameters(Ymin, Ymax, Crmin, Crmax, Cbmin, Cbmax)
    def CbminChange(value):
        Cbmin = value
        tracker.parameters(Ymin, Ymax, Crmin, Crmax, Cbmin, Cbmax)
    def CbmaxChange(value):
        Cbmax = value
        tracker.parameters(Ymin, Ymax, Crmin, Crmax, Cbmin, Cbmax)
    
    tracker = skinDetector()
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('test')
    cv2.createTrackbar('Crmin', 'test', 133, 173, CrminChange)
    cv2.createTrackbar('Crmax', 'test', 133, 173, CrmaxChange)
    cv2.createTrackbar('Cbmin', 'test', 77, 127, CbminChange)
    cv2.createTrackbar('Cbmax', 'test', 77, 127, CbmaxChange)
    tracker.parameters(Ymin, Ymax, Crmin, Crmax, Cbmin, Cbmax)
    tracker.loadCascade('./cascade/aGest.xml')
    
    while True:
        _,image = cam.read()
        tracker.loadImg(image)
        mask = tracker.getMask()
        result = cv2.bitwise_and(image, image, mask=mask)
        notMask = cv2.bitwise_not(mask, mask)
        result[:,:,0] += notMask[:]
        result[:,:,1] += notMask[:]
        result[:,:,2] += notMask[:]
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        hands_rect = tracker.detectMultiScale(image,1.3,5)
        for (x,y,w,h) in hands_rect:
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
        cv2.imshow('test', image)
        c = cv2.waitKey(1)
        if c & 0xFF == 27:
            break"""