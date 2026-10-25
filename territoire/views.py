from django.shortcuts import render, get_object_or_404
from .models import Mairie

def index_public(request):
    mairies = Mairie.objects.all()
    context = {
        'mairies': mairies,
        'titre_page': 'Communautedurable.cm - Portail National',
        'slogan': "Le territoire de demain, aujourd'hui"
    }
    return render(request, 'territoire/index.html', context)

def detail_mairie(request, slug):
    mairie = get_object_or_404(Mairie, slug=slug)
    context = {
        'mairie': mairie,
    }
    return render(request, 'territoire/detail.html', context)

def presentation_cameroun(request):
    return render(request, 'territoire/cameroun.html')