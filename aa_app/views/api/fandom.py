from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from aa_app import models

import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@login_required
def newFandom(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    f = models.newFandom(d["name"])
    return EMPTY_JSON_200

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    f = models.Fandom.objects.get(name__iexact = (d["oldName"]))
    f.setName(d["name"])
    return EMPTY_JSON_200
