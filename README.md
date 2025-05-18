# GameForge

GameForge permet aux utilisateurs de créer des concepts de jeux vidéo en générant automatiquement un univers, une
histoire et des images conceptuelles
grâce à l'intelligence artificielle.


## Présentation du projet

* Génération automatique de l'univers du jeu et d'un scénario narratif structuré en 3 actes.
* Authentification utilisatAeur: (connexion, inscription, déconnexion).
* Galerie publique et tableau de bord privé pour visualiser ses propres jeux.
* Ajout de personnages personnalisés à chaque jeu.



## Technologies utilisées

* Django : Framework web Python.
* MySQL : Système de gestion de base de données relationnelle.
* Tailwind CSS : Framework CSS pour un design moderne et réactif.
* Hugging Face Inference API : Génération d'univers textuels et d'illustrations.
* Python : Langage de programmation principal.
* HTML: Système de templates pour Django.
* .env : Gestion sécurisée des tokens et API.


### 1. Cloner le dépôt

git clone https://github.com/Hasso2021/-gameforge-django.git
cd gameforge-django


### 2. Créer un environnement virtuel

python -m venv myenv
# Windows
myenv\Scripts\activate


### 3. Installer les dépendances

pip install django
pip install mysqlclient
pip install python-dotenv
pip install requests
pip install Pillow


### 4. Configurer Hugging Face

Crée un fichier `.env` à la racine :

HF_TOKEN=ton_token_huggingface

#### Modèle IA utilisés

Texte : mistralai/Mixtral-8x7B-Instruct-v0.1
Utilisé pour générer l’univers du jeu et une histoire immersive.

Images : stabilityai/stable-diffusion-xl-base-1.0
Utilisé pour générer les images du personnage et de l’environnement du jeu.

### 5. Configurer la base de données

Crée une base de données MySQL nommée `gameforge_db` et modifie le fichier `settings.py` :

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'gameforge_db',
'USER': 'root',
'PASSWORD': 'Hello123',
'HOST': 'localhost',
'PORT': '3306',
}
}

### 6. Créer les migrations et migrer la base de données
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver



## Modèles Django
- `User`: Modèle utilisateur personnalisé.
- `Game`: Modèle de jeu avec un titre, une description, une image et un utilisateur associé.
- `Character`: Modèle de personnage avec un nom, une description, une image et un jeu associé.



## Captures d'écran
- voir le dossier `screenshots` pour les captures d'écran de l'application.