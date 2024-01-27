from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def home(request):
    return render(request, "searchapp/base.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, message=f"Your account has been created: {username}"
            )
            return redirect("volt-login")
    else:
        form = UserRegisterForm()
    return render(request, "searchapp/register.html", {"form": form})


def search(request):
    return render(request, "searchapp/search.html")
