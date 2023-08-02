# Mitigationofipspoofingattacks

Software-Defned Networking (SDN) represents a network architecture that ofers a
separate control and data layer, facilitating its rapid deployment and utilization for
diverse purposes. However, despite its ease of implementation, SDN is susceptible to
numerous security attacks, primarily stemming from its centralized nature. Among
these threats, Denial of Service (DoS) and Distributed Denial of Service (DDoS) attacks pose the most substantial risks. In the event of a successful attack on the SDN
controller, the entire network may sufer signifcant disruption. Hence, safeguarding
the controller becomes crucial to ensure the integrity and availability of the SDN
network.


This thesis focuses on examining the IP spoofng attack and its impact on the
Data Plane, particularly concerning the metrics of an SDN switch. The investigation centers around attacks that manipulate fow-rules to amplify the number of rules
and deplete the resources of a switch within the Data Plane of an SDN network. To
conduct the study, a software-defned network architecture was constructed using
Mininet, with a Ryu controller employed for managing network operations. Various experiments were carried out to observe the response of the SDN system when
subjected to an IP spoofng attack, aiming to identify potential mitigation strategies
against such threats.

To simulate the resource exhaustion scenario on the SDN network’s Data Plane,
we deliberately triggered an escalation in the number of fow-rules installed in the
switch. This was achieved by sending packets with spoofed IP addresses, thereby
exploiting the switch’s limited resources. Specifcally, we focused on monitoring the
impact on CPU utilization, storage memory, latency, and throughput within the
switch. Detailed fndings were presented in the form of tables, accompanied by
graphical representations to visually illustrate the efects of increasing fow rules on
the switches. Furthermore, we explored potential mitigation measures by developing
an application that actively monitors the fow rules on the Ryu controller, aiming to
detect and counteract such resource-exhausting effect.
