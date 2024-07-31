from csv import reader

e = {}

with open("01_config_in_row.csv", "r") as csv_file:
	csv_content = reader(csv_file)
	for device in csv_content:
		print (device)
		if not device[0]:	#if empty don't add it 
			continue
		else:
			print("first device ip is :" + str(device[0]))
		e[device[0]] = [] # add ip to dic with empty list
		n = len(device)
		print ("length of this ip conf is" + str(n))
		for conf in range (1, n ):
			print (device[conf])
			if not (device[conf]): 
				continue 
			else:
				e[device[0]].append(device[conf]) #add conf in empty list correspondinf to IP
print (e)
#part2
for ip in e.keys(): #for loop on list of IPs in dic
		print(f"\n{'#' * 50}\nConnecting to the Device {ip}\n{'#' * 50} ") # function to connect to router
		print(f"\nExecuting Commands are\n{'~'*22}\n" + str(e[ip])) #print dic of each IP
		for conf in e[ip]:
			print (conf+'\n')

