conf_dict={'192.168.0.50': ['terminal len 0',
                  'config t',
                  'int gi1',
                  'no shut',
                  'exit',
                  'exit',
                  'show ip int brie',
                  'show run int gi1'],
 '192.168.0.51': ['terminal len 0',
                  'config t',
                  'int lo0',
                  'ip add 10.0.0.1 255.255.255.0',
                  'int lo1',
                  'ip add 11.0.0.1 255.255.255.0',
                  'do show run int loopback0',
                  'do show run int loopback1'],
 '192.168.0.53': ['terminal len 0', 'config t', 'int gi3', 'no shut'],
 'csr1.test.lab': ['terminal len 0',
                   'config t',
                   'int gi2',
                   'no shut',
                   'ip address 2.2.2.2 255.255.255.0',
                   'exit',
                   'exit',
                   'show ip int brie',
                   'show run int gi2']}
for ip in conf_dict.keys(): #for loop on list of IPs in dic
		print(f"\n{'#' * 50}\nConnecting to the Device {ip}\n{'#' * 50} ")
		print(f"\nExecuting Commands are\n{'~'*22}\n" + str(conf_dict[ip])) #print dic of each IP
		for conf in conf_dict[ip]:
			print (conf+'\n')
			
