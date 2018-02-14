# -*- coding: utf-8 -*-

import ctypes.wintypes


class WinProcInfo(ctypes.Structure):
    _fields_ = [
        ('hProcess', ctypes.wintypes.HANDLE),
        ('hThread', ctypes.wintypes.HANDLE),
        ('dwProcessID', ctypes.wintypes.DWORD),
        ('dwThreadID', ctypes.wintypes.DWORD),
    ]
