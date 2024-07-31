import getpass
import sys
import telnetlib

HOST = "192.168.255.40"
user = raw_input("Enter your remote account: ")
password = getpass.getpass()

telnet = telnetlib.Telnet(HOST)

telnet.read_until("Username: ",3)
telnet.write(user + "\n")
if password:
   telnet.read_until("Password:",3)
   telnet.write(password + "\n")

telnet.write("en\n")
if password:
   telnet.read_until("Password:",3)
   telnet.write(password + "\n")
telnet.write("conf t\n")
telnet.write("hostname R1\n")
telnet.write("exit\n")
telnet.write("show ip int br\n")
telnet.write("exit\n")
print telnet.read_all()
