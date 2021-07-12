import copy
from firebaseApi import Firebase

class ContactTracker:
    def __init__(self, beginTime = 0, endTime = 0, overlappingTime = 0, confirmedUserDataList = [], maxLayer = 0):
        self.__beginTime = beginTime - overlappingTime
        self.__endTime = endTime + overlappingTime
        self.__overlappingTime = overlappingTime
        self.__confirmedUserDataList = confirmedUserDataList
        # [{
        #     "userId":"string",
        #     "confirmedTime":"float"
        # }]
        self.__maxLayer = maxLayer
        if self.__maxLayer == 0:
            self.__maxLayer  = 999999

        self.__infectedUserTable = {}
        # {
        #     "user_1":[{
        #         "infectedStrength":"int",
        #         "infectedSite":"string",
        #         "inftectedTimestamp":"float"
        #     }]
        # }
        self.__infectedUserIdSet = set()
        self.__infectedSiteIdSet = set()
        self.__infectedFootprintIdSet = set()
    
        self.__contactTree = []
        self.__firebase = Firebase()
        
        self.buildUserCounter = 0
        self.buildSiteCounter = 0

    def setTime(self, beginTime, endTime, overlappingTime):
        self.__beginTime = beginTime - overlappingTime
        self.__endTime = endTime + overlappingTime
        self.__overlappingTime = overlappingTime

    def setLevelLimit(self, levelLimit):
        self.__maxLayer = levelLimit

    def setConfirmedUserDataList(self, confirmedUserDataList):
        self.__confirmedUserDataList = confirmedUserDataList

    def run(self):
        self.__generateContactTree()

    def getStatisticalData(self):
        return {
            "infectedUserIdSet": self.__infectedUserIdSet,
            "infectedSiteIdSet": self.__infectedSiteIdSet,
            "infectedFootprintIdSet": self.__infectedFootprintIdSet,
            "infectedUserTable": self.__infectedUserTable
        }

    def getLineResult(self):
        userNameList = []
        for userId in self.__infectedUserIdSet:
            userNameList.append(self.__firebase.getUserDataById(userId))

        return {
            "manager":{
                "managerUserId":"",
                "infectedUserSize":len(self.__infectedUserIdSet),
                "infectedSiteSize":len(self.__infectedSiteIdSet),
                "infectedFootprintSize":len(self.__infectedFootprintIdSet),
                "infectedUserNameList":userNameList
            },
            "customer":self.__infectedUserTable
        }
    
    def getBigQueryResult(self):
        pass

    def getWebResult(self):
        return {
            "infectedUserCount":len(self.__infectedUserIdSet),
            "infectedSiteCount":len(self.__infectedSiteIdSet),
            "infectedFootprintCount":len(self.__infectedFootprintIdSet),
            "transmissionChain": self.__contactTree
        }

    def __generateContactTree(self):
        for user in self.__confirmedUserDataList:
            userTree = self.__buildUserTree(user["userId"],"",0,self.__beginTime, self.__endTime)
            self.__contactTree.append({
                "userId": user["userId"],
                "userName":self.__firebase.getUserDataById(user["userId"])["name"],
                "layer":0,
                "infectedSite":userTree
            }) 
            # self.__infectedUserIdSet.add(user["userId"])
        
    def __buildUserTree(self, userId, siteId, layer, beginTime, endTime):
        print("buildUserCounter: ", self.buildUserCounter)
        self.buildUserCounter = self.buildUserCounter+1
        footPrintsDataOfUser = self.__firebase.listFootPrintsDataOfUser(userId, beginTime, endTime)
        print (footPrintsDataOfUser)
        userTree = []
        for footstamp in footPrintsDataOfUser:
            if footstamp["siteId"] != siteId:
                siteTree = self.__buildSiteTree(footstamp["siteId"],userId, layer+1, footstamp["timestamp"]-self.__overlappingTime, footstamp["timestamp"]+self.__overlappingTime)
                userTree.append({
                    "siteId": footstamp["siteId"],
                    "siteName":self.__firebase.getSiteDataById(footstamp["siteId"])["name"],
                    "visitedUser":siteTree
                })
                self.__infectedSiteIdSet.add(footstamp["siteId"])
            else: 
                infectedUserTableData = {
                    "infectedStrength":layer,
                    "infectedSite": siteId,
                    "infectedTimestamp":footstamp["timestamp"]
                }
                if footstamp["userId"] not in self.__infectedUserTable.keys():
                    self.__infectedUserTable[footstamp["userId"]] = [infectedUserTableData]
                else:
                    self.__infectedUserTable[footstamp["userId"]].append(infectedUserTableData)
        return userTree
    
    def __buildSiteTree(self, siteId, userId, layer, beginTime, endTime):
        if layer > self.__maxLayer:
            return []
        print("buildSiteCounter: ", self.buildSiteCounter)
        self.buildSiteCounter = self.buildSiteCounter+1
        footPrintsDataOfSite = self.__firebase.listFootPrintsDataOfSite(siteId, beginTime, endTime)
        print(footPrintsDataOfSite)
        siteTree = []
        for footstamp in footPrintsDataOfSite:
            self.__infectedFootprintIdSet.add(footstamp["id"])
            if footstamp["userId"]!=userId:
                userTree = self.__buildUserTree(footstamp["userId"], siteId,layer, footstamp["timestamp"], self.__endTime)
                siteTree.append({
                    "userId": footstamp["userId"],
                    "userName": self.__firebase.getUserDataById(footstamp["userId"])["name"],
                    "layer": layer,
                    "infectedSite": userTree
                })
                self.__infectedUserIdSet.add(footstamp["userId"])
        return siteTree
