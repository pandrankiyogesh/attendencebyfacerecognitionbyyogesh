import os
import cv2
import face_recognition
import pickle #important for images load and dump
#importing the student images.
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("servies.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-52375-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-52375.appspot.com"
})
filimg='images'
images=os.listdir(filimg)
imglist=[]
studentids=[]
for i in images:
     imglist.append(cv2.imread(filimg+'/{}'.format(i)))
     studentids.append(i.replace(".png",""))
     filename=filimg+'/{}'.format(i)
     bucket=storage.bucket()
     blob=bucket.blob(filename)
     blob.upload_from_filename(filename)

#function for finding the encodings
def findencodings(imagelist):
    encodelist=[]
    for image in imagelist:
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encodes=face_recognition.face_encodings(image)[0]
        encodelist.append(encodes)
    return encodelist

encodelists=findencodings(imglist)
encodelistmatchings=[encodelists,studentids]
file= open("Encodefiles.p",'wb')
pickle.dump(encodelistmatchings,file) #this is used to store the encodings to not let every time load the encodings.
                                      #image encodings hence these are stored using pickle module.
file.close()


