from django.http import HttpResponse
from django.shortcuts import render

from aa_app import models

import json, datetime

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

def newConvention(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    startDate = datetime.datetime(int(d["startYear"]), int(d["startMonth"]), int(d["startDay"]))
    endDate = datetime.datetime(int(d["endYear"]), int(d["endMonth"]), int(d["endDay"]))
    c = models.newConvention(d["name"], startDate, endDate, int(d["numAttenders"]), d["location"])
    return EMPTY_JSON_200

def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(name = (d["conID"]))
    c.setName(d["name"])
    return EMPTY_JSON_200

def setNumAttenders(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(name = (d["conID"]))
    c.setNumAttenders(int(d["numAttenders"]))
    return EMPTY_JSON_200

def setLocation(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(name = (d["conID"]))
    c.setLocation(d["location"])
    return EMPTY_JSON_200

def setStartDate(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(name = (d["conID"]))
    c.setStartDate(datetime.datetime(int(d["startYear"]), int(d["startMonth"]), int(d["startDay"])))
    return EMPTY_JSON_200

def setEndDate(request):
    d = json.loads(bytes.decode(request.body))
    u = models.User.objects.get(cookieID = request.session["cookieID"])
    c = models.Convention.objects.get(name = (d["conID"]))
    c.setEndDate(datetime.datetime(int(d["endYear"]), int(d["endMonth"]), int(d["endDay"])))
    return EMPTY_JSON_200
