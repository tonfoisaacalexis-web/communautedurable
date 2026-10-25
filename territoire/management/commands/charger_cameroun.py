from django.core.management.base import BaseCommand
from territoire.models import Region, Departement

class Command(BaseCommand):
    help = "Charge les 10 régions et les 58 départements du Cameroun en base de données"

    def handle(self, *args, **options):
        # Dictionnaire complet de l'organisation territoriale officielle du Cameroun
        cameroun_data = {
            "ADAMAOUA": ["DJEREM", "FARO-ET-DEO", "MAYO-BANYO", "MBERE", "VINA"],
            "CENTRE": ["HAUTE-SANAGA", "LEKIE", "MBAM-ET-INOUBOU", "MBAM-ET-KIM", "MEFOU-ET-AFAMBA", "MEFOU-ET-AKONO", "MFOUNDI", "NYONG-ET-KELLE", "NYONG-ET-MFOMO", "NYONG-ET-SOO"],
            "EST": ["BOUMBA-ET-NGOKO", "HAUT-NYONG", "KADEY", "LOM-ET-DJEREM"],
            "EXTREME-NORD": ["DIAMARE", "LOGONE-ET-CHARI", "MAYO-DANAY", "MAYO-KANI", "MAYO-SAVA", "MAYO-TSANAGA"],
            "LITTORAL": ["MOUUNGO", "NKAM", "SANAGA-MARITIME", "WOURI"],
            "NORD": ["BENOUE", "FARO", "MAYO-LOUTI", "MAYO-REY"],
            "NORD-OUEST": ["BOYO", "BUI", "DONGA-MANTUNG", "MENCHUM", "MEZAM", "MOMO", "NGOKETUNJIA"],
            "SUD": ["DJA-ET-LOBO", "MVILA", "OCEAN", "VALLEE-DU-NTEM"],
            "SUD-OUEST": ["FAKO", "LEBIALEM", "MANYU", "MEME", "NDIAN", "KOUPE-MANENGOUBA"],
            "OUEST": ["BAMBOUTOS", "HAUT-NKAM", "HAUTS-PLATEAUX", "KOUNG-KHI", "MENOUA", "MIFI", "NDE", "NOUN"]
        }

        self.stdout.write(self.style.WARNING("Début du chargement des données territoriales..."))

        for region_nom, departements in cameroun_data.items():
            # 1. Création ou récupération de la région
            region_obj, created = Region.objects.get_or_create(nom=region_nom.title())
            if created:
                self.stdout.write(f"Région créée : {region_obj.nom}")

            # 2. Création des départements associés
            for dept_nom in departements:
                # Remplacement des tirets par des espaces pour une belle écriture (ex: Vallée du Ntem)
                nom_propre = dept_nom.replace("-", " ").title()
                # Corrections spécifiques pour les liaisons françaises
                nom_propre = nom_propre.replace(" Et ", " et ")
                
                dept_obj, d_created = Departement.objects.get_or_create(
                    region=region_obj,
                    nom=nom_propre
                )
                if d_created:
                    self.stdout.write(f"  -> Département créé : {dept_obj.nom}")

        self.stdout.write(self.style.SUCCESS("Félicitations ! Les 10 régions et 58 départements du Cameroun sont opérationnels."))