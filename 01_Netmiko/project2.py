from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from paramiko import SSHException
with open('devices.txt') as devices_ips:
	for IP in devices_ips :
		cisco1 = {
		    "device_type": "cisco_ios",
		    "ip": IP,
		    "username": "admin",
		    "password": "admin",
		    "secret": "admin", #enable secret password
		    "global_delay_factor":2
		}
		try :
			connect = ConnectHandler(**cisco1)
			print("\n ##### connecting to device",IP.strip() + "\n ##### ")
		except NetmikoTimeoutException:
			print("\n ##### device not reachable" , IP , "\n ##### ")
			continue
		except NetmikoAuthenticationException:
			print("\n ##### Authentication is wrong" , IP , "\n ##### ")
			continue
		except SSHException:
			print("\n ##### ssh not configured" , IP , "\n ##### ")
			continue
		
		connect.find_prompt()
		connect.enable()
		connect.config_mode()
		with open('conf.txt') as conf_lines:
			config_commands = conf_lines.read().splitlines() #convert txt to list
			output = connect.send_config_set(config_commands)  # send_config_set (cmd should be a list )
			print(output)
			output = connect.save_config()
			print(output)
			output = connect.send_command('sh ip int bri')
			print(output)
			connect.disconnect()
