from django.shortcuts import render
from django.db.models import Q
from ..models import ArticleVitrine

def vitrine_marche_national(request):
    """Moteur de recherche permanent pour orienter les consommateurs vers les vendeurs disponibles"""
    produit_recherche = request.GET.get('produit', '').strip()
    ville_recherche = request.GET.get('ville', '').strip()
    
    resultats = []
    recherche_elargie = False
    
    if produit_recherche and ville_recherche:
        # 1. Recherche stricte : Produit exact dans la ville exacte demandée
        resultats = ArticleVitrine.objects.filter(
            Q(nom_produit__icontains=produit_recherche) & 
            Q(localite_stock__icontains=ville_recherche)
        ).order_by('-date_publication')
        
        # 2. Logique de repli par défaut : Si vide, on élargit à toute la région/localités voisines
        if not resultats.exists():
            resultats = ArticleVitrine.objects.filter(
                nom_produit__icontains=produit_recherche
            ).order_by('-date_publication')
            recherche_elargie = True
            
    context = {
        'resultats': resultats,
        'produit_recherche': produit_recherche,
        'ville_recherche': ville_recherche,
        'recherche_elargie': recherche_elargie
    }
    return render(request, 'territoire/vitrine_marche.html', context)