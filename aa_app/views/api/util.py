from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

from aa_app import models

import base64, json

import requests # python-requests.org

@login_required
#@user_passes_test(lambda u: not u.confirmToken)
def uploadFile(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    f = base64.b64decode(d["file"])
    r = requests.post("https://m.fuwa.se/api/upload", files = {"file[]": f}).json()[0]
    url = "https://fuwa.se" + r["url"] if r["status"] == "error" and r["error"] == "exists" else r["url"] 
    return JsonResponse({"url": url})

def findFandom(request):
    d = json.loads(bytes.decode(request.body))
    fs = models.Fandom.objects.filter(name__icontains = (d["query"])).annotate(Count("items")).order_by("-items__count")
    return JsonResponse({"results": [f.name for f in fs[:10]]})

def findKind(request):
    d = json.loads(bytes.decode(request.body))
    ks = models.Kind.objects.filter(name__icontains = (d["query"])).annotate(Count("items")).order_by("-items__count")
    return JsonResponse({"results": [k.name for k in ks[:10]]})

@login_required
#@user_passes_test(lambda u: not u.confirmToken)
def contactUs(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    u.sendFeedback(d["subject"], d["body"])
    return JsonResponse({})