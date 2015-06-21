from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def newItem(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    convention = models.Convention.objects.get(ID = int(d["conID"]))
    fandom = models.Fandom.objects.get(name = d["fandom"])
    kind = models.Kind.objects.get(name = d["kind"])
    i = models.newItem(u, convention, d["name"], fandom, kind, Decimal(d["price"]), Decimal(d["cost"]), int(d["numSold"]), int(d["numLeft"]))
    return HttpResponse(json.dumps({"itemID": i.ID}), content_type = "application/json")

def setNumSold(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setNumSold(int(d["numSold"]))
    return EMPTY_JSON_200

def setNumLeft(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setNumLeft(int(d["numLeft"]))
    return EMPTY_JSON_200

def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setName(d["name"])
    return EMPTY_JSON_200
