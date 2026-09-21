# Lecture 03 — Worksheet (GA-03) & Exit Ticket

Name: ________________  Date: ______

## Part A — Application models (5 min)
Classify: web browsing / BitTorrent swarm / WhatsApp delivery / campus file share —
client-server, P2P, or hybrid? One reason each.

## Part B — Journey ordering (GA-03b, pairs, 12 min)
Order these for a **first-visit** `https://example.com` load (number 1–8):

| # | Event | Your order |
|---|---|---|
| a | TLS ClientHello | |
| b | DNS query for example.com | |
| c | HTTP GET / | |
| d | TCP SYN | |
| e | HTTP 200 (HTML body) | |
| f | DNS answer | |
| g | TCP SYN-ACK | |
| h | TCP ACK completes handshake | |

Which steps are **skipped** on a reload with warm caches? ________

## Part C — Socket reasoning (5 min)
1. Web server (80) and dev server (8080) share one IP. Kernel receives a packet for
   IP:8080. How does it pick the right process?
2. Your program called `connect(("example.com", 80))`. What went on the wire?

## Part D — Latency budget (pairs, 6 min)
RTT = 50 ms. First visit, uncached: DNS 1 RTT + TCP 1 + TLS 1.3 1 + HTTP 1.
1. Time before HTTP request can be sent? ________
2. Same page on a 150 ms RTT mobile link? ________
3. Name one architectural fix for (2). ________

## Exit ticket (3 items)
1. Socket = ________ + ________.
2. Order: DNS / TCP handshake / TLS / HTTP GET (first visit): ________
3. One packet type you saw in the capture whose purpose you can't yet explain:
