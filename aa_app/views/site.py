from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.db.models import Sum, Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

import operator

from aa_app import models

def root(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
        context["currUserItemsSold"] = u.items.aggregate(Sum("numSold"))["numSold__sum"] or 0
    return render_to_response("root.html", context)

def about(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    return render_to_response("about.html", context)

@ensure_csrf_cookie
def signup(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        resp = HttpResponse(status = 307)
        resp["Location"] = "/"
        return resp
    else:
        return render_to_response("signup.html", context)
    
@ensure_csrf_cookie
def login(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        resp = HttpResponse(status = 307)
        resp["Location"] = "/"
        return resp
    else:
        return render_to_response("login.html", context)

def user(request, username):
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    context["pageUser"] = get_object_or_404(models.User, username = username)
    return render_to_response("user.html", context)

def convention(request, conID):
    context = RequestContext(request)
    context["convention"] = get_object_or_404(models.Convention, ID = int(conID))
    if context["convention"] == models.INV_CON:
        raise Http404("Accessing the INV_CON is disallowed.")
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    return render_to_response("convention.html", context)

def event(request, eventID):
    context = RequestContext(request)
    context["event"] = get_object_or_404(models.Event, ID = int(eventID))
    if context["event"] == models.INV_EVENT:
        raise Http404("Accessing the INV_EVENT is disallowed.")
    itemKindsCounter = {}
    itemFandomsCounter = {}
    itemsSoldTotal = context["event"].items.aggregate(Sum("numSold"))["numSold__sum"] or 0
    for k in context["event"].items.all():
        if k.kind in itemKindsCounter:
            itemKindsCounter[k.kind] += k.numSold
        else:
            itemKindsCounter[k.kind] = k.numSold
        if k.fandom in itemFandomsCounter:
            itemFandomsCounter[k.fandom] += k.numSold
        else:
            itemFandomsCounter[k.fandom] = k.numSold
    if itemsSoldTotal:
        for k in itemKindsCounter:
            itemKindsCounter[k] /= itemsSoldTotal
        for k in itemFandomsCounter:
            itemFandomsCounter[k] /= itemsSoldTotal
    context["eventTopItemKinds"] = sorted(itemKindsCounter.items(), key = operator.itemgetter(1), reverse = True)
    context["eventTopItemFandoms"] = sorted(itemFandomsCounter.items(), key = operator.itemgetter(1), reverse = True)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
        if u.writeups.filter(event = context["event"]).exists():
            context["currUserEventWriteup"] = u.writeups.get(event = context["event"])
    return render_to_response("event.html", context)

def eventreviews(request, eventID):
    context["event"] = get_object_or_404(models.Event, ID = int(eventID))
    if context["event"] == models.INV_EVENT:
        raise Http404("Accessing the INV_EVENT is disallowed.")
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
        if u.writeups.filter(event = context["event"]).exists():
            context["currUserEventWriteup"] = u.writeups.get(event = context["event"])
    return render_to_response("eventreviews.html", context)

@login_required
def inventory(request, eventID = None):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    if eventID != None and get_object_or_404(models.Event, ID = int(eventID)) != models.INV_EVENT:
        eventID = int(eventID)
        context["event"] = get_object_or_404(models.Event, ID = int(eventID))
        if u.miscCosts.filter(event = context["event"]).exists():
            context["miscCost"] = u.miscCosts.get(event = context["event"])
    else:
        context["event"] = models.INV_EVENT
        context["invEvent"] = True
    context["kinds"] = list(models.Kind.objects.all())
    context["fandoms"] = list(models.Fandom.objects.all())
    context["eventItems"] = u.items.filter(event = context["event"])
    return render_to_response("inventory.html", context)

@login_required
def myconventions(request):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    return render_to_response("myconventions.html", context)

@login_required
def mywriteups(request):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    return render_to_response("mywriteups.html", context)
    
@login_required
def addconvention(request):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    return render_to_response("addconvention.html", context)
    
@login_required
def addevent(request, conID):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    context["convention"] = get_object_or_404(models.Convention, ID = int(conID))
    if context["convention"] == models.INV_CON:
        raise Http404("Accessing the INV_CON is disallowed.")
    return render_to_response("addevent.html", context)
        
def writeup(request, writeupID):
    writeupID = int(writeupID)
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    context["writeup"] = get_object_or_404(models.Writeup, ID = writeupID)
    return render_to_response("writeup.html", context)

def search(request, query = None):
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    if query is None:
        query = ""
    context["query"] = query
    context["cons"] = models.Convention.objects.filter(Q(name__icontains = query) | Q(website__icontains = query)).exclude(ID = models.INV_CON.ID).distinct()
    return render_to_response("search.html", context)
    