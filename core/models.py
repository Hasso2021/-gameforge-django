from django.db import models
from django.contrib.auth.models import User # User here is the default Django user model

class Game(models.Model): 
    title = models.CharField(max_length=100) 
    genre = models.CharField(max_length=50)
    theme = models.TextField()
    inspirations = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games') #
    is_public = models.BooleanField(default=False)
    #favorited_by = models.ManyToManyField(User, related_name='favorites', blank=True)

    universe = models.TextField(blank=True, null=True) # stock l'univers du jeu
    story = models.TextField(blank=True, null=True) # stock l'histoire du jeu

    concept_art_character = models.ImageField(upload_to='characters/', blank=True, null=True) # ici on est en train de stockker l'image du personnage dans le dossier characters
    concept_art_environment = models.ImageField(upload_to='environments/', blank=True, null=True)

    def __str__(self):  
        return self.title

class Character(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    background = models.TextField()
    abilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"  #

# class Location permet de stcoker 
class Location(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_main_setting = models.BooleanField(default=False)

    def __str__(self):
        return self.name