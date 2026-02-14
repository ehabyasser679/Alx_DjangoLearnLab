from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserCreationForm


def registeration(request):
    if request.method == "POST":
        UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        UserCreationForm()
        return render(request, "blog/register.html", {"form": form})

