# import pygame
# import os

# pygame.mixer.init()
# pygame.mixer.music.load('./assets/music.mp3')
# pygame.mixer.music.play(-1)

import pygame
import os
import random

songs = []
current_index = 0

def load_music():
    global songs, current_index
    music_folder = "assets"  # ← مسیر صحیح پوشه
    songs = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".mp3")]
    random.shuffle(songs)
    current_index = 0
    if songs:
        play_current()

def play_current():
    if songs:
        pygame.mixer.music.load(songs[current_index])
        pygame.mixer.music.play()

def update_music():
    global current_index
    if not songs:
        return
    if not pygame.mixer.music.get_busy():
        current_index = (current_index + 1) % len(songs)
        play_current()
