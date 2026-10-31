from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importations directes depuis les fichiers sources des vues
from territoire.views.territoire_views import index_public, detail_mairie, presentation_cameroun
from territoire.views.vitrine_views import vitrine_marche_national
from territoire.views.evenement_views import foire_nationale_communes  # <-- INCLUSION SÉCURISÉE DU HUB ÉVÉNEMENTIEL
from territoire.views.academie_views import (
    academie_home, connexion_academie, deconnexion_academie, 
    telecharger_attestation_pdf, simulation_guichet_paiement
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_public, name='accueil_public'),
    path('cameroun/', presentation_cameroun, name='presentation_cameroun'),
    path('commune/<slug:slug>/', detail_mairie, name='detail_mairie'),
    
    # SYSTÈME MARCHÉ NATIONAL SADDUR (PRODUCTEURS & ENTREPRENEURS)
    path('marche-national/', vitrine_marche_national, name='marche_national_public'),
    
    # SYSTÈME FOIRE NATIONALE ANNUELLE INTER-COMMUNES
    path('foire-nationale/', foire_nationale_communes, name='foire_nationale_public'),
    
    # SYSTÈME ACADÉMIE SADDUR & PAIEMENT ORANGE MONEY
    path('academie/', academie_home, name='academie_public'),
    path('academie/connexion/', connexion_academie, name='connexion_academie'),
    path('academie/deconnexion/', deconnexion_academie, name='deconnexion_academie'),
    path('academie/attestation/<int:inscription_id>/', telecharger_attestation_pdf, name='telecharger_attestation_pdf'),
    path('academie/paiement/simulation/<str:reference>/', simulation_guichet_paiement, name='simulation_guichet_paiement'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)