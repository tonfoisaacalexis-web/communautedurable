from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .academie_models import FormationAgricole, Enseignant

class DemandeInscriptionAcademie(models.Model):
    """Permet aux jeunes et agriculteurs de postuler à une formation via la plateforme"""
    formation = models.ForeignKey(FormationAgricole, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=150, verbose_name="Nom de l'apprenant")
    telephone = models.CharField(max_length=50, verbose_name="Numéro WhatsApp")
    email = models.EmailField(blank=True, null=True, verbose_name="Adresse E-mail")
    commune_residence = models.CharField(max_length=100, verbose_name="Commune de résidence (Ex: Ambam)")
    activite_actuelle = models.CharField(max_length=150, verbose_name="Votre activité actuelle", help_text="Ex: Élève, Agriculteur...")
    motivation = models.TextField(verbose_name="Pourquoi voulez-vous suivre cette formation agropastorale ?")
    valide_par_saddur = models.BooleanField(default=False, verbose_name="Inscription validée par SADDUR")
    date_demande = models.DateTimeField(auto_now_add=True)

    STATUT_PAIEMENT = [
        ('EN_ATTENTE', 'En attente de paiement'),
        ('SUCCES', 'Payé avec succès'),
        ('ECHEC', 'Échec du paiement / Annulé'),
    ]
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT, default='EN_ATTENTE', verbose_name="Statut du paiement")
    reference_transaction = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="Référence Orange Money")

    def __str__(self):
        return f"{self.nom_complet} - Inscription : {self.formation.titre}"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Candidature Académie"
        verbose_name_plural = "⚡ Académie : Inscriptions"


class CandidatureFormateur(models.Model):
    """Permet aux experts du MINADER/MINEPIA de postuler pour devenir Formateur Référent SADDUR"""
    MINISTERE_CHOICES = [
        ('MINADER', 'MINADER (Agriculture / Développement Rural)'),
        ('MINEPIA', 'MINEPIA (Élevage / Pêches / Industries Animales)'),
        ('MINFOF', 'MINFOF (Forêts / Faune)'),
        ('PRIVE_ONG', 'Secteur Privé / Consultant / ONG'),
    ]

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente d’étude'),
        ('APPROUVE', 'Candidature Acceptée / Recruté'),
        ('REJETE', 'Candidature Refusée / Rejeté'),
    ]
    
    nom_complet = models.CharField(max_length=150, verbose_name="Nom complet de l'expert")
    ministere_origine = models.CharField(max_length=20, choices=MINISTERE_CHOICES, default='MINADER', verbose_name="Administration / Ministère")
    specialite = models.CharField(max_length=150, help_text="Ex: Ingénieur Agronome, Technicien d'Élevage", verbose_name="Spécialité technique")
    telephone_whatsapp = models.CharField(max_length=50, verbose_name="Numéro WhatsApp professionnel")
    email = models.EmailField(verbose_name="Adresse E-mail")
    commune_base = models.CharField(max_length=100, verbose_name="Ville / Commune d'affectation actuelle")
    biographie_experience = models.TextField(verbose_name="Résumé de votre expérience de terrain")
    cv_document = models.FileField(upload_to='cv_formateurs/', blank=True, null=True, verbose_name="Curriculum Vitae")
    
    statut_selection = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name="Statut du dossier")
    motif_rejet = models.TextField(blank=True, null=True, help_text="Saisir le motif précis en cas de rejet. Il sera envoyé à l'expert.", verbose_name="Motif du rejet")
    date_postulation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidature RH : {self.nom_complet} [{self.get_statut_selection_display()}]"

    class Meta:
        app_label = 'territoire'
        verbose_name = "Candidature Expert"
        verbose_name_plural = "⚡ Académie : Recrutement Experts"


@receiver(post_save, sender=DemandeInscriptionAcademie)
def creer_compte_etudiant_automatique(sender, instance, created, **kwargs):
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
def traitement_automatique_decision_rh(sender, instance, created, **kwargs):
    if instance.statut_selection == 'APPROUVE':
        if not Enseignant.objects.filter(telephone=instance.telephone_whatsapp).exists():
            Enseignant.objects.create(
                nom_complet=instance.nom_complet,
                specialite=f"{instance.specialite} ({instance.get_ministere_origine_display()})",
                biographie=instance.biographie_experience,
                telephone=instance.telephone_whatsapp
            )
            print(f"[LOG SADDUR] SUCCESS: Notification d'intégration transmise à {instance.email}")
            
    elif instance.statut_selection == 'REJETE':
        motif = instance.motif_rejet if instance.motif_rejet else "Le profil ne correspond pas aux critères techniques requis pour cette cohorte."
        print(f"[LOG SADDUR] REJET: Notification d'infirmation transmise à {instance.email}. Motif: {motif}")