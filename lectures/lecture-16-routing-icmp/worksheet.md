# Lecture 16 — Worksheet (post-midterm briefing) & Exit Ticket

Name: ________________  Date: ______

## Part A — Longest-prefix match drills (7 min)
Table: `10.0.0.0/8 → R-A` · `10.1.0.0/16 → R-B` · `10.1.2.0/24 → R-C` · `0.0.0.0/0 → R-D`
1. 10.1.2.77 → ________ 2. 10.1.9.9 → ________ 3. 10.200.1.1 → ________
4. 172.16.0.1 → ________ 5. 10.1.2.255 → ________ (think: directly connected?)

## Part B — Static routing design (LAB-07 preview, 8 min)
R1—R2—R3; nets: N1 behind R1 (10.1.0.0/24), transit 10.12.0.0/30 (R1–R2),
10.23.0.0/30 (R2–R3), N3 behind R3 (10.3.0.0/24).
6. What routes must R1 have to reach N3? (count them) ________
7. What must R3 have to reply? ________
8. R2 needs routes to ________ and ________.

## Part C — Traceroute mechanics (5 min)
9. TTL=1 packet → which device drops it, and what does it send back? ________
10. Hop 3 shows `* * *`, hop 4 answers. Two benign explanations: ________

## Exit ticket (3 items)
1. LPM = most-________-prefix wins.
2. ICMP Time Exceeded is triggered when ________.
3. Static routes are configured by ________; dynamic routes are ________.
