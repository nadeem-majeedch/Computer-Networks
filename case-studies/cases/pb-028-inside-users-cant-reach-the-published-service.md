# PB-028 — The Service That Works Outside but Not Inside (L14, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L14 — IP Addressing at Scale: DHCP & NAT |
| CLOs | CLO2 (NAT translation semantics), CLO6 (diagnose asymmetric path behavior) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: NAT |
| Evidence policy | Synthetic evidence, labeled; NAT behaviors per standard many-to-one model, hairpin support flagged as implementation-dependent |

---

## Student version

### Scenario
Meridian publishes its analytics dashboard on the internet: `meridian-dash.example.net`
→ public IP 203.0.113.10, port-forwarded by the edge router to internal
10.20.40.25:8080. External users are fine. Internal users who type the public name get
a timeout — every time. Using the internal name (`10.20.40.25:8080`) works.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
DNS: meridian-dash.example.net → 203.0.113.10 (public, correct)
External test (phone on LTE): https://meridian-dash.example.net works, 200 OK
Internal test (office LAN):   same URL → TCP connect timeout (~21 s)
Internal test (direct IP):    http://10.20.40.25:8080 works, 200 OK
Edge router:                  port-forward 203.0.113.10:443 → 10.20.40.25:8080
                              (NAT table shows the rule; no hairpin/NAT-reflection
                               feature enabled)
```

### Problem statement
Explain the packet flow for a working external connection, show precisely where the
internal connection dies, and present at least two fixes with trade-offs.

### Evidence pack
The labeled synthetic evidence. Fact: the router has no hairpin-NAT feature enabled.
Assumption to label: egress firewall permits internal→internet generally (other sites
load fine).

### Constraints
- Trace *packets*, not feature names: the death point must be mechanical.
- Fixes must each state a trade-off (no free options).

### Student questions
1. Trace one external request: destination IP at each hop, and what the NAT table does.
2. Trace the internal request that uses the public IP: what does the edge router do
   when the SYN arrives from *inside* toward 203.0.113.10:443?
3. Why does the direct-IP test work? What does that isolate the problem to?
4. Give two fixes with one trade-off each (e.g., split-horizon DNS vs enabling NAT
   reflection vs routed public space).

### Expected learning outcomes
- Explain NAT translation as a table rewrite on the *path*.
- Diagnose hairpin (NAT loopback) failure mechanically.
- Evaluate standard mitigations with trade-offs.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Outside→in works because the router rewrites the destination. Inside→public: what
   path does that SYN take?"
2. "The router *is* 203.0.113.10's owner. A SYN from inside arrives addressed to its
   own public IP — but hairpin isn't enabled. Draw the two arrows."

### Solution
1. External: SYN dst 203.0.113.10:443 → edge router rewrites dst to 10.20.40.25:8080
   (table entry created for the reply mapping) → server → reply to router (src
   rewritten back to 203.0.113.10) → client. Works because every packet *crosses* the
   router.
2. Internal SYN dst 203.0.113.10:443: routed toward the edge router (default route).
   The router must translate inbound *and* route the translated packet back out the
   same internal interface (hairpin/loopback) — with hairpin disabled, the router
   drops/refuses the flow (behavior varies by vendor ⚠ — commonly a silent drop, hence
   the ~21 s client timeout with retries). No translation entry is usable because the
   reply would need to be NATed twice in opposite directions on one interface.
3. Direct IP works because traffic stays inside the LAN: no NAT involved — 10.20.40.25
   is reachable by normal routing. This isolates the failure to the *NAT/edge path*,
   not the service, not DNS, not the server.
4. Fixes: (a) **Split-horizon DNS** — internal DNS returns 10.20.40.25 for the same
   name; trade-off: DNS infrastructure change, name-based TLS still fine, but clients
   on VPN/other segments need the view too. (b) **Enable NAT reflection/hairpin** on
   the router; trade-off: vendor-dependent feature ⚠, adds asymmetric flows (all
   internal traffic hairpins through the edge router = wasted bandwidth, plus router
   CPU). (c) True fix at scale: give the service real internal+public addressing
   (routed public space or a reverse proxy that serves both faces); trade-off:
   architecture change, IPv4 scarcity cost.

### Reasoning process
Facts: external OK, public-name internal timeout, direct-IP OK, no hairpin. Model: NAT
rewrite requires router traversal; hairpin = same-interface loop; without it, flow
drops. Isolate via the direct-IP control test. Mitigations: change *name resolution*
(a), change *router behavior* (b), change *addressing architecture* (c).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "DNS is broken" | DNS resolves correctly (external proof); resolution isn't the failure |
| "Firewall blocks port 8080" | Direct-IP test on 8080 succeeds internally |
| "The server refuses internal clients" | It serves 200 OK to direct-IP requests |
| "Add a port-forward for the internal interface" | The rule exists for the public face; the missing piece is the *loop path*, not another forward |

### Extension question
Why do some vendors warn that NAT reflection breaks symmetric applications or loops?
Sketch the packet flow that goes wrong when the *server itself* tries to call back to
the client's public-looking address. (Server replies to the reflected source; the
return path re-enters NAT from inside again — reflection of reflection; symmetric NAT
mappings and connection tracking can mismatch ⚠ vendor-specific — discuss conceptually
only.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both traces mechanical; hairpin death point precise; three fixes with trade-offs; control-test logic explicit |
| 3 Proficient | Correct diagnosis + two fixes; one trade-off vague |
| 2 Developing | Blames DNS or firewall without the packet path |
| 1 Beginning | "Use the internal IP" (workaround, no mechanism) |

### References
- PD §4.3.3 (NAT), §4.3.4 context (NAT traversal) ⚠ verify section mapping
- Kurose & Ross §4.3.4 (NAT); RFC 4787 (NAT behavioral requirements) for hairpin
  discussion
