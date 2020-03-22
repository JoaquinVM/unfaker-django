from django.shortcuts import render

# Create your views here.
def feed_view(request):
    return render(request, "feed.html", {})


def new_view(request):
    return render(request, "noticia.html", {})


def profile_view(request):
    return render(request, "profile.html", {})


def publish_view(request):
    return render(request, "publish.html", {})
