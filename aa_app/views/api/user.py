from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError

from aa_app import models

import json, uuid

@user_passes_test(lambda u: u.is_anonymous())
def newUser(request):
    d = json.loads(bytes.decode(request.body))
    try:
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
        u.sendConfirmEmail()
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@user_passes_test(lambda u: u.is_anonymous())
def login(request):
    d = json.loads(bytes.decode(request.body))
    u = auth.authenticate(username = d["username"], password = d["password"])
    if u is None:
        return JsonResponse({"error": "bad login attempt"}, status = 400)
    auth.login(request, u)
    return JsonResponse({})

@login_required
def logout(request):
    auth.logout(request)
    return JsonResponse({})

@user_passes_test(lambda u: u.confirmToken)
@login_required
def resendConfirmEmail(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.sendConfirmEmail()
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
@user_passes_test(lambda u: u.confirmToken)
def checkConfirmToken(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        if u.confirmToken != uuid.UUID(d["token"]):
            return JsonResponse({"error": "wrong token"}, status = 400)
        u.setConfirmToken(None)
    except ValueError as ex:    # raised by uuid.UUID() conversion of string
        return JsonResponse({"error": "wrong token"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@user_passes_test(lambda u: u.is_anonymous())
def requestReset(request):
    d = json.loads(bytes.decode(request.body))
    try:
        u = models.User.objects.get(email = d["email"])
        u.sendResetEmail()
    except models.User.DoesNotExist as ex:
        return JsonResponse({"error": "no user with that email"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@user_passes_test(lambda u: u.is_anonymous())
def checkResetToken(request):
    d = json.loads(bytes.decode(request.body))
    try:
        u = models.User.objects.get(email = d["email"])
        if u.resetToken != uuid.UUID(d["token"]):
            return JsonResponse({"error": "wrong token"}, status = 400)
        u.setPassword(d["token"])
        u.setResetToken(None)
    except ValueError as ex:    # raised by uuid.UUID() conversion of string
        return JsonResponse({"error": "wrong token"}, status = 400)
    except models.User.DoesNotExist as ex:
        return JsonResponse({"error": "no user with that email"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setEmail(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.setEmail(d["email"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setPassword(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    if not u.check_password(d["oldPassword"]):
        return JsonResponse({"error": "wrong current password"}, status = 400)
    u.setPassword(d["password"])
    return JsonResponse({})

@login_required
def setStartYear(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        if d["startYear"] == "":
            u.setStartYear(None)
        else:
            u.setStartYear(int(d["startYear"]))
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setImage(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.setImage(d["image"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setDescription(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.setDescription(d["description"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setWebsite1(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.setWebsite1(d["website1"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setWebsite2(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.setWebsite2(d["website2"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
def setWebsite3(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        u.setWebsite3(d["website3"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
