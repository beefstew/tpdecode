# tpdecode
Command-line control of TP-Link Smart Plug

# Description
The most useful thing in this repository is a program to control a TP-Link [HS110 Wi-Fi Smart Plug](http://www.tp-link.com/en/products/details/HS110.html). This means that you can flip the relay in the smart plug on & off from your computer.

I use this to control a space heater under my desk from my Mac's menubar, like so:
![MacOS menu bar](https://raw.githubusercontent.com/beefstew/tpdecode/master/images/MacOS%20menu%20bar.png)

This project was guided by [Robin Wilson](http://blog.rtwilson.com/hacking-the-worcester-wave-thermostat-in-python-part-2/). Some of the artifacts used to decode the TCP data that revealed the client commands and server responses are included, but it was really decompiling the Android source code (courtesy of [Decompile Android](http://www.decompileandroid.com/)) that revealed the XOR obfuscation of the protocol buffer messages. The source code suggests that this decoding scheme will also work with with the TP-Link IOT sensors, routers, thermostats, and range extenders.

# Installation
The `tplink_on-off.py` control program is a simple Python script. To run it, you will need to:

1. Install [Python 3](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2. Install the [bitstring](https://pypi.python.org/pypi/bitstring/3.1.3) module using [PIP](https://packaging.python.org/tutorials/installing-packages/)

	`$ pip install bitstring`

3. Copy `tplink_on-off.py` to anywhere on your local disk

	`$ sudo cp tplink_on-off.py tpdecode/tplink_on-off.py /usr/local/bin`

4. Ensure the script has execute permissions

	`$ sudo chmod 755 /usr/local/bin/tplink_on-off.py`

## MacOS scripts

If you want to call the on/off script from your Mac's menubar, the easiest way is using AppleScript files. I've included two one-liner `.scpt` files that call the on/off script from `/usr/local/bin`:

	do shell script "/Library/Frameworks/Python.framework/Versions/3.5/bin/python3 /usr/local/bin/tplink_on-off.py on"

To make these scripts appear in your menu bar:

1. Copy the scripts into `/Users/<your username>/Library/Scripts`
2. Re-name the scripts with the name you want to appear in the menu (optional)
3. Enable the Script Menu
	1. Open the `/Applications/Utilities/Script Editor.app`
	2. Navigate to the "Script Editor > Preferences" menu
	3. Enable the "Script Menu" checkbox


# Usage

To turn the relay in the smart plug on, use either:

	$ tplink_on-off.py on
	$ tplink_on-off.py 1

Similarly, these commands will turn off the relay:

	$ tplink_on-off.py off
	$ tplink_on-off.py 0

# Protocol reverse engineering
Obtain some packet capture (pcap) data of the traffic between the phone client and device; I suggest [sslsplit](https://www.roe.ch/SSLsplit), using a command similar to `sslsplit -c mitmproxy-ca-cert.pem -k mitmproxy-ca.pem -P -l connections.log -S logs/ -D tcp 192.168.0.10 9999`.

Run `tpdecode` and either point it at your `logs` directory, or specify individual files. The script will decode the file(s) and write them to `{original_name}-decoded`.
