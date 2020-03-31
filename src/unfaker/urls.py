"""unfaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import feed_view, new_view, publish_view, profile_view, signin_view, login_view, logout_view, profileedit_view, change_password_view, explore_view, following_view, fresh_view
from django.conf import settings
from django.conf.urls.static import static
from main.views import error404, error500
from django.conf.urls import handler404, handler500

handler404 = 'main.views.error404'
handler500 = 'main.views.error500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', feed_view, name='feed'),
    path('following', following_view, name='following'),
    path('fresh', fresh_view, name='fresh'),
    path('explore', explore_view, name='explore'),
    path('explore/(?P<texto>\w+)', explore_view, name='explore'),
    path('new/<int:id>', new_view, name='new'),
    path('publish', publish_view, name="publish"),
    path('profile', profile_view, name='profile'),
    path('signin', signin_view, name='signin'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path ('profileedit', profileedit_view, name='profileedit')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)