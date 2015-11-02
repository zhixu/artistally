from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q

from aa_app import models

import json, datetime, uuid

@login_required
def newEvent(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        startDate = datetime.datetime.strptime(d["startDate"], "%Y-%m-%d")
        endDate = datetime.datetime.strptime(d["endDate"], "%Y-%m-%d")
        c = models.Convention.objects.get(ID = int(d["conID"]))
        e = models.newEvent(c, d["name"], startDate, endDate, d["location"])
        if "numAttenders" in d:
            e.setNumAttenders(int(d["numAttenders"]))
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({"eventID": e.ID})

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        e.setName(d["name"])
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setNumAttenders(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        e.setNumAttenders(int(d["numAttenders"]))
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setLocation(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        e.setLocation(d["location"])
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setStartDate(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        e.setStartDate(datetime.datetime.strptime(d["startDate"], "%Y-%m-%d"))
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setEndDate(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        e.setEndDate(datetime.datetime.strptime(d["endDate"], "%Y-%m-%d"))
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def copyInventory(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        if e == models.INV_EVENT:
            return JsonResponse({"error": "invalid: event"}, status = 400)
        for i in u.items.filter(event = models.INV_EVENT):
            nI = None
            if not i.tag:
                iTag = uuid.uuid4()
                while u.items.filter(tag = iTag).exists():
                    iTag = uuid.uuid4()
                i.setTag(uuid.uuid4())
            else:
                nI = u.items.get(Q(event = e) & Q(tag = i.tag))
            if nI:
                nI.setName(i.name)
                nI.setFandom(i.fandom)
                nI.setKind(i.kind)
                nI.setPrice(i.price)
                nI.setCost(i.cost)
                nI.setNumSold(i.numSold)
                nI.setNumleft(i.numLeft)
                nI.setImage(i.image)
            else:
                nI = models.newItem(u, e, i.name, i.fandom, i.kind, i.price, i.cost, i.numSold, i.numLeft)
                nI.setImage(i.image)
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def recopyInventory(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        if e == models.INV_EVENT:
            return JsonResponse({"error": "invalid: event"}, status = 400)
        for i in u.items.filter(event = e):
            nI = None
            if not i.tag:
                iTag = uuid.uuid4()
                while u.items.filter(tag = iTag).exists():
                    iTag = uuid.uuid4()
                i.setTag(uuid.uuid4())
            else:
                nI = u.items.get(Q(event = models.INV_EVENT) & Q(tag = i.tag))
            if nI:
                nI.setName(i.name)
                nI.setFandom(i.fandom)
                nI.setKind(i.kind)
                nI.setPrice(i.price)
                nI.setCost(i.cost)
                nI.setNumSold(0)
                nI.setNumleft(i.numLeft)
                nI.setImage(i.image)
            else:
                nI = models.newItem(u, models.INV_EVENT, i.name, i.fandom, i.kind, i.price, i.cost, 0, i.numLeft)
                nI.setImage(i.image)
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def spillInventory(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        if e == models.INV_EVENT:
            return JsonResponse({"error": "invalid: event"}, status = 400)
        u.items.filter(event = e).delete()
        for i in u.items.filter(event = models.INV_EVENT):
            if not i.tag:
                iTag = uuid.uuid4()
                while u.items.filter(tag = iTag).exists():
                    iTag = uuid.uuid4()
                i.setTag(uuid.uuid4())
            nI = models.newItem(u, e, i.name, i.fandom, i.kind, i.price, i.cost, i.numSold, i.numLeft)
            nI.setImage(i.image)
            nI.setTag(i.tag)
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def respillInventory(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        if e == models.INV_EVENT:
            return JsonResponse({"error": "invalid: event"}, status = 400)
        u.items.filter(event = models.INV_EVENT).delete()
        for i in u.items.filter(event = e):
            if not i.tag:
                iTag = uuid.uuid4()
                while u.items.filter(tag = iTag).exists():
                    iTag = uuid.uuid4()
                i.setTag(uuid.uuid4())
            nI = models.newItem(u, models.INV_EVENT, i.name, i.fandom, i.kind, i.price, i.cost, 0, i.numLeft)
            nI.setImage(i.image)
            nI.setTag(i.tag)
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
