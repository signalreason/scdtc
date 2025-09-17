# scdtc
demo of mac api client connecting to sierra chart DTC running in parallels windows vm

The connection model is all here, but it needs work to actually do something with the connection.
I did at least figure out how to get it all connected using the Rithmic feed.
- set Allow Support for Sierra Chart Data Feeds to "No".

  <img width="610" height="336" alt="image" src="https://github.com/user-attachments/assets/41ebd628-4939-42f8-bb84-56942ba35893" />
- make sure the selected service is a broker feed

  <img width="551" height="150" alt="image" src="https://github.com/user-attachments/assets/8834a532-da6b-4350-bb2f-f4f10e3c6bd7" />
- get the IPv4 address of your Windows VM

		  PS C:\Users\demo> ipconfig
		  
		  Windows IP Configuration
		  
		  
		  Ethernet adapter Ethernet:
		  
		     Connection-specific DNS Suffix  . : localdomain
		     IPv6 Address. . . . . . . . . . . : fdb2:2c26:f4e4:0:12c7:1569:5216:bb42
		     Temporary IPv6 Address. . . . . . : fdb2:2c26:f4e4:0:d0e8:9711:4a9e:69dd
		     Link-local IPv6 Address . . . . . : fe80::238d:95be:a091:8864%5
		     IPv4 Address. . . . . . . . . . . : 10.211.55.3
		     Subnet Mask . . . . . . . . . . . : 255.255.255.0
		     Default Gateway . . . . . . . . . : 10.211.55.1
- run the proxy in the VM so that the "client" is connecting from localhost

      C:\Users\demo\src>py dtcproxy.py
      Proxy listening on 0.0.0.0:12000
      Client connected: ('10.211.55.2', 59695)
- run the mac client (it will connect to the proxy)

      src/scdtc (main) > python3 dtc_demo.py
