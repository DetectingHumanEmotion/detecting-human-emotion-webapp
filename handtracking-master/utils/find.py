import subprocess

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

command_ports = 'snmpwalk -v1 -c public@6 172.30.6.128 .1.3.6.1.2.1.17.4.3.1.2'.split()
command_MACs = 'snmpwalk -v1 -c public@6 172.30.6.128 .1.3.6.1.2.1.17.4.3.1.1'.split()

def get_port_and_mac():
    ports = list()
    macs = list()

    #get all the ports
    for port in run_command(command_ports):
        port=str(port, 'utf-8')
        port = port[-3:-1]
        # print(port)
        ports.append(port)

    #get all the MAC addresses
    for mac in run_command(command_MACs):
        mac=str(mac,'utf-8').replace(" ",":")
        mac = mac[-19:-2]
        # print(mac)
        macs.append(mac)

    #Combine the port and address together
    port_MAC=zip(ports,macs)
    port_MAC.sort()

    #check the results
    # for i in port_MAC:
    #     print(i)

    return port_MAC

# if __name__ == "__main__":
#     get_port_and_mac()