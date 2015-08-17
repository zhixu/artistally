from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@login_required
def newItem(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    convention = models.Convention.objects.get(ID = int(d["conID"]))
    fandom = models.Fandom.objects.get(name = d["fandom"])
    kind = models.Kind.objects.get(name = d["kind"])
    i = models.newItem(u, convention, d["name"], fandom, kind, Decimal(d["price"]), Decimal(d["cost"]), int(d["numSold"]), int(d["numLeft"]))
    if "image" in d and d["image"] != "":
        i.setImage(d["image"])
    return HttpResponse(json.dumps({"itemID": i.ID}), content_type = "application/json")

@login_required
def setNumSold(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setNumSold(int(d["numSold"]))
    return EMPTY_JSON_200

@login_required
def setNumLeft(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setNumLeft(int(d["numLeft"]))
    return EMPTY_JSON_200

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setName(d["name"])
    return EMPTY_JSON_200

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    i = models.Item.objects.get(ID = int(d["itemID"]))
    assert i.user == u, "not your item"
    i.setImage(d["image"] if d["image"] != "" else None)
    return EMPTY_JSON_200
