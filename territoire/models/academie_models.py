from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

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

    # Classification officielle de la tarification et de la durée SADDUR
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
    
    # Sélection de la catégorie de l'offre SADDUR pour calcul automatique
    categorie_filiere = models.CharField(max_length=20, choices=TYPE_FILIERE_CHOICES, default='COURTE', verbose_name="Catégorie tarifaire")
    
    tarif = models.PositiveIntegerField(default=25000, verbose_name="Tarif de la formation (FCFA)", blank=True)
    duree_estimee = models.CharField(max_length=50, verbose_name="Durée estimée", blank=True)
    
    # Lien d'accès au Groupe WhatsApp Privé pour le Coaching Synchrone SADDUR
    lien_groupe_whatsapp = models.URLField(blank=True, null=True, help_text="Lien d'invitation du groupe WhatsApp privé. Ex: https://whatsapp.com...", verbose_name="Lien du groupe WhatsApp (Coaching)")
    
    date_creation = models.DateTimeField(auto_now_add=True)

    # AUTOMATISATION SADDUR : Calcul autonome des prix et durées lors de la sauvegarde
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
    lien_video_demonstration = models.URLField(blank=True, null=True, help_text="Lien YouTube ou Vimeo de la démonstration pratique au champ")

    def __str__(self):
        return f"{self.formation.titre} - Cap: {self.ordre} : {self.titre}"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Leçon / Chapitre"
        verbose_name_plural = "⚡ Académie : Leçons"
        ordering = ['ordre']


class DemandeInscriptionAcademie(models.Model):
    """Permet aux jeunes et agriculteurs de postuler à une formation via la plateforme"""
    formation = models.ForeignKey(FormationAgricole, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=150, verbose_name="Nom de l'apprenant")
    telephone = models.CharField(max_length=50, verbose_name="Numéro WhatsApp")
    email = models.EmailField(blank=True, null=True, verbose_name="Adresse E-mail")
    commune_residence = models.CharField(max_length=100, verbose_name="Commune de résidence (Ex: Ambam)")
    activite_actuelle = models.CharField(max_length=150, verbose_name="Votre activité actuelle", help_text="Ex: Élève, Agriculteur, Sans emploi...")
    motivation = models.TextField(verbose_name="Pourquoi voulez-vous suivre cette formation agropastorale ?")
    valide_par_saddur = models.BooleanField(default=False, verbose_name="Inscription validée par SADDUR")
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_complet} - Inscription : {self.formation.titre}"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Candidature Académie"
        verbose_name_plural = "⚡ Académie : Inscriptions"

        # SUIVI DU PAIEMENT ORANGE MONEY SADDUR
    STATUT_PAIEMENT = [
        ('EN_ATTENTE', 'En attente de paiement'),
        ('SUCCES', 'Payé avec succès'),
        ('ECHEC', 'Échec du paiement / Annulé'),
    ]
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT, default='EN_ATTENTE', verbose_name="Statut du paiement")
    reference_transaction = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="Référence Orange Money")


class CandidatureFormateur(models.Model):
    """Permet aux experts du MINADER/MINEPIA de postuler pour devenir Formateur Référent SADDUR"""
    MINISTERE_CHOICES = [
        ('MINADER', 'MINADER (Agriculture / Développement Rural)'),
        ('MINEPIA', 'MINEPIA (Élevage / Pêches / Industries Animales)'),
        ('MINFOF', 'MINFOF (Forêts / Faune)'),
        ('PRIVE_ONG', 'Secteur Privé / Consultant / ONG'),
    ]
    
    nom_complet = models.CharField(max_length=150, verbose_name="Nom complet de l'expert")
    ministere_origine = models.CharField(max_length=20, choices=MINISTERE_CHOICES, default='MINADER', verbose_name="Administration / Ministère")
    specialite = models.CharField(max_length=150, help_text="Ex: Ingénieur Agronome, Technicien d'Élevage, Éco-garde", verbose_name="Spécialité technique")
    telephone_whatsapp = models.CharField(max_length=50, verbose_name="Numéro WhatsApp professionnel")
    email = models.EmailField(verbose_name="Adresse E-mail")
    commune_base = models.CharField(max_length=100, verbose_name="Ville / Commune d'affectation actuelle")
    biographie_experience = models.TextField(verbose_name="Résumé de votre expérience de terrain")
    cv_document = models.FileField(upload_to='cv_formateurs/', blank=True, null=True, help_text="Téléverser votre CV ou note technique (PDF)", verbose_name="Curriculum Vitae")
    
    est_approuve = models.BooleanField(default=False, verbose_name="Dossier validé par le Bureau SADDUR")
    date_postulation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidature RH : {self.nom_complet} ({self.specialite})"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Candidature Expert"
        verbose_name_plural = "⚡ Académie : Recrutement Experts"


@receiver(post_save, sender=DemandeInscriptionAcademie)
def creer_compte_etudiant_automatique(sender, instance, created, **kwargs):
    """Crée un compte utilisateur Django dès que SADDUR valide l'inscription du jeune"""
    if instance.valide_par_saddur:
        username = instance.telephone.strip().replace(" ", "")
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=instance.email if instance.email else '',
                password="Saddur2026!"
            )
            user.first_name = instance.nom_complet
            user.save()


@receiver(post_save, sender=CandidatureFormateur)
def promouvoir_en_enseignant_officiel(sender, instance, created, **kwargs):
    """Transforme l'expert en Enseignant officiel dès qu'il est approuvé"""
    if instance.est_approuve:
        if not Enseignant.objects.filter(telephone=instance.telephone_whatsapp).exists():
            Enseignant.objects.create(
                nom_complet=instance.nom_complet,
                specialite=f"{instance.specialite} ({instance.get_ministere_origine_display()})",
                biographie=instance.biographie_experience,
                telephone=instance.telephone_whatsapp
            )