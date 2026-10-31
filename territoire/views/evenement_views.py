from django.shortcuts import render
from ..models import ActeurEvenement, ProjetPavillonMairie

def foire_nationale_communes(request):
    """Pilote le carrefour interactif de la foire annuelle SADDUR"""
    bailleurs = ActeurEvenement.objects.filter(type_acteur='BAILLEUR')
    annonceurs = ActeurEvenement.objects.filter(type_acteur='ANNONCEUR')
    pavillons = ProjetPavillonMairie.objects.all().select_related('mairie')
    
    context = {
        'bailleurs': bailleurs,
        'annonceurs': annonceurs,
        'pavillons': pavillons,
    }
    return render(request, 'territoire/foire_nationale.html', context)