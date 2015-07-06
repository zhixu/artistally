from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

from aa_app import models

def root(request):
    context = Context()
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    return HttpResponse(loader.get_template("root.html").render(context))

def signup(request):
    if "cookieID" in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/"
        return resp
    else:
        return HttpResponse(loader.get_template("signup.html").render(Context()))
    
def login(request):
    if "cookieID" in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/"
        return resp
    else:
        return HttpResponse(loader.get_template("login.html").render(Context()))

def user(request, username):
    context = Context()
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    context["pageUser"] = models.User.objects.get(username = username)
    return HttpResponse(loader.get_template("user.html").render(context))

def convention(request, conID):
    context = Context()
    context["convention"] = models.Convention.objects.get(ID = int(conID))
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
        context["currUserConItems"] = u.items.filter(convention = context["convention"])
        if u.writeups.filter(convention = context["convention"]).exists():
            context["currUserConWriteup"] = u.writeups.get(convention = context["convention"])
    return HttpResponse(loader.get_template("convention.html").render(context))

def addconvention(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"currUser": u})
        return HttpResponse(loader.get_template("addconvention.html").render(context))

def addwriteup(request, conID = None):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"currUser": u})
        context["cons"] = models.Convention.objects.all()
        if conID != None:
            context["currCon"] = models.Convention.objects.get(ID = conID)
        return HttpResponse(loader.get_template("addwriteup.html").render(context))

def addkind(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"currUser": u})
        return HttpResponse(loader.get_template("addkind.html").render(context))

def addfandom(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"currUser": u})
        return HttpResponse(loader.get_template("addfandom.html").render(context))

def additem(request, conID = None):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"currUser": u})
        context["cons"] = models.Convention.objects.all()
        context["kinds"] = models.Kind.objects.all()
        context["fandoms"] = models.Fandom.objects.all()
        if conID != None:
            context["currCon"] = models.Convention.objects.get(ID = conID)
        return HttpResponse(loader.get_template("additem.html").render(context))
        
def item(request, itemID):
    context = Context()
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    context["item"] = models.Item.objects.get(ID = int(itemID))
    return HttpResponse(loader.get_template("item.html").render(context))
        
def writeup(request, writeupID):
    context = Context()
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    context["writeup"] = models.Writeup.objects.get(ID = int(writeupID))
    return HttpResponse(loader.get_template("writeup.html").render(context))