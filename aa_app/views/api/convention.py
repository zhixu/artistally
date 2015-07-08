from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

import json, datetime

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def newConvention(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    startDate = datetime.datetime.strptime(d["startDate"], '%Y-%m-%d')
    endDate = datetime.datetime.strptime(d["endDate"], '%Y-%m-%d')
    c = models.newConvention(d["name"], startDate, endDate, int(d["numAttenders"]), d["location"])
    return HttpResponse(json.dumps({"conID": c.ID}), content_type = "application/json")

def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = (d["conID"]))
    c.setName(d["name"])
    return EMPTY_JSON_200

def setNumAttenders(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = (d["conID"]))
    c.setNumAttenders(int(d["numAttenders"]))
    return EMPTY_JSON_200

def setLocation(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = (d["conID"]))
    c.setLocation(d["location"])
    return EMPTY_JSON_200

def setStartDate(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = (d["conID"]))
    c.setStartDate(datetime.datetime.strptime(d["startDate"], '%Y-%m-%d'))
    return EMPTY_JSON_200

def setEndDate(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = (d["conID"]))
    c.setEndDate(datetime.datetime.strptime(d["endDate"], '%Y-%m-%d'))
    return EMPTY_JSON_200

def setWebsite(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(ID = (d["conID"]))
    c.setWebsite(d["website"])
    return EMPTY_JSON_200
