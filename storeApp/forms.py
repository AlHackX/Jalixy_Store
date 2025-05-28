from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from storeApp.models import Review
import re

class ReviewForm(forms.ModelForm):

    RATING_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label='Calificación'
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu reseña...'}),
        }


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label = "Nombre de usuario",
        max_length = 150,
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Ej: usuario123'
        }),
        error_messages = {
            'required': 'Debes ingresar un nombre de usuario',
            'max_length': 'Máximo 150 caracteres',
            'invalid': 'Solo letras, números y @/./+/-/_'
        }
    )
    
    password1 = forms.CharField(
        label = "Contraseña",
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Crea una contraseña segura'
        }),
        error_messages = {
            'required': 'Debes crear una contraseña'
        }
    )
    
    password2 = forms.CharField(
        label = "Confirmar contraseña",
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña'
        }),
        error_messages = {
            'required': 'Debes confirmar tu contraseña'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError(
                "No se permiten caracteres especiales excepto @/./+/-/_",
                code='invalid_username'
            )
        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres",
                code='password_too_short'
            )
        return password1
    
    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if len(password2) < 8:
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres",
                code='password_too_short'
            )
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label = "Nombre de usuario",
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Tu nombre de usuario'
        })
    )
    
    password = forms.CharField(
        label = "Contraseña",
        widget = forms.PasswordInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Tu contraseña'
        })
    )

    error_messages = {
        'invalid_login': "Usuario o contraseña incorrectos. Verifica tus datos.",
        'inactive': "Esta cuenta está inactiva.",
    }