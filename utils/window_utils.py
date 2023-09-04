#%%
import re
import win32gui, win32ui , win32con, win32api
import numpy as np

def list_visable_windows():
    """
    Print all visable windows.
    """
    name_list = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            name_list.append(win32gui.GetWindowText(hwnd))
            # print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)
    #remove empty strings
    name_list = [x for x in name_list if x]
    return name_list    

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

def grab_window_bitmap(title = None):  # sourcery skip: raise-specific-error
    """
    Grab a screenshot of the specified window.

    Args:
        title (_type_, optional): _description_. Defaults to None.
    """
    
    w = 1920 # set this
    h = 1080 # set this
    # get the window handle
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        raise Exception(f"Window {title} not found.")
    '''
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
    '''
    # get the window size
    react = win32gui.GetWindowRect(hwnd)
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    # w = right - left
    # h = bot - top
    
    wDC = win32gui.GetWindowDC(hwnd) # type: ignore
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC) # type: ignore
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = np.fromstring(signedIntsArray, dtype='uint8') # type: ignore
    
    img.shape = (h,w,4)
    # cut off the alpha channel
    # img = img[:,:,:3]
    return img
    
def grab_save_window_screenshot(hwnd=None):
    
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