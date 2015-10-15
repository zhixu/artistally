from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

from decimal import Decimal
import json

@login_required
def newItem(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        f = models.Fandom.objects.get(name__iexact = d["fandom"])
        k = models.Kind.objects.get(name__iexact = d["kind"])
        i = models.newItem(u, e, d["name"], f, k, Decimal(d["price"]), Decimal(d["cost"]), int(d["numSold"]), int(d["numLeft"]))
        if "image" in d:
            i.setImage(d["image"])
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: event"}, status = 400)
    except models.Fandom.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: fandom"}, status = 400)
    except models.Kind.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: kind"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({"itemID": i.ID})

@login_required
def deleteItem(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.delete()
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    return JsonResponse({})

@login_required
def setNumSold(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setNumSold(int(d["numSold"]))
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setNumLeft(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setNumLeft(int(d["numLeft"]))
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setName(d["name"])
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setImage(d["image"])
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setPrice(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setPrice(Decimal(d["price"]))
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setCost(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setCost(Decimal(d["cost"]))
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setFandom(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setFandom(models.Fandom.objects.get(name__iexact = d["fandom"]))
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except models.Fandom.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: fandom"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setKind(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        i = models.Item.objects.get(ID = int(d["itemID"]))
        if i.user != u:
            return JsonResponse({"error": "not your item"}, status = 400)
        i.setKind(models.Fandom.objects.get(name__iexact = d["kind"]))
    except models.Item.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    except models.Kind.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: kind"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
