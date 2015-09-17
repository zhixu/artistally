from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test

from aa_app import models

import json

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@user_passes_test(lambda u: u.is_anonymous())
def newUser(request):
    d = json.loads(bytes.decode(request.body))
    u = models.newUser(d["username"], d["password"], d["email"])
    if "startYear" in d and d["startYear"] != "":
        u.setStartYear(int(d["startYear"]))
    if "image" in d:
        u.setImage(d["image"])
    if "description" in d:
        u.setDescription(d["description"])
    if "website1" in d:
        u.setWebsite1(d["website1"])
    if "website2" in d:
        u.setWebsite2(d["website2"])
    if "website3" in d:
        u.setWebsite3(d["website3"])
    return EMPTY_JSON_200

@user_passes_test(lambda u: u.is_anonymous())
def login(request):
    d = json.loads(bytes.decode(request.body))
    u = auth.authenticate(username = d["username"], password = d["password"])
    assert u, "wrong username or password"
    auth.login(request, u)
    return EMPTY_JSON_200

@login_required
def logout(request):
    auth.logout(request)
    return EMPTY_JSON_200

@login_required
def setEmail(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setEmail(d["email"])
    return EMPTY_JSON_200

@login_required
def setPassword(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    assert u.check_password(d["oldPassword"]), "wrong current password"
    u.setPassword(d["password"])
    return EMPTY_JSON_200

@login_required
def setStartYear(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setStartYear(int(d["startYear"]))
    return EMPTY_JSON_200

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setImage(d["image"])
    return EMPTY_JSON_200

@login_required
def setDescription(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setImage(d["description"])
    return EMPTY_JSON_200

@login_required
def setWebsite1(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setImage(d["website1"])
    return EMPTY_JSON_200

@login_required
def setWebsite2(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setImage(d["website2"])
    return EMPTY_JSON_200

@login_required
def setWebsite3(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.setImage(d["website3"])
    return EMPTY_JSON_200
