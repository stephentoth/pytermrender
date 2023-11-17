from pytermrender import *
from colorama import Fore, Back, Style
from just_playback import Playback
import math

BPM=112
BEAT_SUB=16
FRAMERATE=(BPM*BEAT_SUB/60)

Screen = TermScreen(height=20, width=64, framerate=FRAMERATE)
playback = Playback()

def setup():
    global Screen
    print("Setup")
    playback.load_file('media/WavetapperSample.wav')
    playback.loop_at_end(True)
    playback.play()
    playback.set_volume(0.5)
    Screen.tickers["music"] = {}
    print("Clearing Screen")
    clearScreen()
    return

def teardown():
    clearScreen();
    print("Teardown")
    print("Stopping Playback")
    playback.stop()
    print("Teardown Complete")
    return

def tick():
    global Screen
    Screen.frame_no+=1
    Screen.tickers["music"][0]=(Screen.frame_no//BEAT_SUB)//4       # bar
    Screen.tickers["music"][1]=(Screen.frame_no//BEAT_SUB//1)%4     # beat
    Screen.tickers["music"][2]=(Screen.frame_no//(BEAT_SUB//2))%8   # 8th
    Screen.tickers["music"][3]=(Screen.frame_no//(BEAT_SUB//4))%16  # 16th
    Screen.tickers["music"][4]=(Screen.frame_no//(BEAT_SUB//8))%32  # 32nd
    Screen.tickers["music"][5]=(Screen.frame_no//(BEAT_SUB//16))%64 # 64th

    Screen.state["cursorX"]=Screen.tickers["music"][5]
    
    if Screen.tickers["music"][1] in [0,2]:
        Screen.state["cursorActive"]=True
    else:
        Screen.state["cursorActive"]=False
    return

def draw():
    clearScreen()
    clearAllBuffers()
    
    cursorX=Screen.state["cursorX"]
    cursorActive=Screen.state["cursorActive"]
    bar=Screen.tickers["music"][0]
    
    drawBox(0,0, Screen.width,Screen.height, '#')
    
    printBuffer(2,  1, "FPS: "+str(Screen.framerate)[:6])
    printBuffer(15, 1, "Frame: "+str(Screen.frame_no))
    printBuffer(37, 1, "Sample: Wavtapper - Frums")
    printBuffer(2,  2, [x for x in Screen.tickers["music"].values()])
    printBuffer(0,  3, "="*Screen.width)
    
    printBuffer(0,  4, "1234567890123456789012345678901234567890123456789012345678901234")
    printBuffer(0,  5, "0        1     |   2         3 |       4       | 5         6    ")
    
    clearLine(6)
    putBuffer(cursorX, 6, "$")
    if cursorActive:
        putBuffer(cursorX, 6, Fore.GREEN, buffer="color")
    
    clearLine(7)
    printBuffer(0,7,"X            X          X       X       X   X")
    
    clearLine(8)
    match bar % 4:
        case 0:
            printBuffer(52,8,"X")
        case 1:
            printBuffer(52,8,"X   Y")
        case 2:
            printBuffer(52,8,"X")
        case 3:
            printBuffer(52,8,"X   Y  Z Z")
    
    for ix in range(cursorX):
        putBuffer(ix, 7, Fore.RED,  buffer="color")
        putBuffer(ix, 8, Fore.BLUE, buffer="color")
    
    return

run()
