#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import pkg_resources
import sys
required = {'pygame','python-bidi'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import pygame
import random
import copy
import math

pygame.init()
width = 800
height = 450
from pygame.locals import *
from bidi import algorithm
import persian_reshaper
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("TSP")
WHITE = (255, 255, 255)
ACTIVE_COLOR = pygame.Color('dodgerblue1')
INACTIVE_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.SysFont("Times New Roman", 25)
cities=[]
flag1=1
flag2=0
background = (0, 0, 0)
white = (236, 240, 241)
violet = (136, 78, 160)
purple = (99, 57, 116)

points = 10
d = 10
dataa=[]
bestEverOrder = []
bestDistance = 0
order=[]
count = 0.0
x = -1
pause = False
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#Reset the Population and Cities        
def reset():
    global bestEverOrder, bestDistance, order, x, count, pause,dataa
    count = 0.0
    order=[]
    x = -1
    bestEverOrder = []
    bestDistance = 0
    pause = False
#uniform crossover 
def crossover():
    global order, count, x,dataa
    x = 0
    count += 1.0
    for i in range(len(order) - 1):
        if order[i] < order[i + 1]:
            x = i
    y = 0
    for j in range(len(order)):
        if order[x] < order[j]:
            y = j

    swap(order, x, y)

    order[x + 1:] = reversed(order[x + 1:])
def swap(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp

#calculate distanse between two cities
def total_distance(a):
    dist = 0
    for i in range(len(order)-1):
        dist += math.sqrt((a[order[i]].x - a[order[i+1]].x)**2 + (a[order[i]].y - a[order[i+1]].y)**2)

    return dist

# Draw Current and all time best routes
def draw(cities):

    
    # Add Information on Screen
    font = pygame.font.SysFont("Times New Roman", 25)
    text2 = font.render(algorithm.get_display(persian_reshaper.reshape(u'بررسی مسیرها')), True, white)
    display.blit(text2, (70, 10))

    text = font.render(algorithm.get_display(persian_reshaper.reshape(u'بهترین مسیر تا الان')), True, white)
    display.blit(text, (width/2 + 100, 10))

    for i in range(len(order)):
        index = order[i]
        pygame.draw.ellipse(display, white, (cities[index].x, cities[index].y, d, d))

    for i in range(len(order)-1):
        pygame.draw.line(display, white, (cities[order[i]].x + d/2, cities[order[i]].y+d/2), (cities[order[i+1]].x+d/2,
                                                                                              cities[order[i+1]].y+d/2)
                         , 2)

    for i in range(len(order) - 1):
        pygame.draw.line(display, purple, (width/2 + cities[bestEverOrder[i]].x + d / 2, cities[bestEverOrder[i]].y + d / 2),
                         (width/2 + cities[bestEverOrder[i + 1]].x + d / 2, cities[bestEverOrder[i + 1]].y + d / 2), 3)

    for i in range(len(bestEverOrder)):
        index = bestEverOrder[i]
        pygame.draw.ellipse(display, white, (width/2 + cities[index].x, cities[index].y, d, d))

def draw_button(button, screen):
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    
    
    text_surf = FONT.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'callback': callback,
        }
    return button
# Genetic Algorithm Works Here
def main_GA():
    
    loop = True
    global bestEverOrder, bestDistance, order, x, count, pause, points,dataa
    reset()
        
    font = pygame.font.SysFont("Times New Roman", 20)
##  for i in range(totalCities):
##      x = random.randrange(10, width/2 - 10)
##      y = random.randrange(40, height-210)
##      cities.append([x, y])
##      order-.append(i)
    points = len(dataa)
    for i in range(len(dataa)):
        
        dataa[i][0] = int(dataa[i][0])
        dataa[i][1] = int(dataa[i][1])
        
    for i in range(len(dataa)):
        order.append(i)
        i = City(dataa[i][0], dataa[i][1])
        cities.append(i)
    bestDistance = total_distance(cities)
    bestEverOrder = copy.deepcopy(order)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main_GA()
        display.fill(background)
        # Step 1 : Calculate Fitness of population
        dist = total_distance(cities)
        # Step 2 : calculate best fitness of the total fitnesses
        if dist < bestDistance:
            bestDistance = dist
            bestEverOrder = copy.deepcopy(order)

        
        crossover()    
        draw(cities)
        
        currenttext = font.render( algorithm.get_display(persian_reshaper.reshape(u': مسافت فعلی'))+ str(dist), True, white)
        display.blit(currenttext, (50, height - 30))

        text = font.render( algorithm.get_display(persian_reshaper.reshape(u': بهترین مسافت یافت شده')) + str(bestDistance), True, white)
        display.blit(text, (width / 2, height - 30))
            
        
        pygame.display.update()
    
    if x == -1:
        pause = True
        pauseUnpause()
    clock.tick(100000)
        
        

    
    
    
      
def main():
    
    screen = pygame.display.set_mode((800, 450))
    clock = pygame.time.Clock()
    done = False
    press=False
    
     
    button1 = create_button(70, 375, 250, 50, algorithm.get_display(persian_reshaper.reshape(u'شروع عملیات')), main_GA)
    # A list that contains all buttons.
    button_list = [button1]

    while not done:
        
        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
                done = True
            # This block is executed once for each MOUSEBUTTONDOWN event.
              
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    
                    for button in button_list:
                        if button['rect'].collidepoint(event.pos):
                            button['callback']()
            elif event.type == pygame.MOUSEMOTION:
                # When the mouse gets moved, change the color of the
                # buttons if they collide with the mouse.
                for button in button_list:
                    if button['rect'].collidepoint(event.pos):
                        # `event.pos` is the mouse position.
                        button['color'] = ACTIVE_COLOR
                    else:
                        button['color'] = INACTIVE_COLOR
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(20, 350, 360, 5))            
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(380, 25, 5, 330))            
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(20, 25, 5, 330))
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(20, 25, 360, 5))
            filled_rect = pygame.Rect(420, 75, 330, 300)
            pygame.draw.rect(screen, (255,255,255), filled_rect)  
            screen.blit(FONT.render(algorithm.get_display(persian_reshaper.reshape(u'---------------- راهنما ---------------')), True, INACTIVE_COLOR), (430, 100))
            screen.blit(FONT.render(algorithm.get_display(persian_reshaper.reshape(u'سلام به برنامه مسئله فروشنده دوره گرد')), True, INACTIVE_COLOR), (430, 150))
            screen.blit(FONT.render(algorithm.get_display(persian_reshaper.reshape(u'خوش آمدید در ابتدا موقعیت شهر ها را ' )), True, INACTIVE_COLOR), (430, 175))
            screen.blit(FONT.render(algorithm.get_display(persian_reshaper.reshape(u'در کادر سفید رنگ صفحه وارد کنید و  ')), True, INACTIVE_COLOR), (430, 200))
            screen.blit(FONT.render(algorithm.get_display(persian_reshaper.reshape(u'در ادامه کلید شروع عملیات را بزنید.   ')), True, INACTIVE_COLOR), (430, 225))
            #construct the guid with draw.rect and screen.blit
            px, py = pygame.mouse.get_pos() 
            #position x , y of the city that will be add if the user use the mousebutton 
            if flag1==1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.ellipse(screen,(236, 240, 241),(px,py,10,10))
                    dataa.append([px,py])
                    
                flag1==0
                flag2==1
            
            if flag2==1:
                if event.type == pygame.MOUSEBUTTONUP:
                    press == False
                        
                flag2==0 
                flag1==1
        
        
        for button in button_list:
            draw_button(button, screen)
        pygame.display.update()
        clock.tick(30)
    
        
def pauseUnpause():
    global pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    pause = False
    main_GA()
if __name__ == '__main__':
    main()
    
    
pygame.quit()


# In[ ]:




