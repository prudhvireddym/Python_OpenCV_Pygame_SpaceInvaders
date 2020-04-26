# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 20:40:26 2020

@author: prudh
"""

import numpy as np
import cv2
import pickle

##########################################################
width = 640
height = 480
threshold = 0.65
##########################################################


cap = cv2.VideoCapture(2)
cap.set(3,width)
cap.set(4,height)


pickel_in = open("model_trained.p","rb")
model = pickle.load(pickel_in)

def preprocessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Convert image to grey - sets the depth to 0
    img = cv2.equalizeHist(img) #Equalize the light in the image
    img = img/255
    return img

while True:
    success,imgOriginal = cap.read()
    img = np.asarray(imgOriginal)
    img = cv2.resize(img,(32,32))
    img = preprocessing(img)
    cv2.imshow("Preprocesses Imgs",img)
    img = img.reshape(1,32,32,1)
    
    #Prediction
    classIndex = int(model.predict_classes(img))
    print(classIndex)
    predictions = model.predict(img)
    probValue = np.amax(predictions)
    print(classIndex,probValue)

    if probValue> threshold:
        if(classIndex==0):
            classIndex = str("Palm")
        elif(classIndex==1):
            classIndex = str("Point UP")
        elif(classIndex==2):
            classIndex = str("Fist")
            
        cv2.putText(imgOriginal,str(classIndex) + "   "+str(probValue),
                    (50,50),cv2.FONT_HERSHEY_COMPLEX,
                    1,(0,0,255),1)
    
    cv2.imshow("Original Image",imgOriginal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
