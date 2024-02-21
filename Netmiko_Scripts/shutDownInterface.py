
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
node = {
'device_type': 'cisco_ios',
'host': devicesList[0],
'username': username,
'password': password
}

# establish connection
ssh = ConnectHandler(**node)

intStatus = ''
configuration = []

intStatus = ssh.send_command('sh ip int b').split('\n')

for interface in intStatus:

    #Removes first value which is a part of the menu
    if(interface.split(' ')[0] == 'Interface'):
        continue
    else:
        #Take only the name of the interface from the string in interface
        intName = interface.split(' ')[0]

        #Checks if the value is not equal Vlan1 or GigabitEthernet0/0 which you don't want to change
        if(intName != 'Vlan1' and intName != 'GigabitEthernet0/0' ):
            configuration = [
            'int ' + intName,
            'shutdown'
            ]

            # push configuration set to the node
            ssh.send_config_set(configuration)

            # inform user of completion
            print("The interface: {} has been shutdown!".format(intName))
        else:
            print("The interface: {} is UP! No changes were made.".format(intName))

print(ssh.send_command('sh ip int b'))
# disconnect from node
ssh.disconnect()
