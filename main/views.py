from django.contrib import auth 
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import (
    LoginForm,
    SignUpForm,
    TalkForm,
    UsernameChangeForm,
    EmailChangeForm,
)
from .models import Talk, User

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            #これなんでpassword"1"なの？と思ったら、２はあれだ、検証用だ
            #もう一度入力してね！ってやつ
            password = form.cleaned_data["password1"]

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)

            return redirect("index")
    
    context = {"form": form}
    return render(request, "main/signup.html", context)

# def login(request):
#     return render(request, "main/login.html")

class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    template_name = "main/login.html"

@login_required
def friends(request):
    friends = User.objects.exclude(id=request.user.id)
    context = {"friends": friends}
    return render(request, "main/friends.html", context)

@login_required
def talk_room(request, user_id):
    friend = get_object_or_404(User, id=user_id)

    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        | Q(sender=friend, receiver=request.user)
    ).order_by("time")

    if request.method == "GET":
        form = TalkForm()
    elif request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            new_talk = form.save(commit=False)
            new_talk.sender = request.user
            new_talk.receiver = friend
            new_talk.save()
            return redirect("talk_room", user_id)
    
    context = {
        "form": form,
        "friend": friend,
        "talks": talks,
    }

    return render(request, "main/talk_room.html", context)

@login_required
def settings(request):
    return render(request, "main/settings.html")

@login_required
def username_change(request):
    if request.method == "GET":
        form = UsernameChangeForm(instance=request.user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
    context = {"form": form}
    return render(request, "main/username_change.html", context)

@login_required
def username_change_done(request):
    return render(request, "main/username_change_done.html")

@login_required
def email_change(request):
    if request.method == "GET":
        form = EmailChangeForm(instance=request.user)
    elif request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("email_change_done")

    context = {"form": form}
    return render(request, "main/email_change.html", context)

@login_required
def email_change_done(request):
    return render(request, "main/email_change_done.html")
