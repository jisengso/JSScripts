#!/usr/env python3

import configparser, os, random, time, sys

if __name__ == "__main__":
    configFilename = "/etc/ipSwitcher.conf"
    """
    Example config file:
    
    [ipSwitcher]
    ifName = enp3s0
    ipRange = 192.168.1.2-254
    cidr = 24
    gateway = 192.168.1.1
    
   
    """
   
    config = configparser.ConfigParser()
    config.readfp(open(configFilename))
    
    interface = config.get("ipSwitcher", "ifName")
    ipRange = config.get("ipSwitcher", "ipRange")
    cidr = config.get("ipSwitcher", "cidr")
    gateway = config.get("ipSwitcher", "gateway")
    
    ipMembers = ipRange.split(".")
    finalNumbers = []
    
    while True:
    
        for member in ipMembers:
            limit = member.split("-")
            if len(limit) == 1:
                finalNumbers.append(limit[0])
            elif len(limit) == 2:
                finalNumbers.append(str(random.randrange(int(limit[0]), int(limit[1])+1)))
            
        targetIp = ".".join(finalNumbers)
        targetIpCidr = "".join([targetIp, "/", cidr])
    
        print("ifconfig", interface, targetIpCidr)
        print("route add default gateway", gateway)
        sys.stdout.flush()
        time.sleep(random.randint(3600, 36000))
                         
