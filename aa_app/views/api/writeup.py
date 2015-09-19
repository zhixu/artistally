from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from aa_app import models

from decimal import Decimal
import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@login_required
def newWriteup(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    c = models.Convention.objects.get(ID = int(d["conID"]))
    w = models.newWriteup(u, c, int(d["rating"]), d["review"])
    return HttpResponse(json.dumps({"writeupID": w.ID}), content_type = "application/json")

@login_required
def setRating(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    w = models.Writeup.objects.get(ID = int(d["writeupID"]))
    assert w.user == u, "not your writeup"
    w.setRating(int(d["rating"]))
    return EMPTY_JSON_200

@login_required
def setReview(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    w = models.Writeup.objects.get(ID = int(d["writeupID"]))
    assert w.user == u, "not your writeup"
    w.setReview(d["review"])
    return EMPTY_JSON_200
