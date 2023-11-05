import time
import math
import functools
printr = functools.partial(print, end="")

from just_playback import Playback
playback = Playback()

from colorama import Fore, Back, Style

###############
BPM=112
BEAT_SUB=16

FRAMERATE=(BPM*BEAT_SUB/60)
HEIGHT=24
WIDTH=64
###############
FRAME_NO=0
MUSIC_TIME=[0 for i in range(int(math.log2(BEAT_SUB)))]
###############

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

def printBuffer(x, y, val):
    global screen_buffer
    string=str(val)
    if len(string) > WIDTH-x:
        return
    for i, l in enumerate(string):
        screen_buffer[y][x+i]=l
    pass

def clearLine(y):
    global screen_buffer
    screen_buffer[y]=[" "]*WIDTH
    pass


####################
def trackers():
    global FRAME_NO
    global MUSIC_TIME
    FRAME_NO+=1
    MUSIC_TIME[0]=(FRAME_NO//BEAT_SUB)//4
    MUSIC_TIME[1]=(FRAME_NO//BEAT_SUB//1)%4
    MUSIC_TIME[2]=(FRAME_NO//(BEAT_SUB//2))%8
    MUSIC_TIME[3]=(FRAME_NO//(BEAT_SUB//4))%16
    #MUSIC_TIME[1]=(FRAME_NO//(BEAT_SUB*int(math.log2(BEAT_SUB//8))))%4
#    MUSIC_TIME[2]=(FRAME_NO//8)%8
#    for i in range(len(MUSIC_TIME)):
#        MUSIC_TIME[i]=(FRAME_NO//2**(i+1)) % 2**(i)

def main():
    setup()
    try:
        framerateMaker(renderLoop, FRAMERATE)
        pass
    except KeyboardInterrupt:
        pass
    teardown()



def setup():
    global playback
    print("Setup")
    print("Clearing")
    clearScreen()
    clearAllBuffers()
    #playback.load_file('')
    #playback.play()


def teardown():
    print("Teardown")
    print("Stopping Playback")
    #playback.stop()
    print("Teardown Complete")
    pass


cursorX=1
cooldown=[0]*4*4
def draw():
    global screen_buffer,screen_buffer_color
    global MUSIC_TIME
    global cursorX,cooldown
    clearAllBuffers()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == 0 or x == WIDTH-1:
                screen_buffer[y][x]='#'
            if y == 0 or y == HEIGHT-1:
                screen_buffer[y][x]='#'
    printBuffer(0,3,"1234567890123456789012345678901234567890123456789012345678901234")
    printBuffer(0,4,"0        1         2         3         4         5         6    ")
    clearLine(5)
    if cursorX >= WIDTH:
        cursorX=0
    screen_buffer[5][cursorX] = "x"

    printBuffer(1,1,FRAME_NO)
    printBuffer(6,1,FRAMERATE)
    printBuffer(1,2,MUSIC_TIME)
    cursorX=cursorX+1


if __name__ == "__main__":
    main()
