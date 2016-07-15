#!/usr/bin/env python3

# Decode TP-Link packet capture data
#
#
#   Copyright 2016 Christopher Horn (http://chrishorn.info)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   Please see the LICENSE file for more details.


from os import listdir
from os.path import isfile, join
from bitstring import BitArray
import re
import argparse


# nifty
# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description="""Decode TCP data payloads for TP-Link devices.
Original files will not be modified. A copy of the file will be created with the suffix \'-decode\'""")

parser.add_argument('-d', '--dir', metavar='directory', nargs='?', default='',
                    help='directory to scan for files to decode')
parser.add_argument('files', metavar='filename', nargs='*',
					help='files to decode')

args = parser.parse_args()

# build a list of files to decode
filelist = []
if args.dir:
	for f in listdir(args.dir):
		if isfile( join(args.dir, f) ) and not re.search('-decoded$', f):
			filelist.append( join(args.dir, f) )	
	filelist += args.files
else:
	filelist = args.files

if filelist == []:
	parser.print_help()

# sslsplit was used to capture the traffic between the iPhone app and the HS110 plug
# it turns out that the raw pcap could've been used, there is no SSL going on
for file in filelist:
	bArr = []
	decoded = []

	# couldn't figure out a nicer way of slurping the bytes into memory
	print("reading from " + str(file) + "... ", end="")
	f = open(file, "rb")
	f.seek(0, 2)
	end = f.tell()
	f.seek(0, 0)
	for i in range(0, end):	
		byte = f.read(1)
		bArr.append( byte )
		f.seek(i, 0)
		#print( str(i) + "_" + str(f.tell()) + " ", end="" )
		i += 1
	f.close()

	print( str(len(bArr)) + " bytes")
	#print( "obfuscated: " + str(bArr) )
	decoded = []

	# this part was gleaned from the decompiled Android app source code (http://www.decompileandroid.com/)
	# HSSmartPlugUtils.java shows the bit array decode function
	# basically, each bit is XOR'd with the previous. the first bit is XOR'd with -85
	# in Java, the -85 is represented in bits with "two's complement" -- conveniently, BitArray does this, too
	i = BitArray(int=-85, length=8)
	#print( BitArray(bArr[0]).bin + " <=> " + i.bin )
	for i2 in range(0, len(bArr)):
		#print( str(i2) + " = " + BitArray(bArr[i2]).bin )
		b = i ^ BitArray(bArr[i2])
		i = bArr[i2]
		decoded.append(b)
		#print( b.hex )
		#print( str(b) + " type= " + str(type(b)) )

	#print( "decoded: ", end="")
	#print( decoded )

	# iterate through the BitArray and write it out as bytes
	f = open(file + "-decoded", "wb")
	for byte in decoded:
		f.write( byte.tobytes() )
	f.close()

