from pytermrender import *
from colorama import Fore, Back, Style

Screen = TermScreen(height=24, width=80, framerate=30)


def setup():
    print("Setup")
    print("Clearing")
    clearScreen()
    return


def teardown():
    clearScreen()
    print("Teardown")
    print("Teardown Complete")
    return


#not strictly needed, but useful
def tick():
    Screen.frame_no+=1
    return

def draw():
    clearScreen()
    clearAllBuffers()
    frame = Screen.frame_no

    drawBox(0,0,Screen.width,Screen.height,'#')
    printBuffer(1,1,str(Screen.framerate)+'fps -'+str(frame)+'-')
    for ix, c in enumerate(str(frame)):
        putBuffer(8+ix,1, Fore.BLUE, buffer="color")
    return


run()
