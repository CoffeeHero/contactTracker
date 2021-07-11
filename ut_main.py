import unittest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebaseApi import Firebase
from contactTracing import ContactTracker
import random
from firebaseApi import Firebase

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_1(self):
        self.assertEqual(self.footprintList_1, self.footprintList_2)

def TestdataGenerate():
    cred = credentials.Certificate('firebase_key.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    # siteData = {
    #    "providerId":"unimportant",
    #    "id":"site",
    #    "qurcode":"blablabla",
    # }
    # userData = {
    #     "providerId":"whatever",
    #     "id":"user",
    #     "name":"user01",
    #     "role":"customer",
    #     "lineId":"whateverLineId",
    # }
    # footprintData = {
    #     "siteId":"string",
    #     "userId":"string",
    #     "timestamp":"float"
    # }

    # site
    siteCount = 9
    for i in range(siteCount):
        db.collection('TestingData').document("EpidemicPreventionDB").collection('sites').document("site_"+str(i+1)).set({
            "providerId":"unimportant",
            "id":"site_"+str(i+1),
            "qurcode":"blablabla",
        })
    
    # userCount
    userCount = 9
    for i in range(userCount):
        db.collection('TestingData').document("EpidemicPreventionDB").collection('users').document("user_"+str(i+1)).set({
            "providerId":"whatever",
            "id":"user_"+str(i+1),
            "name":"user01",
            "role":"customer",
            "lineId":"whateverLineId",
        })

    # footprint
    footprintCountRange = [1, 5]
    footprintIndex = 1
    for userIndex in range(userCount):
        footprintCount = random.randint(footprintCountRange[0], footprintCountRange[1])
        for index in range(footprintCount):
            footprintData = {
                "userId":"user_"+str(userIndex+1),
                "siteId":"site_"+str(random.randint(1, siteCount)),
                "timestamp":footprintIndex*100,
                "footprintId":"footprint_"+str(footprintIndex)
            }
            footprintIndex = footprintIndex+1
            db.collection('TestingData').document("EpidemicPreventionDB").collection('footprints').document(footprintData["footprintId"]).set(footprintData)
            db.collection('TestingData').document("EpidemicPreventionDB").collection('sites').document(footprintData["siteId"]).collection("footPrintIds").document(footprintData["footprintId"]).set(footprintData)
            db.collection('TestingData').document("EpidemicPreventionDB").collection('users').document(footprintData["userId"]).collection("footPrintIds").document(footprintData["footprintId"]).set(footprintData)

def classFirebaseTest():
    firebase = Firebase()
    footPrintsDataOfSite = firebase.listFootPrintsDataOfSite("site_1")
    print(footPrintsDataOfSite)
    footPrintsDataOfUser = firebase.listFootPrintsDataOfUser("user_6", 2000,2100)
    print(footPrintsDataOfUser)


if __name__ == '__main__':
    # unittest.main()
    # TestdataGenerate()
    # classFirebaseTest()