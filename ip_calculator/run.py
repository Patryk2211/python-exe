import socket
import sys
import json

def check_ip(ip):
	if (ip.count('.') == 3 and ip.count('/') == 1):
		if ip.replace('.', '', 3).replace('/', '', 1).isdigit():
			
			elements = ip.replace('/', '.').split('.')
			fails = 0
			for i in range(3):
				if not (int(elements[i]) >= 0 and int(elements[i]) <= 255): 
					fails +=1
			if not (int(elements[4]) >= 0 and int(elements[4]) <= 32): 
				fails += 1
			
			if fails == 0: return True
			else: return False
		else: return False
	else: return False

def v4_decimal_to_binary(decimal_ip):
	elements = decimal_ip.replace('/', '.').split('.')
	binary_address = "{0:08b}".format(int(elements[0])) + "." + "{0:08b}".format(int(elements[1])) + "." + "{0:08b}".format(int(elements[2])) + "." + "{0:08b}".format(int(elements[3]))
	return binary_address
	
def v4_binary_to_decimal(binary_ip):
	decimal_address = str(int(binary_ip[0:8],2)) + "." + str(int(binary_ip[9:17],2)) + "." +  str(int(binary_ip[18:26],2)) + "." +  str(int(binary_ip[27:35],2))
	return decimal_address
	
def mask(ip):
	elements = ip.replace('/', '.').split('.')
	binary_mask = ""
	for i in range(32):
		if i < int(elements[4]):
			binary_mask += "1"
			if(i == 7 or i == 15 or i == 23):
				binary_mask += "."
		else: 
			binary_mask += "0"
			if(i == 7 or i == 15 or i == 23):
				binary_mask += "."

	#print("Binary mask: " + binary_mask)
	return binary_mask
	
def net_address(ip):
	elements = ip.replace('/', '.').split('.')
	decimal_host = elements[0] + "." + elements[1] + "." + elements[2] + "." + elements[3] 
	binary_host = v4_decimal_to_binary(decimal_host)
	binary_mask = mask(ip)
	binary_net_address = ""
	for i in range(35):
		if (binary_host[i] == "1") and (binary_mask[i] == "1"):
			binary_net_address += "1"
		elif(binary_host[i] == "."):
			binary_net_address += "."
		else:
			binary_net_address += "0"
			
	return binary_net_address
	
def net_class(ip):
	elements = ip.replace('/', '.').split('.')
	first = int(elements[0])
	if(first >= 0 and first <= 127): return "Class A"
	if(first >= 128 and first <= 191): return "Class B"
	if(first >= 192 and first <= 223): return "Class C"	
	if(first >= 224 and first <= 240): return "Class D"
	if(first >= 240 and first <= 255): return "Class E"
	
def broadcast(ip):
	binary_mask = mask(ip)
	binary_mask_negation = ""
	for i in range(35):
		if binary_mask[i] == "1":
			binary_mask_negation += "0"
		elif binary_mask[i] == ".":
			binary_mask_negation += "."
		else:
			binary_mask_negation += "1"
			
	decimal_mask_negation = v4_binary_to_decimal(binary_mask_negation)
	binary_net_address = net_address(ip)
	decimal_net_address = v4_binary_to_decimal(binary_net_address)
	decimal_broadcast_address = []
	binary_broadcast_address = ""
	mask_negation_elements = decimal_mask_negation.split(".")
	net_address_elements = decimal_net_address.split(".")
	for i in range(4):
		decimal_broadcast_address.append(str(int(mask_negation_elements[i]) + int(net_address_elements[i])))
	
	string_tmp = ".".join(decimal_broadcast_address)
	binary_broadcast_address = v4_decimal_to_binary(string_tmp)
	
	return binary_broadcast_address
	
def first_host_address(ip):
	binary_net_address = net_address(ip)
	decimal_net_address = v4_binary_to_decimal(binary_net_address)
	elements_decimal_net_address = decimal_net_address.split(".")
	elements_decimal_first_host_address = []
	for i in range(4):
		if i == 3:
			elements_decimal_first_host_address.append(str(int(elements_decimal_net_address[i]) + 1))
		else:
			elements_decimal_first_host_address.append(str(elements_decimal_net_address[i]))
			
	decimal_first_host_address = ".".join(elements_decimal_first_host_address)
	binary_first_host_address = v4_decimal_to_binary(decimal_first_host_address)
	return binary_first_host_address
	
