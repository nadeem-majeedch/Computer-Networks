# Weekly Quiz — Week 11 (L21, L22)

| Field | Value |
|---|---|
| Coverage | L21 — DNS · L22 — DHCP deep dive & address management |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO4|L21]** Give the DNS record type for: (i) name → IPv4, (ii) name → IPv6,
(iii) mail routing, (iv) name → name.

**Q2 [I|CLO4|L21]** A recursive resolver receives a query for `cs.example.edu` with an
empty cache. Order the queries it makes, starting at a root server, and state what each
answer returns.

**Q3 [I|CLO4|L21]** What does the TTL field in a DNS record control, and what breaks
operationally if it is set very high (e.g., 7 days) before a planned server move?

**Q4 [I|CLO4|L22]** After DHCP lease expiry without renewal, what does the client do,
and what must the server eventually be able to do with the old address?

**Q5 [I|CLO6|L22]** A DHCP server hands addresses from 10.5.0.10–10.5.0.200. Staff
complain of intermittent failures at 09:00. Name the capacity concept (per L22) and one
mitigation.

**Q6 [I|CLO7|L21]** Why does the course treat "trust the resolver's answer" as a
security question, and name one standard mitigation family.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** (i) A · (ii) AAAA · (iii) MX · (iv) CNAME. [B·CLO4]

**Q2.** Root → referral to the `.edu` TLD servers; `.edu` → referral to `example.edu`
nameservers; `example.edu` → authoritative answer for `cs.example.edu` (with TTL).
Accept "TLD → authoritative" ordering with correct referral semantics. [I·CLO4]

**Q3.** TTL bounds how long resolvers may cache the record. A 7-day TTL means caches
worldwide can serve the old address for up to a week after you switch DNS — clients
keep hitting the dead server. Standard practice: lower TTL *ahead* of a planned move. [I·CLO4]

**Q4.** The client stops using the address and must re-run discovery (may self-assign
link-local per stack policy). The server must be able to **reuse** the address for
another client after expiry — which is why lease *duration* trades pool size against
churn. [I·CLO4]

**Q5.** Pool exhaustion / churn spike at login hour: 191 addresses for a burst of
requests (plus short default leases multiplying renewals) → some Discovers go
unserved. Mitigations: lengthen lease time, enlarge pool/subnet, add a relay-served
scope, or stagger logins. [I·CLO6]

**Q6.** A compromised/misconfigured resolver can return attacker-chosen addresses
(caching lies), redirecting users; mitigation family: DNSSEC (cryptographic origin
authentication of records) — also accept validating resolvers/DoT/DoH as transport
hardening with correct reasoning. [I·CLO7]
