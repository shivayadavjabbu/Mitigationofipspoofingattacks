#!/bin/bash
rm ./storagecpu
touch ./storagecpu
while true; do
  # Collect flow rules from switches s1, s2, and s3 in Mininet
  flow_rules_s1=$(sudo ovs-ofctl dump-flows switch1 | wc -l)
  flow_rules_s2=$(sudo ovs-ofctl dump-flows switch2 | wc -l)
  flow_rules_s3=$(sudo ovs-ofctl dump-flows switch3 | wc -l)

  # Add the total flow rules to the file "storagecpu"
  total_flow_rules=$((flow_rules_s1 + flow_rules_s2 + flow_rules_s3))

  total_storage=$( ps aux | grep "root" | grep "503"| grep " ovs-vswitchd unix:/var/run/openvswitch/db.sock"| cut -d ' ' -f 1-20 )
  echo "$total_flow_rules  $total_storage " >> ./storagecpu

  # Sleep for 30 seconds before collecting the flow rules again
  sleep 60
done
