from datetime import timezone
import json;
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.management.base import CommandError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post
import datetime

def index(request):
    return render(request, "network/index.html")


#Save post
@csrf_exempt
@login_required
def createPost(request):
    if (request.method != 'POST'):
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # get content post
    data = json.loads(request.body)
    content = data["content"]
    date = datetime.datetime.now(tz=timezone.utc)

    # Save post data
    try: 
        post = Post(
            content = content,
            created_by = request.user,
            created_date = date
        )

        post.save()
    except IntegrityError:
            # already been created because we got IntegrityError
            raise CommandError("Post not saved")

    return JsonResponse({"message": "Post created successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def getPostList(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, "network/post.html", {
        "posts": posts
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
