from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from users.forms import LoginForm, RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(  # ← use create_user, not create!
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            login(request, user)  # auto-login after register
            return redirect("home")
        return render(request, "users/register.html", {"form": form})

    return render(request, "users/register.html", {"form": RegisterForm()})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Wrong username or password!")
        return render(request, "users/login.html", {"form": form})

    return render(request, "users/login.html", {"form": LoginForm()})


def logout_view(request):
    logout(request)  # safe to call even if anonymous
    return redirect("home")