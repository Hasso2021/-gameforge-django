import uuid
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.core.files.base import ContentFile
from .models import Game, Character
from .forms import GameForm, CharacterForm
from .ai import query_text_model, generate_image
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


# SIGNUP
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
        else:
            print("Form is not valid:", form.errors)
            # Handle form errors here if needed
            # You can also add a message to the user about the error
            messages.error(request, "There was an error with your signup.")
            return redirect('signup')  # Redirect to the signup page again
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

    
#  HOME
def home(request):
    return render(request, 'core/home.html')

#  CREATE GAME + AI generation
@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user

            # AI prompt
            prompt = (
                f"Crée un univers de jeu pour un jeu vidéo de genre {game.genre} "
                f"avec une ambiance {game.theme}. "
                f"Inspirations: {game.inspirations}. "
                f"Fournis une description immersive du monde et une histoire principale en 3 actes avec un retournement narratif."
            )

            # TEXT AI
            ai_text = query_text_model(prompt)
            game.universe = ai_text.split("Acte")[0].strip()
            game.story = "\n".join(["Acte" + part for part in ai_text.split("Acte")[1:]])

            # IMAGE AI — Character
            char_prompt = f"Portrait stylisé d'un personnage d'un jeu {game.genre} ambiance {game.theme}"
            char_data = generate_image(char_prompt)
            if char_data:
                game.concept_art_character.save(f"char_{uuid.uuid4().hex}.png", ContentFile(char_data))

            # IMAGE AI — Environment
            env_prompt = f"Environnement immersif d'un jeu {game.genre} ambiance {game.theme}"
            env_data = generate_image(env_prompt)
            if env_data:
                game.concept_art_environment.save(f"env_{uuid.uuid4().hex}.png", ContentFile(env_data))

            game.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm()
    return render(request, 'core/create_game.html', {'form': form})


#GAME DETAIL
@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'core/game_detail.html', {'game': game})


#ADD CHARACTER
@login_required
def add_character(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.game = game
            character.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = CharacterForm()
    return render(request, 'core/add_character.html', {'form': form, 'game': game})


#  DASHBOARD — user games only
@login_required
def user_dashboard(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'core/dashboard.html', {'games': games})


# PUBLIC GALLERY
@login_required
def game_gallery(request):
    games = Game.objects.filter(is_public=True)
    return render(request, 'core/gallery.html', {'games': games})
