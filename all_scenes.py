import pygame as pg
import sys
import os
from load_img import *
from game_button import *
from scene import *
pg.init()

width = 800
height = 800

IS_FULLSCREEN = False
IS_SMALL_WIN = True
IS_MEDIUM_WIN = False

class MainMenu(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.btn_start = GameButton(width//2+175, height-500, 150, 150, img = 'assets/start_button_unactivate.png', img_activate = 'assets/start_button_activate.png')
        self.btn_exit = GameButton(width//2+175, height-150, 150, 150, img = 'assets/exit_button_unactivate.png', img_activate = 'assets/exit_button_activate.png')
        self.btn_settings = GameButton(width//2+175, height-325, 150, 150, img = 'assets/settings_button_unactivate.png', img_activate = 'assets/settings_button_activate.png')
        self.name = 'MainMenu'
        self.start_music('sound/fon_music.mp3')
        self.bg = load_img('assets/img_bg3.png', (width, height))

        
    def hendler(self, event):
        super().hendler(event)
        if self.btn_start.is_clicked(event):
            return 'game'
        if self.btn_exit.is_clicked(event):
            return 'quit'
        if self.btn_settings.is_clicked(event):
            return 'settings'
            
    def update(self):
        super().update()
        self.btn_start.update(self.mouse)
        self.btn_exit.update(self.mouse)
        self.btn_settings.update(self.mouse)
            
    def draw(self, scene):
        super().draw(scene)
        self.btn_start.draw(scene, self.font)
        self.btn_exit.draw(scene, self.font)
        self.btn_settings.draw(scene, self.font)
        
class GameMenu(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.bg = load_img('assets/img_bg3.png', (width, height))
        self.btn_new_game = pg.Rect(width-200, height-400, 100, 50)
        self.btn_load_game = pg.Rect(width-200, height-350, 100, 50)
        self.btn_return_game = pg.Rect(width-200, height-300, 100, 50)
        self.color_new_game = (200, 200, 200)
        self.color_load_game = (200, 200, 200)
        self.color_return_game = (255, 200, 100)
        self.start_music('sound/fon_music_2.mp3')
        
    def update(self):
        super().update()
        if self.btn_new_game.collidepoint(self.mouse):
            self.color_new_game = (100, 100, 100)
        else:
            self.color_new_game = (200, 200, 200)
        if self.btn_load_game.collidepoint(self.mouse):
            self.color_load_game = (150, 150, 150)
        else:
            self.color_load_game = (200, 200, 200)
        if self.btn_return_game.collidepoint(self.mouse):
            self.color_return_game = (205, 255, 205)
        else:
            self.color_return_game = (255, 200, 100)
            
    def draw(self, scene):
        super().draw(scene)
        pg.draw.rect(scene, self.color_new_game, self.btn_new_game)
        pg.draw.rect(scene, self.color_load_game, self.btn_load_game)
        pg.draw.rect(scene, self.color_return_game, self.btn_return_game)
        scene.blit(self.font.render('New game', True, (0, 0, 0)), (self.btn_new_game.x, self.btn_new_game.y))
        scene.blit(self.font.render('Load game', True, (0, 0, 0)), (self.btn_load_game.x, self.btn_load_game.y))
        scene.blit(self.font.render('Back', True, (0, 0, 0)), (self.btn_return_game.x, self.btn_return_game.y))
    
    def hendler(self, event):
        super().hendler(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.btn_new_game.collidepoint(self.mouse):
                    return 'scenarios'
                elif self.btn_load_game.collidepoint(self.mouse):
                    print('Load Game')
                    return 'load_game'
                elif self.btn_return_game.collidepoint(self.mouse):
                    print('Back')
                    return 'MainMenu'
                
class SettingsMenu(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.width = width
        self.height = height
        self.r_width, self.r_height = self.width-200, self.height-200
        self.recurse_scene = pg.Surface((self.r_width,
                                         self.r_height))
        self.main_bg = load_img('assets/img_bg3.png',
                                (self.width,
                                 self.height))
        self.rec_bg = load_img('assets/Setting_bg.png',
                               (self.r_width,
                                self.r_height))
        self.rect_recurse_scene = pg.Rect(100,
                                          100,
                                          self.r_width,
                                          self.r_height)
        self.move = False
        button_x = self.rect_recurse_scene.x + self.r_width - 150
        button_y = self.rect_recurse_scene.y + self.r_height - 150
#         self.self.r_width//2+150
#         self.r_height-200
        self.btn_exit = GameButton(button_x,
                                   button_y,
                                   150,
                                   150,
                                   img = 'assets/exit_button_unactivate.png',
                                   img_activate = 'assets/exit_button_activate.png')
#         self.btn_small_res = GameButton(200,  200, 140, 40, text='800x800')
        self.btn_small_res = GameMoveButton(200, 200, 140, 40,
                                            img = 'assets/music_way.png',
                                            img_activate = 'assets/polzynok_unactivate.png')
        self.btn_medium_res = GameButton(400,  200, 140, 40, text='1024x768')
        self.btn_fullscreen = GameButton(600,  200, 140, 40, text='full')
        self.music_slider = Slider(self.width,
                                   self.height,
                                   400,
                                   50,
                                   val=audio_manager.music_volume,
                                   track_path='assets/music_way.png',
                                   handle_path = 'assets/polzynok_unactivate.png')
        self.sound_slider = Slider(self.width,
                                   self.height+100,
                                   400,
                                   50,
                                   val=audio_manager.sound_volume,
                                   name='sound',
                                   track_path='assets/sound_way.png',
                                   handle_path = 'assets/polzynok_unactivate.png')
        self.offset_x = 0
        self.offset_y = 0
        
        self.resize = False
        self.resize_mouse_pos = (0, 0)
        self.resize_start_pos = (0, 0)
        self.resize_start_size = (self.r_width, self.r_height)
        
        self.resize_max_w = width - 50
        self.resize_max_h = height - 50
        self.resize_min_w = 200
        self.resize_min_h = 200
        
        self.sqrt_resize = 16
        
    def _get_coords_sqrt_resize(self):
        return pg.Rect(self.rect_recurse_scene.x,
                       self.rect_recurse_scene.y,
                       self.sqrt_resize,
                       self.sqrt_resize)
        
    def draw(self, scene):
        super().draw(scene)
        if self.main_bg:
            scene.blit(self.main_bg, (0, 0))
        else:
            scene.fill((0, 255, 0))
        if self.rec_bg:
            scale = pg.transform.scale(self.rec_bg,
                                           (self.rect_recurse_scene.width,
                                            self.rect_recurse_scene.height))
            self.recurse_scene.blit(scale, (0, 0))
        else:
            self.recurse_scene.fill((255, 0, 0))
        scene.blit(self.recurse_scene, self.rect_recurse_scene)
        self.music_slider.draw(scene)
        self.sound_slider.draw(scene)
        self.btn_exit.draw(scene, self.font)
        
        self.btn_small_res.draw(scene, self.font, scalew = 2, scaleh = 2)
        self.btn_medium_res.draw(scene, self.font)
        self.btn_fullscreen.draw(scene, self.font)
        
    def update(self):
        super().update()
        
        self.button_resize(self.rect_recurse_scene.x,
                           self.rect_recurse_scene.y,
                           self.rect_recurse_scene.width,
                           self.rect_recurse_scene.height)
        
    def hendler(self, event):
        global IS_FULLSCREEN, IS_MEDIUM_WIN, IS_SMALL_WIN, width, height
        
        super().hendler(event)
        
        self.music_slider.hendler(event)
        self.sound_slider.hendler(event)
        
        if self.btn_exit.is_clicked(event):
            return 'MainMenu'
        
        if self.btn_small_res.is_clicked(event):
            width, height = 800, 800
            IS_SMALL_WIN = not IS_SMALL_WIN
            if IS_SMALL_WIN:
                IS_FULLSCREEN, IS_MEDIUM_WIN = False, False
            return 'apply_res'
        
        if self.btn_medium_res.is_clicked(event):
            width, height = 1024, 768
            IS_MEDIUM_WIN = not IS_MEDIUM_WIN
            if IS_MEDIUM_WIN:
                IS_FULLSCREEN, IS_SMALL_WIN = False, False
            return 'apply_res'
        
        if self.btn_fullscreen.is_clicked(event):
            IS_FULLSCREEN = not IS_FULLSCREEN
            if IS_FULLSCREEN:
                IS_SMALL_WIN, IS_MEDIUM_WIN = False, False
            return 'apply_res'
        
        if (event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect_recurse_scene.collidepoint(event.pos)
            and not self.music_slider.move
            and not self.sound_slider.move
            and not self.resize):
            self.move = True
            self.offset_x = self.rect_recurse_scene.x - event.pos[0]
            self.offset_y = self.rect_recurse_scene.y - event.pos[1]
            
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.move = False
            self.resize = False
            
        elif event.type == pg.MOUSEMOTION and self.move:
            new_x = event.pos[0] + self.offset_x
            new_y = event.pos[1] + self.offset_y
            max_x = self.width - self.rect_recurse_scene.width
            max_y = self.height - self.rect_recurse_scene.height
            self.rect_recurse_scene.x = max(0, min(new_x, max_x))
            self.rect_recurse_scene.y = max(0, min(new_y, max_y))
            
        sqrt = self._get_coords_sqrt_resize()
        
        if (event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
            and sqrt.collidepoint(event.pos)):
            self.resize = True
            self.resize_mouse_pos = event.pos
            self.resize_start_pos = (self.rect_recurse_scene.x,
                                     self.rect_recurse_scene.y)
            self.resize_start_size = (self.r_width, self.r_height)
            
        elif event.type == pg.MOUSEMOTION and self.resize:
            self.dx = self.resize_mouse_pos[0] - event.pos[0]
            self.dy = self.resize_mouse_pos[1] - event.pos[1]
            
            new_w = max(self.resize_min_w,
                        min(self.resize_start_size[0] + self.dx,
                                               self.resize_max_w))
            new_h = max(self.resize_min_h,
                        min(self.resize_start_size[1] + self.dy,
                                               self.resize_max_h))
            self.r_width = new_w
            self.r_height = new_h
            
            self.rect_recurse_scene.x = self.resize_start_pos[0] + self.resize_start_size[0] - new_w
            self.rect_recurse_scene.y = self.resize_start_pos[1] + self.resize_start_size[1] - new_h
            
            self.rect_recurse_scene.width = new_w
            self.rect_recurse_scene.height = new_h
            
            self.recurse_scene = pg.Surface((new_w, new_h))
            self.button_resize(self.rect_recurse_scene.x,
                               self.rect_recurse_scene.y,
                               new_w,
                               new_h)
            
    def button_resize(self, x, y, w, h):
        scale = max(0.35, min(1.0,
                              min(w/self.resize_max_w,
                                h/self.resize_max_h)))
        
        pad = int(100 * scale)
        title_pad = int(250 * scale)
        
        res_width = int(140 * scale)
        res_height = int(40 * scale)
        res_pad = int(100 * scale)
        
        res_buttons = (self.btn_small_res,
                       self.btn_medium_res,
                       self.btn_fullscreen)
        
        for i, btn in enumerate(res_buttons):
            btn.rect.width = res_width
            btn.rect.height = res_height
            btn.rect.x = x + pad
            btn.rect.y = y + pad + title_pad + res_pad * i
            
        self.btn_small_res.update(self.mouse)
        self.btn_small_res.activate = True if IS_SMALL_WIN else False
        
        self.btn_medium_res.update(self.mouse)
        self.btn_medium_res.activate = True if IS_MEDIUM_WIN else False
        
        self.btn_fullscreen.update(self.mouse)
        self.btn_fullscreen.activate = True if IS_FULLSCREEN else False
        
        slider_w = int(400 * scale)
        slider_h = int(50 * scale)
        
        self.sound_slider.main_rect.width = slider_w
        self.music_slider.main_rect.width = slider_w
        self.sound_slider.main_rect.height = slider_h
        self.music_slider.main_rect.height = slider_h
        
        self.sound_slider.main_rect.x = x + 1.25 * pad 
        self.sound_slider.main_rect.y = y + pad
        self.music_slider.main_rect.x = x + 1.25 * pad
        self.music_slider.main_rect.y = y + pad + res_pad
        
        for s in (self.music_slider, self.sound_slider):
            s.polzynok_width = max(10, s.main_rect.width // 5)
            s.runway = s.main_rect.width - s.polzynok_width
            s.polzynok_rect.height = slider_h
            if s.picture_main_rect:
                s.picture_main_rect = load_img(s.track_path, (s.main_rect.width,
                                                              s.main_rect.height))
            if s.picture_polzynok:
                s.picture_polzynok = load_img(s.handle_path, (s.polzynok_width,
                                                              s.main_rect.height))
            s.polzynok_move_by_value()
        
        exit_res = int(scale * 200)
        self.btn_exit.rect.width = exit_res
        self.btn_exit.rect.height = exit_res
        self.btn_exit.rect.x = x + w - exit_res - pad
        self.btn_exit.rect.y = y + h - exit_res - pad
        if self.btn_exit.img and self.btn_exit.img_activate:
            self.btn_exit.img = load_img(self.btn_exit.img_path, (exit_res, exit_res))
            self.btn_exit.img_activate = load_img(self.btn_exit.img_activate_path, (exit_res, exit_res))
        self.btn_exit.update(self.mouse)
        
class Scenarios(Scene):
    castles = [{'title':'Necrptozis',
                'heroes':['Vidomina', 'Straker'],
                'bonus':['gold', 'resources', 'artifact']},
               {'title':'Sky castle',
                'heroes':['Gabriel', 'Azazel'],
                'bonus':['gold', 'resources', 'artifact']}]
    difficulty = ('easy', 'normal', 'hard')
    def __init__(self, width, height):
        super().__init__(width, height)
        self.width = width
        self.height = height
        self.main_bg = load_img('assets/scenarios_bg.png',
                                (self.width,
                                 self.height))
        self.rect_list = pg.Rect(100, 100, 400, 600)
        self.btn_exit = GameButton(self.width - 200,
                                   self.height - 200,
                                   150,
                                   150,
                                   img = 'assets/exit_button_unactivate.png',
                                   img_activate = 'assets/exit_button_activate.png')
        
    def hendler(self, event):
        super().hendler(event)
        
        if self.btn_exit.is_clicked(event):
            return 'MainMenu'
        
    def draw(self, scene):
        super().draw(scene)
        
        if self.main_bg:
            scene.blit(self.main_bg, (0, 0))
        else:
            scene.fill((0, 255, 0))
        scene.blit(load_img('assets/setting_bg.png',
                                (400,
                                600)), self.rect_list)
        self.btn_exit.draw(scene, self.font)