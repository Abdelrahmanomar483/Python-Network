from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import datetime
from paramiko import SSHException
import time
import datetime
import schedule

def BACKUP():
	TNOW = datetime.datetime.now().replace(microsecond=0)
	IP_LIST = open('routers.txt')
	for IP in IP_LIST:
	    RTR = {
		'device_type': 'cisco_ios',
		'ip':   IP,
		'username': 'admin',
		'password': 'admin',
		"secret": "admin", #enable secret password
		"global_delay_factor":2
	    }

	    print ('\n #### Connecting to the Router ' + IP.strip() + '#### \n')
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
	    output = net_connect.find_prompt()
	    print(output)
	    print('\n Initiating config backup \n')
	    output = net_connect.send_command('do show run')
	    SAVE_FILE = open('ROUTER_' + IP + str(TNOW) + ".txt", 'w')
	    SAVE_FILE.write(output)
	    SAVE_FILE.close()
	    print('\n Finished config backup \n')
	    net_connect.disconnect()
schedule.every().minute.at(":00").do(BACKUP) #Run backup every minute for testing
schedule.every().day.at("11:59").do(BACKUP) #Run backup every dat at midnight which is reaiable , task will be run in bg
while True:
    schedule.run_pending()
    time.sleep(1)
