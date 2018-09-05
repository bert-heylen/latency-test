import os
import time
import subprocess
import sys

def check_hosts(hosts):
    print('Checking if all hosts are up.  Only up hosts will be included in the script.')
    for host in hosts:
        line = 'ping ' + str(host) +  ' -c 5 -i 0.2 -W 3 >> /dev/null'
        result = os.system(line)
        if result == 0:
            print('Host {} is up.'.format(host))
            hosts[host][2] = 1
        else:
            print('Host {} is down.'.format(host))
            hosts[host][2] = 0
    return;

def ping_hosts(hosts):
    for host in hosts:
        if hosts[host][0] == 'ping' and hosts[host][2] == 1:
            proc = subprocess.Popen(['ping', '-c', '1', host], stdout=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            try:
                hosts[host][3] = stdout.decode('ASCII').split('\n')[1].split(' ')[6].split('=')[1]
            except:
                hosts[host][3] = -1
    return;

def write(hosts):
    header = ''
    result = ''
    
    # If output file does not exist, create it with header row
    if not os.path.exists('./output-latency.txt'):
        for host in hosts:
            if hosts[host][2] == 1:
                header = str(header) + str(host) + ','

        output = open('./output.txt', 'w')
        output.write(str(header))
        output.write('\n')
        output.close
    
    # If output file exists, write values to line
    for host in hosts:
        if hosts[host][2] == 1:
            result = str(result) + str(hosts[host][3]) + ','
        
    output = open('./output.txt', 'a')
    output.write(str(result))
    output.write('\n')
    output.close
    
    # Check for values over threshold and write to seperate file
    for host in hosts:
        if not hosts[host][1] == '':
            if float(hosts[host][3]) >= float(hosts[host][1]):
                result = time.strftime('%d/%m-%H:%M:%S') + ' - ' + host + ' went over threshold of ' + str(hosts[host][1]) + '. Value: ' + str(hosts[host][3])
                output = open('./output-warnings.txt', 'a')
                output.write(str(result))
                output.write('\n')
                output.close()
            elif hosts[host][3] == -1:
                result = time.strftime('%d/%m-%H:%M:%S') + ' - ' + host + ' unreachable.'
                output = open('./output-warnings.txt', 'a')
                output.write(str(result))
                output.write('\n')
                output.close()
    return;
    
def main():
    
    hosts = {}

    if not len(sys.argv) > 1:
        # Get user input
        check = 'y'
        while (check == 'y'):
            data = input('Enter IP or hostname: ')
            data2 = input('Enter "ping" for ICMP or port number for TCP test: ')
            data3 = input('Enter RTT threshold, hit enter for none: ')
            data3 = float(data3)
            check = input('Do you want to enter another host - y/n:  ')
            
            hosts[data] = [data2, data3, '', ''] 
    else:
        f = open(sys.argv[1], 'r')
        for entry in f:
            entry = entry.strip()
            print(entry)
            threshold = entry.split(',')[2]
            threshold = float(threshold)
            hosts[entry.split(',')[0]] = [entry.split(',')[1], threshold, '', '']
        f.close()
    
    # Check if hosts are up before starting the real script
    check_hosts(hosts)
    
    print('Monitoring... Hit CTRL-C to stop.  Tail the logfiles for real-time data.')

    if os.path.exists('./output.txt'):
        os.remove('./output.txt')
    if os.path.exists('./output_threshold.txt'):
        os.remove('./output_threshold.txt')

    while(True):
        ping_hosts(hosts)
        write(hosts)
        
        time.sleep(5)
    
if __name__ == '__main__':
    main()