from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

import base64, json

import requests

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def uploadFile(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    f = base64.b64decode(d["file"])
    r = requests.post("https://fuwa.se/api/upload", files = {"file[]": f}).json()[0]
    url = "https://fuwa.se" + r["url"] if r["status"] == "error" and r["error"] == "exists" else r["url"] 
    print(url)
    return HttpResponse(json.dumps({"url": url}), content_type = "application/json")
