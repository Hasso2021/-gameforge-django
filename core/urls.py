from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_game, name='create_game'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('gallery/', views.game_gallery, name='game_gallery'),
    path('<int:game_id>/add_character/', views.add_character, name='add_character'),

]