from django.core.exceptions import ValidationError
import re


def validate_no_html(value):
    """Blocks any HTML or script tags to prevent XSS injection"""
    if re.search(r'<[^>]*>',value):
        raise ValidationError('HTML tags are not allowed in this field.')
    return value

def validate_alphanumeric_spaces(value):
    """Only allows letters,numbers and spaces"""
    if not re.match(r'^[a-zA-Z0-9\s]+$',value):
        raise ValidationError('Only letters, numbers and spaces are allowed.')
    return value