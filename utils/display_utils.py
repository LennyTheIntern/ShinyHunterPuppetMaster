#%%
from tkinter import NO
import cv2
from window_utils import grab_window_bitmap , list_visable_windows
import numpy as np


def display_img_stream(window_name=None):
    while True:
        img = grab_window_bitmap(window_name)
        cv2.imshow(window_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
