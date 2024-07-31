from csv import reader
from netmiko import ConnectHandler
from getpass import getpass 
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import datetime
from paramiko import SSHException
import getpass

conf_dict = {}
with open("02_config_in_column.csv", "r") as csv_file:
	csv_content = reader(csv_file)
	#print (csv_content)
	ips = next(csv_content)
	#print (ips)
	for conf in csv_content:
		#print (conf)
		for ip in ips:
			if not ip:
				continue
			if ip not in conf_dict.keys():
				conf_dict[ip] = []
			n = ips.index(ip)
			if not conf[n]:
				continue
			conf_dict[ip].append(conf[n])
#print (conf_dict)

user = input("Enter your remote account: ")
password = getpass.getpass()
secret = getpass.getpass()
	
for ip in conf_dict.keys(): #for loop on list of IPs in dic
		print(f"\n{'#' * 50}\nConnecting to the Device {ip}\n{'#' * 50} ") # function to connect to router
		RTR = {
			'device_type': 'cisco_ios',
			'ip':   ip,
			'username': user,
			'password': password,
			"secret": secret, #enable secret password
			"global_delay_factor":2
		    }
		try:
			net_connect = ConnectHandler(**RTR)
		except NetmikoTimeoutException:
			print ('Device not reachable' )
			continue
		except NetmikoAuthenticationException:
			print ('Authentication Failure' )
			continue
		except SSHException:
			print ('Make sure SSH is enabled' )
			continue
		output = net_connect.find_prompt()
		print(output)
		output = net_connect.enable()
		print(output)
		output = net_connect.find_prompt()
		print(output)
		output = net_connect.config_mode()
		print(output)
		print(f"\nExecuting Commands are\n{'~'*22}\n" + str(conf_dict[ip])) #print dic of each IP
		conf = conf_dict[ip]
		print(type(conf))
		output = net_connect.send_config_set(conf)  
		print (output+'\n')
		print ("saving configuration")
		output = net_connect.save_config()
		net_connect.disconnect()

