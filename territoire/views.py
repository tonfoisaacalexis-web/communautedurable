from django.shortcuts import render, get_object_or_404
from .models import Mairie

def index_public(request):
    """Affiche la vitrine publique avec la grille des mairies"""
    mairies = Mairie.objects.all()
    
    context = {
        'mairies': mairies,
        'titre_page': 'Communautedurable.cm - Portail National',
        'slogan': 'Le territoire de demain, aujourd\'hui'
    }
    return render(request, 'territoire/index.html', context)


def detail_mairie(request, slug):
    """Affiche la page de détails spécifique à une commune (ex: Ambam)"""
    mairie = get_object_or_404(Mairie, slug=slug)
    
    context = {
        'mairie': mairie,
    }
    return render(request, 'territoire/detail.html', context)


def presentation_cameroun(request):
    """Affiche l'espace institutionnel de présentation du Cameroun"""
    return render(request, 'territoire/cameroun.html')