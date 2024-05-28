import requests

url = "https://kvantomat.serveo.net"


def met(new_url, urls):
    global url
    if requests.get("https://github.com/"):
        url = new_url
    return url
