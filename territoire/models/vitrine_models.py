from django.db import models
from django.utils.text import slugify

class EntrepreneurAgricole(models.Model):
    """Banque de données permanente des producteurs et entrepreneurs SADDUR"""
    nom_complet = models.CharField(max_length=150, verbose_name="Nom de l'entrepreneur")
    nom_entreprise = models.CharField(max_length=150, verbose_name="Nom de l'exploitation / GIC")
    telephone_whatsapp = models.CharField(max_length=50, verbose_name="N° WhatsApp Commercial")
    ville_base = models.CharField(max_length=100, verbose_name="Ville / Localité d'activité (Ex: Ambam)")
    biographie = models.TextField(blank=True, null=True, verbose_name="Présentation de l'activité")
    date_adhesion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_complet} - {self.nom_entreprise} ({self.ville_base})"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Entrepreneur SADDUR"
        verbose_name_plural = "🌐 Marché : Entrepreneurs"


class ArticleVitrine(models.Model):
    """Les articles publiés : Qui, Où, Quand, Comment, Combien"""
    entrepreneur = models.ForeignKey(EntrepreneurAgricole, on_delete=models.CASCADE, related_name='articles', verbose_name="Vendeur (Qui)")
    nom_produit = models.CharField(max_length=150, help_text="Ex: Manioc, Poulet de chair, Djansang", verbose_name="Nom du produit")
    quantite_disponible = models.CharField(max_length=100, help_text="Ex: 500 kg, 200 sujets", verbose_name="Quantité / Stock disponible")
    localite_stock = models.CharField(max_length=100, help_text="Ex: Ambam, Ebolowa, Douala 1er", verbose_name="Lieu de stockage (Où)")
    prix_unitaire = models.PositiveIntegerField(verbose_name="Prix unitaire (Combien en FCFA)")
    mode_livraison = models.TextField(help_text="Ex: Retrait sur place, Livraison par agence Voyage", verbose_name="Mode de livraison (Comment)")
    disponibilite_temps = models.CharField(max_length=150, help_text="Ex: Disponible immédiatement, Récolte le 15/11", verbose_name="Disponibilité (Quand)")
    image_produit = models.ImageField(upload_to='marche/', blank=True, null=True, verbose_name="Photo du produit")
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_produit} - {self.prix_unitaire} FCFA ({self.localite_stock})"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Article en Vente"
        verbose_name_plural = "🌐 Marché : Articles de la Vitrine"