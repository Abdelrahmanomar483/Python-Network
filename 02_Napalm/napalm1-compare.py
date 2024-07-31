# scp should be configured before on device "ip scp server enable"
from napalm import get_network_driver
optional_args = {'enable_password': 'admin'}
driver = get_network_driver('ios')
device = driver('192.168.255.60', 'admin', 'admin', optional_args = optional_args)
device.open()

device.load_merge_candidate(filename='routes.txt')  #add configuration to candidate
print (device.compare_config())     #compare current conf to candidate

if len(device.compare_config()) > 0:
    choice = input("\nWould you like to commit the configuration? [yN]: ")
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

