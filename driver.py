import serial
import pyperclip
from pymouse import PyMouse
port = "/dev/cu.usbmodemFA141"
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
def replyPaste():
	clipboard = pyperclip.paste()
	
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
			mouse.move(ray[1]*screen_width, ray[2]*screen_height)
		elif(len(ray)>1 and ray[0]==ord('C')):
			print("CLICK")
			pos = mouse.position()
			mouse.click(pos[0], pos[1]);
		print(ray);
	
if __name__ == "__main__":
	main()
