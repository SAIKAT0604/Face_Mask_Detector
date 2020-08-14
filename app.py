#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Import necessary linbraries
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import tkinter
from tkinter import messagebox
import smtplib
from datetime import datetime
from PIL import Image

# Initialize Tkinter
root = tkinter.Tk()
root.withdraw()

#Load trained deep learning model
model = load_model('mask_detector_model.h5')

#Classifier to detect face
face_det_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Capture Video
vid_source=cv2.VideoCapture(0)

# Dictionaries containing details of Wearing Mask and Color of rectangle around face. If wearing mask then color would be 
# green and if not wearing mask then color of rectangle around face would be red
text_dict={0:'Mask ON',1:'No Mask'}
rect_color_dict={0:(0,255,0),1:(0,0,255)}

SUBJECT = "VIOLATION OF FACE-MASK POLICY"   
c=int(0)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)

# While Loop to continuously detect camera feed
while(True):

    ret, img = vid_source.read()
    #grayscale_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_det_classifier.detectMultiScale(img,1.3,5)  

    for (x,y,w,h) in faces:
    
        face_img = img[y:y+w,x:x+w]
        resized_img = cv2.resize(face_img,(224,224))
        normalized_img = resized_img/255.0
        reshaped_img = np.reshape(normalized_img,(1,224,224,3))
        result=model.predict(reshaped_img)
        
        label=np.argmax(result,axis=1)[0]
        label2 = "{}: {:.2f}%".format(text_dict[label], max(result[0][1],result[0][0]) * 100)
      
        cv2.rectangle(img,(x,y),(x+w,y+h),rect_color_dict[label],2)
        #cv2.rectangle(img,(x,y-40),(x+w,y),rect_color_dict[label],-1)
        cv2.putText(img, label2, (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.45,rect_color_dict[label],2) 
        #cv2.putText(img, result, (x, y-20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),2)
        
        # If label = 1 then it means wearing No Mask and 0 means wearing Mask
        if (label == 1):
            # Throw a Warning Message to tell user to wear a mask if not wearing one. This will stay
            #open and No Access will be given He/She wears the mask
            c=c+1;
            if(c>3):
            	now = datetime.now()
            	dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
            	im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            	image = Image.fromarray(im_rgb, 'RGB')
            	image.save('static/images/'+dt_string+'.jpg')
            	messagebox.showwarning("Warning","Access Denied. Please wear a Face Mask")
            	#mail section(uncomment the following section and provide the email ids and password) 
	            #TEXT = "One Visitor violated Face Mask Policy. Find the violater's image in the images folder named "+dt_string+".jpg .\nPlease Alert the appropriate authorities."
                #message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                #mail = smtplib.SMTP('smtp.gmail.com', 587)
                #mail.ehlo()
                #mail.starttls()
                #mail.login('Enter your email','Enter your Password')
                #mail.sendmail('Enter your email','Enter Recieving/Admin email',message)
                #mail.close
        else:
            c=0
            pass
            break

    cv2.imshow('LIVE Video Feed',img)
    key=cv2.waitKey(1)
    
    if(key==27):
        break
        
cv2.destroyAllWindows()
vid_source.release()

