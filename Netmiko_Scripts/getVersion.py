
#!/usr/bin/env python3

from netmiko import ConnectHandler
from getpass import getpass

# Prompt for username and password
username = input("Username: ")
password = getpass()
#device = input("What node are you configuring? ")

with open('ipAddresses') as f:
    devicesList = f.read().splitlines()

# node aka router or switch connection information
for device in devicesList:

    print('Connecting to: ' + device)
    node = {
    'device_type': 'cisco_ios',
    'host': device,
    'username': username,
    'password': password
    }

# establish connection
    ssh = ConnectHandler(**node)

    shVersionLine = ssh.send_command('sh version').split('\n')

    #Take only the name of the interface from the string
    answer = shVersionLine[0].split(' ')[5]
    print("The device with IP address: {} has version: {}".format(device, answer.strip(',')))

#print(ssh.send_command('sh version'))
# disconnect from node
ssh.disconnect()

