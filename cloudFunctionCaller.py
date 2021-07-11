from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import config

def cloudFunctionCallerHttp(method = "POST", headers = {} , body = {}, url = ""):
    createCreds = service_account.IDTokenCredentials.from_service_account_file(config.GCF_service_account_credentials, target_audience=url)
    create_session = AuthorizedSession(createCreds)
    if method == "POST":
        response = create_session.post(url, headers = headers, json = body)
    elif method == "GET":
        response = create_session.get(url, headers = headers, json = body)
    print(response)
    print(response.text)
    return response