from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from .validators import CustomPasswordValidator

def validate_mobile_number(value):
    if not value.isdigit():
        raise ValidationError('Mobile number must contain only digits.')
    if len(value) < 10 or len(value) > 15:
        raise ValidationError('Mobile number must be between 10 and 15 digits.')

class Registration_Data(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=128, validators=[CustomPasswordValidator])  # Use function for validation
    email = models.EmailField(max_length=100, unique=True, validators=[EmailValidator()])
    mobile_number = models.CharField(max_length=15, validators=[validate_mobile_number])
    referral = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user_id

    def save(self, *args, **kwargs):
        CustomPasswordValidator(self.password)  # Validate password before saving
        super().save(*args, **kwargs)
