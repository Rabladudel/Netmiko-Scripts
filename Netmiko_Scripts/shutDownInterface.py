
from netmiko import ConnectHandler
from getpass import getpass

# Prompt for username and password
username = input("Username: ")
password = getpass()


#Create file with name 'ipAddresses' and paste there IP addresses of the devices
with open('ipAddresses') as f:
    devicesList = f.read().splitlines()

#Information needed to connect to the device
node = {
'device_type': 'cisco_ios',
'host': devicesList[0], #if you use more then one device, remove '[0]'
'username': username,
'password': password
}

# establish connection
ssh = ConnectHandler(**node)

#Command to execute
intStatus = ssh.send_command('sh ip int b').split('\n')

for interface in intStatus:

    #Split the whole command into lines
    interfaceToFilter = interface.split(' ')
    #Remove '' elements, created by split() method
    interfaceFiltered = [item for item in interfaceToFilter if item != '']

    #Removes first value which is a part of the menu
    if(interfaceFiltered[0] == 'Interface'):
        continue
    else:
        #Takes only required information for the script which are: [0] = 'GigabitEthernet' -/- [5] = 'down' [4] = 'administratively'
        intName = interfaceFiltered[0]
        intShutManually = interfaceFiltered[4]
        intStat = interfaceFiltered[5]

        #Checks if the value is 'administratively' which means, the port is already shutdown
        if(intShutManually == 'administratively'):
            print("The interface: {} is already administratively down! No changes were made.".format(intName))

        #Checks if the value is not 'up' which means, the port is down
        elif(intStat != 'up'): #Can be changed to (intStat == 'down')
            configuration = [
            'int ' + intName, #Command: interface {interface name in the variable}
            'shutdown' #Command: shutdown 
            ]

            #Executes commands from variable: configuration
            ssh.send_config_set(configuration)

            #Inform about a state of the interface
            print("The interface: {} has been shutdown!".format(intName)) 
        #If any port is neither 'down' or 'administratively down'
        else:
            print("The interface: {} is UP! No changes were made.".format(intName))

#Show information about interfaces after executing the code
print(ssh.send_command('sh ip int b'))
# disconnect from node
ssh.disconnect()
