import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("servies.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-52375-default-rtdb.firebaseio.com/",
    'storageBucket':'faceattendancerealtime-52375.appspot.com'
})
refer=db.reference('students') #this is the reference.'/students'
#start of the json file for storage
data={
    "250625":
        {
            "name":"Yogesh",
            "major":"CSE",
            "starting year":2018,
            "total attendance":6,
            "standing":"G",
            "year":4,
            "last-attendance-time":"2022-12-11 00:54:34"
        },
  "321654":
        {
            "name":"tutor",
             "major":"ROBOTICS",
            "starting year":2017,
            "total attendance":5,
            "standing":"G",
            "year":3,
            "last-attendance-time":"2022-12-11 00:54:34"
        },
"852741":
        {
            "name":"Rose",
             "major":"MECH",
            "starting year":2018,
            "total attendance":8,
            "standing":"B",
            "year":3,
            "last-attendance-time":"2022-12-11 00:54:34"
        },
"963852":
        {
            "name":"Elon",
             "major":"science",
            "starting year":2019,
            "total attendance":9,
            "standing":"G",
            "year":1,
            "last-attendance-time":"2022-12-11 00:54:34"
        }
}

for key,value in data.items():
    refer.child(key).set(value)