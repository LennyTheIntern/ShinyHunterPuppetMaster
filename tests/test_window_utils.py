# test windoes utils
# ------------------------------------------------
#%%
import pytest
from utils.window_utils import list_visable_windows, grab_screen, grab_window_bitmap, grab_save_window_screenshot
import win32gui, win32ui , win32con, win32api
import numpy as np
from dataclasses import dataclass
import cv2
#%%

@dataclass
class Window:
    """
    Dataclass for window.
    """
    hwnd: int
    title: str
    rect: tuple
    cropped_x: int
    cropped_y: int
    w: int
    h: int


def test_savebitfile():
    """
    Test grab_screen() function.
    """
    h_list = []
    name_list = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            h_list.append(hwnd)
            name_list.append(win32gui.GetWindowText(hwnd))
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)

    for h in h_list:
        grab_save_window_screenshot(h)
    assert True

def test_grab_screen_cv2():
    """
    Test grab_screen() function.
    """
    
    window_name = 'mGBA - Pokemon - FireRed Version (USA, Europe) (Rev 1) (60.1 fps) - 0.10.2'
    go = True
    #136302
    
    
    while go:
        img = grab_window_bitmap(win32gui.GetWindowText(136302))
        cv2.imshow("stream", img)
        wait = cv2.waitKey(100)
        if wait == ord('q'):
            go = False
            cv2.destroyAllWindows()
    assert True