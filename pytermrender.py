import __main__
import time, math
from colorama import Fore, Back, Style
import functools
#from dataclasses import dataclass
printr = functools.partial(print, end="")

## Definitions


class RenderException(Exception):
    pass


class TermScreen:
    width: int
    height: int
    framerate: float
    frame_no: int = 0
    buffers: list = ["char", "color"]
    tickers: dict
    def __init__(self, *, width: int = 80, height: int = 24, framerate: float = 30.0):
        self.width=width
        self.height=height
        self.framerate=framerate
        self.buffer_char  = [[" "]*self.width for i in range(self.height)]
        self.buffer_color = [[Style.RESET_ALL]*self.width for i in range(self.height)]
        return

    def reset_buffer(self, buffer="char"):
        if buffer not in self.buffers:
            raise RenderException("Buffer Does not exist")
        match buffer:
            case "char":
                self.buffer_char = [[" "]*self.width for i in range(self.height)]
            case "color":
                self.buffer_color = [[Style.RESET_ALL]*self.width for i in range(self.height)]
        return
    
    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                printr(self.buffer_color[y][x])
                printr(self.buffer_char[y][x])
            print() #print \n
        return

def framerateMaker(func, perSec):
    interval = 1.0 / perSec
    while True:
        start_time = time.time()
        func()
        elapsed = time.time() - start_time
        if elapsed < interval:
            time.sleep(interval-elapsed)
    return

def renderLoop():
    global Screen
    pro_tick()
    pro_draw()
    Screen.render()
    return
################

## Library Functions

def clearScreen():
    printr('\033[2J')

def clearBuffer(buf="char"):
    global Screen
    Screen.reset_buffer(buf)
    return

def clearAllBuffers():
    global Screen
    for buf in Screen.buffers:
        Screen.reset_buffer(buf)
    return

def printBuffer(x, y, val):
    global Screen
    string=str(val)
    if len(string) > Screen.width-x:
        raise RenderException("Too Long to fit in screen")
    for i, char in enumerate(string):
        Screen.buffer_char[y][x+i]=char

def clearLine(y):
    global Screen
    Screen.buffer_char[y]=[" "]*Screen.width

def drawBox(x,y,width,height,char):
    global Screen
    if x+width > Screen.width or y+height > Screen.height:
        raise RenderException("Box too BIG")
    for w_x in range(width):
        for w_y in range(height):
            if (w_x==0 or w_x==width-1) or (w_y==0 or w_y==height-1):
                Screen.buffer_char[y+w_y][x+w_x] = char

####################



def tick():
    global Screen
    Screen.frame_no+=1

def setup():
    print("Setup")
    clearScreen()
    clearAllBuffers()
    return


def teardown():
    print("Default Teardown")
    return


def draw():
    return

def run():
    global Screen
    global pro_tick, pro_draw

    if hasattr(__main__, "Screen"): 
        Screen = __main__.Screen
    else:
        raise RenderException("Screen Not defined")

    if hasattr(__main__, "setup"): 
        pro_setup = __main__.setup
    else:
        pro_setup = setup
    
    if hasattr(__main__, "teardown"): 
        pro_teardown = __main__.teardown
    else:
        pro_teardown = teardown
    
    if hasattr(__main__, "tick"): 
        pro_tick = __main__.tick
    else:
        pro_tick = tick
    
    if hasattr(__main__, "draw"): 
        pro_draw = __main__.draw
    else:
        pro_draw = draw

    pro_setup()
    try:
        framerateMaker(renderLoop, Screen.framerate)
    except KeyboardInterrupt:
        pass
    pro_teardown()

