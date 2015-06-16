from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

from aa_app import models

def root(request):
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"isUser": True, "username": u.username})
        return HttpResponse(loader.get_template("root_user.html").render(context))
    else:
        context = Context({"isUser": False})
        return HttpResponse(loader.get_template("root_nonuser.html").render(context))

def signup(request):
    assert "cookieID" not in request.session
    context = Context({"isUser": False})
    return HttpResponse(loader.get_template("signup.html").render(context))
    
def login(request):
    assert "cookieID" not in request.session
    context = Context({"isUser": False})
    return HttpResponse(loader.get_template("login.html").render(context))

def user(request, username):
    context = Context()
    pass

def convention(request, conID):
    context = Context()
    pass

def item(request, itemID):
    context = Context()
    pass