# Lecture 14 — Worksheet & Exit Ticket

Name: ________________  Date: ______

## Part A — DORA mechanics (7 min)
1. Order and broadcast/unicast-ness: Discover ________ / Offer ________ /
   Request ________ / Ack ________
2. The client's source IP during Discover: ________; destination: ________
3. Which option number is the message type? ________ The router (gateway) option? ________

## Part B — Lease lifecycle (5 min)
4. Lease 8 hours: renewal (T1) at hour ________ via ________ (broadcast/unicast);
   rebinding (T2) at hour ________ via ________.
5. What must the client do if no Ack arrives by expiry? ________

## Part C — NAT table completion (pairs, 10 min)
Inside host 192.168.50.20; NAT public IP 203.0.113.7.

| # | Inside packet | NAT table entry | Public packet | Return mapping |
|---|---|---|---|---|
| 1 | 192.168.50.20:51000 → 1.2.3.4:443 | | 203.0.113.7:____ → 1.2.3.4:443 | |
| 2 | 192.168.50.21:51000 → 1.2.3.4:443 | | | |
| 3 | 192.168.50.20:51001 → 5.6.7.8:80 | | | |

6. Why must entries 1 and 2 use *different* public ports? ________

## Part D — Consequences (5 min)
7. Two NAT consequences that break applications: ________ / ________
8. "NAT is a firewall" — correct this statement in one sentence. ________

## Exit ticket (3 items)
1. DORA: ________
2. T1 renewal happens at ________ of the lease.
3. NAT's real resource is the ________, not the address.
