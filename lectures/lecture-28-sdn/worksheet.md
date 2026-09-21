# Lecture 28 — Worksheet (GA-28) & Exit Ticket

Name: ________________  Date: ______  Pair: ________________

## Part A — Planes sort (in notes) — quick check
1. "OSPF picks a new path after a link fails" — plane: ________
2. "Operator sets VLAN policy for the building" — plane: ________
3. "Switch forwards a frame out port 3" — plane: ________

## Part B — GA-28 rules (25 min)
Goal 1 — reachability: write the rule(s) so H1→H2 works on the trace:
```text
(match)  in_port=1 eth_type=ip ip_src=10.1.0.1 ip_dst=10.1.0.2
(action) ________
```
4. Goal 2 — block H2's HTTP (tcp_dst=80), pass everything else (two rules, in
   priority order):
   - Rule A (priority ___): match ________ action ________
   - Rule B (priority ___): match ________ action ________
5. Goal 3 — mirror H1→H2 traffic to monitoring port: action additions: ________
6. Goal 4 — after H2's IP changes, which rule(s) break and why? ________

## Exit ticket (3 items)
1. The plane that "tells the worker the rules": ________
2. Reactive installation installs on ________; the rest of the flow follows
   ________.
3. One property where distributed routing still wins: ________
