# Driver code to support smart mouse operations on the PC end

import pyperclip

def _readline(self):
    eol = chr(0)
    leneol = len(eol)
    line = bytearray()
    while True:
        c = self.ser.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)

def main:

    #copy from clipboard
    pyperclip.copy()

    #paste to clipboard
    pyperclip.paste()

