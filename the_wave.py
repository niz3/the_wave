#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pyglet
from pyglet.gl import *
from engine import *
import ctypes
import random

class Window(pyglet.window.Window):
	def on_draw(self):
		window.clear()
		if game_state == states.RUN:
			glClearColor(0, 128, 128, 255)
			#background.draw()
			terrain.draw()
			sprite.draw()
			scoretext.draw()
			wave.draw()
		if game_state == states.MENU:
			bg.draw()
			for m in menu:
				m.draw()
		if game_state == states.PAUSE:
			pause.draw()
			for m in pause_menu:
				m.draw()
		if game_state == states.GAMEOVER:
			gameover.draw()

	def on_key_press(self, symbol, modifiers):
		global double_jump, selection, game_state, pause_selection, score
		if(symbol==key.SPACE and(sprite.y-5<=terrain.get_y(sprite.x+(sprite.width/2)+terrain.terrain_progress) or double_jump==True)):
			sprite.vspeed=7
			sprite.y+=10
			double_jump=not double_jump
		if game_state == states.MENU:
			if symbol == key.DOWN:
				selection+=1
				if selection == 3:
					selection=0
			if symbol == key.UP:
				selection-=1
				if selection == -1:
					selection=2
			if symbol == key.RETURN:
				if selection == 0:
					game_state=states.RUN
					score = 0
					sprite.x=256;sprite.y=500;sprite.hspeed=0;sprite.vspeed=0
				if selection == 1:
					game_state=states.HISCORE
				if selection == 2:
					self.close()
			
		if game_state == states.PAUSE:
			if symbol == key.DOWN:
				pause_selection+=1
				if pause_selection == 2:
					pause_selection=0
			if symbol == key.UP:
				pause_selection-=1
				if pause_selection == -1:
					pause_selection=1
			if symbol == key.RETURN:
				if pause_selection == 0:
					game_state = states.RUN
				if pause_selection == 1:
					game_state = states.MENU

		if game_state == states.RUN:
			if symbol == key.ESCAPE:
				game_state = states.PAUSE
				
		if game_state == states.GAMEOVER:
			if symbol == key.ENTER:
				game_state = states.MENU

def update(dt):
	global score, double_jump, game_state
	
	for m in menu:
		m.color=(255, 255, 255)
	menu[selection].color=(100, 100, 0)
	for m in pause_menu:
		m.color=(255, 255, 255)
	pause_menu[pause_selection].color=(100, 100, 0)
	
	if game_state == states.RUN:
		score+=0.1
		scoretext.text="Score: "+str(int(score))
		#background.x+=background.hspeed
		terrain.progress(4)
		sprite.x+=sprite.hspeed
		terrain_y=terrain.get_y(sprite.x+(sprite.width/2)+terrain.terrain_progress)
		if sprite.y<=terrain_y:
			sprite.vspeed=0
			sprite.y=terrain_y
			double_jump=False
		else:
			sprite.vspeed+=sprite.gravity
			sprite.y+=sprite.vspeed
		if(sprite.y-5<=terrain_y):
			sprite.y=terrain_y
			if(keys[key.LEFT]):
				sprite.hspeed=-3
			elif(keys[key.RIGHT]):
				sprite.hspeed=1
			else:
				sprite.hspeed=-1
			#if(keys[key.SPACE]):
				#sprite.vspeed+=7
				#sprite.y+=10
		else:
			if(keys[key.LEFT]):
				sprite.hspeed=-2
			elif(keys[key.RIGHT]):
				sprite.hspeed=1
		if(sprite.x+sprite.width>=window.width-200):
			sprite.x=window.width-sprite.width-200
		if(sprite.x<=32):
			game_state=states.GAMEOVER
			sprite.x=32
		sprite.animate()

glEnable(GL_TEXTURE_2D)
block=pyglet.image.load('block.png')
loltexture=block.get_texture()
glBindTexture(GL_TEXTURE_2D, loltexture.id);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL);
#glTexImage2D (GL_TEXTURE_2D, 0, GL_RGB, block.width, block.height, 0, GL_RGB, GL_UNSIGNED_BYTE, ctypes.byref(loltexture.image_data));


class states():
	RUN=0
	MENU=1
	PAUSE=2
	HISCORE=3
	GAMEOVER=4

game_state=states.MENU
#menu
bg=pyglet.sprite.Sprite(pyglet.resource.image('thewave.png'))
start=pyglet.sprite.Sprite(pyglet.resource.image('start.png'),x=200, y=350)
hiscore=pyglet.sprite.Sprite(pyglet.resource.image('hiscore.png'),x=200, y=200)
quit=pyglet.sprite.Sprite(pyglet.resource.image('quit.png'),x=200, y=50)
menu=[start, hiscore, quit]
selection=0
#pause menu
resume=pyglet.sprite.Sprite(pyglet.resource.image('start.png'),x=200, y=350)
pause=pyglet.sprite.Sprite(pyglet.resource.image('pause.png'))
pause_quit=pyglet.sprite.Sprite(pyglet.resource.image('quit.png'),x=200, y=200)
pause_menu=[resume, pause_quit]
pause_selection=0
#gameover
gameover=pyglet.sprite.Sprite(pyglet.resource.image('gameover.png'))

score=0.0
double_jump=False
scoretext=pyglet.text.Label("Score: ", font_name="Arial", font_size=16, x=0, y=600-24, color=(0,0,0,255))
terrain=Terrain()
sprite=Sprite(img="snubbe.png", x=256, y=500, width=32, height=32, gravity=-0.2)
wave=Sprite(img="wave.png", x=0, y=0, width=128, height=512)
#background=Sprite(img="background.png", x=0, y=0, width=1600, height=600, hspeed=-2)
keys=key.KeyStateHandler()
window=Window(width=800, height=600, caption="The Wave")
window.push_handlers(keys)
pyglet.clock.schedule(update)
pyglet.app.run()