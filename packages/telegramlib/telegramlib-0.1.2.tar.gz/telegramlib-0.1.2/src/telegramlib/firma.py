import colorama, random, platform, sys, os, ctypes
from time import sleep

def morpheus_typing(monito, color = colorama.Fore.LIGHTCYAN_EX, reactivate_cursor = True):
    lock = get_terminal_lock()
    lock.lock()
    set_cursor_visibility_to(False)
    delete_multiple_lines(100000)
    colorama.init(autoreset = True)
    for char in monito:
        try:
            print(color + char, end = '')
            sleep(random.randrange(5, 20)/100)
        except KeyboardInterrupt:
            pass
    sleep_lock(1.5)
    print()
    delete_multiple_lines(100000)
    set_cursor_visibility_to(reactivate_cursor)
    lock.unlock()

def sleep_lock(t):
    lock = get_terminal_lock()
    lock.lock()
    for _ in range(int(t*100)):
        try:
            sleep(t/600)
        except KeyboardInterrupt:
            pass
    lock.unlock()

class UnixTerminalLock:
    def __init__(self):
        import sys
        import termios
        import tty
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
    
    def lock(self):
        import tty
        tty.setcbreak(self.fd)

    def unlock(self):
        import termios
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

class WindowsTerminalLock:
    def __init__(self):
        import msvcrt
        self.running = True
    
    def lock(self):
        import threading
        self.running = True
        self.thread = threading.Thread(target = self._block_input)
        self.thread.start()
    
    def _block_input(self):
        import msvcrt
        while self.running:
            if msvcrt.kbhit():
                msvcrt.getch()
    
    def unlock(self):
        self.running = False
        self.thread.join()

def get_terminal_lock():
    os_name = platform.system()
    if os_name == "Windows":
        return WindowsTerminalLock()
    elif os_name in ["Linux", "Darwin"]:
        return UnixTerminalLock()
    else:
        raise NotImplementedError(f"Sistema operativo non supportato: {os_name}")
    
class _CursorInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),
                ("visible", ctypes.c_byte)]

def set_cursor_visibility_to(visible: bool):
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = visible
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        if visible:
            sys.stdout.write("\033[?25h")
        else:
            sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def delete_multiple_lines(n = 1):
    print()
    for _ in range(n + 1):
        try:
            sys.stdout.write("\x1b[2K")  # delete the last line
            sys.stdout.write("\x1b[1A")  # cursor up one line
        except KeyboardInterrupt:
            pass 