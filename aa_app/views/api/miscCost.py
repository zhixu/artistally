from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError

from aa_app import models

from decimal import Decimal
import json

@login_required
@user_passes_test(lambda u: not u.confirmToken)
def newMiscCost(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        e = models.Event.objects.get(ID = int(d["eventID"]))
        m = models.newMiscCost(u, e, Decimal(d["amount"]), d["name"])
    except models.Event.DoesNotExist as ex:
        return JsonResponse({"error": "invalid: event"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({"miscCostID": m.ID})

@login_required
@user_passes_test(lambda u: not u.confirmToken)
def deleteMiscCost(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        m = models.MiscCost.objects.get(ID = int(d["miscCostID"]))
        if m.user != u:
            return JsonResponse({"error": "not your miscCost"}, status = 400)
        m.delete()
    except models.MiscCost.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the item"}, status = 400)
    return JsonResponse({})

@login_required
@user_passes_test(lambda u: not u.confirmToken)
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

@login_required
@user_passes_test(lambda u: not u.confirmToken)
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        m = models.MiscCost.objects.get(ID = int(d["miscCostID"]))
        if m.user != u:
            return JsonResponse({"error": "not your miscCost"}, status = 400)
        m.setName(d["name"])
    except models.MiscCost.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the miscCost"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
