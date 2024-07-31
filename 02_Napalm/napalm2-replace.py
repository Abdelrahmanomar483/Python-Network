# scp should be configured before on device "ip scp server enable"
from napalm import get_network_driver
import json
optional_args = {'enable_password': 'admin'}
driver = get_network_driver('ios')
device = driver('192.168.255.60', 'admin', 'admin', optional_args = optional_args)
device.open()


#device.load_merge_candidate(filename='routes.txt')
device.load_replace_candidate(filename="ROUTER_192.168.255.602024-07-22 14:23:22.txt") #replace current config with backup config 
print (device.compare_config())		#compare what's different 

if len(device.compare_config()) > 0:
    choice = input("\nWould you like to Replace the configuration? [yN]: ")
    if choice == 'y':
        print('Committing ...')
        device.commit_config()
        choice = input("\nWould you like to Rollback to previous config? [yN]: ")
        if choice == 'y':
            print('Committing ...')
            device.rollback()

    else:
        print('Discarding ...')
        device.discard_config()

else:
    print ('No difference')

# close the session with the device.
device.close()
print('Done.')

