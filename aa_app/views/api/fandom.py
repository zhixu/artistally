from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

import json

EMPTY_JSON_200 = JsonResponse({})

@login_required
def newFandom(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        f = models.newFandom(d["name"])
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return EMPTY_JSON_200

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        f = models.Fandom.objects.get(name__iexact = d["oldName"])
        f.setName(d["name"])
    except models.Fandom.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the fandom"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return EMPTY_JSON_200
