from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from aa_app import models

import json, datetime

EMPTY_JSON_200 = JsonResponse({})

@login_required
def newConvention(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    startDate = datetime.datetime.strptime(d["startDate"], "%Y-%m-%d")
    endDate = datetime.datetime.strptime(d["endDate"], "%Y-%m-%d")
    c = models.newConvention(d["name"], startDate, endDate, int(d["numAttenders"]), d["location"], d["website"])
    if "image" in d:
        c.setImage(d["image"])
    if "prevConID" in d:
        c.setPrevCon(models.Convention.objects.get(ID = int(d["prevConID"])))
    return JsonResponse({"conID": c.ID})

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setName(d["name"])
    return EMPTY_JSON_200

@login_required
def setNumAttenders(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setNumAttenders(int(d["numAttenders"]))
    return EMPTY_JSON_200

@login_required
def setLocation(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setLocation(d["location"])
    return EMPTY_JSON_200

@login_required
def setStartDate(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setStartDate(datetime.datetime.strptime(d["startDate"], "%Y-%m-%d"))
    return EMPTY_JSON_200

@login_required
def setEndDate(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setEndDate(datetime.datetime.strptime(d["endDate"], "%Y-%m-%d"))
    return EMPTY_JSON_200

@login_required
def setWebsite(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setWebsite(d["website"])
    return EMPTY_JSON_200

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setImage(d["image"])
    return EMPTY_JSON_200

@login_required
def setPrevCon(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    c.setPrevCon(models.Convention.objects.get(ID = int(d["prevConID"])))
    return EMPTY_JSON_200
