import requests
from django.core.files.base import ContentFile
from dotenv import load_dotenv

import os


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# --- TEXT MODEL CONFIG

TEXT_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
TEXT_HEADERS = {
    "Authorization": "Bearer {HF_TOKEN}"
}

# --- IMAGE MODEL CONFIG
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
IMAGE_HEADERS = {
    "Authorization": "Bearer {HF_TOKEN}"
}

def query_text_model(prompt):
    response = requests.post(TEXT_API_URL, headers=TEXT_HEADERS, json={
        "inputs": prompt,
        "parameters": {"max_new_tokens": 400}
    })

    if response.status_code != 200:
        print("Text API error:", response.status_code, response.text)
        return "Erreur lors de la génération."

    try:
        return response.json()[0]["generated_text"]
    except Exception as e:
        print("Text parsing failed:", e)
        return "Erreur de décodage texte."

def generate_image(prompt):
    response = requests.post(IMAGE_API_URL, headers=IMAGE_HEADERS, json={"inputs": prompt})

    if response.status_code != 200:
        print("Image API error:", response.status_code, response.text)
        return None

    return response.content  