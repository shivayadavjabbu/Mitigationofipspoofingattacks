#!/bin/bash

# set the IP addresses of h1 and h9
clinet="10.0.0.1"
server="10.0.0.9"

ping_output=$(ping -c 100 -i 0.1 $server)
flow_rules_s1=$(sudo ovs-ofctl dump-flows s1 | wc -l)
flow_rules_s2=$(sudo ovs-ofctl dump-flows s2 | wc -l)
flow_rules_s3=$(sudo ovs-ofctl dump-flows s3 | wc -l)


total_flow_rules=$((flow_rules_s1 + flow_rules_s2 + flow_rules_s3)/3)
roundtime_value=$(echo "$ping_output" | sed -n '2p')
roundtime_value=$(echo "$roundtime_value" | awk '{print $4}' | cut -d '/' -f 2)
    
echo "$total_flow_rules $roundtime_value" >> $latency
