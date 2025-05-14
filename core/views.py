from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import GameForm, CharacterForm
from .ai import query_text_model, generate_image
from django.core.files.base import ContentFile
from .ai import query_text_model, generate_image



@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user

            # 1. Generate universe and story
            prompt = (
                f"Crée un univers de jeu pour un jeu vidéo de genre {game.genre} avec une ambiance {game.theme}. "
                f"Inspirations: {game.inspirations}. "
                f"Fournis une description immersive du monde et une histoire principale en 3 actes avec un retournement."
            )
            ai_text = query_text_model(prompt)
            game.universe = ai_text.split("Acte")[0].strip()
            game.story = "\n".join(["Acte" + part for part in ai_text.split("Acte")[1:]])

            # 2. Generate character art
            char_prompt = f"Portrait stylisé d'un personnage dans un jeu {game.genre}, ambiance {game.theme}"
            char_img = generate_image(char_prompt)
            if char_img:
                game.concept_art_character.save(f"{game.title}_char.png", ContentFile(char_img), save=False)

            # 3. Generate environment art
            env_prompt = f"Illustration d'un lieu emblématique dans un univers {game.theme} ({game.genre})"
            env_img = generate_image(env_prompt)
            if env_img:
                game.concept_art_environment.save(f"{game.title}_env.png", ContentFile(env_img), save=False)

            game.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm()

    return render(request, 'core/create_game.html', {'form': form})


@login_required
def add_character(request, game_id):
    game = get_object_or_404(Game, id=game_id, user=request.user)
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

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'core/game_detail.html', {'game': game})

@login_required
def game_gallery(request):
    games = Game.objects.filter(is_public=True)
    return render(request, 'core/gallery.html', {'games': games})