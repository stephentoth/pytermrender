# Python Term Render
A quick to use and dead simple framework for making terminal based graphics in python.

```
example_music.py
################################################################
# FPS: 29.866  Frame: 251            Sample: Wavtapper - Frums #
# [3, 3, 7, 14, 29, 59]                                        #
================================================================
1234567890123456789012345678901234567890123456789012345678901234
0        1     |   2         3 |       4       | 5         6    
                                                           $    
X            X          X       X       X   X                   
                                                    X   Y  Z Z  
#                                                              #
################################################################
```

## Quick start
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 example.py
```

## Usage
Programs take the following form,
```
from pytermrender import *
from colorama import Fore, Back, Style

Screen = TermScreen(height=24, width=80, framerate=30) # Screen must be defined

def setup():
    print("Setup")
    print("Clearing")
    clearScreen()


def teardown():
    clearScreen()
    print("Teardown")
    print("Teardown Complete")

def tick():
    Screen.frame_no+=1

def draw():
    clearScreen()
    clearAllBuffers()
    frame = Screen.frame_no

    drawBox(0,0,Screen.width,Screen.height,'#')
    printBuffer(1,1,str(Screen.framerate)+'fps -'+str(frame)+'-')
    for ix, c in enumerate(str(frame)):
        putBuffer(8+ix,1, Fore.BLUE, buffer="color")

run()
```
import everything from the pytermrender lib and define setup, teardown, tick, and draw. then just call run().

The setup function is called on program start, and teardown is called on Ctrl+c.

The tick function is called every frame before the draw function.
It can be used to do the program logic.

The draw function is called after the tick function and is where the program should actually manipulate the screen buffers.
As of now, there are only two buffers, "char" and "color".
Both of these buffers get printed to the screen every frame.
Use the char buffer for printable characters and the color buffer for non-printable characters, like ANSI char sequences.


## Library Reference
Pytermrender provides several library functions for quick usage:
```
clearScreen():
  | Clear the terminal

clearAllBuffers():
  | Clear all buffers

clearBuffer(buffer="char"):
  | Clear a specific buffer
  | buffer can be one of [ "char", "color" ]

clearLine(y, buffer="char"):
  | Clear a line of a buffer
  | buffer can be one of [ "char", "color" ]

putBuffer(x, y, char, *, buffer="char"):
  | Put a char into a specific location in a buffer
  | buffer can be one of [ "char", "color" ]
  | NOTE: multi-char strings can be used, but can cause unintended results
  |   If you want to put multi-char strings, use printBuffer

printBuffer(x, y, string):
  | Print a string into the char buffer

drawBox(x, y, width, height, char):
  | Draw a box in the char buffer with the supplied char
```


Pytermrender also provides a convienent way to store state inside the Screen object.
```
Screen.tickers
  | a dictionary to store variables that change every frame.
Screen.state
  | a dictionary to store variables that are more static.
```
Example usage as follows:
```
tick():
    global Screen
    Screen.tickers["music"][0]=(Screen.frame_no//BEAT_SUB)//4
    Screen.state["cursorActive"]=True

draw():
    bar=Screen.tickers["music"][0]
    cursorActive=Screen.state["cursorActive"]
    if cursorActive:
        putBuffer(0, 0, "$")
```
