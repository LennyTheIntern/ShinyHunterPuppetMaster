from dataclasses import dataclass, field,fields
from math import e
from requests import post
from shinyHuntEvent import post_event
from utils.window_utils import send_input_to_window

TOOLS:list[int]

#possably have window as env variable
def SendInput(keys):
    win = 'WINDOW'
    # send input to window
    
def orient(direction:str):
    #call sendinput
    #call screen check
    pass

def run_in_line(num_units:int):
    post_event("oreint",'up') 
    post_event('run_n_blocks',num_units)
    post_event("oreint",'down') 
    post_event('run_n_blocks',num_units)
    
def run_in_circle(num_units:int):
    post_event("oreint",'up')
    post_event('run_n_blocks',num_units)
    post_event("oreint",'left') 
    post_event('run_n_blocks',num_units)
    post_event("oreint",'left') 
    post_event('run_n_blocks',num_units)
    
def run_n_blocks(num_units:int):
    #call sendinput
    #call screen check
    pass

def screen_check():
    #call screen check
    #battle screen
    post_event('battle',None)
    #selection screen
    post_event('selection',None)
    #overworld screen
    post_event('overworld',None)
    pass







    