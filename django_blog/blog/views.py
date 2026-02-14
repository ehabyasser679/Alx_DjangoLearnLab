from django.shortcuts import render, redirect
from django.contrib.auth.forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def registeration(request):
    if request.method == "POST":
        CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        CustomUserCreationForm()
        return render(request, "blog/register.html", {"form": form})

