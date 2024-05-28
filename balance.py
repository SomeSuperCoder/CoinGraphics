import requests
import json
from url import url


def balance_def(id):
    id_user = id.replace("ID: ", "")
    return json.loads(requests.get(f"{url}/get_account/{id_user}").text)["balance"]
