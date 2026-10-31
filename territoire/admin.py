from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Mairie, Region, Departement, DocumentMunicipal, 
    SuggestionCitoyenne, Enseignant, FormationAgricole, ChapitreCours, 
    DemandeInscriptionAcademie, CandidatureFormateur,
    EntrepreneurAgricole, ArticleVitrine,
    ActeurEvenement, ProjetPavillonMairie  # <-- INCLUSION SÉCURISÉE DES MODÈLES DE LA FOIRE
)


# --- CONFIGURATION DES TITRES DU BACK-OFFICE ---
admin.site.site_header = "Communautedurable.cm"
admin.site.site_title = "Communautedurable.cm"
admin.site.index_title = "Gestion de l'espace Territoire & Académie"

# --- ENREGISTREMENTS SIMPLES ---
admin.site.register(Region)
admin.site.register(Departement)
admin.site.register(DocumentMunicipal)

@admin.register(SuggestionCitoyenne)
class SuggestionCitoyenneAdmin(admin.ModelAdmin):
    list_display = ('nom_expediteur', 'mairie', 'sujet', 'date_envoi')
    list_filter = ('mairie', 'date_envoi')
    search_fields = ('nom_expediteur', 'sujet', 'message')

@admin.register(Mairie)
class MairieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement', 'nom_du_maire', 'est_premium', 'apercu_photo_du_maire')
    search_fields = ('nom', 'nom_du_maire')
    prepopulated_fields = {'slug': ('nom',)}
    list_filter = ('departement', 'est_premium')
    list_editable = ('est_premium',)

    def apercu_photo_du_maire(self, obj):
        if obj.photo_du_maire:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 1px solid #ddd;" />', 
                obj.photo_du_maire.url
            )
        return "Pas de photo"
    apercu_photo_du_maire.short_description = "Photo"

    class Media:
        css = {
            'all': ('territoire/css/custom_admin.css',)
        }

# --- MODULES DE L'ACADÉMIE AGROPASTORALE SADDUR ---

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'specialite', 'suivi_etudiants', 'chiffre_affaires_total', 'part_enseignant_40', 'part_saddur_60')
    search_fields = ('nom_complet', 'specialite')

    def suivi_etudiants(self, obj):
        formations_ids = obj.formations.values_list('id', flat=True)
        total = DemandeInscriptionAcademie.objects.filter(formation_id__in=formations_ids, valide_par_saddur=True).count()
        return format_html('<b>{} apprenants</b>', total)
    suivi_etudiants.short_description = "Volume Élèves"

    def chiffre_affaires_total(self, obj):
        ca_total = 0
        for formation in obj.formations.all():
            eleves_valides = DemandeInscriptionAcademie.objects.filter(formation=formation, valide_par_saddur=True).count()
            ca_total += eleves_valides * formation.tarif
        ca_propre = f"{ca_total:_}".replace("_", " ")
        return format_html('<span style="color: #1e293b; font-weight: bold;">{} FCFA</span>', ca_propre)
    chiffre_affaires_total.short_description = "CA Global Généré"

    def part_enseignant_40(self, obj):
        ca_total = 0
        for formation in obj.formations.all():
            eleves_valides = DemandeInscriptionAcademie.objects.filter(formation=formation, valide_par_saddur=True).count()
            ca_total += eleves_valides * formation.tarif
        part_prof = int(ca_total * 0.40)
        prof_propre = f"{part_prof:_}".replace("_", " ")
        return format_html('<span style="color: #2563eb; font-weight: 800;">{} FCFA (40%)</span>', prof_propre)
    part_enseignant_40.short_description = "Rémunération Expert"

    def part_saddur_60(self, obj):
        ca_total = 0
        for formation in obj.formations.all():
            eleves_valides = DemandeInscriptionAcademie.objects.filter(formation=formation, valide_par_saddur=True).count()
            ca_total += eleves_valides * formation.tarif
        part_saddur = int(ca_total * 0.60)
        saddur_propre = f"{part_saddur:_}".replace("_", " ")
        return format_html('<span style="color: #059669; font-weight: 800;">{} FCFA (60%)</span>', saddur_propre)
    part_saddur_60.short_description = "Part SADDUR"

@admin.register(FormationAgricole)
class FormationAgricoleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_production', 'enseignant', 'niveau', 'tarif', 'duree_estimee', 'date_creation')
    prepopulated_fields = {'slug': ('titre',)}
    list_filter = ('type_production', 'niveau', 'enseignant')
    search_fields = ('titre', 'description')

@admin.register(ChapitreCours)
class ChapitreCoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'formation', 'ordre')
    list_filter = ('formation',)

@admin.register(DemandeInscriptionAcademie)
class DemandeInscriptionAcademieAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'formation', 'commune_residence', 'telephone', 'valide_par_saddur', 'bouton_attestation')
    list_filter = ('formation', 'valide_par_saddur', 'commune_residence')
    list_editable = ('valide_par_saddur',)

    def bouton_attestation(self, obj):
        if obj.valide_par_saddur:
            return format_html(
                '<a class="button" href="/academie/attestation/{}/" target="_blank" style="background-color: #059669; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; text-decoration: none;">📄 Télécharger PDF</a>',
                obj.id
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">Non validé</span>')
    bouton_attestation.short_description = "Attestation SADDUR"

@admin.register(CandidatureFormateur)
class CandidatureFormateurAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'ministere_origine', 'specialite', 'telephone_whatsapp', 'est_approuve', 'date_postulation')
    list_filter = ('ministere_origine', 'est_approuve', 'date_postulation')
    search_fields = ('nom_complet', 'specialite', 'biographie_experience')
    list_editable = ('est_approuve',)


# --- MODULES DU MARCHÉ NATIONAL CONNECTÉ SADDUR ---

@admin.register(EntrepreneurAgricole)
class EntrepreneurAgricoleAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'nom_entreprise', 'ville_base', 'telephone_whatsapp', 'date_adhesion')
    search_fields = ('nom_complet', 'nom_entreprise', 'ville_base')
    list_filter = ('ville_base', 'date_adhesion')

@admin.register(ArticleVitrine)
class ArticleVitrineAdmin(admin.ModelAdmin):
    list_display = ('nom_produit', 'entrepreneur', 'prix_unitaire', 'quantite_disponible', 'localite_stock', 'disponibilite_temps', 'date_publication')
    list_filter = ('localite_stock', 'date_publication', 'nom_produit')
    search_fields = ('nom_produit', 'localite_stock')


# --- NOUVEAU : ENREGISTREMENT DES MODULES DE LA FOIRE NATIONALE SADDUR ---

@admin.register(ActeurEvenement)
class ActeurEvenementAdmin(admin.ModelAdmin):
    list_display = ('nom_organisation', 'type_acteur', 'telephone_contact')
    list_filter = ('type_acteur',)
    search_fields = ('nom_organisation', 'opportunites_offertes')

@admin.register(ProjetPavillonMairie)
class ProjetPavillonMairieAdmin(admin.ModelAdmin):
    list_display = ('titre_realisation', 'mairie', 'budget_estime', 'stade_projet')
    list_filter = ('mairie', 'stade_projet')
    search_fields = ('titre_realisation', 'description_technique')