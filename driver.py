#!/usr/bin/env python3
import serial
import pyperclip
import subprocess
import os
from pykeyboard import PyKeyboard
from sys import platform
from pymouse import PyMouse
import serial.tools.list_ports
global_clipboard = "aroo?"
def find_port():
	ports = list(serial.tools.list_ports.comports())
	for p in ports:
		if "Arduino" in p[1]:
			return p[0]
	return False
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
	print(bytearray(clipboard, "UTF-8"))
	for q in clipboard:
		print("Writing byte...")
		ser.write(q.encode("UTF-8"))
	ser.write(b'\n')
def clipboard_paste():
	if(platform == "darwin"):
		print("Paste returning: "+ global_clipboard)
		return global_clipboard; 
	else:
		print("Paste returning: "+pyperclip.paste())
		return pyperclip.paste()
def clipboard_copy(x):
	print("About to copy: "+x)
	if(platform == "darwin"):
		global_clipboard = x	
	else:
		pyperclip.copy(x)
def fuck_with_arduino(port):
	print("Fucking with the arduino")
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
	keyboard = PyKeyboard()
	screen_size = mouse.screen_size();
	screen_width = screen_size[0]/255
	screen_height = screen_size[1]/255
	assert(ser.isOpen())
	while True:
		ray = ser.readline();
		if(len(ray)>2 and ray[0]==109):
			mouse.move(int(ray[1]*screen_width), int(ray[2]*screen_height))
		elif(len(ray)>1 and ray[0]==ord('C')):
			print("CLICK" + str(ray[1]))
			pos = mouse.position()
			mouse.click(pos[0], pos[1], ray[1]);
		elif(len(ray)>0 and ray[0]==ord('p')):
			print("PASTE MOTHERFUCKER")
			ray = ray.decode()
			print(ray)
			clipboard_copy(ray);
			keyboard.type_string(ray);
		elif(len(ray)>0 and ray[0]==ord('c')):
			print("COPY MOTHERFUCKER")
			print(ray)
			replyCopy(ser)
		elif(len(ray)>1 and ray[0]==ord('s')):
			print("Status: <"+str(ray[1]))
		#print(ray);
def main():
	print("Searching for an arduino to fuck with...")
	while True:
		while not find_port():
			pass
		try:
			fuck_with_arduino(find_port())	
		except serial.serialutil.SerialException:
			print("Arduino unplugged")
if __name__ == "__main__":
	main()
