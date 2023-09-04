#%%
import re
import win32gui, win32ui , win32con, win32api
import numpy as np
from dataclasses import dataclass, field ,fields
import cv2
from matplotlib import pyplot as plt

@dataclass
class Window:
    """
    Dataclass for window.
    """    
    hwnd:   int
    text:   str = field(init=False)
    left:   int = field(init=False)
    top:    int = field(init=False)
    right:  int = field(init=False) 
    bot:    int = field(init=False)
    width:  int = field(init=False)
    height: int = field(init=False)
    
    def __post_init__(self):
        self.text = win32gui.GetWindowText(self.hwnd)
        self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(self.hwnd)
        self.width = self.right - self.left
        self.height = self.bot - self.top
    
    @property
    def np_bitmap(self):
        wDC = win32gui.GetWindowDC(self.hwnd) # type: ignore
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.width, self.height) , dcObj, (0,0), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC) # type: ignore
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = np.frombuffer(signedIntsArray, dtype='uint8') # type: ignore
        
        img.shape = (self.height,self.width,4)
        # cut off the alpha channel
        # img = img[:,:,:3]
        return img

def screenshot_window(window:Window,dest:str = 'img_bank/'):
    # save numpy array as bmp file
    # window.np_bitmap.save(f'{dest}pic_{window.text}_{window.hwnd}.bmp')
    # save nuympy array as png file
    plt.imsave(f"{dest}'pic_{window.text}_{window.hwnd}.png'",window.np_bitmap) 

def send_input_to_window(window:Window,keys:str):
    """
    Send input to the specified window.

    Args:
        window (Window): Window to send input to.
        keys (str): Keys to send to the window.
    """
    win32gui.SetForegroundWindow(window.hwnd)
    for key in keys:
        win32api.keybd_event(ord(key), 0, 0, 0)
        win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)


# %%
def list_visable_windows():
    """
    Print all visable windows.
    """
    win_list = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            win_list.append(Window(hwnd))
            # print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)
    #remove empty strings
    win_list = [x for x in win_list if x.text != '']
    return win_list    

def grab_screen():
    w = 1920 # set this
    h = 1080 # set this
    bmpfilenamename = "out.bmp" #set this

    hwnd= None #desktop
    wDC = win32gui.GetWindowDC(hwnd) # type: ignore
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC) # type: ignore
    win32gui.DeleteObject(dataBitMap.GetHandle())

# def grab_window_bitmap(window:Window = None):  # sourcery skip: raise-specific-error
#     """
#     Grab a screenshot of the specified window.

#     Args:
#         title (_type_, optional): _description_. Defaults to None.
#     """
    
#     w = 1920 # set this
#     h = 1080 # set this
#     # get the window handle
#     # hwnd = win32gui.FindWindow(None, title)
#     # if not hwnd:
#     #     raise Exception(f"Window {title} not found.")
#     # '''
#     # cDC.SelectObject(dataBitMap)
#     # cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
#     # '''
#     # get the window size
#     # react = win32gui.GetWindowRect(hwnd)
#     # left, top, right, bot = win32gui.GetWindowRect(hwnd)
#     # w = right - left
#     # h = bot - top
    
#     wDC = win32gui.GetWindowDC(window.hwnd) # type: ignore
#     dcObj=win32ui.CreateDCFromHandle(wDC)
#     cDC=dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, window.width, window.height)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0,0),(window.width, window.height) , dcObj, (0,0), win32con.SRCCOPY)
#     signedIntsArray = dataBitMap.GetBitmapBits(True)
#     # Free Resources
#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC) # type: ignore
#     win32gui.DeleteObject(dataBitMap.GetHandle())
#     img = np.fromstring(signedIntsArray, dtype='uint8') # type: ignore
    
#     img.shape = (h,w,4)
#     # cut off the alpha channel
#     # img = img[:,:,:3]
#     return img



# def grab_window_bitmap(title = None):  # sourcery skip: raise-specific-error
#     """
#     Grab a screenshot of the specified window.

#     Args:
#         title (_type_, optional): _description_. Defaults to None.
#     """
    
#     w = 1920 # set this
#     h = 1080 # set this
#     # get the window handle
#     hwnd = win32gui.FindWindow(None, title)
#     if not hwnd:
#         raise Exception(f"Window {title} not found.")
#     '''
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
#     '''
#     # get the window size
#     react = win32gui.GetWindowRect(hwnd)
#     # left, top, right, bot = win32gui.GetWindowRect(hwnd)
#     # w = right - left
#     # h = bot - top
    
#     wDC = win32gui.GetWindowDC(hwnd) # type: ignore
#     dcObj=win32ui.CreateDCFromHandle(wDC)
#     cDC=dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
#     signedIntsArray = dataBitMap.GetBitmapBits(True)
#     # Free Resources
#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC) # type: ignore
#     win32gui.DeleteObject(dataBitMap.GetHandle())
#     img = np.fromstring(signedIntsArray, dtype='uint8') # type: ignore
    
#     img.shape = (h,w,4)
#     # cut off the alpha channel
#     # img = img[:,:,:3]
#     return img
    
def grab_save_window_screenshot(window:Window,dest:str = 'img_bank/'):
    
    """
    Grab a screenshot of the current window.
    """
    w = 1920 # set this
    h = 1080 # set this
    # get the window handle
    # hwnd = win32gui.FindWindow(None, title)
    # if not hwnd:
    #     raise Exception(f"Window {title} not found.")
    '''
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
    '''
    # get the window size
    react = win32gui.GetWindowRect(hwnd) # type: ignore
    left, top, right, bot = win32gui.GetWindowRect(hwnd) # type: ignore
    w = right - left
    h = bot - top
    
    wDC = win32gui.GetWindowDC(hwnd) # type: ignore
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((left,top),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, f'img_bank/pic_{win32gui.GetWindowText(hwnd)}_{hwnd}.bmp') # type: ignore
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC) # type: ignore
    win32gui.DeleteObject(dataBitMap.GetHandle())
    # img = np.fromstring(signedIntsArray, dtype='uint8') # type: ignore
    # img.shape = (h,w,4)
    # cut off the alpha channel
    # img = img[:,:,:3]
    # return img
    # ------------------------------------
    # hwin = None
    # if title == None:
    #     hwin = win32gui.FindWindow(None, title)
    
    # left, top, right, bot = win32gui.GetWindowRect(hwin)
    # w = 1920
    # h = 1080
    
    # # save the screen
    # hwndDC = win32gui.GetWindowDC(hwin)
    # mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    # saveDC = mfcDC.CreateCompatibleDC()
    # saveBitMap = win32ui.CreateBitmap()
    # saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # saveDC.SelectObject(saveBitMap)
    # saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (0, 0),  win32con.SRCCOPY)
    
    # #save to file
    # saveBitMap.SaveBitmapFile(saveDC, f'img_bank/pic_{title}.bmp')
    
    # mfcDC.DeleteDC()
    # saveDC.DeleteDC()
    # #realease resources
    # win32gui.ReleaseDC(hwin, hwndDC)
    # win32gui.DeleteObject(saveBitMap.GetHandle())

# %%
