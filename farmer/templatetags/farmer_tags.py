from django import template
import os

register = template.Library()

@register.filter
def is_image(file_url):
    if not file_url:
        return False
    # Ensure we're working with a string (url)
    url = str(file_url).lower()
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    return any(url.endswith(ext) for ext in image_extensions)
