from django.shortcuts import render
from .forms import NoticiaForm
from .forms import DenunciaForm
from .forms import UsuarioForm

# Create your views here.
def feed_view(request):
    return render(request, "feed.html", {})


def new_view(request):
    form = DenunciaForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "noticia.html", context)


def profile_view(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "profile.html", context)


def publish_view(request):
    form = NoticiaForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "publish.html", context)
