from django import forms
from .models import Pelicula


class PeliculasForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = '__all__'
        
class SalaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = '__all__'
        