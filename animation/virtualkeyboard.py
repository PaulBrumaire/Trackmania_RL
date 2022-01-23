import keyboard
import pyglet
import numpy as np
from pyglet.gl import *

win = pyglet.window.Window(600,450)
left=[100,100]
down=[250,100]
up=[250,250]
right=[400,100]

keys=[up,right,down,left]
def square(x,y):
    glVertex3f(x,y,0)
    glVertex3f(x+100,y,0)

    glVertex3f(x+100,y,0)
    glVertex3f(x+100,y+100,0)

    glVertex3f(x+100,y+100,0)
    glVertex3f(x,y+100,0)

    glVertex3f(x,y+100,0)
    glVertex3f(x,y,0)

def draw_rect(x, y, width, height, color):
    width = int(round(width))
    height = int(round(height))
    image_pattern = pyglet.image.SolidColorImagePattern(color=color)
    image = image_pattern.create_image(width, height)
    image.blit(x+25, y+25)

frame1=None
frame2=None
def update_frame(x,y):
    global frame1, frame2
    if(keyboard.is_pressed('up')):
        frame1 = 0
    elif(keyboard.is_pressed("down")):
        frame1 = 2
    else:
        frame1 = None
    if(keyboard.is_pressed("left")):
        frame2 = 3
    elif(keyboard.is_pressed("right")):
        frame2 = 1
    else:
        frame2 = None

    
    
@win.event
def on_draw():
    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINES)
    square(left[0],left[1])
    square(down[0],down[1])
    square(up[0],up[1])
    square(right[0],right[1])
    glEnd()
    if(frame1 is not None):
        draw_rect(keys[frame1][0],keys[frame1][1],50,50,(255, 0, 0, 1))
    if(frame2 is not None):    
        draw_rect(keys[frame2][0],keys[frame2][1],50,50,(255, 0, 0, 1))
    
    # draw_rect(125,125,50,50,(255, 0, 0, 1))

# every 1/10 th get the next frame
pyglet.clock.schedule(update_frame, 10)
pyglet.app.run()
    