from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('create/', views.create_game, name='create_game'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('gallery/', views.game_gallery, name='game_gallery'),
    path('<int:game_id>/add_character/', views.add_character, name='add_character'),

     # Auth
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    #Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

]