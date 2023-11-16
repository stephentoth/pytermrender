from pytermrender import *
Screen = TermScreen(height=24, width=80, framerate=30)

#not strictly needed, but useful
def tick():
    Screen.frame_no+=1

def setup():
    print("Setup")
    print("Clearing")
    clearScreen()
    pass


def teardown():
    print("Teardown")
    print("Teardown Complete")
    pass


def draw():
    clearScreen()
    clearAllBuffers()
    drawBox(0,0,Screen.width,Screen.height,'#')
    printBuffer(1,1,str(Screen.framerate)+'fps '+str(Screen.frame_no))


run()
