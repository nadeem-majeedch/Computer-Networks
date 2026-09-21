# PB-024 — Two Machines, One Identity (L12, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L12 — IP Fundamentals & ARP |
| CLOs | CLO2 (ARP semantics), CLO6 (evidence-based diagnosis) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic (packet/ARP reasoning) · Topic: ARP |
| Evidence policy | Synthetic ARP tables/logs, labeled; "last reply wins" semantics per ARP behavior |

---

## Student version

### Scenario
The analytics file server (10.20.30.40) becomes unreachable "randomly" — often after a
particular student powers on a dual-boot lab machine in the same room. A witness
captured ARP activity on a third machine:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
ARP cache on witness (10.20.30.55), sampled over 4 minutes:
  10.20.30.40 → MAC 02:11:32:aa:00:01  (server NIC)
  10.20.30.40 → MAC 02:11:32:de:ad:07  (the lab machine — 90 s later)
  10.20.30.40 → MAC 02:11:32:aa:00:01  (again, 2 min later)
Witness log: "10.20.30.40 is at ..." replies from BOTH MACs after a single request
Server logs: clean; no reboots
Both machines' configs:
  server:  10.20.30.40/24  (static)
  lab pc:  10.20.30.40/24  (static — "copied the settings from the server sheet")
```

### Problem statement
Diagnose the fault, explain the ARP flip-flop mechanism reply-by-reply, and predict the
symptom pattern's timing (why "random", why the lab machine's presence matters).

### Evidence pack
The labeled synthetic evidence. Facts: two MACs answer for one IP; both are static
configs. Assumption (label it): both stacks answer ARP freely — standard behavior.

### Constraints
- Explain *why both reply* and *why the cache alternates* (ARP has no authentication
  and accepts the last reply).
- Symptom pattern must follow from the mechanism, not from vibes.

### Student questions
1. What protocol rule makes both machines answer an ARP request for 10.20.30.40?
2. Walk through one flip-flop: request → two replies → which entry wins on the witness?
   What determines traffic delivery at that instant?
3. Why do symptoms look "random" to users, and why does the lab machine's schedule
   correlate?
4. Fixes: two, at different levels (config hygiene vs protocol-level protection). Which
   stops recurrence, and which detects it fast next time?

### Expected learning outcomes
- Explain ARP reply semantics and cache-update rules without authentication.
- Diagnose duplicate-IP conflicts from cache flip-flops.
- Separate immediate fix from durable prevention/detection.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "ARP requests ask 'who has this IP?'. Which machines believe they have it?"
2. "The cache isn't lying — it's faithfully recording whichever reply arrived last."

### Solution
1. Both machines are configured with 10.20.30.40/24. An ARP request broadcast to the
   segment is answered by *every* host that holds the IP — two do, so two replies
   (each to the requester, unicast) come back.
2. The witness updates/refreshes its entry for each reply as it arrives ("last reply
   wins"); the winner's MAC is used for the next outgoing frame. If the lab machine's
   reply arrives last, the file server's traffic is delivered to the lab machine —
   which typically drops it (no service listening) → "server unreachable". When the
   server's reply lands last (or the entry re-resolves), everything works again.
3. Deterministic per-packet, but *random to users*: resolution order depends on reply
   arrival timing, cache ages (entries expire and re-resolve), and which hosts are
   actively sending. The lab machine's presence is the trigger — while it is on, both
   hosts contest; powered off, only the server answers. Hence "after the lab machine
   boots" correlation.
4. Immediate: correct the lab machine's address (config hygiene — removes the second
   claimant). Durable: address-assignment discipline (IPAM/documented static ranges;
   DHCP for everything that isn't documented-static; conflict detection on hosts ⚠
   behavior varies by OS). Detection: DHCP servers and some stacks log duplicate-
   address conflicts; a monitoring check can ARP for the server IP from two vantage
   points and alarm on disagreement. Which stops recurrence: hygiene; which detects
   fast: monitoring.

### Reasoning process
Facts: two MACs answer one IP; both static; symptoms intermittent; lab machine boots
correlate. Model: ARP is trust-all, last-reply-wins; two claimants → per-resolution
coin flip → user-visible flapping. Cause chain complete without unverified assumptions.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The switch is corrupting tables" | Switches don't map IPs at all — this is L3/ARP state on hosts |
| "The server ARP cache is stale" | The *witness* cache flips; the server is a passive claimant |
| "Reboot the server" | The lab machine still claims the IP; conflict resumes on next boot |
| "It's DNS" | No names involved; raw IP access also fails |

### Extension question
A security engineer notes this *exact* mechanism is also an attack (ARP spoofing).
What one difference in the evidence distinguishes the accident from the attack here,
and what control mitigates the attack version? (Accident: both claimants are known,
legitimate machines; the lab PC's config *says* the IP. Attack: a third MAC with no
config change, often answering aggressively/gratuitously. Mitigation class: Dynamic
ARP Inspection / port security with trusted bindings ⚠ switch-feature dependent.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Reply semantics + last-wins precise; flapping mechanism tied to symptom timing; fix/detect split; attack variant noted |
| 3 Proficient | Correct diagnosis and mechanism; timing explanation partial |
| 2 Developing | "IP conflict" named; ARP mechanics absent |
| 1 Beginning | Reboots server |

### References
- PD §5.4.1 / ARP section (ARP operation) ⚠ verify section number per edition
- Kurose & Ross §6.4.1 (ARP); RFC 826 (ARP) for reply/cache semantics
