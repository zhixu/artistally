from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

from aa_app import models

def root(request):
    context = Context({"isUser": "cookieID" in request.session})
    if context["isUser"]:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    return HttpResponse(loader.get_template("root.html").render(context))

def signup(request):
    if "cookieID" in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/"
        return resp
    else:
        return HttpResponse(loader.get_template("signup.html").render(Context({"isUser": False})))
    
def login(request):
    if "cookieID" in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/"
        return resp
    else:
        return HttpResponse(loader.get_template("login.html").render(Context({"isUser": False})))

def user(request, username):
    context = Context({"isUser": "cookieID" in request.session})
    if context["isUser"]:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    context["pageUser"] = models.User.objects.get(username = username)
    return HttpResponse(loader.get_template("user.html").render(context))

def convention(request, conID):
    context = Context({"isUser": "cookieID" in request.session})
    if context["isUser"]:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    context["convention"] = models.Convention.objects.get(ID = int(conID))
    return HttpResponse(loader.get_template("convention.html").render(context))

def addconvention(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        context = Context({"isUser": "cookieID" in request.session})
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
        return HttpResponse(loader.get_template("addconvention.html").render(context))

def addkind(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        context = Context({"isUser": "cookieID" in request.session})
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
        return HttpResponse(loader.get_template("addkind.html").render(context))

def addfandom(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        context = Context({"isUser": "cookieID" in request.session})
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
        return HttpResponse(loader.get_template("addfandom.html").render(context))

def additem(request):
    if "cookieID" not in request.session:
        resp = HttpResponse(status = 307)
        resp["Location"] = "/login"
        return resp
    else:
        context = Context({"isUser": "cookieID" in request.session})
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
        context["cons"] = models.Convention.objects.all()
        context["kinds"] = models.Kind.objects.all()
        context["fandoms"] = models.Fandom.objects.all()
        return HttpResponse(loader.get_template("additem.html").render(context))
        
def item(request, itemID):
    context = Context({"isUser": "cookieID" in request.session})
    if context["isUser"]:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context["currUser"] = u
    context["item"] = models.Item.objects.get(ID = int(itemID))
    return HttpResponse(loader.get_template("item.html").render(context))