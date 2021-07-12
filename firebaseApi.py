import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage
import config
import cv2
import numpy
import base64

class Firebase:
    def __init__(self):
        # self.__cred = credentials.Certificate(firebaseConfig.keyFile)
        # initialize_app(self.__cred, {'storageBucket': firebaseConfig.storageBucket})
        cred = credentials.Certificate(config.FS_service_account_credentials)
        firebase_admin.initialize_app(cred)
        self.__firestore = firestore.client()
        self.__myDb = self.__firestore.collection(config.projectName).document(config.dbName)
        self.__sitesCollection = self.__myDb.collection(config.siteTable)
        self.__usersCollection = self.__myDb.collection(config.userTable)
        self.__footPrintsCollection = self.__myDb.collection(config.footPrintTable)
        
    def createSite(self, siteData):
        response = self.__sitesCollection.add(siteData)[1]
        self.__sitesCollection.document(response.id).update({'id':response.id})
        return response.id

    def addQrCodeUrlToSite(self,siteId, qrCodeUrl):
        self.__sitesCollection.document(siteId).update({'qrCodeUrl':qrCodeUrl})

    def listFootPrintsDataOfSite(self, siteId, beginTime, endTime):
        footPrintIdsOfSite = list(doc.id for doc in self.__sitesCollection.document(siteId).collection('footPrintIds').stream())
        footPrintsDataOfSite = []
        for footPrintId in footPrintIdsOfSite:
            footprintData = self.__footPrintsCollection.document(footPrintId).get().to_dict()
            if footprintData["timestamp"]>=beginTime and footprintData["timestamp"]<=endTime:
                footPrintsDataOfSite.append(footprintData)
        return footPrintsDataOfSite

    def createUser(self, userData):
        response = self.__usersCollection.add(userData)[1]
        self.__usersCollection.document(response.id).update({'id':response.id})
        return response.id

    def addSiteIdToUser(self,siteId,userId):
        self.__usersCollection.document(userId).collection('siteIds').document(siteId).set(None)

    def addFootPrintIdToUser(self,footPrintId,userId):
        self.__usersCollection.document(userId).collection('footPrintIds').document(footPrintId).set(None)

    def addFootPrintIdToSite(self,footPrintId,siteId):
        self.__sitesCollection.document(siteId).collection('footPrintIds').document(footPrintId).set(None)

    def listFootPrintsDataOfUser(self, userId, beginTime, endTime):
        footPrintIdsOfUser = list(doc.id for doc in self.__usersCollection.document(userId).collection('footPrintIds').stream())
        footPrintsDataOfUser = []
        for footPrintId in footPrintIdsOfUser:
            footprintData = self.__footPrintsCollection.document(footPrintId).get().to_dict()
            if footprintData["timestamp"]>=beginTime and footprintData["timestamp"]<=endTime:
                footPrintsDataOfUser.append(footprintData)
        return footPrintsDataOfUser

    def listSitesDataOfUser(self, userId):
        siteIdsOfUser = list(doc.id for doc in self.__usersCollection.document(userId).collection('siteIds').stream())
        sitesDataOfUser = []
        for siteId in siteIdsOfUser:
            sitesDataOfUser.append(self.__sitesCollection.document(siteId).get().to_dict())

        return sitesDataOfUser

    def createFootPrint(self, footPrintData):
        response = self.__footPrintsCollection.add(footPrintData)[1]
        self.__footPrintsCollection.document(response.id).update({'id':response.id})
        return response.id

    def uploadImage(self, img, fileName):
        img = cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR)
        img = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
        img = base64.b64decode(img)
        bucket = storage.bucket()
        blob = bucket.blob('siteQrCode/' + fileName)
        blob.upload_from_string(img)
        imageUrl = blob.public_url
        blob.make_public()

        return imageUrl

    def getUserDataById(self, userId):
        userData = self.__usersCollection.document(userId).get().to_dict()
        return userData

    def getSiteDataById(self, siteId):
        siteData = self.__sitesCollection.document(siteId).get().to_dict()
        return siteData

    def getFootprintDataById(self, footprintId):
        footprintData = self.__footPrintsCollection.document(footprintId).get().to_dict()
        return footprintData

    # def createDevice(request):
    #     devices_ref.document(request['device']).set(request)

    # def queryDevice():
    #     return list(doc.to_dict() for doc in devices_ref.stream())

    # def captureUpdate(request):
    #     devices_ref.document(request['device']).update({'config.capture':request['config']['capture']})

    # def recognitionUpdate(request):
    #     devices_ref.document(request['device']).update({'config.recognition':request['config']['recognition']})

    # def alertUpdate(request):
    #     devices_ref.document(request['device']).update({'config.alert':request['config']['alert']})

    # def operationActivationUpdate(request):
    #     devices_ref.document(request['device']).update({'operation.activation':request['operation']['activation']})

