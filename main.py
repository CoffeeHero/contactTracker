from cloudFunctionCaller import cloudFunctionCallerHttp
from contactTracing import ContactTracker
from datetime import datetime
import time
import config

def epidemicPrevention(request):
    event = request.get_json()
    contactTracker = ContactTracker(event["infectedUserList"][0]["confirmedTime"]-event["lurkingTimeSpan"], event["infectedUserList"][0]["confirmedTime"]+event["lurkingTimeSpan"], event["overlappingTime"], event["infectedUserList"], event["spreadStrength"])
    contactTracker.run()

    # Line
    lineModel = contactTracker.getLineResult()
    lineModel["manager"]["managerUserId"] = event["managerId"]
    lineModel["confirmedCustomer"] = {
        "userId":event["infectedUserList"][0]["userId"],
        "infectedTimestamp":event["infectedUserList"][0]["confirmedTime"]
    }


    return contactTracker.getWebResult()



# if __name__ == '__main__':
#     epidemicPrevention([],0,0,0,0)

# input = {
#     "inftectedUserList":[{
#         "userId":"string",
#         "confirmedTime":"float"
#     }],
#     "overlappingTime":"float",
#     "lurkingTimeSpan":"float",
#     "spreadStrength":"int", # 0 for infinity
#     "managerId":"string"
# }


# web output = {
#     "infectedUserCount": "int",
#     "infectedSiteCount": "int",
#     "infectedFootprintCount": "int",
#     "transmissionChain":[{
#         "userId":"string",
#         "userName":"string",
#         "layer":"float",
#         "infectedSite":[{
#             "siteId":"string",
#             "siteName":"string",
#             "visitedUser":[]
#         }]
#     }]
# }

# line output = {
#     "manager":{
#         "managerUserId": "string", // manager uid
#         "infectedUserSize":"int",
#         "infectedSiteSize":"int",
#         "infectedFootprintSize":"int",
#         "infectedUserNameList":[]
        
#     },
#     "customer":[
#         {
#             "userId": "string", // customer uid
#             "infectedHsitoryList": [
#                 {
#                     "infectedStrength": "int",
#                     "infectedSite": "string",
#                     "infectedTimestamp": "float"
#                 }
#             ]
#         }
#     ],
#     "confirmedCustomer":{
#         "userId":"string",
#         "infectedTimestamp":"float"
#     }
# }