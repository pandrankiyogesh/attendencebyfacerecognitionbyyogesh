import os
import pickle
from firebase_admin import db
import cvzone
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from datetime import datetime
comparision=[]
dis=[]
cap = cv2.VideoCapture(0) #index 0 for the single camera.
cap.set(3, 640)  # setting width of cam
cap.set(4, 480)  # setting height of cam
imgbackground=cv2.imread('resourses/background.png')
#importing the mode images
foldermodepath='resourses/Modes'
modepathlist=os.listdir(foldermodepath)
imagemodelist=[]
for modes in modepathlist:
    imagemodelist.append(cv2.imread(foldermodepath+'/{}'.format(modes)))
#imorting the encoding file
file=open("Encodefiles.p",'rb')
encodelistmatchings=pickle.load(file)
file.close()
encodelists, studentids=encodelistmatchings
counter=0 #setting of frames.
dis=-1
modetype=-1
cred = credentials.Certificate("servies.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-52375-default-rtdb.firebaseio.com/",
    'storageBucket':'faceattendancerealtime-52375.appspot.com'
})
while True:
    success, img = cap.read() #returns two values one is (true/false) other one is actual data that was read.
    another=img
    imgs=cv2.resize(img,(0,0),None,0.25,0.25) #the pixel values of height and width are to one forth of org image
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB) #we have to convert it because encodings are rgb format.Then only facerecoginition is happened.
    facecurrframe=face_recognition.face_locations(imgs) #we will get the pixel values.
    if facecurrframe:
        encodcurr = face_recognition.face_encodings(imgs, facecurrframe)
        if not success:
            print("Failed to read frame from the camera.")
            break
        cv2.imshow("Face Attendance", imgbackground)
        imgbackground[162:162 + 480, 55:55 + 640] = img  # the two parameters are one is for setting height and width
        imgbackground[44:44 + 633, 808:808 + 414] = imagemodelist[modetype]
        for c in encodcurr:
            comparision = face_recognition.compare_faces(encodelists, c)
        for d in encodcurr:
            dis = face_recognition.face_distance(encodelists, d)
        matchedfaceid = np.argmin(dis)
        for loc in facecurrframe:
            y1, x2, y2, x1 = loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = x1 + 55, y1 + 162, x2 - x1, y2 - y1
            cvzone.cornerRect(imgbackground, bbox, rt=0)
        if comparision != []:
            if comparision[matchedfaceid]:
                print("know face detected")
                print("matched face id", studentids[matchedfaceid])
                if counter == 0:
                    counter = 1
                    modetype = 1
        if counter != 0:
            if counter == 1:
                ref = db.reference('students/' + '{}'.format(studentids[matchedfaceid])).get()
                bucket = storage.bucket()
                blob = bucket.get_blob('images/' + '{}.png'.format(studentids[matchedfaceid]))
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                re = db.reference('students/' + '{}'.format(studentids[matchedfaceid]))
                imgst = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # update data at attendence.
                # this is datetime object.
                dtime = datetime.strptime(ref['last-attendance-time'],
                                          "%Y-%m-%d %H:%M:%S")  # according to the real time data-base time format
                x = (datetime.now() - dtime).total_seconds()
                if x > 30:
                    ref['total attendance'] += 1
                    re.child('total attendance').set(ref['total attendance'])
                    re.child('last-attendance-time').set(datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"))  # last updated time from that we are calculatings secs.
                else:
                    modetype = 3
                    counter = 0
                    imgbackground[44:44 + 633, 808:808 + 414] = imagemodelist[modetype]
            if modetype != 3:
                if counter > 10 and counter < 20:
                    modetype = 2
                    imgbackground[44:44 + 633, 808:808 + 414] = imagemodelist[modetype]
                if counter <= 10:
                    cv2.putText(imgbackground, str(ref['total attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(ref['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(studentids[matchedfaceid]), (1006, 493), cv2.FONT_HERSHEY_COMPLEX,
                                0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgbackground, str(ref['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(imgbackground, str(ref['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    cv2.putText(imgbackground, str(ref['starting year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,
                                (100, 100, 100), 1)
                    (w, h), _ = cv2.getTextSize(str(ref['name']), cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgbackground, str(ref['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (50, 50, 50), 1)
                    if studentids[matchedfaceid] == '250625':
                        imgbackground[175:175 + 216, 909:909 + 218] = imgst
                    else:
                        imgbackground[175:175 + 216, 909:909 + 216] = imgst
                counter += 1
                if counter >= 20:
                    counter = 0
                    modetype = 0
                    ref = []
                    imgst = []
                    imgbackground[44:44 + 633, 808:808 + 414] = imagemodelist[modetype]
            else:
                counter=0
                modetype=0

    #cv2.imshow("webcam", img)
    cv2.waitKey(1)