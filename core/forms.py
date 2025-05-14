from django import forms
from .models import Game, Character

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'genre', 'theme', 'inspirations', 'is_public']

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'role', 'background', 'abilities']