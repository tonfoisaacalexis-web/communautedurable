from django.shortcuts import render, get_object_or_404
from django.contrib import messages  # <-- AJOUTEZ CET IMPORT ICI
from .models import Mairie, SuggestionCitoyenne

def detail_mairie(request, slug):
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
            # AJOUT : Déclenche l'alerte verte de succès pour le citoyen
            messages.success(request, "Votre courrier officiel a été transmis avec succès au Secrétariat de la Mairie.")
            
    context = {
        'mairie': mairie,
    }
    return render(request, 'territoire/detail.html', context)

def presentation_cameroun(request):
    return render(request, 'territoire/cameroun.html')