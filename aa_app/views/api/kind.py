from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def newKind(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    k = models.newKind(d["name"])
    return EMPTY_JSON_200

def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    k = models.Kind.objects.get(name = (d["oldName"]))
    k.setName(d["name"])
    return EMPTY_JSON_200
