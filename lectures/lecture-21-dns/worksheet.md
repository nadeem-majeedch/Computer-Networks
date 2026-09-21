# Lecture 21 — Worksheet (GA-21) & Exit Ticket

Name: ________________  Date: ______

## Part A — dig drills (pairs, 12 min)
1. `dig +short example.com` → ________
2. `dig +short MX gmail.com` → ________ (highest-priority first? note the number) ________
3. `dig +trace www.wikipedia.org`: list the referral chain (root/TLD/auth):
   ________ → ________ → ________
4. `dig -x 8.8.8.8` returns a ________ record for ________

## Part B — Capture the walk (pairs, 10 min)
5. Flush local caches, capture, resolve a fresh domain. How many UDP/53 exchanges
   visible? ________
6. Mark which message was the referral from the TLD: frame # ________
7. Warm cache repeat: how many exchanges now? ________

## Part C — Reasoning (8 min)
8. TTL 300 s, site failover between DCs: worst-case staleness? ________
9. A friend resolves the domain; your resolver says NXDOMAIN. Two hypotheses: ________
10. Why do DNSSEC-signed responses sometimes arrive over TCP? ________

## Exit ticket (3 items)
1. The walk: stub → ________ → (iterative) root/TLD/________
2. CNAME = ________; MX = ________
3. DNSSEC gives ________, not ________.
