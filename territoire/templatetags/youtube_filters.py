from django import template
import re

register = template.Library()

@register.filter(name='replace_youtube_links')
def replace_youtube_links(url):
    """Extrait l'ID de n'importe quelle adresse YouTube pour générer un lien d'intégration Embed valide"""
    if not url:
        return ""
    reg = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)'
    match = re.match(reg, url)
    if match:
        video_id = match.group(4)
        return f"https://youtube.com{video_id}?rel=0&modestbranding=1"
    return url