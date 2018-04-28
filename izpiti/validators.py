from django.core.exceptions import ValidationError

def validate_current(value):
    print(value)
    if value >= 2019:
        raise ValidationError("neaaa deva")