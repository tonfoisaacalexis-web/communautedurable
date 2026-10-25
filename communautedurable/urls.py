"""
URL configuration for communautedurable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://djangoproject.com
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from territoire.views import index_public, detail_mairie  # <-- On importe bien les deux vues ici

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_public, name='accueil_public'),  # La racine du site web
    path('mairie/<slug:slug>/', detail_mairie, name='detail_mairie'),  # <-- C'est cette ligne exacte qui manquait !
]

# Servir les fichiers médias (photos des maires et armoiries) en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)