# tpdecode
Decode TP-Link packet capture data

# Description
Guided by [Robin Wilson](http://blog.rtwilson.com/hacking-the-worcester-wave-thermostat-in-python-part-2/), this script will decode TCP data to reveal the structure of client commands and server responses. Built using traffic intercpeted from a [HS110 Wi-Fi Smart Plug](http://www.tp-link.com/en/products/details/HS110.html), the Android source code (courtesy of [Decompile Android](http://www.decompileandroid.com/) suggests that this decoder could also work with with their IOT sensors, routers, thermostats, and range extenders.

# Usage
Obtain some packet capture (pcap) data of the traffic between the phone client and device; I suggest [sslsplit](https://www.roe.ch/SSLsplit), using a command similar to `sslsplit -c mitmproxy-ca-cert.pem -k mitmproxy-ca.pem -P -l connections.log -S logs/ -D tcp 192.168.0.10 9999`.

Run `tpdecode` and either point it at your `logs` directory, or specify individual files. The script will decode the file(s) and write them to `original_name-decoded`.
