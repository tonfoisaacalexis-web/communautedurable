from django.contrib import admin
from django.utils.html import format_html
from .models import Mairie, Region, Departement  # <-- Assurez-vous d'importer Region et Departement ici
from .models import Mairie, Region, Departement, DocumentMunicipal # <-- Ajoutez DocumentMunicipal ici

admin.site.register(DocumentMunicipal)

# Enregistrement simple pour avoir accès aux formulaires
admin.site.register(Region)
admin.site.register(Departement)

# --- CONFIGURATION DES TITRES DU BACK-OFFICE ---
admin.site.site_header = "Communautedurable.cm"
admin.site.site_title = "Communautedurable.cm"
admin.site.index_title = "Gestion de l'espace Territoire"

@admin.register(Mairie)
class MairieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement', 'nom_du_maire', 'apercu_photo_du_maire')
    search_fields = ('nom', 'nom_du_maire')
    prepopulated_fields = {'slug': ('nom',)}
    list_filter = ('departement',)

    def apercu_photo_du_maire(self, obj):
        if obj.photo_du_maire:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 50%; border: 1px solid #ddd;" />', 
                obj.photo_du_maire.url
            )
        return "Pas de photo"
    apercu_photo_du_maire.short_description = "Photo"

    # --- INJECTION CSS POUR AGRANDIR TOUS LES CARACTÈRES ---
    class Media:
        css = {
            'all': ('territoire/css/custom_admin.css',)
        }