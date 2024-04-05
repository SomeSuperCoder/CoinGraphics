import requests
import json

def balance_def(id):
    id_user = id.replace("ID: ", "")
    return json.loads(requests.get(f"http://127.0.0.1:8000/get_account/{id_user}").text)["balance"]
