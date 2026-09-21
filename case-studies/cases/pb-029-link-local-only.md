# PB-029 — Fe80 and Nothing Else (L15, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L15 — IPv6 |
| CLOs | CLO2 (address types; SLAAC/RA role) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: IPv6 |
| Evidence policy | Synthetic outputs, labeled; RA/SLAAC semantics per RFC 4861 |

---

## Student version

### Scenario
A lab host shows an IPv6 address — but only one. IPv4 works fine on the same network
(which has IPv6 routers elsewhere in the building). The instructor says "the network
serves RAs"; this host disagrees.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Host addresses:
  IPv6: fe80::21a:2bff:fe33:4411/64   (and no other IPv6 address)
  IPv4: 10.20.30.87/24 (gateway 10.20.30.1) — healthy
Neighbor host (same switch, works): 2001:db8:20:30::a1/64  (GUA via SLAAC)
                                     + fe80::... (link-local, normal)
Packet check (instructor-provided capture on the same port):
  IPv4 DHCP: DISCOVER → OFFER → REQUEST → ACK      (normal)
  IPv6:      RS sent by host at t=0 …              no RA observed in 60 s
```

### Problem statement
Identify the missing ingredient for global IPv6 connectivity, explain how the working
neighbor got its GUA, and name the two most likely failure points (with the evidence
that separates them).

### Evidence pack
The labeled synthetic outputs. Facts: link-local present (L2 fine); no RA on the wire
for this host; neighbor has a GUA. Everything else is reasoning.

### Constraints
- Explain what each address type provides (fe80 vs 2001:db8::/32 example) before
  diagnosing.
- Two failure hypotheses maximum; each with a discriminating check.

### Student questions
1. What is fe80::/10 for, and why does having it prove *nothing* about internet
   reachability?
2. How did the neighbor host build its 2001:db8:20:30::a1 address (name the mechanism
   and the router's role)?
3. The capture shows RS but no RA. What is the *router side* of this exchange supposed
   to be?
4. Name the two most likely failure points and one check for each.

### Expected learning outcomes
- Distinguish link-local vs global unicast addressing and their roles.
- Explain RS/RA and SLAAC prefix assignment.
- Localize a "no GUA" symptom to router vs host causes with evidence.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "fe80 is self-generated for the *link*. Which message is supposed to hand the host
   a *routable* prefix?"
2. "The neighbor works — so *a* router is speaking somewhere. Is it speaking on this
   port?"

### Solution
1. fe80::/10 is link-local: self-derived (usually EUI-64/randomized) per interface,
   used for on-link neighbor discovery/RA exchange itself. It is never routed; it
   proves L2 is up and IPv6 stacks run — nothing about global reachability.
2. SLAAC: the host sends a Router Solicitation; a router answers with a Router
   Advertisement carrying the on-link prefix (e.g., 2001:db8:20:30::/64) and flags;
   the host combines prefix + interface identifier into its GUA, installs a default
   route from the RA source, and may run DAD. (DHCPv6 possible too — but the
   neighbor's address pattern (2001:db8:20:30::a1 — low, static-looking) could be
   either; state the ambiguity honestly ⚠.)
3. Router side: respond to RS with an RA (periodically, too — unsolicited RAs every
   few hundred seconds ⚠ per RFC 4861 defaults). No RA in 60 s = the prefix-serving
   step never happened for this host.
4. Failure points: (a) *this host/port* doesn't receive RAs — e.g., RA guard on the
   port, multicast filtering issue; check: capture the *neighbor's* port (does it see
   RAs? if yes, the network speaks RAs — then why not here?) and compare switch-port
   configs (RA guard/port ACL on this port?). (b) *host* ignores/filters ICMPv6 or
   RS goes out a different VLAN — check: host firewall rules, and whether the RS
   actually left (capture shows it did ⇒ host-side sending fine; so suspicion shifts
   to inbound RA path/port policy). The capture already separates them: RS sent ✓,
   RA absent ⇒ inbound path/port/router targeted to this port.

### Reasoning process
Facts: LLA present, no GUA, RS out, no RA in, neighbor GUA works. Model: GUA via
SLAAC needs RA (or DHCPv6); RA absent on this port = the discriminating evidence.
Hypotheses: port-level RA suppression vs host-side filtering; the existing capture
already favors the former.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "IPv6 is down on the host" | Stack runs — it built fe80 and sent RS |
| "The network has no IPv6" | Neighbor has a GUA on the same switch |
| "Add a static 2001:db8 address" | Masks the missing RA; wrong prefix policy, no default route, breaks again on the next host |
| "DHCP is broken" | IPv4 DHCP works; and SLAAC doesn't use DHCP for the address itself |

### Extension question
The instructor mentions "RA guard". Explain, in this incident's terms, what RA guard
is *for* when used correctly — and what misconfiguration of it looks like. (Correct:
prevents *rogue* RAs on access ports while allowing them from the uplink. Misconfigured
here: guard applied to the wrong port class — the access port swallowing legitimate
RAs. One policy switch, opposite effects.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | fe80 semantics precise; SLAAC/RA walk-through; both hypotheses with discriminating checks; capture evidence used to bias correctly |
| 3 Proficient | Correct mechanism and cause; checks generic |
| 2 Developing | "No IPv6 address" conflated with "no connectivity" |
| 1 Beginning | Sets a static IPv6 address |

### References
- RFC 4861 (ND: RS/RA), RFC 4862 (SLAAC) — behavior cited in lecture
- PD §4.3 (IPv6 addressing/format) ⚠ verify section mapping
