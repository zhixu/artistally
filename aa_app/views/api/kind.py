from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

import json

@login_required
def newKind(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        k = models.newKind(d["name"])
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        k = models.Kind.objects.get(name__iexact = d["oldName"])
        k.setName(d["name"])
    except models.Kind.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the kind"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({})
