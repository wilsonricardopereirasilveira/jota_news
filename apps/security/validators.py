# apps/security/validators.py
import bleach
from django.core.exceptions import ValidationError

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li',
    'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    '*': ['class']
}


def clean_html(text):
    """Clean HTML content removing potentially dangerous tags"""
    if not text:
        return text

    cleaned = bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )

    return cleaned


def validate_no_script(value):
    """Ensure no script tags are present"""
    if '<script' in value.lower() or 'javascript:' in value.lower():
        raise ValidationError("Script content not allowed")