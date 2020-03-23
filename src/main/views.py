from django.shortcuts import render
from .forms import NoticiaForm

# Create your views here.
def feed_view(request):
    return render(request, "feed.html", {})


def new_view(request):
    return render(request, "noticia.html", {})


def profile_view(request):
    return render(request, "profile.html", {})


def publish_view(request):
    form = NoticiaForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "publish.html", context)
