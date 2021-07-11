from cloudFunctionCaller import cloudFunctionCallerHttp
from contactTracing import ContactTracker
from datetime import datetime
import time
import config

def epidemicPrevention(confirmedUserIdList, beginTime, endTime, overlappingTime, levelLimit):
    contactTracker = ContactTracker(beginTime, endTime, overlappingTime, confirmedUserIdList, levelLimit)
    contactTracker.run()
    # contactTracker.getWebResult()
    # contactTracker.getBigQueryResult()
    # contactTracker.getLineResult()

if __name__ == '__main__':
    epidemicPrevention([],0,0,0,0)