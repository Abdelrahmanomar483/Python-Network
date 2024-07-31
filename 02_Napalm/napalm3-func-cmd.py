import json
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from napalm import get_network_driver
import time
import datetime
from getpass import getpass 
from time import sleep


username = input('username: ')
password = getpass('password: ')
enable_password = getpass('enable_password: ')
enable_secret = getpass('enable_secret: ')
TNOW = datetime.datetime.now().replace(microsecond=0)


optional_args = {'enable_password': enable_password, 'secret': enable_secret}
cisco = ['192.168.255.60', '192.168.255.50']
arista = ['192.168.67.30']

def save_to_file (output,IP):
        SAVE_FILE = open('ROUTER_' + IP + str(TNOW) +".txt",'a+')
        SAVE_FILE.write(output)
        SAVE_FILE.close()


def getfacts(ips, vendor, mode):
    for ip in ips:
        print('Connecting to' + vendor + 'device ' + str(ip))
        try:
            driver = get_network_driver(mode)
            device = driver(ip,username ,password ,optional_args=optional_args)
            device.open()
        except NetmikoTimeoutException:
            print('Device not reachable')
            continue
        except NetmikoAuthenticationException:
            print('Authentication Failure')
            continue
        except SSHException:
            print('Make sure SSH is enabled')
            continue
            
        facts = device.get_facts()
        a = (json.dumps(facts, sort_keys=True, indent=4))
        print(json.dumps(facts, sort_keys=True, indent=4))
        print('#######\nGET FACTS\n#######')
        save_to_file(a,ip)
        print(".................Waiting 1 minute.............")
        sleep(60)
        print(".................1 minute has passed..............")
        
        print('#######\nGET ARP\n#######')
        arptable = device.get_arp_table()
        print(json.dumps(arptable, sort_keys=True, indent=4))
        b = (json.dumps(arptable, sort_keys=True, indent=4))
        save_to_file(b,ip)
        print(".................Waiting 1 minute.............")
        sleep(60)
        print(".................1 minute has passed..............")
	
        print('#######\nGET CONFIG\n#######')
        config = device.get_config()
        print(json.dumps(config, sort_keys=True, indent=4))
        c = (json.dumps(config, sort_keys=True, indent=4))
        save_to_file(c,ip)

        print('#######\nGET BGP Peers \n#######')
        peers = device.get_bgp_neighbors()
        print(json.dumps(peers, sort_keys=True, indent=4))
        d = (json.dumps(peers, sort_keys=True, indent=4))
        save_to_file(d,ip)

        print('#######\nGET ENVIRONMENT\n#######')
        environment = device.get_environment()
        print(json.dumps(environment, sort_keys=True, indent=4))
        f = (json.dumps(environment, sort_keys=True, indent=4))
        save_to_file(f,ip)

        print('#######\nGET INTERFACES\n#######')
        interfaces = device.get_interfaces()
        print(json.dumps(interfaces, sort_keys=True, indent=4))
        g = (json.dumps(interfaces, sort_keys=True, indent=4))
        save_to_file(g,ip)

        print('#######\nGET INTERFACE COUNTERS\n#######')
        interfacecounter = device.get_interfaces_counters()
        print(json.dumps(interfacecounter, sort_keys=True, indent=4))
        h = (json.dumps(interfacecounter, sort_keys=True, indent=4))
        save_to_file(h,ip)

        print('#######\nPING\n#######')
        pingtest = device.ping('192.168.255.60')
        print(json.dumps(pingtest, sort_keys=True, indent=4))

        print('#######\nTRACEROUTE\n#######')
        pingtest = device.traceroute('192.168.255.60')
        print(json.dumps(pingtest, sort_keys=True, indent=4))

        print(vendor + 'Device ' + str(ip) + ' software version is ' + facts['os_version'])
        device.close()


getfacts(cisco, ' cisco ', 'ios')
getfacts(arista, ' arista ', 'eos')
