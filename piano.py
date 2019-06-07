import pygame
import os
from pygame.locals import *
import math
import numpy
bits = 16
pygame.mixer.pre_init(44100, -bits, 2)
pygame.mixer.init()

width = 800
height = 300
Key_Count = 15
button_width = width/Key_Count
header_height = 50
bkg_image =  pygame.transform.scale(pygame.image.load(os.path.dirname(__file__)+"/bkg.jpg"),(width,height))
key_image = pygame.image.load(os.path.dirname(__file__)+"/key.jpg")


def Sound(freq): 
        duration = 5
        frequency_l = freq
        frequency_r = freq
        sample_rate = 20000


        n_samples = int(round(duration*sample_rate))
        buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
        max_sample = 2**(bits - 1) - 1

        for s in range(n_samples):
                t = float(s)/sample_rate
                buf[s][0] = buf[s][1] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))   # sterio

        sound = pygame.sndarray.make_sound(buf)
        return sound

def colorize(image, newColor):
    image = image.copy()
    image.fill(newColor[0:3] + (150,), None, pygame.BLEND_RGBA_MULT)
    return image


class Button(object):
        def __init__(self,start):
                self.pos = start
                self.color = (255,255,255)
                self.image = pygame.transform.scale(key_image,(button_width,height-header_height))
                self.rect = self.image.get_rect()
                self.rect.x = start
                self.rect.y = header_height

        def click(self):
                self.image = colorize(self.image, (50, 50, 50))
                sound = sounds["key"+str(self.pos)]
                sound.play()
        def unclick(self):
                self.image = pygame.transform.scale(key_image,(button_width,height-header_height))
                sound = sounds["key"+str(self.pos)]
                sound.fadeout(500)
        def draw(self,win):
                x = self.pos
                win.blit(self.image,(x,header_height))
        def check_click(self, mouse):
            return self.rect.collidepoint(mouse)




def redrawWindow(win):
    win.fill((100,0,0)) 
    win.blit(bkg_image,(0,0))
    for b in buttons:
            b.draw(win)
    pygame.display.update()


def main():
    global buttons,sounds
    pygame.mixer.music.fadeout(400)
    pygame.mixer.fadeout(10)
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("LOADING SOUNDS..." )
    clock = pygame.time.Clock()
    buttons = []
    sounds = {}
    clicked = {}
    for i in range(width/button_width):
        clicked[len(buttons)*button_width] = False
        sounds["key"+str(len(buttons)*button_width)] = Sound(100*((len(buttons)+1)*button_width/button_width))
        buttons.append(Button(len(buttons)*button_width))
    pygame.display.set_caption("Piano | By Zayd " )
    

    while True:
        pygame.time.delay(10)           
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                        print("click")
            elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed() == True):
                for b in buttons:
                        if b.check_click(event.pos):
                                b.click()
                                clicked[b.pos] = True
            else : 
                for b in buttons:
                     if clicked[b.pos]:
                        b.unclick()    
        redrawWindow(win)
        

main()
