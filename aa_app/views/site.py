from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.db.models import Sum, Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie

import operator, datetime, collections

import numpy

from aa_app import models

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def root(request):
    context = {}
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
        context["currUserItemsSold"] = u.items.aggregate(Sum("numSold"))["numSold__sum"] or 0
        context["announcements"] = models.Announcement.objects.all()
    return render(request, "root.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def about(request):
    context = {}
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
    return render(request, "about.html", context)

@ensure_csrf_cookie
@user_passes_test(lambda u: u.is_anonymous(), login_url = "/")
def signup(request):
    context = {}
    return render(request, "signup.html", context)
    
@ensure_csrf_cookie
@user_passes_test(lambda u: u.is_anonymous(), login_url = "/")
def login(request):
    context = {}
    return render(request, "login.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def user(request, username):
    context = {}
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
    context["pageUser"] = get_object_or_404(models.User, username = username)
    return render(request, "user.html", context)

@ensure_csrf_cookie
@user_passes_test(lambda u: u.is_anonymous(), login_url = "/")
def forgot(request):
    context = {}
    return render(request, "forgot.html", context)

@login_required
@user_passes_test(lambda u: u.confirmToken, login_url = "/")
def confirm(request):
    context = {}
    u = context["currUser"] = request.user
    return render(request, "confirm.html", context)

@login_required
def edituser(request):
    context = {}
    u = context["currUser"] = request.user
    return render(request, "edituser.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def convention(request, conID):
    context = {}
    c = context["convention"] = get_object_or_404(models.Convention, ID = int(conID))
    if c == models.INV_CON:
        raise Http404("Accessing the INV_CON is disallowed.")
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
    context["topKinds"] = c.topKinds
    context["topFandoms"] = c.topFandoms
    context["profitCounts"], context["profitBins"] = numpy.histogram(numpy.asarray([c.userProfit(u) for u in c.itemUsers], dtype = "float"), bins = max(1, min(10, c.itemUsers.count())))

    if (min(len(context["topKinds"]), len(context["topFandoms"]), len(context["profitCounts"]), len(context["profitBins"])) is 0):
        context["hasConData"] = False
    else:
        context["hasConData"] = True
    
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

    for event in c.events.all():
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

#    avgKindPrice_1Y = collections.Counter()
#    for kind in valueSoldSum_1Y:
#        if numSoldSum_1Y[kind] == 0:
#            avgKindPrice_1Y[kind] = None
#        else:
#            avgKindPrice_1Y[kind] = valueSoldSum_1Y[kind] / numSoldSum_1Y[kind]
#    avgKindPrice_2Y = collections.Counter()
#    for kind in valueSoldSum_2Y:
#        if numSoldSum_2Y[kind] == 0:
#            avgKindPrice_2Y[kind] = None
#        else:
#            avgKindPrice_2Y[kind] = valueSoldSum_2Y[kind] / numSoldSum_2Y[kind]
#    avgKindPrice_5Y = collections.Counter()
#    for kind in valueSoldSum_5Y:
#        if numSoldSum_5Y[kind] == 0:
#            avgKindPrice_5Y[kind] = None
#        else:
#            avgKindPrice_5Y[kind] = valueSoldSum_5Y[kind] / numSoldSum_5Y[kind]

    avgKindPrice_All = collections.Counter()
    for kind in valueSoldSum_1Y:
        if numSoldSum_All[kind] == 0:
            avgKindPrice_All[kind] = None
        else:
            avgKindPrice_All[kind] = valueSoldSum_All[kind] / numSoldSum_All[kind]

    votedKindsAll = [k[0] for k in sorted(voteSum_All.items(), key = operator.itemgetter(1), reverse = True)]
    votedKindPricesAll = [avgKindPrice_All[k] for k in votedKindsAll]

    context["votedKinds"] = {}
    if (len(votedKindsAll) > 5):
        context["votedKindsMoreThan5"] = True
        context["votedKinds"]["all"] = zip(votedKindsAll[:5], votedKindPricesAll[:5])
    else:
        context["votedKindsMoreThan5"] = False
        context["votedKinds"]["all"] = zip(votedKindsAll, votedKindPricesAll)
    
    context["eventsWithUserWriteups"] = {}
    for writeup in u.writeups.all():
        if writeup.event.convention.ID == int(conID):
            context["eventsWithUserWriteups"][writeup.event.ID] = writeup.ID

    return render(request, "convention.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def event(request, eventID):
    context = {}
    e = context["event"] = get_object_or_404(models.Event, ID = int(eventID))
    if e == models.INV_EVENT:
        raise Http404("Accessing the INV_EVENT is disallowed.")
    context["topKinds"] = e.topKinds
    context["topFandoms"] = e.topFandoms
    context["votedKinds"] = [k[0] for k in sorted(e.kindUserVotes.items(), key = operator.itemgetter(1), reverse = True)]
    context["votedKindPrices"] = [e.avgKindPrice[k] for k in context["votedKinds"]]
    context["profitCounts"], context["profitBins"] = numpy.histogram(numpy.asarray([e.userProfit(u) for u in e.itemUsers], dtype = "float"), bins = max(1, min(10, e.itemUsers.count())))
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
        if u.writeups.filter(event = e).exists():
            context["currUserEventWriteup"] = u.writeups.get(event = e)
    return render_to_response("event.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def eventreviews(request, eventID):
    context = {}
    e = context["event"] = get_object_or_404(models.Event, ID = int(eventID))
    if e == models.INV_EVENT:
        raise Http404("Accessing the INV_EVENT is disallowed.")
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
        if u.writeups.filter(event = e).exists():
            context["currUserEventWriteup"] = u.writeups.get(event = e)
    return render(request, "eventreviews.html", context)

@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def inventory(request, eventID = None):
    u = request.user
    context = {"currUser": u}
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
    return render(request, "inventory.html", context)

@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def myconventions(request):
    u = request.user
    context = {"currUser": u}
    return render(request, "myconventions.html", context)

@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def mywriteups(request):
    u = request.user
    context = {"currUser": u}
    return render(request, "mywriteups.html", context)
    
@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def addconvention(request):
    u = request.user
    context = {"currUser": u}
    return render(request, "addconvention.html", context)

@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def addevent(request, conID):
    u = request.user
    context = {"currUser": u}
    c = context["convention"] = get_object_or_404(models.Convention, ID = int(conID))
    if c == models.INV_CON:
        raise Http404("Accessing the INV_CON is disallowed.")
    return render(request, "addevent.html", context)

@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def editconvention(request, conID):
    u = request.user
    context = {"currUser": u}
    c = context["convention"] = get_object_or_404(models.Convention, ID = int(conID))
    if c == models.INV_CON:
        raise Http404("Accessing the INV_CON is disallowed.")
    context["editCon"] = True
    return render(request, "addconvention.html", context)

@login_required
@user_passes_test(lambda u: not u.confirmToken, login_url = "/confirm")
def editevent(request, eventID):
    u = request.user
    context = {"currUser": u}
    e = context["event"] = get_object_or_404(models.Event, ID = int(eventID))
    if e == models.INV_EVENT:
        raise Http404("Accessing the INV_EVENT is disallowed.")
    context["editEvent"] = True
    return render(request, "addevent.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def writeup(request, writeupID):
    writeupID = int(writeupID)
    context = {}
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
    w = context["writeup"] = get_object_or_404(models.Writeup, ID = writeupID)
    return render(request, "writeup.html", context)

@user_passes_test(lambda u: u.is_anonymous() or not u.confirmToken, login_url = "/confirm")
def search(request, query = None):
    context = {}
    if request.user.is_authenticated():
        u = context["currUser"] = request.user
    if query is None:
        query = ""
    context["query"] = query
    context["cons"] = models.Convention.objects.filter(Q(name__icontains = query) | Q(website__icontains = query)).exclude(ID = models.INV_CON.ID).distinct()
    return render(request, "search.html", context)
