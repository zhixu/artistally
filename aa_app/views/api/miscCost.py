from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = JsonResponse({})

@login_required
def newMiscCost(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        c = models.Convention.objects.get(ID = int(d["conID"]))
        m = models.newMiscCost(u, c, Decimal(d["amount"]))
    except models.Convention.DoesNotExist as e:
        return JsonResponse({"error": "invalid: convention"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return JsonResponse({"miscCostID": m.ID})

@login_required
def setAmount(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        m = models.MiscCost.objects.get(ID = int(d["miscCostID"]))
        if m.user is not u:
            return JsonResponse({"error": "not your miscCost"}, status = 400)
        m.setAmount(Decimal(d["amount"]))
    except models.MiscCost.DoesNotExist as e:
        return JsonResponse({"error": "couldn't find the miscCost"}, status = 400)
    except ValidationError as e:
        return JsonResponse({"error": "invalid: %s" % ", ".join(e.message_dict.keys())}, status = 400)
    return EMPTY_JSON_200
