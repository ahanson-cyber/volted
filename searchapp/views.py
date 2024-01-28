from django.shortcuts import render, redirect
from django.contrib import messages
from searchapp.forms import UserRegisterForm
from django_elasticsearch_dsl.search import Search
from django.http import JsonResponse


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


def autocomplete(request):
    query = request.GET.get("query", "")

    # Use Elasticsearch DSL to perform autocomplete search
    s = Search(index="articles").query("prefix", article_name=query)
    response = s.execute()

    # Extract titles from the search results
    titles = [hit.article_name for hit in response]

    return JsonResponse(titles, safe=False)
