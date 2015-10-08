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
    return render_to_response("about.html", context)

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
    conID = int(conID)
    if conID == models.INV_CON.ID:
        raise Http404("Accessing the INV_CON is disallowed.")
    context = RequestContext(request)
    context["convention"] = get_object_or_404(models.Convention, ID = conID)
    itemKindsCounter = {}
    itemFandomsCounter = {}
    itemsSoldTotal = context["convention"].items.aggregate(Sum("numSold"))["numSold__sum"] or 0
    for k in context["convention"].items.all():
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
    context["conTopItemKinds"] = sorted(itemKindsCounter.items(), key = operator.itemgetter(1), reverse = True)
    context["conTopItemFandoms"] = sorted(itemFandomsCounter.items(), key = operator.itemgetter(1), reverse = True)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
        context["currUserConItems"] = u.items.filter(convention = context["convention"])
        if u.writeups.filter(convention = context["convention"]).exists():
            context["currUserConWriteup"] = u.writeups.get(convention = context["convention"])
    return render_to_response("convention.html", context)

def conreviews(request, conID):
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    context["convention"] = get_object_or_404(models.Convention, ID = conID)
    return render_to_response("conreviews.html", context)

@login_required
def inventory(request, conID = None):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    if conID != None and get_object_or_404(models.Convention, ID = int(conID)) != models.INV_CON:
        conID = int(conID)
        context["convention"] = get_object_or_404(models.Convention, ID = conID)
        if u.miscCosts.filter(convention = context["convention"]).exists():
            context["miscCost"] = u.miscCosts.get(convention = context["convention"])
    else:
        context["convention"] = models.INV_CON
        context["invCon"] = True
    context["kinds"] = list(models.Kind.objects.all())
    context["fandoms"] = list(models.Fandom.objects.all())
    context["conItems"] = u.items.filter(convention = context["convention"])
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
    context["cons"] = models.Convention.objects.exclude(ID = models.INV_CON.ID)
    return render_to_response("addconvention.html", context)

@login_required
def addwriteup(request, conID = None):
    u = request.user
    context = RequestContext(request, {"currUser": u})
    context["cons"] = models.Convention.objects.exclude(ID = models.INV_CON.ID)
    if conID != None:
        conID = int(conID)
        if conID == models.INV_CON.ID:
            raise Http404("Reviewing the INV_CON is disallowed.")
        context["currCon"] = get_object_or_404(models.Convention, ID = conID)
    return render_to_response("addwriteup.html", context)

#@login_required
#def addkind(request):
#    u = request.user
#    context = RequestContext(request, {"currUser": u})
#    return render_to_response("addkind.html", context)
    
#@login_required
#def addfandom(request):
#    u = request.user
#    context = RequestContext(request, {"currUser": u})
#    return render_to_response("addfandom.html", context)

#@login_required
#def additem(request, conID = None):
#    u = request.user
#    context = RequestContext(request, {"currUser": u})
#    context["cons"] = models.Convention.objects.exclude(ID = models.INV_CON.ID)
#    context["kinds"] = models.Kind.objects.all()
#    context["fandoms"] = models.Fandom.objects.all()
#    if conID != None:
#        assert int(conID) != models.INV_CON.ID, "you can't make an item for the INV_CON"
#        context["currCon"] = models.Convention.objects.get(ID = int(conID))
#    return render_to_response("additem.html", context)
        
def item(request, itemID):
    itemID = int(itemID)
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    context["item"] = get_object_or_404(models.Item, ID = itemID)
    return render_to_response("item.html", context)
        
def writeup(request, writeupID):
    writeupID = int(writeupID)
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    context["writeup"] = get_object_or_404(models.Writeup, ID = writeupID)
    #context["miscCost"] = u.miscCosts.get(convention = context["writeup"].convention)
    return render_to_response("writeup.html", context)

def search(request, query):
    context = RequestContext(request)
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    context["query"] = query
    context["cons"] = models.Convention.objects.filter(Q(name__icontains = query) | Q(location__icontains = query) | Q(website__icontains = query)).exclude(ID = models.INV_CON.ID).distinct()
    return render_to_response("search.html", context)
    