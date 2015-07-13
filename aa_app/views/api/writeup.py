from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def newWriteup(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = int(d["conID"]))
    w = models.newWriteup(u, c, int(d["rating"]), d["review"], Decimal(d["miscCosts"]))
    return HttpResponse(json.dumps({"writeupID": w.ID}), content_type = "application/json")

def setRating(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    w = models.Writeup.objects.get(ID = int(d["writeupID"]))
    assert w.user == u, "not your writeup"
    w.setRating(int(d["rating"]))
    return EMPTY_JSON_200

def setReview(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    w = models.Writeup.objects.get(ID = int(d["writeupID"]))
    assert w.user == u, "not your writeup"
    w.setReview(d["review"])
    return EMPTY_JSON_200

def setMiscCosts(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    w = models.Writeup.objects.get(ID = int(d["writeupID"]))
    assert w.user == u, "not your writeup"
    w.setMiscCosts(Decimal(d["miscCosts"]))
    return EMPTY_JSON_200
