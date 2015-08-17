from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@login_required
def newMiscCost(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    m = models.newMiscCost(u, c, Decimal(d["amount"]))
    return HttpResponse(json.dumps({"miscCostID": m.ID}), content_type = "application/json")

@login_required
def setAmount(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    m = models.MiscCost.objects.get(ID = int(d["miscCostID"]))
    assert m.user == u, "not your miscCost"
    m.setAmount(int(d["amount"]))
    return EMPTY_JSON_200
