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
    pass

def item(request, itemID):
    context = Context({"isUser": "cookieID" in request.session})
    pass