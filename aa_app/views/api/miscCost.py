from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

from decimal import Decimal
import json

@login_required
def newMiscCost(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        m = models.newMiscCost(u, e, Decimal(d["amount"]))
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({"miscCostID": m.ID})

@login_required
def setAmount(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        m = models.MiscCost.objects.get(ID = int(d["miscCostID"]))
        if m.user != u:
            return JsonResponse({"error": "not your miscCost"}, status = 400)
        m.setAmount(Decimal(d["amount"]))
    except models.MiscCost.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the miscCost"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
