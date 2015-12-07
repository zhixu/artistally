from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError

from aa_app import models

import json

@login_required
@user_passes_test(lambda u: not u.confirmToken)
def newFandom(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        f = models.newFandom(d["name"])
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})

@login_required
@user_passes_test(lambda u: not u.confirmToken)
def setName(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    try:
        f = models.Fandom.objects.get(name__iexact = d["oldName"])
        f.setName(d["name"])
    except models.Fandom.DoesNotExist as ex:
        return JsonResponse({"error": "couldn't find the fandom"}, status = 400)
    except ValidationError as ex:
        return JsonResponse({"error": "invalid: %s" % ", ".join(ex.message_dict.keys())}, status = 400)
    return JsonResponse({})
