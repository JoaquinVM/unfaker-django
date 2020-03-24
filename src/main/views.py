from django.shortcuts import render
from .forms import NoticiaForm
from .forms import DenunciaForm
from .forms import UsuarioForm
from django.core.files.storage import FileSystemStorage

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

    if request.method == 'POST' and request.FILES['imagen'] and form.is_valid():
        myfile = request.FILES['imagen']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile) # saves the file to `media` folder
        uploaded_file_url = fs.url(filename) # gets the url
        form.save(filename)
        return render(request, 'publish.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'publish.html')
    # form = NoticiaForm(request.POST or None)
    # if form.is_valid() and request.POST.get('imagen', False):
    #     imagen = request.POST.get('imagen', False)
    #     fs = FileSystemStorage()
    #     filename = fs.save(imagen.name, imagen)
    #     form.save(imagen=filename)
    # context = {
    #     'form': form
    # }
    # return render(request, "publish.html", context)
