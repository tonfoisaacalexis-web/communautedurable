from django.db import models
from django.utils.text import slugify

class Region(models.Model):
    """Les 10 régions du Cameroun (ex: Sud, Centre, Littoral...)"""
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Région"
        verbose_name_plural = "Régions"


class Departement(models.Model):
    """Les 58 départements du Cameroun (ex: Vallée du Ntem, Mvila...)"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='departements')
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        unique_together = ('region', 'nom')


class Mairie(models.Model):
    """Les 360 communes du Cameroun"""
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='mairies')
    nom = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    latitude = models.FloatField(blank=True, null=True, default=2.3833, help_text="Ex: 2.3833 pour Ambam")
    longitude = models.FloatField(blank=True, null=True, default=11.2833, help_text="Ex: 11.2833 pour Ambam")
    
    # Informations institutionnelles
    nom_du_maire = models.CharField(max_length=200, blank=True, null=True)
    mot_du_maire = models.TextField(blank=True, null=True)
    photo_du_maire = models.ImageField(upload_to='maires/', blank=True, null=True)
    armoiries = models.ImageField(upload_to='armoiries/', blank=True, null=True)
    
    # Statut Commercial / Fonctionnalités
    est_premium = models.BooleanField(default=False, help_text="Cochez pour activer les accès Celcom/Publications de la Mairie")
    date_activation_premium = models.DateTimeField(blank=True, null=True)
    
    # Historique et Géographie locale
    histoire = models.TextField(blank=True, null=True)
    geographie = models.TextField(blank=True, null=True)

    # Aspects socio-économiques et planification stratégique
    aspect_socio_economique = models.TextField(blank=True, null=True, verbose_name="Aspect Socio-Économique")
    vision_mairie = models.TextField(blank=True, null=True, verbose_name="Vision de la Commune")
    projets_court_terme = models.TextField(blank=True, null=True, verbose_name="Projets à Court Terme")
    projets_long_terme = models.TextField(blank=True, null=True, verbose_name="Projets à Long Terme")
    partenaires_commune = models.TextField(blank=True, null=True, verbose_name="Partenaires au Développement")
    
    # Contacts
    email_contact = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    adresse_physique = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mairie de {self.nom}"

    class Meta:
        verbose_name = "Mairie"
        verbose_name_plural = "Mairies"
        unique_together = ('departement', 'nom')


class DocumentMunicipal(models.Model):
    """Permet aux mairies Premium de téléverser des documents officiels (PDF)"""
    TYPE_CHOICES = [
        ('APPEL_OFFRE', "Appel d'Offres / Marché Public"),
        ('BULLETIN', 'Bulletin / Journal Municipal'),
        ('ACTE', 'Formulaire Administratif / État Civil'),
    ]

    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=200)
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES, default='BULLETIN')
    fichier_pdf = models.FileField(upload_to='documents_mairies/')
    date_publication = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.mairie.nom}"

    class Meta:
        verbose_name = "Document Municipal"
        verbose_name_plural = "Documents Municipaux"


class SuggestionCitoyenne(models.Model):
    """Permet aux citoyens d'envoyer des suggestions et courriers officiels à la mairie"""
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='suggestions')
    nom_expediteur = models.CharField(max_length=150, verbose_name="Nom complet")
    email_expediteur = models.EmailField(verbose_name="Adresse E-mail")
    sujet = models.CharField(max_length=200, verbose_name="Sujet du message")
    message = models.TextField(verbose_name="Message / Courrier")
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion de {self.nom_expediteur} pour {self.mairie.nom}"

    class Meta:
        verbose_name = "Boîte à suggestions"
        verbose_name_plural = "Boîtes à suggestions"