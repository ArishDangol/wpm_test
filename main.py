import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test")    #prints the text you want to see on console
    stdscr.addstr("\nPress any key to begin!")    #prints the text you want to see on console
    #text starts at 1 line down and starts at 0 space from left
    stdscr.refresh()
    stdscr.getkey()     #waits for user to type something

# function for overlaying text
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    
    
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        
        if char!= correct_char:
            color = curses.color_pair(2)
        
        stdscr.addstr(0, i, char, color)    #overlay text 

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()
    
def wpm_test(stdscr):
    target_text = load_text()
    current_text = [] 
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round(len(current_text) / (time_elapsed / 60) / 5)  #character per minutes divide by 5 words per minutes gives us wpm
        
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()
        
        #current text is list and target text is string
        #convert list to string
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()     #it is blocking and waiting for user input
        except:
            continue   #skip down and go to top of the loop
        
        if ord(key) == 27:       #ASCII value for escape button ordinal value press escape to exit the proram
            break
        
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    #green is foreground color and white is background color and id is 1
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    #green is foreground color and white is background color and id is 1
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)    #green is foreground color and white is background color and id is 1
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0, "You completed the test! Press any key to continue.....")
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break        
    
wrapper(main)   #passing main function to wrapper


