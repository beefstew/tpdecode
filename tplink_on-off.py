#!/usr/bin/env python3

# Control relay on TP-Link plug
#
#
#   Copyright 2016 Christopher Horn (http://chrishorn.info)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   Please see the LICENSE file for more details.

import socket
from bitstring import BitArray
import signal
import re
import sys

getsysinfo  = bytearray(b'\x00\x00\x00\\\xd0\xf2\x97\xfa\x9f\xeb\x8e\xfc\xde\xe4\x9f\xbd\xda\xbf\xcb\x94\xe6\x83\xe2\x8e\xfa\x93\xfe\x9b\xb9\x83\xf8\x85\xf8\xd4\xf6\x85\xe6\x8e\xeb\x8f\xfa\x96\xf3\xd1\xeb\x90\xb2\xd5\xb0\xc4\x9b\xf5\x90\xe8\x9c\xc3\xa2\xc1\xb5\xdc\xb3\xdd\xff\xc5\xbe\xc3\xbe\x92\xb0\xc3\xba\xc9\xbd\xd8\xb5\x97\xad\xd6\xf4\x93\xf6\x82\xdd\xae\xd7\xa4\xcd\xa3\xc5\xaa\x88\xb2\xc9\xb4\xc9\xb4\x00')
setrelayon  = bytearray(b'\x00\x00\x00*\xd0\xf2\x81\xf8\x8b\xff\x9a\xf7\xd5\xef\x94\xb6\xc5\xa0\xd4\x8b\xf9\x9c\xf0\x91\xe8\xb7\xc4\xb0\xd1\xa5\xc0\xe2\xd8\xa3\x81\xf2\x86\xe7\x93\xf6\xd4\xee\xdf\xa2\xdf\xa2\x00')
setrelayoff = bytearray(b'\x00\x00\x00*\xd0\xf2\x81\xf8\x8b\xff\x9a\xf7\xd5\xef\x94\xb6\xc5\xa0\xd4\x8b\xf9\x9c\xf0\x91\xe8\xb7\xc4\xb0\xd1\xa5\xc0\xe2\xd8\xa3\x81\xf2\x86\xe7\x93\xf6\xd4\xee\xde\xa3\xde\xa3\x00')

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
	#print( returndata )
	
	# if sysinfo call worked, flip relay
	if returnSuccessful(returndata):

		if re.search('\"relay_state\":1', str(decode(returndata)) ):
			print("Relay on; setting to off... ", end='')
			returndata = send(setrelayoff)
		else:
			print("Relay off; setting to on... ", end='')
			returndata = send(setrelayon)

	else:
		print("Failed to fetch current relay state.")

	return returndata

# takes raw return data
# returns True if rdata look good, else False
def returnSuccessful(rdata):
	if rdata == None:
		print("Return data is null. Strange.")
	elif rdata == b'':
		print("Return data is empty. Listener received 0 bytes.")
	else:
		rdata_decoded = decode(rdata)

		if re.search('\"err_code\":0', str(rdata_decoded) ):
			# no errors
			return True
		else:
			return False


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

# tplink_on-off.py usage:
# 	calling with [on|1] argument will turn on relay
#	calling with [off|0] argument will turn off relay
if len(sys.argv) > 1:
	if sys.argv[1] == "0" or sys.argv[1] == "off":
		print("Setting relay to off... ", end='')
		returndata = send(setrelayoff)

	elif sys.argv[1] == "1" or sys.argv[1] == "on":
		print("Setting relay to on... ", end='')
		returndata = send(setrelayon)

	else:
		sys.exit('ERROR: invalid argument: %s' % sys.argv[1])

else:
	print("Flipping relay...")
	returndata = flipRelay()


if returnSuccessful(returndata):
	print("success")
	sys.exit(0)
else:
	print("failed")
	print(decode(returndata))
	sys.exit(1)
