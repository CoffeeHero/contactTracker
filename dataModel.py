input = {
    "inftectedUserList":[{
        "userId":"string",
        "confirmedTime":"float"
    }],
    "overlappingTime":"float",
    "lurkingTimeSpan":"float",
    "spreadStrength":"int", # 0 for infinity
    "managerId":"string"
}


output = {
    "inftectedUserCount": "int",
    "inftectedSiteCount": "int",
    "inftectedFootprintCount": "int",
    "transmissionChain":[{
        "userId":"string",
        "userName":"string",
        "layer":"float",
        "infectedSite":[{
            "siteId":"string",
            "siteName":"string",
            "visitedUser":[]
        }]
    }]
}