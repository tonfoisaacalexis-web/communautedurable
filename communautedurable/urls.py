"""
URL configuration for communautedurable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://djangoproject.com
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from territoire.views import index_public, detail_mairie, presentation_cameroun  # Fusion complète des imports

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_public, name='accueil_public'),  # La racine publique du site web
    path('mairie/<slug:slug>/', detail_mairie, name='detail_mairie'),  # Route dynamique des communes
    path('republique-du-cameroun/', presentation_cameroun, name='presentation_cameroun'),  # Nouvel espace permanent national
]

# Servir les fichiers médias (photos des maires et armoiries) en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)