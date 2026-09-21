# Lecture 09 — Worksheet & Exit Ticket

Name: ________________  Date: ______

## Part A — Tag anatomy (5 min)
Frame on a trunk: `DA | SA | __ | __ | original EtherType | payload`
1. Fill the two missing fields and their sizes: ________ ( __ bits), ________ ( __ bits)
2. TPID value: ________  VID range: ________
3. What changes when the same logical frame is delivered to a host on an access port? ________

## Part B — Trunk reasoning (10 min)
SW1—trunk(VLAN 10,20)—SW2. A1,B1 ∈ VLAN10 on SW1; A2 ∈ VLAN10, C1 ∈ VLAN20 on SW2.
4. Frame A1→B1: does it cross the trunk? Tagged? ________
5. Frame A1→A2: path? Tagged on trunk? ________
6. Frame A1→C1: what device must act, and at which layer? ________
7. Native VLAN is 1 on SW1, 20 on SW2: describe the leak. ________

## Part C — Design (10 min)
8. Allocate VIDs for 12 departments × (staff/students/devices) + 10 spare. Describe your
   ID plan in 2 lines. ________
9. Guest devices must reach the internet but never printers. Name the two mechanisms
   (L2 + L3) you would use. ________
10. True/false: VLANs alone prevent a staff laptop from ARP-spoofing the finance VLAN.
    Why? ________

## Exit ticket (3 items)
1. The TPID that marks an 802.1Q tag is `0x______`.
2. Access ports send frames (tagged/untagged): ________; trunk ports carry frames for VLAN (one/many): ________.
3. Communication between two hosts in different VLANs requires: ________.
