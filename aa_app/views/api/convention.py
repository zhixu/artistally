from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

import json, datetime

@login_required
def newConvention(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        startDate = datetime.datetime.strptime(d["startDate"], "%Y-%m-%d")
        endDate = datetime.datetime.strptime(d["endDate"], "%Y-%m-%d")
        c = models.newConvention(d["name"], startDate, endDate, int(d["numAttenders"]), d["location"], d["website"])
        if "image" in d:
            c.setImage(d["image"])
        if "prevConID" in d:
            c.setPrevCon(models.Convention.objects.get(ID = int(d["prevConID"])))
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({"conID": c.ID})

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setName(d["name"])
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setNumAttenders(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setNumAttenders(int(d["numAttenders"]))
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setLocation(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setLocation(d["location"])
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setStartDate(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setStartDate(datetime.datetime.strptime(d["startDate"], "%Y-%m-%d"))
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setEndDate(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setEndDate(datetime.datetime.strptime(d["endDate"], "%Y-%m-%d"))
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setWebsite(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setWebsite(d["website"])
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setImage(d["image"])
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setPrevCon(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setPrevCon(models.Convention.objects.get(ID = int(d["prevConID"])))
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find one or both conventions"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setUser(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setUser(u)
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def unsetUser(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.unsetUser(u)
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def copyInventory(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        if c == models.INV_CON:
            return JsonResponse({"error": "invalid: convention"}, status = 400)
        for i in u.items.filter(convention = models.INV_CON):
            nI = models.newItem(u, c, i.name, i.fandom, i.kind, i.price, i.cost, i.numSold, i.numLeft)
            if i.image:
                nI.setImage(i.image)
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})
