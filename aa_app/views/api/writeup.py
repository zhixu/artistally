from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = JsonResponse({})

@login_required
def newWriteup(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        w = models.newWriteup(u, c, int(d["rating"]), d["review"])
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "invalid: convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({"writeupID": w.ID})

@login_required
def setRating(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        w = models.Writeup.objects.get(ID = int(d["writeupID"]))
        if w.user != u:
            return JsonResponse({"error": "not your writeup"}, status = 400)
        w.setRating(int(d["rating"]))
    except models.Writeup.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the writeup"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return EMPTY_JSON_200

@login_required
def setReview(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        w = models.Writeup.objects.get(ID = int(d["writeupID"]))
        if w.user != u:
            return JsonResponse({"error": "not your writeup"}, status = 400)
        w.setReview(d["review"])
    except models.Writeup.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the writeup"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return EMPTY_JSON_200
