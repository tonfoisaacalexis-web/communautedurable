from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Mairie, SuggestionCitoyenne

def index_public(request):
    """Affiche la vitrine publique avec la grille des mairies"""
    mairies = Mairie.objects.all()
    context = {
        'mairies': mairies,
        'titre_page': 'Communautedurable.cm - Portail National',
        'slogan': "Le territoire de demain, aujourd'hui"
    }
    return render(request, 'territoire/index.html', context)

def detail_mairie(request, slug):
    """Affiche la page de détails d'une commune avec gestion de la boîte à suggestions"""
    mairie = get_object_or_404(Mairie, slug=slug)
    
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        
        if nom and email and sujet and message:
            SuggestionCitoyenne.objects.create(
                mairie=mairie,
                nom_expediteur=nom,
                email_expediteur=email,
                sujet=sujet,
                message=message
            )
            messages.success(request, "Votre courrier officiel a été transmis avec succès au Secrétariat de la Mairie.")
            
    context = {
        'mairie': mairie,
    }
    return render(request, 'territoire/detail.html', context)

def presentation_cameroun(request):
    """Affiche la page de présentation nationale de la République"""
    return render(request, 'territoire/cameroun.html')