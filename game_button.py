import pygame as pg
import sys
import os
from load_img import *
from game_sound import audio_manager


class Slider:
    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 val=0.5,
                 name='music',
                 track_path=None,
                 handle_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.s_width, self.s_height = x-700, y-750
        self.track_path = 'assets/music_way.png' if name == 'music' else 'assets/sound_way.png'
        self.handle_path = 'assets/polzynok_unactivate.png'
#         self.picture_main_rect = load_img('assets/music_way.png', (self.width, self.height)) if name == 'music' else load_img('assets/sound_way.png',
#                                                                                                                               (self.width, self.height))
        self.picture_main_rect = load_img(self.track_path,
                                          (self.width,
                                           self.height))
        self.main_rect = pg.Rect(self.x,
                                 self.y,
                                 self.width,
                                 self.height)
        self.val_max = 1.0
        self.val_min = 0.0
        self.val = val
        self.polzynok_width = self.width // 5
        self.picture_polzynok = load_img(self.handle_path,
                                         (self.polzynok_width,
                                          self.height))
        self.polzynok_rect = pg.Rect(self.main_rect.x,
                                     self.main_rect.y,
                                     self.polzynok_width,
                                     self.height)
        self.move = False
        self.runway = self.main_rect.width - self.polzynok_width
        self.name = name
        self.polzynok_move_by_value()
        
    def draw(self, scene):
        if self.picture_main_rect:
            scene.blit(self.picture_main_rect, self.main_rect)
        else:
            pg.draw.rect(scene, (100, 100, 100), self.main_rect, border_radius = 5)
        if self.picture_polzynok:
            scene.blit(self.picture_polzynok, self.polzynok_rect)
        else:
            pg.draw.rect(scene, (50, 50, 50), self.polzynok_rect, border_radius = 5)
            
    def move_update(self, x, y):
        self.main_rect.x = x + self.s_width
        self.main_rect.y = y + self.s_height
        self.polzynok_move_by_value()
        
    def polzynok_move(self, local_x):
        min_x = self.main_rect.x
        max_x = self.main_rect.right - self.polzynok_width
        self.polzynok_rect.x = max(min_x, min(local_x, max_x))
        self.polzynok_rect.y = self.main_rect.y
        
    def polzynok_move_by_value(self):
        self.polzynok_rect.x = self.main_rect.x + int(self.runway * self.val)
        self.polzynok_rect.y = self.main_rect.y
        
    def hendler(self, event):
        if (event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
            and self.polzynok_rect.collidepoint(event.pos)):
            self.move = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.move = False
        elif event.type == pg.MOUSEMOTION and self.move:
            self.polzynok_move(event.pos[0])
            self.val = (self.polzynok_rect.x - self.main_rect.x) / self.runway
            if self.name == 'music':
                audio_manager.set_volume_music(self.val)
            else:
                audio_manager.set_volume_sound(self.val)

class GameButton:
    def __init__(self,
                 x, y, w, h,
                 img = None, img_activate = None,
                 text = '', color = (255, 0, 0),
                 color_activate = (0, 0, 255)):
        self.img_path = img
        self.img_activate_path = img_activate
        self.img = load_img(self.img_path, (w, h))
        self.img_activate = load_img(self.img_activate_path, (w, h))
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.color_activate = color_activate
        self.text = text
        self.activate = False
        
    def draw(self, scene, font):
        if self.img:
            img = self.img_activate if self.activate else self.img
            scene.blit(img, self.rect)
        else:
            color = self.color_activate if self.activate else self.color
            pg.draw.rect(scene, color, self.rect)
            if font and self.text:
                txt = font.render(self.text, True, (0, 0, 0))
                scene.blit(txt, (self.rect.x, self.rect.y))
                
    def update(self, mouse_pos):
        self.activate = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            audio_manager.play_sound(audio_manager.path_sound)
            return True
        
class GameMoveButton(GameButton):
    def __init__(self,
                 x, y, w, h,
                 img = None, img_activate = None,
                 text = '', color = (255, 0, 0),
                 color_activate = (0, 0, 255)):
        super().__init__(x, y, w, h,
                 img = img, img_activate = img_activate,
                 text = text, color = color,
                 color_activate = color_activate)
        self.x = x
        self.y = y
        
    def draw(self, scene, font, scalew = 1, scaleh = 1):
        print(self.rect.width)
        if self.activate:
            new_w = scalew * self.rect.width
            new_h = scaleh * self.rect.height
            self.rect.width = new_w
            print(self.rect.width)
            self.rect.height = new_h
            new_rect = pg.Rect(self.x, self.y, new_w, new_h)
        else:
            new_rect = self.rect
        if self.img and self.img_activate:
            img = self.img_activate if self.activate else self.img
            scale = pg.transform.scale(self.img,
                                           (new_rect.width,
                                            new_rect.height)) #img_unactivate на основной сцене 
            scene.blit(scale, new_rect)
        else:
            color = self.color_activate if self.activate else self.color
            pg.draw.rect(scene, color, new_rect)
            if font and self.text:
                txt = font.render(self.text, True, (0, 0, 0))
                scene.blit(txt, (new_rect.x, new_rect.y))
#         super().draw(scene, font)