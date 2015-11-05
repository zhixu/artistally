from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.db.models import Sum, Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

import operator, datetime, collections

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

@login_required
def edituser(request):
    context = RequestContext(request)
    u = request.user
    context["currUser"] = u
    return render_to_response("edituser.html", context)

def convention(request, conID):
    context = RequestContext(request)
    context["convention"] = get_object_or_404(models.Convention, ID = int(conID))
    if context["convention"] == models.INV_CON:
        raise Http404("Accessing the INV_CON is disallowed.")
    if request.user.is_authenticated():
        u = request.user
        context["currUser"] = u
    
    year = datetime.timedelta(days = 365, hours = 6)
    voteSum_1Y = collections.Counter()
    voteSum_2Y = collections.Counter()
    voteSum_5Y = collections.Counter()
    voteSum_All = collections.Counter()
    valueSoldSum_1Y = collections.Counter()
    valueSoldSum_2Y = collections.Counter()
    valueSoldSum_5Y = collections.Counter()
    valueSoldSum_All = collections.Counter()
    numSoldSum_1Y = collections.Counter()
    numSoldSum_2Y = collections.Counter()
    numSoldSum_5Y = collections.Counter()
    numSoldSum_All = collections.Counter()
    
    for event in context["convention"].events.all():
        if datetime.date.today() - event.endDate <= year:
            voteSum_1Y += event.kindUserVotes
            valueSoldSum_1Y += event.kindValueSold
            numSoldSum_1Y += event.kindNumSold
        if datetime.date.today() - event.endDate <= 2 * year:
            voteSum_2Y += event.kindUserVotes
            valueSoldSum_2Y += event.kindValueSold
            numSoldSum_2Y += event.kindNumSold
        if datetime.date.today() - event.endDate <= 5 * year:
            voteSum_5Y += event.kindUserVotes
            valueSoldSum_5Y += event.kindValueSold
            numSoldSum_5Y += event.kindNumSold
        voteSum_All += event.kindUserVotes
        valueSoldSum_All += event.kindValueSold
        numSoldSum_All += event.kindNumSold
        
    avgKindPrice_1Y = collections.Counter()
    for kind in valueSoldSum_1Y:
        if numSoldSum_1Y[kind] == 0:
            avgKindPrice_1Y[kind] = None
        else:
            avgKindPrice_1Y[kind] = valueSoldSum_1Y[kind] / numSoldSum_1Y[kind]
    avgKindPrice_2Y = collections.Counter()
    for kind in valueSoldSum_2Y:
        if numSoldSum_2Y[kind] == 0:
            avgKindPrice_2Y[kind] = None
        else:
            avgKindPrice_2Y[kind] = valueSoldSum_2Y[kind] / numSoldSum_2Y[kind]
    avgKindPrice_5Y = collections.Counter()
    for kind in valueSoldSum_5Y:
        if numSoldSum_5Y[kind] == 0:
            avgKindPrice_5Y[kind] = None
        else:
            avgKindPrice_5Y[kind] = valueSoldSum_5Y[kind] / numSoldSum_5Y[kind]
    avgKindPrice_All = collections.Counter()
    for kind in valueSoldSum_1Y:
        if numSoldSum_All[kind] == 0:
            avgKindPrice_All[kind] = None
        else:
            avgKindPrice_All[kind] = valueSoldSum_All[kind] / numSoldSum_All[kind]
        
#    context["votedKinds"] = {}
#    context["votedKindPrices"] = {}
#    context["votedKinds"]["thisYear"] = [k[0] for k in sorted(voteSum_1Y.items(), key=operator.itemgetter(1), reverse = True)]
#    context["votedKindPrices"]["thisYear"] = [avgKindPrice_1Y[k] for k in context["votedKinds"]["thisYear"]]
#    context["votedKinds"]["twoYears"] = [k[0] for k in sorted(voteSum_2Y.items(), key=operator.itemgetter(1), reverse = True)]
#    context["votedKindPrices"]["twoYears"] = [avgKindPrice_2Y[k] for k in context["votedKinds"]["twoYears"]]
#    context["votedKinds"]["fiveYears"] = [k[0] for k in sorted(voteSum_5Y.items(), key=operator.itemgetter(1), reverse = True)]
#    context["votedKindPrices"]["fiveYears"] = [avgKindPrice_5Y[k] for k in context["votedKinds"]["fiveYears"]]
#    context["votedKinds"]["all"] = [k[0] for k in sorted(voteSum_All.items(), key=operator.itemgetter(1), reverse = True)]
#    context["votedKindPrices"]["all"] = [avgKindPrice_All[k] for k in context["votedKinds"]["all"]]

    
    votedKindsThisYear = [k[0] for k in sorted(voteSum_2Y.items(), key=operator.itemgetter(1), reverse = True)]
    votedKindsTwoYears = [k[0] for k in sorted(voteSum_2Y.items(), key=operator.itemgetter(1), reverse = True)]
    votedKindsFiveYears = [k[0] for k in sorted(voteSum_5Y.items(), key=operator.itemgetter(1), reverse = True)]
    votedKindsAll = [k[0] for k in sorted(voteSum_All.items(), key=operator.itemgetter(1), reverse = True)]
    
    votedKindPricesThisYear = [avgKindPrice_1Y[k] for k in votedKindsThisYear]
    votedKindPricesTwoYears = [avgKindPrice_2Y[k] for k in votedKindsTwoYears]
    votedKindPricesFiveYears = [avgKindPrice_5Y[k] for k in votedKindsFiveYears]
    votedKindPricesAll = [avgKindPrice_All[k] for k in votedKindsAll]
    
    context["votedKinds"] = {}
    context["votedKinds"]["thisYear"] = zip(votedKindsThisYear, votedKindPricesThisYear)
    context["votedKinds"]["twoYears"] = zip(votedKindsTwoYears, votedKindPricesTwoYears)
    context["votedKinds"]["fiveYears"] = zip(votedKindsFiveYears, votedKindPricesFiveYears)
    context["votedKinds"]["all"] = zip(votedKindsAll, votedKindPricesAll)

    return render_to_response("convention.html", context)

def event(request, eventID):
    context = RequestContext(request)
    context["event"] = get_object_or_404(models.Event, ID = int(eventID))
    if context["event"] == models.INV_EVENT:
        raise Http404("Accessing the INV_EVENT is disallowed.")
    context["topKinds"] = context["event"].topKinds
    context["topFandoms"] = context["event"].topFandoms
    context["votedKinds"] = [k[0] for k in sorted(context["event"].kindUserVotes.items(), key=operator.itemgetter(1), reverse = True)]
    context["votedKindPrices"] = [context["event"].avgKindPrice[k] for k in context["votedKinds"]]
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
        context["miscCosts"] = u.miscCosts.filter(event = context["event"])
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
    