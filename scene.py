import pygame as pg
import sys
import os
from load_img import *
from game_button import *
pg.init()

        
class Scene:
    def __init__(self, width, height):
        self.scene = pg.display.set_mode((width, height))
        self.font = pg.font.SysFont('Roboto', 30)
        self.bg = None
        self.btn_exit = GameButton(0, 0, 1, 1)
        
    @property
    def mouse(self):
        return pg.mouse.get_pos()
        
    def hendler(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
    def update(self):
        self.btn_exit.update(self.mouse)
    
    def draw(self, scene):
        if self.bg:
            scene.blit(self.bg, (0, 0))
        else:
            scene.fill((0, 0, 0))
            
    def start_music(self, path):
        if audio_manager.load_music(path):
            audio_manager.play_music()
    