from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def newFandom(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    f = models.newFandom(d["name"])
    return EMPTY_JSON_200

def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    f = models.Fandom.objects.get(name = (d["oldName"]))
    f.setName(d["name"])
    return EMPTY_JSON_200
