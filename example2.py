from pytermrender import *
from colorama import Fore, Back, Style

BPM=112
BEAT_SUB=16
FRAMERATE=(BPM*BEAT_SUB/60)

Screen = TermScreen(height=24, width=64, framerate=FRAMERATE)

cursorX=1
cooldown=0
def tick():
    global cursorX,cooldown
    Screen.frame_no+=1
    cursorX=cursorX+1
    if cursorX >= Screen.width-1:
        cursorX=0
    if cursorX % 12 == 0:
        cooldown=8
    else:
        cooldown-=1
    return
        

def setup():
    print("Setup")
    print("Clearing")
    clearScreen()
    return


def teardown():
    print("Teardown")
    print("Teardown Complete")
    return


def draw():
    clearScreen()
    clearAllBuffers()
    for y in range(Screen.height):
        for x in range(Screen.width):
            if x == 0 or x == Screen.width-1:
                Screen.buffer_char[y][x]='#'
            if y == 0 or y == Screen.height-1:
                Screen.buffer_char[y][x]='#'
    printBuffer(0,3,"1234567890123456789012345678901234567890123456789012345678901234")
    printBuffer(0,4,"0        1         2         3         4         5         6    ")
    #printBuffer(0,4,"2   6   8   6   4   6   8   6   2   6   8   6   4   6   8   6   ")
    clearLine(5)
    Screen.buffer_char[5][cursorX] = "x"
    if cooldown > 0:
        Screen.buffer_color[5][cursorX] = Fore.RED

    printBuffer(1,1,Screen.frame_no)
    printBuffer(8,1,Screen.framerate)


run()
