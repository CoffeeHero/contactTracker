class ContactTracker:
    def __init__(self, beginTime = 0, endTime = 0, overlappingTime = 0, confirmedUserIdList = [], levelLimit = 0):
        self.__beginTime = beginTime - overlappingTime
        self.__endTime = endTime + overlappingTime
        self.__overlappingTime = overlappingTime
        self.__confirmedUserIdList = confirmedUserIdList
        self.__levelLimit = levelLimit

        self.__recursive = 0

    def setTime(self, beginTime, endTime, overlappingTime):
        self.__beginTime = beginTime - overlappingTime
        self.__endTime = endTime + overlappingTime
        self.__overlappingTime = overlappingTime

    def setConfirmedUserIdList(self, confirmedUserIdList):
        self.__confirmedUserIdList = confirmedUserIdList

    def run(self):
        self.recursiveTest()

    def recursiveTest(self):
        print("recursive: ", self.__recursive)
        if(self.__recursive!=100):
            self.__recursive = self.__recursive+1
            self.recursiveTest()