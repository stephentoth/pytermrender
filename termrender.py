import time, math
from colorama import Fore, Back, Style
import functools
printr = functools.partial(print, end="")

###############
FRAMERATE=30
HEIGHT=24
WIDTH=80
###############

FRAME_NO=0
def clearBuffer():
    global screen_buffer,screen_buffer_color
    screen_buffer = [[" "]*WIDTH for y in range(HEIGHT)]
def clearBufferColor():
    global screen_buffer,screen_buffer_color
    screen_buffer_color = [[Style.RESET_ALL]*WIDTH for y in range(HEIGHT)]
def clearAllBuffers():
    clearBuffer()
    clearBufferColor()
def clearScreen():
    printr('\033[2J')

def render(clear=True):
    if clear:
        clearScreen()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            printr(screen_buffer_color[y][x])
            printr(screen_buffer[y][x])
        print() #print \n

def renderLoop():
    trackers()
    draw()
    render()
def framerateMaker(func, perSec):
    interval = 1.0 / perSec
    while True:
        start_time = time.time()
        func()
        elapsed = time.time() - start_time
        if elapsed < interval:
            time.sleep(interval-elapsed)
################

class RenderException(Exception):
    pass

def printBuffer(x, y, val):
    global screen_buffer
    string=str(val)
    if len(string) > WIDTH-x:
        raise RenderException("Too Long")
    for i, l in enumerate(string):
        screen_buffer[y][x+i]=l

def clearLine(y):
    global screen_buffer
    screen_buffer[y]=[" "]*WIDTH

def drawBox(x,y,width,height,char):
    if x+width > WIDTH or y+height > HEIGHT:
        raise RenderException("Box too BIG")
    for w_x in range(width):
        for w_y in range(height):
            if (w_x==0 or w_x==width-1) or (w_y==0 or w_y==height-1):
                screen_buffer[y+w_y][x+w_x] = char

####################
def trackers():
    global FRAME_NO
    FRAME_NO+=1

def main():
    setup()
    try:
        framerateMaker(renderLoop, FRAMERATE)
        pass
    except KeyboardInterrupt:
        pass
    teardown()



def setup():
    print("Setup")
    print("Clearing")
    clearScreen()
    clearAllBuffers()
    pass


def teardown():
    global dat
    print("Teardown")
    print("Teardown Complete")
    pass


def draw():
    global FRAME_NO,screen_buffer,screen_buffer_color
    clearAllBuffers()
    drawBox(0,0,WIDTH,HEIGHT,'#')
    printBuffer(1,1,str(FRAMERATE)+'fps '+str(FRAME_NO))


if __name__ == "__main__":
    main()
