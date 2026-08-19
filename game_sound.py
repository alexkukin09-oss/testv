import pygame as pg
import sys
import os
from load_img import *
pg.init()
pg.mixer.init()

class GameSound:
    def __init__(self, music_volume = 0.0, sound_volume = 0.0):
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self.path_sound = self.load_sound()
        
    def load_music(self, path):
        if path and os.path.exists(path):
            pg.mixer.music.load(path)
            return True
        return False
            
    def play_music(self, loop=-1):
        self.set_volume_music(self.music_volume)
        pg.mixer.music.play(loop)
        
    def stop_music(self):
        pg.mixer.music.stop()
        
    def set_volume_music(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pg.mixer.music.set_volume(self.music_volume)
    
    def set_volume_sound(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        pg.mixer.Sound.set_volume(self.path_sound, self.sound_volume)
        
    def load_sound(self):
        path = 'sound/button_sound.mp3'
        if path and os.path.exists(path):
            snd = pg.mixer.Sound(path)
            snd.set_volume(self.sound_volume)
            return snd
            
    def play_sound(self, name):
        name.play()
        
audio_manager = GameSound()