import pygame
import os

# Inicializar o mixer do Pygame
pygame.mixer.init()

# Caminho base para os sons
BASE_SOUNDS_PATH = r"D:\biblioteca\biblioteca\src\assets\sounds"

# Funções para reproduzir os sons
def play_enter():
    pygame.mixer.Sound(os.path.join(BASE_SOUNDS_PATH, "enter.flac")).play()

def play_send():
    pygame.mixer.Sound(os.path.join(BASE_SOUNDS_PATH, "send.flac")).play()

def play_error():
    pygame.mixer.Sound(os.path.join(BASE_SOUNDS_PATH, "error.flac")).play()

def play_list():
    pygame.mixer.Sound(os.path.join(BASE_SOUNDS_PATH, "list.flac")).play()

def play_delete():
    pygame.mixer.Sound(os.path.join(BASE_SOUNDS_PATH, "delet.flac")).play()

def play_created():
    pygame.mixer.Sound(os.path.join(BASE_SOUNDS_PATH, "created.flac")).play()
