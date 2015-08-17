from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from aa_app import models

import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@login_required
def newKind(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    k = models.newKind(d["name"])
    return EMPTY_JSON_200

@login_required
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    k = models.Kind.objects.get(name = (d["oldName"]))
    k.setName(d["name"])
    return EMPTY_JSON_200
