"""
Pyperclip

A cross-platform clipboard module for Python, with copy & paste functions for plain text.
By Al Sweigart al@inventwithpython.com
BSD License

Usage:
  import pyperclip
  pyperclip.copy('The text to be copied to the clipboard.')
  spam = pyperclip.paste()

  if not pyperclip.is_available():
    print("Copy functionality unavailable!")

On Windows, no additional modules are needed.
On Mac, the pyobjc module is used, falling back to the pbcopy and pbpaste cli
    commands. (These commands should come with OS X.).
On Linux, install xclip, xsel, or wl-clipboard (for "wayland" sessions) via package manager.
For example, in Debian:
    sudo apt-get install xclip
    sudo apt-get install xsel
    sudo apt-get install wl-clipboard

Otherwise on Linux, you will need the qtpy or PyQt5 modules installed.

This module does not work with PyGObject yet.

Cygwin is currently not supported.

Security Note: This module runs programs with these names:
    - which
    - pbcopy
    - pbpaste
    - xclip
    - xsel
    - wl-copy/wl-paste
    - klipper
    - qdbus
A malicious user could rename or add programs with these names, tricking
Pyperclip into running them with whatever permissions the Python process has.

"""
__version__ = '1.9.0'

import base64
import contextlib
import ctypes
import os
import platform
import subprocess
import sys
import time
import warnings

from ctypes import c_size_t, sizeof, c_wchar_p, get_errno, c_wchar
from typing import Union, Optional


_IS_RUNNING_PYTHON_2 = sys.version_info[0] == 2  # type: bool

# For paste(): Python 3 uses str, Python 2 uses unicode.
if _IS_RUNNING_PYTHON_2:
    # mypy complains about `unicode` for Python 2, so we ignore the type error:
    _PYTHON_STR_TYPE = unicode  # type: ignore
else:
    _PYTHON_STR_TYPE = str

ENCODING = 'utf-8'  # type: str

try:
    # Use shutil.which() for Python 3+
    from shutil import which
    def _py3_executable_exists(name):  # type: (str) -> bool
        return bool(which(name))
    _executable_exists = _py3_executable_exists
