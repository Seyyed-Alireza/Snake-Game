# import pygame
# import os

# pygame.mixer.init()
# pygame.mixer.music.load('./assets/music.mp3')
# pygame.mixer.music.play(-1)

import pygame
import os
import random

pygame.mixer.init()
songs = []
current_index = 0

def load_music(path):
    global songs, current_index
    music_folder = f'assets/{path}'
    try:
        songs = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".mp3")]
        random.shuffle(songs)
        current_index = 0
        if songs:
            return play_current()
        return False
    except:
        return False

def play_current():
    if songs:
        try:    
            pygame.mixer.music.load(songs[current_index])
            pygame.mixer.music.play()
            return True
        except:
            return False

def eat_sound():
    eat = pygame.mixer.Sound('assets/eat/eat.wav')
    eat.play()

def stop_music():
    pygame.mixer.music.stop()

def update_music():
    global current_index
    if not songs:
        return
    if not pygame.mixer.music.get_busy():
        current_index = (current_index + 1) % len(songs)
        play_current()
