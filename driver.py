#!/usr/bin/env python3
import serial
import pyperclip
import subprocess
import os
from sys import platform
from pymouse import PyMouse
if platform == "darwin":
	from AppKit import*
	port = "/dev/cu.usbmodemFA141"
else:
	port =".\\\\COM3"
def readline(a_serial, eol=b'\n\n'):
    leneol = len(eol)
    line = bytearray()
    while True:
        c = a_serial.read(1)
        if c:
            line += c
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)
def replyCopy(ser):
	clipboard = clipboard_paste()
	ser.write(b"X")
	print(bytearray(clipboard, "UTF-8"))
	for b in bytearray(clipboard, "UTF-8"):
		ser.write(b)
	ser.write(b'\x00')
def clipboard_paste():
	if(platform == "darwin"):
		stdoutdata = subprocess.getoutput("pbpaste")
		return stdoutdata
	else:
		print(pyperclip.paste())
		return pyperclip.paste()
def clipboard_copy(x):
	if(platform == "drwin"):
		pb = NSPasteboard.generalPasteboard()
		pb.clearContents()
		a = NSArray.arrayWithObject_("hello world")
		pb.writeObjects_(a)
	else:
		print(x)
		return pyperclip.copy(x)
def main():
	ser = serial.Serial(
	port = port,
	baudrate = 9600,
	bytesize = serial.EIGHTBITS, 
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE, 
	timeout = 1,
	xonxoff = False,
	rtscts = False,
	dsrdtr = False,
	writeTimeout = 2
	)	
	
	mouse = PyMouse()
	screen_size = mouse.screen_size();
	screen_width = screen_size[0]/255
	screen_height = screen_size[1]/255
	assert(ser.isOpen())
	while True:
		ray = ser.readline();
		if(len(ray)>2 and ray[0]==109):
			mouse.move(int(ray[1]*screen_width), int(ray[2]*screen_height))
		elif(len(ray)>1 and ray[0]==ord('C')):
			pos = mouse.position()
			mouse.click(pos[0], pos[1]);
		elif(len(ray)>0 and ray[0]==ord('p')):
			print("PASTE MOTHERFUCKER")
			ray = ray
			print(ray)
			clipboard_copy(ray.decode());
		elif(len(ray)>0 and ray[0]==ord('c')):
			print("COPY MOTHERFUCKER")
			print(ray)
			replyCopy(ser)
		#print(ray);
	
if __name__ == "__main__":
	main()
