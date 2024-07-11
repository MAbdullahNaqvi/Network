from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist 
from .models import User, posts, Userprofile

def index(request):
    return render(request, "network/index.html",{
        "active":"index"
    })


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
                "message": "Invalid username and/or password.",
                "active":"register"
            })
    else:
        return render(request, "network/login.html",{
            "active":"login"
        })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match.",
                "active":"register"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Userprofile(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken.",
                "active":"register"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html",{
            "active":"register"
        })


def allposts(request):
    if request.method == "GET":
        allposts = posts.objects.all()
        allposts = allposts.order_by("-timestamp").all()
        
        return JsonResponse([post.serialize() for post in allposts], safe= False)
    else:
        return JsonResponse({"Error: GET Request Required."}, status=400)


@login_required
@csrf_exempt
def upload(request):
    if request.method != "POST":
        return JsonResponse({"error":"Only POST requests are allowed.","status":400}, status=400, safe=False)
    
    data = json.loads(request.body)
    content = data.get("content")
    if content == "":
        return JsonResponse({"error":"Empty Posts are not allowed.","status":400}, status=400, safe=False)

    post = posts(
        content = content,
        account = request.user,
    )
    post.save()
    
    return JsonResponse({"message":"Sucessfuly create new post.","status":201}, status=201, safe=False)


def accounts(request,id):
    return render(request,"network/accounts.html")

@csrf_exempt
@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"error":"Only POST requests are allowed.","status":400}, status=400, safe=False)
    data = json.loads(request.body)
    id = data["id"]
    post = posts.objects.get(pk = id)
    try:
        x = post.likes.get(username = request.user.username)
        return JsonResponse({"error":"All ready liked.","status":400}, status=400, safe=False)
    except ObjectDoesNotExist: 
        post.likes.add(request.user)
        post.save()

        return JsonResponse({"message":"Sucessfuly Liked the post.","status":201}, status=201, safe=False)
    

@csrf_exempt
@login_required
def unlike(request):
    if request.method != "POST":
        return JsonResponse({"error":"Only POST requests are allowed.","status":400}, status=400, safe=False)
    data = json.loads(request.body)
    id = data["id"]
    post = posts.objects.get(pk = id)
    try:
        x = post.likes.get(username = request.user.username)
        post.likes.remove(request.user)
        post.save()

        return JsonResponse({"message":"Sucessfuly Unliked the post.","status":201}, status=201, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"error":"Post is not already unliked.","status":400}, status=400, safe=False)
