# Module 5 Review Questions (L21–L23)

| Field | Value |
|---|---|
| Coverage | L21 DNS · L22 DHCP deep dive & address management · L23 HTTP/2, HTTP/3, SMTP, SSH |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · LAB-12 · GA-21/22 · Cases PB-041…PB-046 |

## Questions

### L21 — DNS
1. [B|CLO4] Recursive vs iterative resolution: who does the legwork in each?
2. [I|CLO4] A client asks for `www.example.com` and the resolver's cache has the
   *authoritative* nameserver for `example.com` but not the A record. What does the
   resolver do, and what does it return?
3. [I|CLO4] TTL 300 vs 86400 on a record: state the operational trade-off each choice
   makes.
4. [I|CLO7] What does DNSSEC sign, and what class of attack does it *not* stop?

### L22 — DHCP deep dive & address management
5. [I|CLO4] Lease lifecycle: bound → renew (T1) → rebind (T2) → expire. What happens
   at each boundary if the original server is down?
6. [I|CLO4] Why does DHCP use timers as *fractions* of the lease (e.g., 50%, 87.5%)
   rather than fixed minutes?
7. [I|CLO6] A scope serves 192.168.20.10–.250 with 24 h leases and 300 devices
   arriving in a 10-minute window each morning. Diagnose and give two fixes.

### L23 — Application-layer protocols
8. [B|CLO4] HTTP/1.1's one-request-per-connection (or pipelining) limitation: name the
   head-of-line problem and what HTTP/2 multiplexing changes.
9. [I|CLO4] Why does HTTP/3 still benefit from HTTP/2's multiplexing *and* fix its
   residual stall problem? (Name the transport.)
10. [I|CLO4] SMTP dialog: state the role of MAIL FROM, RCPT TO, and DATA, and which
    party (envelope vs headers) anti-spoofing checks bind to.
11. [I|CLO4] SSH gives one channel over which many sessions run. Name the transport
    pattern this uses and one benefit.
12. [I|CLO6] A page loads 40 objects over HTTP/1.1 with per-request 50 ms RTT and no
    connection reuse. Minimum time if the browser opens 6 parallel connections?

---

## SELF-CHECK KEY — attempt first, then verify

1. Recursive: the resolver does the legwork and returns a final answer. Iterative: the
   server returns referrals; the *client* (or its resolver) chases each level.
2. Queries the authoritative nameserver directly (skipping root/TLD), gets the A/AAAA
   record with its TTL, caches it, and returns the answer to the client.
3. 300 s: fast propagation of changes, more query load (re-fetches). 86400 s: light
   load, but changes take up to a day to reach all caches.
4. DNSSEC signs DNS records (origin authenticity + integrity via signatures in the
   zone). It does not stop: the resolver lying about *existence* of unsigned zones,
   traffic interception after resolution, or the final server being malicious.
5. At T1 (50%): try renewing with the original server; at T2 (87.5%): broadcast for
   any server; at expiry: release the address, stop using it, re-enter INIT/discovery.
6. Timers must scale with lease length: a 1 h lease with a 24 h fixed renewal would
   expire first; fractional timers keep the renewal cadence proportional to risk.
7. Diagnosis: morning churn (300 × 24 h leases) exhausts a 241-address pool at login
   burst. Fixes: shorten lease time (fast recycling), enlarge the pool/scope, or
   stagger/segment scopes.
8. HTTP/1.1 serializes one request per connection (pipelining stalls on head-of-line);
   HTTP/2 multiplexes streams over one connection so requests interleave without
   waiting.
9. HTTP/3 keeps stream multiplexing but runs on QUIC/UDP, where a lost packet stalls
   only its own stream — the TCP-level head-of-line blocking disappears.
10. MAIL FROM/RCPT TO/DATA build the envelope and body; anti-spoofing (SPF) checks the
    *envelope* sender's IP authorization, DKIM signs headers/body — headers' From: is
    display identity, not necessarily the authenticated one.
11. Multiplexing over one authenticated/encrypted transport channel; benefit: one
    handshake protects all sessions and port exhaustion/firewall churn drop.
12. 40 objects ÷ 6 connections = 7 rounds × 50 ms = **350 ms** minimum [MC]
    (assumptions: no pipelining, no TLS setup amortization, one request per connection
    round).
