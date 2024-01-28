from django.shortcuts import render, redirect
from django.contrib import messages
from searchapp.forms import UserRegisterForm
from django_elasticsearch_dsl.search import Search
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework_simplejwt.tokens import RefreshToken


def home(request):
    return render(request, "searchapp/base.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            # Authenticate the user
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)

            # Generate JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            print(access_token)

            # Include the JWT in response as cookie
            response = redirect("volt-login")
            response.set_cookie("access_token", access_token, httponly=True)
            messages.success(
                request, message=f"Your account has been created: {username}"
            )

            return redirect("volt-login")
    else:
        form = UserRegisterForm()
    return render(request, "searchapp/register.html", {"form": form})


@authentication_classes([JWTAuthentication])
def search(request):
    query = request.GET.get("query", "")
    articles = []

    if query:
        s = Search(index="articles").query("match", article_name=query)
        response = s.execute()

        if response.hits:
            articles = [
                {
                    "article_name": hit.article_name,
                    "article_link": hit.article_link,
                }
                for hit in response.hits
            ]

    return render(request, "searchapp/search.html", {"data": articles})


@authentication_classes([JWTAuthentication])
def autocomplete(request):
    query = request.GET.get("query", "")

    s = Search(index="articles").query("prefix", article_name=query)
    response = s.execute()

    results = [
        {"article_name": hit.article_name, "article_link": hit.article_link}
        for hit in response
    ]

    return JsonResponse(results, safe=False)
