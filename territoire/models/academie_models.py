from django.db import models
from django.utils.text import slugify

class Enseignant(models.Model):
    """Profil des formateurs et ingénieurs agropastoraux experts de SADDUR"""
    nom_complet = models.CharField(max_length=150, verbose_name="Nom de l'enseignant")
    specialite = models.CharField(max_length=150, help_text="Ex: Ingénieur Agronome, Technicien MINEPIA", verbose_name="Spécialité")
    biographie = models.TextField(blank=True, null=True, verbose_name="Biographie / Expérience")
    photo = models.ImageField(upload_to='enseignants/', blank=True, null=True, verbose_name="Photo de profil")
    telephone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro WhatsApp professionnel")

    def __str__(self):
        return f"{self.nom_complet} ({self.specialite})"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Enseignant / Formateur"
        verbose_name_plural = "⚡ Académie : Enseignants"


class FormationAgricole(models.Model):
    """Les cours et programmes de formation de l'Académie SADDUR"""
    NIVEAU_CHOICES = [
        ('DEBUTANT', 'Débutant / Relance'),
        ('INTERMEDIAIRE', 'Intermédiaire / Professionnalisation'),
        ('AVANCE', 'Avancé / Export & Agro-industrie'),
    ]
    
    PRODUCTION_CHOICES = [
        ('ANIMALE', 'Production Animale (Élevage)'),
        ('VEGETALE', 'Production Végétale (Agriculture)'),
        ('FORET_FAUNE', 'Forêt, Faune & Éco-gouvernance (Environnement)'),
    ]

    TYPE_FILIERE_CHOICES = [
        ('COURTE', 'Filière Courte (3-4 semaines) [Manioc, Poulet, Pépinières, PFNL] - 25 000 FCFA'),
        ('COMPLEXE', 'Filière Complexe (6-8 semaines) [Pisciculture, Cacao, Forêt Communautaire] - 50 000 FCFA'),
        ('AGRO_IND', 'Filière Agro-industrielle (8-12 semaines) [Transformation, Export, Crédits Carbone] - 100 000 FCFA'),
    ]
    
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name='formations', verbose_name="Formateur Référent")
    titre = models.CharField(max_length=200, verbose_name="Titre de la formation")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Présentation / Objectifs du cours")
    image_couverture = models.ImageField(upload_to='formations/', blank=True, null=True, verbose_name="Image d'illustration")
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='DEBUTANT')
    type_production = models.CharField(max_length=20, choices=PRODUCTION_CHOICES, default='VEGETALE', verbose_name="Type de production")
    categorie_filiere = models.CharField(max_length=20, choices=TYPE_FILIERE_CHOICES, default='COURTE', verbose_name="Catégorie tarifaire")
    
    tarif = models.PositiveIntegerField(default=25000, verbose_name="Tarif de la formation (FCFA)", blank=True)
    duree_estimee = models.CharField(max_length=50, verbose_name="Durée estimée", blank=True)
    lien_groupe_whatsapp = models.URLField(blank=True, null=True, help_text="Lien d'invitation du groupe WhatsApp privé. Ex: https://whatsapp.com...", verbose_name="Lien du groupe WhatsApp (Coaching)")
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
            
        if self.categorie_filiere == 'COURTE':
            self.tarif = 25000
            self.duree_estimee = "3 à 4 semaines"
        elif self.categorie_filiere == 'COMPLEXE':
            self.tarif = 50000
            self.duree_estimee = "6 à 8 semaines"
        elif self.categorie_filiere == 'AGRO_IND':
            self.tarif = 100000
            self.duree_estimee = "8 à 12 semaines"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} ({self.tarif} FCFA)"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Formation Académie"
        verbose_name_plural = "⚡ Académie : Formations"


class ChapitreCours(models.Model):
    """Les modules ou leçons à l'intérieur d'une formation"""
    formation = models.ForeignKey(FormationAgricole, on_delete=models.CASCADE, related_name='chapitres')
    titre = models.CharField(max_length=200, verbose_name="Titre du chapitre")
    ordre = models.PositiveIntegerField(default=1, help_text="Ex: 1 pour le premier chapitre, 2 pour le suivant...")
    contenu_texte = models.TextField(verbose_name="Contenu de la leçon (Instructions, fiches techniques)")
    lien_video_demonstration = models.URLField(blank=True, null=True, help_text="Lien YouTube de la démonstration pratique au champ")

    def __str__(self):
        return f"{self.formation.titre} - Cap: {self.ordre} : {self.titre}"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Leçon / Chapitre"
        verbose_name_plural = "⚡ Académie : Leçons"
        ordering = ['ordre']