########################################################
class TransmissionTracker:
    def __init__(self, userId, spreadStrength, confirmedTime):
        self.__userId = userId
        self.__spreadStrength = spreadStrength
        self.__confirmedTime = confirmedTime
        self.__contactTree = []
        self.__firebase = Firebase()
        self.buildUserCounter = 0
        self.buildSiteCounter = 0

    def run(self):
        userData = {
            "userId":self.__userId,
            "confirmedTime": self.__confirmedTime,
            "spreadStrength": self.__spreadStrength
        }
        transmissionChain = self.__generateContactTree(userData)

    def getWebResult(self):
        pass

    def getLineResult(self):
        pass

    def getBigQueryResult(self):
        pass

    def __generateContactTree(self):
        for user in self.__confirmedUserDataList:
            userTree = self.__buildUserTree(user["userId"],"",self.__spreadStrength,self.__beginTime, self.__endTime)
            self.__contactTree.append({
                "userId": user["userId"],
                "userName":self.__firebase.getUserDataById(user["userId"])["name"],
                "spreadStrength":self.__spreadStrength,
                "infectedSite":userTree
            }) 

    def __buildUserTree(self, userId, siteId, layer, beginTime, endTime):
        print("buildUserCounter: ", self.buildUserCounter)
        self.buildUserCounter = self.buildUserCounter+1
        footPrintsDataOfUser = self.__firebase.listFootPrintsDataOfUser(userId, beginTime, endTime)
        print (footPrintsDataOfUser)
        userTree = []
        for footstamp in footPrintsDataOfUser:
            if footstamp["siteId"] != siteId:
                siteTree = self.__buildSiteTree(footstamp["siteId"],userId, layer+1, footstamp["timestamp"]-self.__overlappingTime, footstamp["timestamp"]+self.__overlappingTime)
                userTree.append({
                    "siteId": footstamp["siteId"],
                    "siteName":self.__firebase.getSiteDataById(footstamp["siteId"])["name"],
                    "visitedUser":siteTree
                })
                self.__infectedSiteIdSet.add(footstamp["siteId"])
            else: 
                infectedUserTableData = {
                    "infectedStrength":layer,
                    "infectedSite": siteId,
                    "infectedTimestamp":footstamp["timestamp"]
                }
                if footstamp["userId"] not in self.__infectedUserTable.keys():
                    self.__infectedUserTable[footstamp["userId"]] = [infectedUserTableData]
                else:
                    self.__infectedUserTable[footstamp["userId"]].append(infectedUserTableData)
        return userTree
    
    def __buildSiteTree(self, siteId, userId, layer, beginTime, endTime):
        if layer > self.__maxLayer:
            return []
        print("buildSiteCounter: ", self.buildSiteCounter)
        self.buildSiteCounter = self.buildSiteCounter+1
        footPrintsDataOfSite = self.__firebase.listFootPrintsDataOfSite(siteId, beginTime, endTime)
        print(footPrintsDataOfSite)
        siteTree = []
        for footstamp in footPrintsDataOfSite:
            self.__infectedFootprintIdSet.add(footstamp["id"])
            if footstamp["userId"]!=userId:
                userTree = self.__buildUserTree(footstamp["userId"], siteId,layer, footstamp["timestamp"], self.__endTime)
                siteTree.append({
                    "userId": footstamp["userId"],
                    "userName": self.__firebase.getUserDataById(footstamp["userId"])["name"],
                    "layer": layer,
                    "infectedSite": userTree
                })
                self.__infectedUserIdSet.add(footstamp["userId"])
        return siteTree

# inputData = {
#         'userId':,
#         'managerId':
#         'spreadStrength':,
#         'confirmedTime':,
#     }