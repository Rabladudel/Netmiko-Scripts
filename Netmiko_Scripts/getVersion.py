from netmiko import ConnectHandler
from getpass import getpass

# Prompt for username and password
username = input("Username: ")
password = getpass()

#Create file with name 'ipAddresses' and paste there IP addresses of the devices
#With only one IP address in the file, script will show an error.
with open('ipAddresses') as f:
    devicesList = f.read().splitlines()

# node aka router or switch connection information
for device in devicesList:

    print('Connecting to the IP: ' + device)
    node = {
    'device_type': 'cisco_ios',
    'host': device,
    'username': username,
    'password': password
    }

# establish connection
    ssh = ConnectHandler(**node)

    #Save lines of the outcome as a string 
    shVersionLine = ssh.send_command('sh version').split('\n')

    #Take only the name of the interface from the string
    answer = shVersionLine[0].split(' ')[5]
    print("The device with IP address: {} has version: {}".format(device, answer.strip(',')))

# disconnect from node
ssh.disconnect()

