# Lecture 25 — Worksheet & Exit Ticket

Name: ________________  Date: ______

## Part A — Firewall classes (8 min)
1. Stateless filter's blind spot (the FTP problem): ________
2. Stateful fix (mechanism name): ________
3. One thing NGFW sees that stateful can't: ________ ; one thing it still can't: ________

## Part B — Policy design (12 min)
Meridian zones: STAFF / GUEST / DMZ / OUTSIDE. Write allow rules (one line each +
a justification clause):
4. Public HTTPS to the web server: ________
5. Staff → internal file share: ________
6. Guest → anything internal: ________
7. Diagnostics without discovery: ________
8. The default: ________ (+ why log it?)

## Part C — Tunnel math (5 min)
9. Outer overhead 80 B on 1500-MTU path → inner payload ________ B
10. MSS clamp you'd set (safety margin): ________ ; why throughput dips ~5%: ________

## Exit ticket (3 items)
1. Default-drop = ________ by default, ________ by exception.
2. Stateful firewalls auto-allow ________.
3. A VPN gives path ________ and network ________, not endpoint ________.