except ImportError:
    # Use the "which" unix command for Python 2.7 and prior.
    def _py2_executable_exists(name):  # type: (str) -> bool
        return subprocess.call(['which', name],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
    _executable_exists = _py2_executable_exists

# Exceptions
class PyperclipException(RuntimeError):
    pass

class PyperclipWindowsException(PyperclipException):
    def __init__(self, message):
        message += " (%s)" % ctypes.WinError()
        super(PyperclipWindowsException, self).__init__(message)

class PyperclipTimeoutException(PyperclipException):
    pass


def init_osx_pbcopy_clipboard():
    def copy_osx_pbcopy(text):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        p = subprocess.Popen(['pbcopy', 'w'],
                             stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode(ENCODING))

    def paste_osx_pbcopy():
        p = subprocess.Popen(['pbpaste', 'r'],
                             stdout=subprocess.PIPE, close_fds=True)
        stdout, stderr = p.communicate()
        return stdout.decode(ENCODING)

    return copy_osx_pbcopy, paste_osx_pbcopy


def init_osx_pyobjc_clipboard():
    def copy_osx_pyobjc(text):
        '''Copy string argument to clipboard'''
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        newStr = Foundation.NSString.stringWithString_(text).nsstring()
        newData = newStr.dataUsingEncoding_(Foundation.NSUTF8StringEncoding)
        board = AppKit.NSPasteboard.generalPasteboard()
        board.declareTypes_owner_([AppKit.NSStringPboardType], None)
        board.setData_forType_(newData, AppKit.NSStringPboardType)

    def paste_osx_pyobjc():
        "Returns contents of clipboard"
        board = AppKit.NSPasteboard.generalPasteboard()
        content = board.stringForType_(AppKit.NSStringPboardType)
        return content

    return copy_osx_pyobjc, paste_osx_pyobjc


def init_qt_clipboard():
    global QApplication
    # $DISPLAY should exist

    # Try to import from qtpy, but if that fails try PyQt5
    try:
        from qtpy.QtWidgets import QApplication
    except:
        from PyQt5.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    def copy_qt(text):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        cb = app.clipboard()
        cb.setText(text)

    def paste_qt():
        cb = app.clipboard()
        return _PYTHON_STR_TYPE(cb.text())

    return copy_qt, paste_qt


def init_xclip_clipboard():
    DEFAULT_SELECTION='c'
    PRIMARY_SELECTION='p'

    def copy_xclip(text, primary=False):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        selection=DEFAULT_SELECTION
        if primary:
            selection=PRIMARY_SELECTION
        p = subprocess.Popen(['xclip', '-selection', selection],
                             stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode(ENCODING))

    def paste_xclip(primary=False):
        selection=DEFAULT_SELECTION
        if primary:
            selection=PRIMARY_SELECTION
        p = subprocess.Popen(['xclip', '-selection', selection, '-o'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             close_fds=True)
        stdout, stderr = p.communicate()
        # Intentionally ignore extraneous output on stderr when clipboard is empty
        return stdout.decode(ENCODING)

    return copy_xclip, paste_xclip


def init_xsel_clipboard():
    DEFAULT_SELECTION='-b'
    PRIMARY_SELECTION='-p'

    def copy_xsel(text, primary=False):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        selection_flag = DEFAULT_SELECTION
        if primary:
            selection_flag = PRIMARY_SELECTION
        p = subprocess.Popen(['xsel', selection_flag, '-i'],
                             stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode(ENCODING))

    def paste_xsel(primary=False):
        selection_flag = DEFAULT_SELECTION
        if primary:
            selection_flag = PRIMARY_SELECTION
        p = subprocess.Popen(['xsel', selection_flag, '-o'],
                             stdout=subprocess.PIPE, close_fds=True)
        stdout, stderr = p.communicate()
        return stdout.decode(ENCODING)

    return copy_xsel, paste_xsel


def init_wl_clipboard():
    PRIMARY_SELECTION = "-p"

    def copy_wl(text, primary=False):
        text = _PYTHON_STR_TYPE(text)  # Converts non-str values to str.
        args = ["wl-copy"]
        if primary:
            args.append(PRIMARY_SELECTION)
        if not text:
            args.append('--clear')
            subprocess.check_call(args, close_fds=True)
        else:
            pass
            p = subprocess.Popen(args, stdin=subprocess.PIPE, close_fds=True)
            p.communicate(input=text.encode(ENCODING))

    def paste_wl(primary=False):
        args = ["wl-paste", "-n", "-t", "text"]
        if primary:
            args.append(PRIMARY_SELECTION)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, close_fds=True)
        stdout, _stderr = p.communicate()
        return stdout.decode(ENCODING)

    return copy_wl, paste_wl


def init_klipper_clipboard():
    def copy_klipper(text):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        p = subprocess.Popen(
            ['qdbus', 'org.kde.klipper', '/klipper', 'setClipboardContents',
             text.encode(ENCODING)],
            stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=None)

    def paste_klipper():
        p = subprocess.Popen(
            ['qdbus', 'org.kde.klipper', '/klipper', 'getClipboardContents'],
            stdout=subprocess.PIPE, close_fds=True)
        stdout, stderr = p.communicate()

        # Workaround for https://bugs.kde.org/show_bug.cgi?id=342874
        # TODO: https://github.com/asweigart/pyperclip/issues/43
        clipboardContents = stdout.decode(ENCODING)
        # even if blank, Klipper will append a newline at the end
        assert len(clipboardContents) > 0
        # make sure that newline is there
        assert clipboardContents.endswith('\n')
        if clipboardContents.endswith('\n'):
            clipboardContents = clipboardContents[:-1]
        return clipboardContents

    return copy_klipper, paste_klipper


def init_dev_clipboard_clipboard():
    def copy_dev_clipboard(text):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        if text == '':
            warnings.warn('Pyperclip cannot copy a blank string to the clipboard on Cygwin. This is effectively a no-op.')
        if '\r' in text:
            warnings.warn('Pyperclip cannot handle \\r characters on Cygwin.')

        fo = open('/dev/clipboard', 'wt')
        fo.write(text)
        fo.close()

    def paste_dev_clipboard():
        fo = open('/dev/clipboard', 'rt')
        content = fo.read()
        fo.close()
        return content

    return copy_dev_clipboard, paste_dev_clipboard


def init_no_clipboard():
    class ClipboardUnavailable(object):

        def __call__(self, *args, **kwargs):
            additionalInfo = ''
            if sys.platform == 'linux':
                additionalInfo = '\nOn Linux, you can run `sudo apt-get install xclip` or `sudo apt-get install xselect` to install a copy/paste mechanism.'
            raise PyperclipException('Pyperclip could not find a copy/paste mechanism for your system. For more information, please visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error' + additionalInfo)

        if _IS_RUNNING_PYTHON_2:
            def __nonzero__(self):
                return False
        else:
            def __bool__(self):
                return False

    return ClipboardUnavailable(), ClipboardUnavailable()




# Windows-related clipboard functions:
class CheckedCall(object):
    def __init__(self, f):
        super(CheckedCall, self).__setattr__("f", f)

    def __call__(self, *args):
        ret = self.f(*args)
        if not ret and get_errno():
            raise PyperclipWindowsException("Error calling " + self.f.__name__)
        return ret

    def __setattr__(self, key, value):
        setattr(self.f, key, value)


def init_windows_clipboard():
    global HGLOBAL, LPVOID, DWORD, LPCSTR, INT, HWND, HINSTANCE, HMENU, BOOL, UINT, HANDLE
    from ctypes.wintypes import (HGLOBAL, LPVOID, DWORD, LPCSTR, INT, HWND,
                                 HINSTANCE, HMENU, BOOL, UINT, HANDLE)

    windll = ctypes.windll
    msvcrt = ctypes.CDLL('msvcrt')

    safeCreateWindowExA = CheckedCall(windll.user32.CreateWindowExA)
    safeCreateWindowExA.argtypes = [DWORD, LPCSTR, LPCSTR, DWORD, INT, INT,
                                    INT, INT, HWND, HMENU, HINSTANCE, LPVOID]
    safeCreateWindowExA.restype = HWND

    safeDestroyWindow = CheckedCall(windll.user32.DestroyWindow)
    safeDestroyWindow.argtypes = [HWND]
    safeDestroyWindow.restype = BOOL

    OpenClipboard = windll.user32.OpenClipboard
    OpenClipboard.argtypes = [HWND]
    OpenClipboard.restype = BOOL

    safeCloseClipboard = CheckedCall(windll.user32.CloseClipboard)
    safeCloseClipboard.argtypes = []
    safeCloseClipboard.restype = BOOL

    safeEmptyClipboard = CheckedCall(windll.user32.EmptyClipboard)
    safeEmptyClipboard.argtypes = []
    safeEmptyClipboard.restype = BOOL

    safeGetClipboardData = CheckedCall(windll.user32.GetClipboardData)
    safeGetClipboardData.argtypes = [UINT]
    safeGetClipboardData.restype = HANDLE

    safeSetClipboardData = CheckedCall(windll.user32.SetClipboardData)
    safeSetClipboardData.argtypes = [UINT, HANDLE]
    safeSetClipboardData.restype = HANDLE

    safeGlobalAlloc = CheckedCall(windll.kernel32.GlobalAlloc)
    safeGlobalAlloc.argtypes = [UINT, c_size_t]
    safeGlobalAlloc.restype = HGLOBAL

    safeGlobalLock = CheckedCall(windll.kernel32.GlobalLock)
    safeGlobalLock.argtypes = [HGLOBAL]
    safeGlobalLock.restype = LPVOID

    safeGlobalUnlock = CheckedCall(windll.kernel32.GlobalUnlock)
    safeGlobalUnlock.argtypes = [HGLOBAL]
    safeGlobalUnlock.restype = BOOL

    wcslen = CheckedCall(msvcrt.wcslen)
    wcslen.argtypes = [c_wchar_p]
    wcslen.restype = UINT

    GMEM_MOVEABLE = 0x0002
    CF_UNICODETEXT = 13

    @contextlib.contextmanager
    def window():
        """
        Context that provides a valid Windows hwnd.
        """
        # we really just need the hwnd, so setting "STATIC"
        # as predefined lpClass is just fine.
        hwnd = safeCreateWindowExA(0, b"STATIC", None, 0, 0, 0, 0, 0,
                                   None, None, None, None)
        try:
            yield hwnd
        finally:
            safeDestroyWindow(hwnd)

    @contextlib.contextmanager
    def clipboard(hwnd):
        """
        Context manager that opens the clipboard and prevents
        other applications from modifying the clipboard content.
        """
        # We may not get the clipboard handle immediately because
        # some other application is accessing it (?)
        # We try for at least 500ms to get the clipboard.
        t = time.time() + 0.5
        success = False
        while time.time() < t:
            success = OpenClipboard(hwnd)
            if success:
                break
            time.sleep(0.01)
        if not success:
            raise PyperclipWindowsException("Error calling OpenClipboard")

        try:
            yield
        finally:
            safeCloseClipboard()

    def copy_windows(text):
        # This function is heavily based on
        # http://msdn.com/ms649016#_win32_Copying_Information_to_the_Clipboard

        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.

        with window() as hwnd:
            # http://msdn.com/ms649048
            # If an application calls OpenClipboard with hwnd set to NULL,
            # EmptyClipboard sets the clipboard owner to NULL;
            # this causes SetClipboardData to fail.
            # => We need a valid hwnd to copy something.
            with clipboard(hwnd):
                safeEmptyClipboard()

                if text:
                    # http://msdn.com/ms649051
                    # If the hMem parameter identifies a memory object,
                    # the object must have been allocated using the
                    # function with the GMEM_MOVEABLE flag.
                    count = wcslen(text) + 1
                    handle = safeGlobalAlloc(GMEM_MOVEABLE,
                                             count * sizeof(c_wchar))
                    locked_handle = safeGlobalLock(handle)

                    ctypes.memmove(c_wchar_p(locked_handle), c_wchar_p(text), count * sizeof(c_wchar))

                    safeGlobalUnlock(handle)
                    safeSetClipboardData(CF_UNICODETEXT, handle)

    def paste_windows():
        with clipboard(None):
            handle = safeGetClipboardData(CF_UNICODETEXT)
            if not handle:
                # GetClipboardData may return NULL with errno == NO_ERROR
                # if the clipboard is empty.
                # (Also, it may return a handle to an empty buffer,
                # but technically that's not empty)
                return ""
            locked_handle = safeGlobalLock(handle)
            return_value = c_wchar_p(locked_handle).value
            safeGlobalUnlock(handle)
            return return_value

    return copy_windows, paste_windows


def init_wsl_clipboard():

    def copy_wsl(text):
        text = _PYTHON_STR_TYPE(text) # Converts non-str values to str.
        p = subprocess.Popen(['clip.exe'],
                             stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-16le'))

    def paste_wsl():
        ps_script = '[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes((Get-Clipboard -Raw)))'

        # '-noprofile' speeds up load time
        p = subprocess.Popen(['powershell.exe', '-noprofile', '-command', ps_script],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             close_fds=True)
        stdout, stderr = p.communicate()

        if stderr:
            raise Exception(f"Error pasting from clipboard: {stderr}")

        try:
            base64_encoded = stdout.decode('utf-8').strip()
            decoded_bytes = base64.b64decode(base64_encoded)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Decoding error: {e}")

    return copy_wsl, paste_wsl


# Automatic detection of clipboard mechanisms and importing is done in determine_clipboard():
def determine_clipboard():
    '''
    Determine the OS/platform and set the copy() and paste() functions
    accordingly.
    '''

    global Foundation, AppKit, qtpy, PyQt5

    # Setup for the CYGWIN platform:
    if 'cygwin' in platform.system().lower(): # Cygwin has a variety of values returned by platform.system(), such as 'CYGWIN_NT-6.1'
        # FIXME: pyperclip currently does not support Cygwin,
        # see https://github.com/asweigart/pyperclip/issues/55
        if os.path.exists('/dev/clipboard'):
            warnings.warn('Pyperclip\'s support for Cygwin is not perfect, see https://github.com/asweigart/pyperclip/issues/55')
            return init_dev_clipboard_clipboard()

    # Setup for the WINDOWS platform:
    elif os.name == 'nt' or platform.system() == 'Windows':
        return init_windows_clipboard()

    if platform.system() == 'Linux' and os.path.isfile('/proc/version'):
        with open('/proc/version', 'r') as f:
            if "microsoft" in f.read().lower():
                return init_wsl_clipboard()

    # Setup for the MAC OS X platform:
    if os.name == 'mac' or platform.system() == 'Darwin':
        try:
            import Foundation  # check if pyobjc is installed
            import AppKit
        except ImportError:
            return init_osx_pbcopy_clipboard()
        else:
            return init_osx_pyobjc_clipboard()

    # Setup for the LINUX platform:

    if os.getenv("WAYLAND_DISPLAY") and _executable_exists("wl-copy")  and _executable_exists("wl-paste"):
        return init_wl_clipboard()

    # `import PyQt4` sys.exit()s if DISPLAY is not in the environment.
    # Thus, we need to detect the presence of $DISPLAY manually
    # and not load PyQt4 if it is absent.
    elif os.getenv("DISPLAY"):
        if _executable_exists("xclip"):
            # Note: 2024/06/18 Google Trends shows xclip as more popular than xsel.
            return init_xclip_clipboard()
        if _executable_exists("xsel"):
            return init_xsel_clipboard()
        if _executable_exists("klipper") and _executable_exists("qdbus"):
            return init_klipper_clipboard()

        try:
            # qtpy is a small abstraction layer that lets you write
            # applications using a single api call to either PyQt or PySide.
            # https://pypi.python.org/pypi/QtPy
            import qtpy  # check if qtpy is installed
            return init_qt_clipboard()
        except ImportError:
            pass

        # If qtpy isn't installed, fall back on importing PyQt5
        try:
            import PyQt5  # check if PyQt5 is installed
            return init_qt_clipboard()
        except ImportError:
            pass

    return init_no_clipboard()


def set_clipboard(clipboard):
    '''
    Explicitly sets the clipboard mechanism. The "clipboard mechanism" is how
    the copy() and paste() functions interact with the operating system to
    implement the copy/paste feature. The clipboard parameter must be one of:
        - pbcopy
        - pbobjc (default on Mac OS X)
        - qt
        - xclip
        - xsel
        - klipper
        - windows (default on Windows)
        - no (this is what is set when no clipboard mechanism can be found)
    '''
    global copy, paste

    clipboard_types = {
        "pbcopy": init_osx_pbcopy_clipboard,
        "pyobjc": init_osx_pyobjc_clipboard,
        "qt": init_qt_clipboard,  # TODO - split this into 'qtpy' and 'pyqt5'
        "xclip": init_xclip_clipboard,
        "xsel": init_xsel_clipboard,
        "wl-clipboard": init_wl_clipboard,
        "klipper": init_klipper_clipboard,
        "windows": init_windows_clipboard,
        "no": init_no_clipboard,
    }

    if clipboard not in clipboard_types:
        raise ValueError('Argument must be one of %s' % (', '.join([repr(_) for _ in clipboard_types.keys()])))

    # Sets pyperclip's copy() and paste() functions:
    copy, paste = clipboard_types[clipboard]()


def lazy_load_stub_copy(text):
    '''
    A stub function for copy(), which will load the real copy() function when
    called so that the real copy() function is used for later calls.

    This allows users to import pyperclip without having determine_clipboard()
    automatically run, which will automatically select a clipboard mechanism.
    This could be a problem if it selects, say, the memory-heavy PyQt5 module
    but the user was just going to immediately call set_clipboard() to use a
    different clipboard mechanism.

    The lazy loading this stub function implements gives the user a chance to
    call set_clipboard() to pick another clipboard mechanism. Or, if the user
    simply calls copy() or paste() without calling set_clipboard() first,
    will fall back on whatever clipboard mechanism that determine_clipboard()
    automatically chooses.
    '''
    global copy, paste
    copy, paste = determine_clipboard()
    return copy(text)


def lazy_load_stub_paste():
    '''
    A stub function for paste(), which will load the real paste() function when
    called so that the real paste() function is used for later calls.

    This allows users to import pyperclip without having determine_clipboard()
    automatically run, which will automatically select a clipboard mechanism.
    This could be a problem if it selects, say, the memory-heavy PyQt5 module
    but the user was just going to immediately call set_clipboard() to use a
    different clipboard mechanism.

    The lazy loading this stub function implements gives the user a chance to
    call set_clipboard() to pick another clipboard mechanism. Or, if the user
    simply calls copy() or paste() without calling set_clipboard() first,
    will fall back on whatever clipboard mechanism that determine_clipboard()
    automatically chooses.
    '''
    global copy, paste
    copy, paste = determine_clipboard()
    return paste()


def is_available():
    return copy != lazy_load_stub_copy and paste != lazy_load_stub_paste


# Initially, copy() and paste() are set to lazy loading wrappers which will
# set `copy` and `paste` to real functions the first time they're used, unless
# set_clipboard() or determine_clipboard() is called first.
copy, paste = lazy_load_stub_copy, lazy_load_stub_paste



__all__ = ['copy', 'paste', 'set_clipboard', 'determine_clipboard']













# # Pyperclip v1.4
#
# # A cross-platform clipboard module for Python. (only handles plain text for now)
# # By Al Sweigart al@coffeeghost.net
#
# # Usage:
# #   import pyperclip
# #   pyperclip.copy('The text to be copied to the clipboard.')
# #   spam = pyperclip.paste()
#
# # On Mac, this module makes use of the pbcopy and pbpaste commands, which should come with the os.
# # On Linux, this module makes use of the xclip command, which should come with the os. Otherwise run "sudo apt-get install xclip"
#
#
# # Copyright (c) 2010, Albert Sweigart
# # All rights reserved.
# #
# # BSD-style license:
# #
# # Redistribution and use in source and binary forms, with or without
# # modification, are permitted provided that the following conditions are met:
# #     * Redistributions of source code must retain the above copyright
# #       notice, this list of conditions and the following disclaimer.
# #     * Redistributions in binary form must reproduce the above copyright
# #       notice, this list of conditions and the following disclaimer in the
# #       documentation and/or other materials provided with the distribution.
# #     * Neither the name of the pyperclip nor the
# #       names of its contributors may be used to endorse or promote products
# #       derived from this software without specific prior written permission.
# #
# # THIS SOFTWARE IS PROVIDED BY Albert Sweigart "AS IS" AND ANY
# # EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# # WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# # DISCLAIMED. IN NO EVENT SHALL Albert Sweigart BE LIABLE FOR ANY
# # DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# # LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# # ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# # Change Log:
# # 1.2 Use the platform module to help determine OS.
# # 1.3 Changed ctypes.windll.user32.OpenClipboard(None) to ctypes.windll.user32.OpenClipboard(0), after some people ran into some TypeError
#
# import platform, os
# from subprocess import call, Popen, PIPE
#
# def winGetClipboard():
#     ctypes.windll.user32.OpenClipboard(0)
#     pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 is CF_TEXT
#     data = ctypes.c_char_p(pcontents).value
#     #ctypes.windll.kernel32.GlobalUnlock(pcontents)
#     ctypes.windll.user32.CloseClipboard()
#     return data
#
# def winSetClipboard(text):
#     text = str(text)
#     GMEM_DDESHARE = 0x2000
#     ctypes.windll.user32.OpenClipboard(0)
#     ctypes.windll.user32.EmptyClipboard()
#     try:
#         # works on Python 2 (bytes() only takes one argument)
#         hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text))+1)
#     except TypeError:
#         # works on Python 3 (bytes() requires an encoding)
#         hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text, 'ascii'))+1)
#     pchData = ctypes.windll.kernel32.GlobalLock(hCd)
#     try:
#         # works on Python 2 (bytes() only takes one argument)
#         ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text))
#     except TypeError:
#         # works on Python 3 (bytes() requires an encoding)
#         ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text, 'ascii'))
#     ctypes.windll.kernel32.GlobalUnlock(hCd)
#     ctypes.windll.user32.SetClipboardData(1, hCd)
#     ctypes.windll.user32.CloseClipboard()
#
# def macSetClipboard(text):
#     text = str(text)
#     p = Popen(['pbcopy', 'w'], stdin=PIPE)
#     try:
#         # works on Python 3 (bytes() requires an encoding)
#         p.communicate(input=bytes(text, 'utf-8'))
#     except TypeError:
#         # works on Python 2 (bytes() only takes one argument)
#         p.communicate(input=bytes(text))
#
# def macGetClipboard():
#     p = Popen(['pbpaste', 'r'])
#     stdout, stderr = p.communicate()
#     return bytes.decode(stdout)
#
# def gtkGetClipboard():
#     return gtk.Clipboard().wait_for_text()
#
# def gtkSetClipboard(text):
#     global cb
#     text = str(text)
#     cb = gtk.Clipboard()
#     cb.set_text(text)
#     cb.store()
#
# def qtGetClipboard():
#     return str(cb.text())
#
# def qtSetClipboard(text):
#     text = str(text)
#     cb.setText(text)
#
# def xclipSetClipboard(text):
#     p = Popen(['xclip', '-selection', 'c'], stdin=PIPE)
#     try:
#         # works on Python 3 (bytes() requires an encoding)
#         p.communicate(input=bytes(text, 'utf-8'))
#     except TypeError:
#         # works on Python 2 (bytes() only takes one argument)
#         p.communicate(input=bytes(text))
#
# def xclipGetClipboard():
#     p = Popen(['xclip', '-selection', 'c', '-o'], stdout=PIPE)
#     stdout, stderr = p.communicate()
#     return bytes.decode(stdout)
#
# def xselSetClipboard(text):
#     p = Popen(['xsel', '-i'], stdin=PIPE)
#     try:
#         # works on Python 3 (bytes() requires an encoding)
#         p.communicate(input=bytes(text, 'utf-8'))
#     except TypeError:
#         # works on Python 2 (bytes() only takes one argument)
#         p.communicate(input=bytes(text))
#
#
# def xselGetClipboard():
#     p = Popen(['xsel', '-o'], stdin=PIPE)
#     stdout, stderr = p.communicate()
#     return bytes.decode(stdout)
#
#
# if os.name == 'nt' or platform.system() == 'Windows':
#     import ctypes
#     getcb = winGetClipboard
#     setcb = winSetClipboard
# elif os.name == 'mac' or platform.system() == 'Darwin':
#     getcb = macGetClipboard
#     setcb = macSetClipboard
# elif os.name == 'posix' or platform.system() == 'Linux':
#     xclipExists = call(['which', 'xclip'],
#                 stdout=PIPE, stderr=PIPE) == 0
#     if xclipExists:
#         getcb = xclipGetClipboard
#         setcb = xclipSetClipboard
#     else:
#         xselExists = call(['which', 'xsel'],
#                 stdout=PIPE, stderr=PIPE) == 0
#         if xselExists:
#             getcb = xselGetClipboard
#             setcb = xselSetClipboard
#         try:
#             import gtk
#             getcb = gtkGetClipboard
#             setcb = gtkSetClipboard
#         except Exception:
#             try:
#                 import PyQt4.QtCore
#                 import PyQt4.QtGui
#                 app = PyQt4.QApplication([])
#                 cb = PyQt4.QtGui.QApplication.clipboard()
#                 getcb = qtGetClipboard
#                 setcb = qtSetClipboard
#             except:
#                 raise Exception('Pyperclip requires the gtk or PyQt4 module installed, or the xclip command.')
# copy = setcb
# paste = getcb
