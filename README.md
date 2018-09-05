This is a little script that allows to check network latency for a number of hosts.
By default it will poll every 5 seconds, which can easily be changed in the "sleep" command at the bottom of the script.

The script allows to set a threshold (in milliseconds), and will generate an entry in the "warning" log when a host's latency goes over that threshold.

At this point, it only allows ICMP for the latency test but the goal is to also include monitoring of a TCP connection on a specific port.  This has not been implemented yet.

If ran without any arguments, the script will ask for input from the CLI, but it can also be ran with the argument <inputfile>.

The inputfile is a csv file in the format: host,protocol,threshold
- host: IP or hostname of the device to check
- protocol: "ping" for ICMP or "<port number>" for TCP check.  The TCP check has not been implemented yet so only "ping" works.
- threshold: threshold for warning generation, set in milliseconds
    
The script creates two output files:
- output-latency.txt: CSV file of the actual monitoring results.  Includes a header for easy import and graph creation in Excel.  A failed ping is marked with value "-1".
- output-warning.txt: log file that keeps timestamped entries for values gone above the threshold set, or for a device that was unreachable.
