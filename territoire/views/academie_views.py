from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ..models import FormationAgricole, DemandeInscriptionAcademie
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import uuid
import requests
from django.conf import settings

def academie_home(request):
    """Affiche le catalogue global pour les visiteurs ou redirige vers le paiement au moment de postuler"""
    if request.method == "POST":
        formation_id = request.POST.get('formation_id')
        nom = request.POST.get('nom')
        whatsapp = request.POST.get('whatsapp')
        ville = request.POST.get('ville')
        
        if formation_id and nom and whatsapp and ville:
            formation_obj = get_object_or_404(FormationAgricole, id=formation_id)
            
            # 1. Génération d'une référence transactionnelle Orange Money unique
            ref_unique = f"SADDUR-{uuid.uuid4().hex[:8].upper()}"
            
            # 2. Création de l'inscription à l'état "EN_ATTENTE" par défaut
            inscription = DemandeInscriptionAcademie.objects.create(
                formation=formation_obj,
                nom_complet=nom,
                telephone=whatsapp.strip().replace(" ", ""),
                commune_residence=ville,
                activite_actuelle="Apprenant en ligne",
                motivation="Inscription directe via le portail national",
                statut_paiement='EN_ATTENTE',
                reference_transaction=ref_unique
            )
            
            # 3. Redirection de l'émetteur vers le guichet de paiement Orange Money
            return redirect('simulation_guichet_paiement', reference=ref_unique)

    # LOGIQUE DE FILTRAGE DES COURS ULTRA-FLUIDE POUR LES TESTS
    if request.user.is_authenticated and not request.user.is_superuser:
        username_propre = request.user.username.strip().replace(" ", "")[-9:]
        formations_valides = DemandeInscriptionAcademie.objects.filter(
            telephone__contains=username_propre,
            valide_par_saddur=True
        ).values_list('formation_id', flat=True)
        
        if formations_valides.exists():
            formations = FormationAgricole.objects.filter(id__in=formations_valides)
        else:
            formations = FormationAgricole.objects.all().order_by('-date_creation')
    else:
        formations = FormationAgricole.objects.all().order_by('-date_creation')
        
    return render(request, 'territoire/academie.html', {'formations': formations})

def simulation_guichet_paiement(request, reference):
    """Gère l'aiguillage de l'émetteur et renvoie les messages de confirmation (succès/échec)"""
    inscription = get_object_or_404(DemandeInscriptionAcademie, reference_transaction=reference)
    
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "REUSSITE":
            # Le réseau Orange Money confirme l'encaissement sur votre numéro 699418222
            inscription.statut_paiement = 'SUCCES'
            inscription.valide_par_saddur = True  # Débloque l'accès aux chapitres et vidéos
            inscription.save()
            messages.success(request, f"🎉 Paiement Orange Money reçu ! Votre inscription au cours de {inscription.formation.titre} est validée. Vos accès sont débloqués.")
        else:
            # L'émetteur a annulé ou la transaction a échoué (solde insuffisant, etc.)
            inscription.statut_paiement = 'ECHEC'
            inscription.save()
            messages.error(request, "❌ Le paiement Orange Money a échoué ou a été décliné par l'émetteur. Veuillez réémettre l'ordre d'inscription.")
            
        return redirect('academie_public')
        
    return render(request, 'territoire/simulation_paiement.html', {'inscription': inscription})

def connexion_academie(request):
    """Gère l'authentification sécurisée des apprenants validés par SADDUR"""
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username').strip().replace(" ", "")
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('academie_public')
        else:
            error_message = "Identifiant ou mot de passe incorrect. Assurez-vous que votre inscription a été validée par SADDUR."
            
    return render(request, 'territoire/connexion_academie.html', {'error_message': error_message})

def deconnexion_academie(request):
    """Déconnecte l'apprenant et le renvoie vers l'accueil"""
    logout(request)
    return redirect('academie_public')

def telecharger_attestation_pdf(request, inscription_id):
    """Génère une attestation officielle SADDUR au format PDF paysage haut de gamme avec espaces de visas"""
    inscription = get_object_or_404(DemandeInscriptionAcademie, id=inscription_id, valide_par_saddur=True)
    formation = inscription.formation
    enseignant_nom = formation.enseignant.nom_complet if formation.enseignant else "la Direction Académique SADDUR"
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Attestation_SADDUR_{inscription.id}.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CertTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor('#065f46'), alignment=1, spaceAfter=20)
    text_style = ParagraphStyle('CertText', parent=styles['Normal'], fontName='Helvetica', fontSize=14, leading=22, textColor=colors.HexColor('#1e293b'), alignment=1, spaceAfter=15)
    code_style = ParagraphStyle('CertCode', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, textColor=colors.HexColor('#64748b'), alignment=1)
    sig_title_style = ParagraphStyle('SigTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#065f46'), alignment=1)
    sig_sub_style = ParagraphStyle('SigSub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, textColor=colors.HexColor('#475569'), alignment=1)

    story.append(Paragraph("<b>ASSOCIATION SADDUR</b><br/><font size=10 color='#10b981'>Ingénierie Territoriale & Transition Durable au Cameroun</font>", ParagraphStyle('H', alignment=1, spaceAfter=30)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("ATTESTATION DE FIN DE SÉMINAIRE", title_style))
    story.append(Paragraph("DE RENFORCEMENT DE CAPACITÉS", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("La Direction Académique de l'Association SADDUR certifie solennellement que", text_style))
    story.append(Paragraph(f"<font size=20 color='#047857'><b>M. / Mme {inscription.nom_complet}</b></font>", text_style))
    story.append(Paragraph("a suivi avec assiduité et validé avec succès l'atelier de formation professionnelle portant sur la thématique :", text_style))
    story.append(Paragraph(f"<b>« {formation.titre} »</b>", ParagraphStyle('T', parent=text_style, fontSize=16, textColor=colors.HexColor('#0f172a'))))
    story.append(Paragraph(f"D'une durée totale estimée à <b>{formation.duree_estimee}</b>, sous la supervision technique de <b>{enseignant_nom}</b>.", text_style))
    story.append(Spacer(1, 30))
    
    bloc_enseignant = [
        Paragraph("<b>Le Formateur Référent</b>", sig_title_style),
        Spacer(1, 45),
        Paragraph(f"{enseignant_nom}", sig_sub_style),
        Paragraph("<font size=8 color='#94a3b8'>Visa électronique activé</font>", sig_sub_style)
    ]
    
    bloc_president = [
        Paragraph("<b>Le Président de l'Association SADDUR</b>", sig_title_style),
        Spacer(1, 45),
        Paragraph("Bureau Exécutif National", sig_sub_style),
        Paragraph("<font size=8 color='#94a3b8'>Fait à Ambam, le 29/10/2026</font>", sig_sub_style)
    ]

    data_signatures = [[bloc_enseignant, "", bloc_president]]
    table_signatures = Table(data_signatures, colWidths=[280, 140, 280])
    table_signatures.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(table_signatures)
    story.append(Spacer(1, 25))
    
    code_verification = f"Réf. Vérification unique : SADDUR-2026-REG-{inscription.id:04d}-{inscription.telephone[-9:]}"
    story.append(Paragraph(code_verification, code_style))
    story.append(Paragraph("Délivré en confiance pour valoir ce que de droit. Ce document officiel est traçable sur le portail national communautedurable.cm.", ParagraphStyle('F', parent=code_style, spaceBefore=5)))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response