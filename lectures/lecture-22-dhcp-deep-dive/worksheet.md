# Lecture 22 — Worksheet (GA-22) & Exit Ticket

Name: ________________  Date: ______

## Part A — DORA dissection (pairs, 12 min)
From the live capture (filter `bootp`), fill:
1. xid: ________ 2. chaddr (client MAC): ________ 3. yiaddr offered: ________
4. giaddr: ________ (and who wrote it?) ________
5. Magic cookie value: ________
6. Option 53 in each of the four messages: ________ / ________ / ________ / ________
7. Options 1/3/6/51 values: ________ / ________ / ________ / ________
8. T1/T2 options (58/59) present? Values vs 51: ________

## Part B — Client state machine (5 min)
9. Label: INIT → ________ → ________ → BOUND → ________ → ________ → (re-INIT)

## Part C — IPAM mini-design (5 min)
Building: VLAN10 staff /24, VLAN20 students /24, VLAN30 devices /24.
10. For VLAN10: pool range, 2 reservations, exclusion %, lease time: ________
11. Conference burst (300 clients, VLAN20, event 4 h): lease you'd set + arithmetic:
    ________

## Exit ticket (3 items)
1. giaddr is written by the ________ and selects the ________.
2. Options 58/59 are ________ / ________.
3. Snooping's binding table feeds ________ and ________.
