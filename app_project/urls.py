"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from app_api.views import register_user, login_user, ArtistView, UserView, ClassificationView, GenreView, StyleView, MediumView, ArtView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'artists', ArtistView, 'artist')
router.register(r'art', ArtView, 'art')
router.register(r'users', UserView, 'user')
router.register(r'classifications', ClassificationView, 'classification')
router.register(r'genres', GenreView, 'genre')
router.register(r'styles', StyleView, 'style')
router.register(r'mediums', MediumView, 'medium')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
