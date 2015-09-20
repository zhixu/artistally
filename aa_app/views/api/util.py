from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from aa_app import models

import base64, json

import requests # python-requests.org

EMPTY_JSON_200 = HttpResponse(json.dumps({}), content_type = "application/json")

@login_required
def uploadFile(request):
    d = json.loads(bytes.decode(request.body))
    u = request.user
    f = base64.b64decode(d["file"])
    r = requests.post("https://fuwa.se/api/upload", files = {"file[]": f}).json()[0]
    url = "https://fuwa.se" + r["url"] if r["status"] == "error" and r["error"] == "exists" else r["url"] 
    print(url)
    return HttpResponse(json.dumps({"url": url}), content_type = "application/json")

def findFandom(request):
    d = json.loads(bytes.decode(request.body))
    fs = models.Fandom.objects.filter(name__icontains = (d["query"])).annotate(Count("items")).order_by("-items__count")
    return HttpResponse(json.dumps({"results": [f.name for f in fs[:10]]}), content_type = "application/json")

def findKind(request):
    d = json.loads(bytes.decode(request.body))
    ks = models.Kind.objects.filter(name__icontains = (d["query"])).annotate(Count("items")).order_by("-items__count")
    return HttpResponse(json.dumps({"results": [k.name for k in ks[:10]]}), content_type = "application/json")
