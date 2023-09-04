# test windoes utils
# ------------------------------------------------
#%%
import pytest
from utils.window_utils import list_visable_windows,Window,screenshot_window
import win32gui, win32ui , win32con, win32api
import numpy as np
from dataclasses import dataclass
import cv2
#%%



def test_savebitfile():
    """
    Test grab_screen() function.
    """
    ls = list_visable_windows()
    # save windows
    for w in ls:
        screenshot_window(w)

    assert True

def test_grab_screen_cv2():
    """
    Test grab_screen() function.
    """
    
    window_name = 'mGBA - Pokemon - FireRed Version (USA, Europe) (Rev 1) (60.1 fps) - 0.10.2'
    go = True
    #136302
    ls = list_visable_windows()
    win:Window = ls[5]
    while go:
        cv2.imshow(win.text, win.np_bitmap)
        wait = cv2.waitKey(100)
        if wait == ord('q'):
            go = False
            cv2.destroyAllWindows()
    assert True
# %%
