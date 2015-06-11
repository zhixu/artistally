from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

from aa_app import models

def root(request):
    if "cookieID" in request.session:
        u = models.User.objects.get(cookieID = request.session["cookieID"])
        context = Context({"username": u.username})
        return HttpResponse(loader.get_template("root_user.html").render(context))
    else:
        return HttpResponse(loader.get_template("root_nonuser.html").render(Context()))

def signup(request):
    assert "cookieID" not in request.session
    return HttpResponse(loader.get_template("signup.html").render(Context()))
    
def login(request):
    assert "cookieID" not in request.session
    return HttpResponse(loader.get_template("login.html").render(Context()))

def user(request, username):
    pass

def convention(request, conID):
    pass

def item(request, itemID):
    pass