def last_host_address(ip):
	binary_broadcast_address = broadcast(ip)
	decimal_broadcast_address = v4_binary_to_decimal(binary_broadcast_address)
	elements_decimal_broadcast_address = decimal_broadcast_address.split(".")
	elements_decimal_last_host_address = []
	for i in range(4):
		if i == 3:
			elements_decimal_last_host_address.append(str(int(elements_decimal_broadcast_address[i]) - 1))
		else:
			elements_decimal_last_host_address.append(str(elements_decimal_broadcast_address[i]))
			
	decimal_last_host_address = ".".join(elements_decimal_last_host_address)
	binary_last_host_address = v4_decimal_to_binary(decimal_last_host_address)
	return binary_last_host_address
	
def max_hosts(ip):
	elements = ip.replace("/", ".").split(".")
	ones_in_mask = int(elements[4])
	return str(2**(32-ones_in_mask) - 2)
	
def write_to_JSON_file(file_name, data):
	file = open(file_name, "a+")
	json.dump(data, file, indent=4)
	file.write("\n\n")
	file.close()
	
	
def main():
	if len(sys.argv) > 1:
		host_ip = str(sys.argv[1])
	else:
		host_ip = socket.gethostbyname(socket.gethostname()) + "/24"

	if not check_ip(host_ip): print("Niepoprawny adres ip")
	else: 
		print("Poprawny adres id: " + host_ip)
		binary_mask = mask(host_ip)
		decimal_mask = v4_binary_to_decimal(binary_mask)
		binary_net_address = net_address(host_ip)
		decimal_net_address = v4_binary_to_decimal(binary_net_address)
		address_class = net_class(host_ip)
		binary_broadcast_address = broadcast(host_ip)
		decimal_broadcast_address = v4_binary_to_decimal(binary_broadcast_address)
		binary_first_host_address = first_host_address(host_ip)
		decimal_first_host_address = v4_binary_to_decimal(binary_first_host_address)
		binary_last_host_address = last_host_address(host_ip)
		decimal_last_host_address = v4_binary_to_decimal(binary_last_host_address)
		binary_max_hosts = "{0:08b}".format(int(max_hosts(host_ip)))
		decimal_max_hosts = max_hosts(host_ip)
		
		
		print("Binary mask: " + binary_mask)
		print("Decimal mask: " + decimal_mask)
		print("Binary net address: " + binary_net_address)
		print("Decimal net address: " + decimal_net_address)
		print("Net address class: " + address_class)
		print("Binary broadcast address: " + binary_broadcast_address)
		print("Decimal broadcast address: " + decimal_broadcast_address)
		print("Binary first host address: " + binary_first_host_address)
		print("Decimal first host address: " + decimal_first_host_address)
		print("Binary last host address: " + binary_last_host_address)
		print("Decimal last host address: " + decimal_last_host_address)
		print("Binary max number of hosts: " + binary_max_hosts)
		print("Decimal max number of hosts: " + decimal_max_hosts)
		
		data = {}
		data["Binary mask"] = binary_mask
		data["Decimal mask"] = decimal_mask
		data["Binary net address"] = binary_net_address
		data["Decimal net address"] = decimal_net_address
		data["Net address class"] = address_class
		data["Binary broadcast address"] = binary_broadcast_address
		data["Decimal broadcast address"] = decimal_broadcast_address
		data["Binary first host address"] = binary_first_host_address
		data["Decimal first host address"] = decimal_first_host_address
		data["Binary last host address"] = binary_last_host_address
		data["Decimal last host address"] = decimal_last_host_address
		data["Binary max number of hosts"] = binary_max_hosts
		data["Decimal max number of hosts"] = decimal_max_hosts
		
		write_to_JSON_file("ips.json", data)

main()

#bin = bin(255)
#print bin
#print int(bin[2:],2)
