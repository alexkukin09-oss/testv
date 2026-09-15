import pygame as pg
import sys
import os
import all_scenes
from all_scenes import GameMenu, MainMenu, SettingsMenu, Scenarios
pg.init()

#персонажи: концентрированная такса, всадники на лосях, чиловый скелет, радиактивный рыцарь, шахматы, серный голем
# git
window = pg.display.set_mode((all_scenes.width, all_scenes.height))
scene = MainMenu(all_scenes.width, all_scenes.height)
pg.display.set_caption('Game')


run = True

current_scene = scene.name
while run:
    for event in pg.event.get():
        result = scene.hendler(event)
        
        if result == 'quit':
            run = False
            
        elif result == 'game':
            scene = GameMenu(all_scenes.width, all_scenes.height)
            
        elif result == 'MainMenu':
            scene = MainMenu(all_scenes.width, all_scenes.height)
            
        elif result == 'settings':
            scene = SettingsMenu(all_scenes.width, all_scenes.height)
            
        elif result == 'scenarios':
            scene = Scenarios(all_scenes.width, all_scenes.height)
            
        elif result == 'apply_res':
            if all_scenes.IS_FULLSCREEN:
                window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                all_scenes.width, all_scenes.height = window.get_size()
                all_scenes.width -= 50
                all_scenes.height -= 100
            else:
                window = pg.display.set_mode((all_scenes.width, all_scenes.height))
            scene = SettingsMenu(all_scenes.width, all_scenes.height)
            
    scene.update()
    scene.draw(window)

    pg.display.flip()

pg.quit()
