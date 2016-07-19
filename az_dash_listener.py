#!/usr/bin/env python3

from scapy.all import *
import socket
from bitstring import BitArray
import signal
import threading

getsysinfo  = bytearray(b'\x00\x00\x00\\\xd0\xf2\x97\xfa\x9f\xeb\x8e\xfc\xde\xe4\x9f\xbd\xda\xbf\xcb\x94\xe6\x83\xe2\x8e\xfa\x93\xfe\x9b\xb9\x83\xf8\x85\xf8\xd4\xf6\x85\xe6\x8e\xeb\x8f\xfa\x96\xf3\xd1\xeb\x90\xb2\xd5\xb0\xc4\x9b\xf5\x90\xe8\x9c\xc3\xa2\xc1\xb5\xdc\xb3\xdd\xff\xc5\xbe\xc3\xbe\x92\xb0\xc3\xba\xc9\xbd\xd8\xb5\x97\xad\xd6\xf4\x93\xf6\x82\xdd\xae\xd7\xa4\xcd\xa3\xc5\xaa\x88\xb2\xc9\xb4\xc9\xb4\x00')
setrelayon  = bytearray(b'\x00\x00\x00*\xd0\xf2\x81\xf8\x8b\xff\x9a\xf7\xd5\xef\x94\xb6\xc5\xa0\xd4\x8b\xf9\x9c\xf0\x91\xe8\xb7\xc4\xb0\xd1\xa5\xc0\xe2\xd8\xa3\x81\xf2\x86\xe7\x93\xf6\xd4\xee\xdf\xa2\xdf\xa2\x00')
setrelayoff = bytearray(b'\x00\x00\x00*\xd0\xf2\x81\xf8\x8b\xff\x9a\xf7\xd5\xef\x94\xb6\xc5\xa0\xd4\x8b\xf9\x9c\xf0\x91\xe8\xb7\xc4\xb0\xd1\xa5\xc0\xe2\xd8\xa3\x81\xf2\x86\xe7\x93\xf6\xd4\xee\xde\xa3\xde\xa3\x00')
recentwakeup = False

def clearRecentwakeup():
	global recentwakeup
	recentwakeup = False

def arp_display(pkt):
	global recentwakeup
	if pkt[ARP].op == 1: #who-has (request)
		if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
			if pkt[ARP].hwsrc == 'a0:02:dc:bb:34:7b': # ON
				#print("'ON' dash button pushed")
				if recentwakeup == False:
					recentwakeup = True
					flipRelay()
					threading.Timer(50, clearRecentwakeup).start()
				else:
					recentwakeup = False
			else:
				print("ARP Probe from unknown device: " + pkt[ARP].hwsrc)

def send(command):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect( ('192.168.0.251', 9999) )
	s.send(command)
	data = s.recv(1024)
	s.close()
	return data

def decode(byts):
	decoded = bytes()
	i = BitArray(int=-85, length=8)
	for b in bytearray(byts):
		#print("b is " + " type " + str(type(b)) )
		#print("b is " + str(BitArray(uintne=b, length=8)) )
		bits = BitArray(uint=b, length=8)
		#print( bits.bin + " <=> " + i.bin )
		db = i ^ bits
		i = bits
		decoded += db.tobytes()
	return( decoded )

def flipRelay():
	returndata = send(getsysinfo)
	if returndata == None:
		print("Network call to device failed to receive anything :/")
	else:
		returndata = decode(returndata)

	#print( returndata )

	if re.search('\"relay_state\":1', str(returndata) ):
		print("Relay on; setting to off... ", end='')
		returndata = decode( send(setrelayoff) )
	else:
		print("Relay off; setting to on... ", end='')
		returndata = decode( send(setrelayon) )

	if returndata == b'': 
		print("failed")
	else:
		if re.search('\"err_code\":0', str(returndata) ):
			print("success")
		else:
			print("failed")
			print(returndata)

def signal_handler(signal, frame):
	print("Exiting.")
	sys.exit(0)

# print out bytearray representations for hard-coding
#f = open("on", "rb")
#byts = f.read()
#print(repr(byts))
#f.close()

# make app terminate-able
signal.signal(signal.SIGINT, signal_handler)

while True:
	sniff(prn=arp_display, filter="arp", store=0, count=10)

