# PB-030 — AAAA Exists, Path Doesn't (L15, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L15 — IPv6 |
| CLOs | CLO2 (dual-stack behavior), CLO6 (multi-cause diagnosis) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic (multi-cause, incomplete evidence) · Topic: IPv6 |
| Evidence policy | Synthetic evidence, labeled; deliberately leaves two live hypotheses; behavior per dual-stack + happy-eyeballs framing (RFC 8305) |

---

## Student version

### Scenario
Since the core switch upgrade, Meridian's intranet portal loads *slowly* for some
staff — a 5–10 s stall, then fine. Others see it instantly. The portal is dual-stack:
DNS publishes both A and AAAA records.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
DNS: portal.meridian.internal → A 10.20.40.10, AAAA 2001:db8:20:40::10   (both correct)
Slow client: ping 2001:db8:20:40::10 → works (small loss ~1%)
             ping 10.20.40.10 → works
             browser: stalls ~6 s, then loads fast
Fast client (same room): browser instant on both stacks
Core switch: recent upgrade; the IPv6 SVI/ACL set was migrated "1:1" per the
             change ticket — no ACL detail available to you (flagged ⚠)
```

### Problem statement
Explain the 6-second stall mechanically using dual-stack connection behavior; present
the two candidate root causes the evidence cannot yet separate; and design the minimal
test that discriminates between them.

### Evidence pack
The labeled synthetic evidence. Facts: both stacks ping OK; the stall is
connection-establishment-shaped; the ACL migration is unaudited. Assumptions you may
adopt (label them): browsers use a happy-eyeballs-style algorithm (address family
preference with fallback timer); "some staff" correlate with an unknown property you
must propose.

### Constraints
- The stall duration (~6 s) is evidence — your mechanism must *predict* it, not just
  tolerate it.
- Two hypotheses max; the discriminating test must be cheap (no lab rebuild).

### Student questions
1. What happens in a happy-eyeballs-style client when the preferred family's TCP SYN
   gets no reply? Connect the ~6 s to the mechanism.
2. Hypothesis A: "IPv6 path partially broken — some port range filtered." Hypothesis
   B: "DNS returns AAAA to some clients but the path is fine — something else stalls."
   Which facts support each?
3. Design the minimal discriminating test (one command on one slow client).
4. The change ticket claims "1:1 ACL migration". What question would you put to the
   network team, and why is "1:1" suspicious for dual-stack?

### Expected learning outcomes
- Reason about dual-stack connection establishment and fallback timing.
- Hold two hypotheses without premature closure; design a discriminating test.
- Treat an unverifiable change claim ("1:1") as a lead, not a fact.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Ping (ICMP) works but the *TCP* connection stalls. What differs between those two
   on an IPv6 path with an ACL problem?"
2. "Six seconds is not random. What timer in a dual-stack client does that remind you
   of?"

### Solution
1. The client tries its preferred family (AAAA) first: SYN to 2001:db8:20:40::10:443
   → no SYN-ACK (dropped somewhere). After its fallback timer (~hundreds of ms per
   attempt; total stall ≈ several seconds with retries ⚠ exact timer per
   implementation, but multi-second stalls are the classic symptom), it attempts the
   A record and connects instantly. ICMP working + TCP stalling = **stateful/policy
   filtering on TCP**, not "no IPv6 at all". The ~6 s ≈ sum of SYN retries before the
   client gives up on v6 — the signature shape.
2. A supported by: v6 ICMP OK, TCP stall, post-upgrade timing, ACLs migrated — a
   missed TCP permit (e.g., only ICMP + a subset of ports carried over) fits all
   facts. B supported by: fast clients exist (so the *server* serves v6 fine) — but B
   in this form (DNS variance) predicts instant fallback (usually <1 s) or different
   stall per resolver; the 6 s uniform stall fits A better. Honest reading: evidence
   favors A; B remains until a test runs (e.g., a broken PMTUD path or an MTU black
   hole could *also* produce "connects then stalls" — note that shape differs: connect
   succeeds; here connect stalls).
3. Minimal test on one slow client: attempt TCP directly against the AAAA:
   `curl -6 -m 20 -v https://portal.meridian.internal` (or `Test-NetConnection
   portal.meridian.internal -Port 443` on Windows) and time it; then the same with
   `-4`. Discriminator: v6 TCP times out while v4 connects ⇒ A confirmed at the TCP
   layer; then narrow with a port sweep (443 vs 80 vs 8443) — a *partial* port filter
   shows as some ports timing out.
4. Ask: "Show me the IPv6 ACL *and its hit counters* next to the v4 one" — 1:1 is
   suspicious because v4/v6 ACL syntax, object groups, and any any/established
   semantics differ subtly; a silent mismatch (missing permit, wrong zone) is the
   classic migration bug. Counters make the claim auditable instead of asserted.

### Reasoning process
Facts: both stacks ping, TCP stalls only on v6, ~6 s uniform, correlation with some
staff (hypothesized: those with v6-preferring resolvers/stacks), post-change timing.
Model: happy-eyeballs fallback ⇒ family-specific TCP filtering explains shape+duration;
discriminate with a direct v6 TCP test + port sweep. Claim "1:1" treated as lead.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Disable IPv6" | Hides the fault; loses the diagnostic; next app that prefers v6 breaks differently |
| "DNS is wrong" | Both records correct; stall is at TCP, not resolution (and resolution errors don't produce 6 s stalls) |
| "Server is overloaded" | Fast clients disprove; load doesn't correlate with address family |
| Accepting "1:1 migrated" | Unverified change claims are leads, not facts; counters were the missing receipt |

### Extension question
Suppose the discriminating test shows v6 TCP *connects* but large responses stall
(small pages load, big ones hang at ~1.4 KB). What class of fault is that, and which
dual-stack knob is implicated? (MTU black hole on the v6 path — PMTUD failure; knobs:
host/router MTU, MSS clamping, filtering of ICMPv6 Packet Too Big. The *shape* —
connects-then-stalls vs stalls-to-connect — is the diagnostic fork; teach students to
read it.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Fallback mechanism + 6 s prediction; both hypotheses with fact-mapping; discriminating test concrete; auditable-ACL question |
| 3 Proficient | Correct primary diagnosis; test less discriminating |
| 2 Developing | "IPv6 broken" without TCP/ICMP distinction |
| 1 Beginning | Turns off IPv6 |

### References
- RFC 8305 (Happy Eyeballs v2) — fallback framing
- PD §4.3 (IPv6), §5.6 context (ICMPv6/PMTUD) ⚠ verify section mapping
