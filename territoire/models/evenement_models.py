from django.db import models
from .territoire_models import Mairie

class ActeurEvenement(models.Model):
    """Les parties prenantes de la Foire Nationale : Bailleurs, Annonceurs, Partenaires"""
    TYPE_ACTEUR_CHOICES = [
        ('BAILLEUR', 'Bailleur de Fonds / Investisseur / Diaspora'),
        ('ANNONCEUR', 'Annonceur / Sponsor / Entreprise Privée'),
        ('PARTENAIRE', 'Partenaire Institutionnel / ONG / Ministère'),
    ]
    
    nom_organisation = models.CharField(max_length=200, verbose_name="Nom de l'organisation / Entreprise")
    type_acteur = models.CharField(max_length=20, choices=TYPE_ACTEUR_CHOICES, default='ANNONCEUR', verbose_name="Catégorie d'acteur")
    logo = models.ImageField(upload_to='foire/logos/', blank=True, null=True, verbose_name="Logo officiel")
    site_web = models.URLField(blank=True, null=True, verbose_name="Lien vers le site web / Brochure")
    telephone_contact = models.CharField(max_length=50, verbose_name="N° WhatsApp de contact B2B")
    opportunites_offertes = models.TextField(help_text="Ex: Financement de micro-centrales solaires, Fourniture d'engrais bio...", verbose_name="Offres / Opportunités pour les Communes")

    def __str__(self):
        return f"{self.nom_organisation} ({self.get_type_acteur_display()})"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Acteur de la Foire"
        verbose_name_plural = "🎪 Foire : Bailleurs & Annonceurs"


class ProjetPavillonMairie(models.Model):
    """Les projets et réalisations exposés par les mairies pour séduire les bailleurs pendant la foire"""
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='pavillons_foire', verbose_name="Mairie Exposante")
    titre_realisation = models.CharField(max_length=250, help_text="Ex: Modernisation du marché de fruits d'Ambam", verbose_name="Titre du projet / Réalisation")
    description_technique = models.TextField(verbose_name="Détails, Impact social & Objectifs de transition durable")
    budget_estime = models.PositiveIntegerField(verbose_name="Budget estimé ou recherché (FCFA)", blank=True, null=True)
    image_illustration = models.ImageField(upload_to='foire/projets/', blank=True, null=True, verbose_name="Photo de la réalisation / Maquette")
    stade_projet = models.CharField(max_length=100, default="Réalisation en cours / Recherche de co-financement", verbose_name="Statut du projet")

    def __str__(self):
        return f"Pavillon {self.mairie.nom} - {self.titre_realisation}"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Projet Exposé (Mairie)"
        verbose_name_plural = "🎪 Foire : Pavillons des Communes"