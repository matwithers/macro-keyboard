import ctypes
import os
import threading

import win32api
import win32con
import win32process

class WindowChangeListener:

    def __init__(self,handleWindowChange):
        self.t = None
        self.handleWindowChange = handleWindowChange

    def runThreaded(self):
        # Start the 'run' method in a daemonized thread.
        self.t = threading.Thread(target=self.__windowChangeEventListener)
        self.t.setDaemon(True)
        self.t.start()

    # main handler to trigger changes to current active window
    # largely copied from:
    # https://github.com/Danesprite/windows-fun
    def __windowChangeEventListener(self):
        # Look here for DWORD event constants:
        # http://stackoverflow.com/questions/15927262/convert-dword-event-constant-from-wineventproc-to-name-in-c-sharp
        # Don't worry, they work for python too.

        WINEVENT_OUTOFCONTEXT = 0x0000
        EVENT_SYSTEM_FOREGROUND = 0x0003
        WINEVENT_SKIPOWNPROCESS = 0x0002

        user32 = ctypes.windll.user32
        ole32 = ctypes.windll.ole32

        WinEventProcType = ctypes.WINFUNCTYPE(
            None,
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.HWND,
            ctypes.wintypes.LONG,
            ctypes.wintypes.LONG,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD
        )

        def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
            # exePath = win32process.GetModuleFileNameEx(handle, 0)
            head, exePath = os.path.split(win32process.GetModuleFileNameEx(handle, 0))
            self.handleWindowChange(exePath)

        WinEventProc = WinEventProcType(callback)

        user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
        hook = user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            0,
            WinEventProc,
            0,
            0,
            WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS
        )

        if hook == 0:
            print('SetWinEventHook failed')
            exit(1)

        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
            # user32.TranslateMessageW(msg)
            user32.DispatchMessageW(msg)

        # Stopped receiving events, so clear up the winevent hook and uninitialise.
        print('Stopped receiving new window change events. Exiting...')
        user32.UnhookWinEvent(hook)
        ole32.CoUninitialize()