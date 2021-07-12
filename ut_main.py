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

def generateUsers(userCount):

    for i in range(userCount):
        db.collection('TestingData').document("EpidemicPreventionDB").collection('users').document("user_"+str(i+1)).set({
            "providerId":"whatever",
            "id":"user_"+str(i+1),
            "name":"Name_"+"user_"+str(i+1),
            "role":"customer",
            "lineId":"whateverLineId",
        })

def generateSites(siteCount):

    for i in range(siteCount):
        db.collection('TestingData').document("EpidemicPreventionDB").collection('sites').document("site_"+str(i+1)).set({
            "providerId":"unimportant",
            "id":"site_"+str(i+1),
            "name":"Name_"+"site_"+str(i+1),
            "qurcode":"blablabla",
        })

def addFootprint(userId, siteId, timestamp, footprintId):
    # footprint
    footprintData = {
        "userId":userId,
        "siteId":siteId,
        "timestamp":timestamp,
        "id":"footprint_"+str(footprintId)
    }
    db.collection('TestingData').document("EpidemicPreventionDB").collection('footprints').document(footprintData["id"]).set(footprintData)
    db.collection('TestingData').document("EpidemicPreventionDB").collection('sites').document(footprintData["siteId"]).collection("footPrintIds").document(footprintData["id"]).set({})
    db.collection('TestingData').document("EpidemicPreventionDB").collection('users').document(footprintData["userId"]).collection("footPrintIds").document(footprintData["id"]).set({})


    # footprintCountRange = [1, 5]
    # footprintIndex = 1
    # for userIndex in range(userCount):
    #     footprintCount = random.randint(footprintCountRange[0], footprintCountRange[1])
    #     for index in range(footprintCount):
    #         footprintData = {
    #             "userId":"user_"+str(userIndex+1),
    #             "siteId":"site_"+str(random.randint(1, siteCount)),
    #             "timestamp":footprintIndex*100,
    #             "footprintId":"footprint_"+str(footprintIndex)
    #         }
    #         footprintIndex = footprintIndex+1
            # db.collection('TestingData').document("EpidemicPreventionDB").collection('footprints').document(footprintData["footprintId"]).set(footprintData)
            # db.collection('TestingData').document("EpidemicPreventionDB").collection('sites').document(footprintData["siteId"]).collection("footPrintIds").document(footprintData["footprintId"]).set(footprintData)
            # db.collection('TestingData').document("EpidemicPreventionDB").collection('users').document(footprintData["userId"]).collection("footPrintIds").document(footprintData["footprintId"]).set(footprintData)

def classFirebaseTest():
    firebase = Firebase()
    footPrintsDataOfSite = firebase.listFootPrintsDataOfSite("site_1",0,10000)
    print(footPrintsDataOfSite)
    footPrintsDataOfUser = firebase.listFootPrintsDataOfUser("user_6", 700,2100)
    print(footPrintsDataOfUser)
    # siteData = firebase.getSiteDataById("site_3")
    # print(siteData)

    # userData = firebase.getUserDataById("user_3")
    # print(userData)

    # footprintData = firebase.getFootprintDataById("footprint_3")
    # print(footprintData)


def contactTrackerTest():
    confirmedUserData = [{
        "userId":"user_1",
        "confirmedTime":50
    }]
    contactTracker = ContactTracker(0, 2000, 50, confirmedUserData,0)
    contactTracker.run()
    print(contactTracker.getStatisticalData())
    # output = contactTracker.getWebResult()
    # print("")
    # print(output)

def generateTestingData():

    generateUsers(16)
    generateSites(9)
    addFootprint("user_1", "site_1",100, 1)
    addFootprint("user_1", "site_2",200, 2)
    addFootprint("user_1", "site_7",3700, 3)
    addFootprint("user_1", "site_8",0, 4)

    addFootprint("user_3", "site_1",103, 5)
    addFootprint("user_3", "site_3",300, 6)
    addFootprint("user_3", "site_4",400, 7)
    addFootprint("user_3", "site_5",500, 8)
    addFootprint("user_3", "site_5",600, 9)

    addFootprint("user_4", "site_1",60, 10)
    addFootprint("user_4", "site_3",280, 11)

    addFootprint("user_7", "site_1",420, 12)
    addFootprint("user_7", "site_5",520, 13)

    addFootprint("user_5", "site_2",900, 14)
    addFootprint("user_5", "site_7",700, 15)

    addFootprint("user_6", "site_2",190, 16)
    addFootprint("user_6", "site_6",600, 17)

    addFootprint("user_8", "site_4",800, 18)

    addFootprint("user_9", "site_6",500, 19)

    addFootprint("user_10", "site_6",630, 20)

    addFootprint("user_11", "site_6",900, 21)

    addFootprint("user_12", "site_7",3500, 22)

    addFootprint("user_13", "site_7",3685, 23)

    addFootprint("user_14", "site_7",3800, 24)

    addFootprint("user_15", "site_8",0, 25)

    addFootprint("user_12", "site_5",603, 26)

    addFootprint("user_16", "site_7",700, 27)



# cred = credentials.Certificate('firebase_key.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

if __name__ == '__main__':
    # unittest.main()
    # generateTestingData()
    contactTrackerTest()
    # classFirebaseTest()