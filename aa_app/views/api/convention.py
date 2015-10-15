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
        c = models.newConvention(d["name"], d["website"])
        if "image" in d:
            c.setImage(d["image"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({"conID": c.ID})

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setName(d["name"])
    except models.Convention.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setWebsite(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setWebsite(d["website"])
    except models.Convention.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setImage(d["image"])
    except models.Convention.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setUser(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.setUser(u)
    except models.Convention.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def unsetUser(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        c.unsetUser(u)
    except models.Convention.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the convention"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
