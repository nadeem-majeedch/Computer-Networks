# Lecture 27 — Worksheet (GA-27) & Exit Ticket

Name: ________________  Date: ______  Pair: ________________

## Part A — Translation table (7 min)
1. VLAN → ________ 2. Campus router → ________ 3. Firewall policy (instance) → ________
4. Firewall policy (subnet) → ________ 5. NAT device → ________ 6. Load balancer → ________

## Part B — SG vs NACL triage (8 min)
Classify the dropping object (SG / NACL / neither):
7. Inbound 443 allowed (NACL+SG); reply dropped because egress ephemeral not
   allowed → ________
8. Instance-level rule denies 22; subnet allows → ________
9. Stateless, ordered, allow+deny, evaluated on both directions → ________

## Part C — GA-27 verification (15 min)
10. Public reach test (443) result: ________
11. Private outbound test result: ________
12. Private inbound test (expected fail) result + why: ________
13. Your SG-to-SG rules (public-web → private-app:5432): ________
14. One troubleshooting step you took when something failed: ________

## Exit ticket (3 items)
1. Private subnet's outbound path: ________
2. SG is (stateful/stateless) and (allow/allow+deny): ________
3. L7 LB adds over L4: ________
