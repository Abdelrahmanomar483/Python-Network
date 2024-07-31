from netmiko import ConnectHandler
from getpass import getpass 
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
import datetime
from paramiko import SSHException
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
    TNOW = datetime.datetime.now().replace(microsecond=0)
    print (TNOW)
    print ('\n #### Connecting to the Router ' + IP.strip() + '#### \n')
    try:
        net_connect = ConnectHandler(**RTR)
    except NetmikoTimeoutException:
        print ('Device not reachable' )
        continue
    except NetmikoAuthenticationException:
        print ('Authentication Failure')
        continue
    except SSHException:
        print ('Make sure SSH is enabled' )
        continue
    output = net_connect.find_prompt()
    print(output)
    output = net_connect.enable()	#en
    print(output)
    output = net_connect.find_prompt()
    print(output)
    output = net_connect.config_mode()	#conf t
    print(output)
    output = net_connect.find_prompt()
    print(output)
    output = net_connect.send_config_from_file(config_file='router_config.txt')		#send cmd from file
    print(output)
    print('\n Saving the Router configuration \n')
    output = net_connect.save_config()		#WR
    print(output)
    output = net_connect.send_command('show ip int brief')	#send dedicated cmd
    print(output)
    print('\n Initiating config backup \n')
    output = net_connect.send_command('show run')
    SAVE_FILE = open('ROUTER_' + IP + str(TNOW) + ".txt", 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close()
    print('\n Finished config backup \n')
    net_connect.disconnect()

##############################
IP_LIST = open('switches.txt')
for IP in IP_LIST:
    RTR = {
        'device_type': 'cisco_ios',
        'ip':   IP,
        'username': 'admin',
        'password': 'admin',
        "secret": "admin", #enable secret password
	"global_delay_factor":2
    }
    TNOW = datetime.datetime.now().replace(microsecond=0)
    print (TNOW)
    print ('\n #### Connecting to the Switch ' + IP.strip() + '#### \n')
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
    net_connect.find_prompt()
    net_connect.enable()
    net_connect.config_mode()
    output = net_connect.send_config_from_file(config_file='switch_config.txt')
    print(output)

    print('\n Saving the Switch configuration \n')
    output = net_connect.save_config()
    print(output)

    output = net_connect.send_command('show ip route')
    print(output)
    print('\n Initiating config backup \n')
    output = net_connect.send_command('show run')
    SAVE_FILE = open('SWITCH_' + IP + str(TNOW) + ".txt", 'w')
    SAVE_FILE.write(output)
    SAVE_FILE.close()
    print('\n Finished config backup \n')
    net_connect.disconnect()
    net_connect.disconnect()
