# PB-051 — The Resolver That Lied (L26, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L26 — Attack & Defense Case Workshop |
| CLOs | CLO3 (protocol attack mechanics), CLO6 (defense evaluation) |
| In-class slot | Workshop; 30 min, groups of 3 (paired defense-ladder discussion) |
| Case type | Attack-analysis (controlled lab) + defense design · Topic: Security / packet capture analysis |
| Evidence policy | **Isolated teaching-lab scenario** (offense simulated by the instructor's tooling; no external targets); synthetic evidence labeled; mechanism per DNS protocol realities |

---

## Student version

### Scenario (isolated lab — no external systems involved)
In the course's isolated lab, the instructor's "adversary VM" attempts to poison the
lab resolver's cache for `portal.meridian.internal` while students sniff the lab VLAN.
Afterwards, the class receives the capture summary and resolver logs:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Capture summary (lab VLAN, UDP/53):
  t0.000  client A: A? portal.meridian.internal  (txid 0x8f3a, port 51022)
  t0.001  resolver → upstream: same question (txid 0x91c2, port 40091)
  t0.018  response → resolver: portal = 10.20.40.25   (txid 0x91c2)   [legit]
  t0.019  response → resolver: portal = 10.66.6.66    (txid 0x91c2, sport 53
          → resolver's dport 40091 — guess correct!)                [forged]
Resolver logs:
  cache set: portal.meridian.internal → 10.66.6.66  (TTL 3600)
Client A (uses resolver): "page loaded" — but the TLS cert warning appeared and
  was clicked through by the tester
```

### Problem statement
Explain why the forged reply won (which fields had to match, and which did the
attacker guess?), why client A still "loaded a page", and what each rung of the
defense ladder would have prevented. Then rank the ladder rungs by effort-to-benefit
for *this* lab.

### Evidence pack
The labeled synthetic capture. Facts: forged response matched txid and port; arrived
1 ms after the legit reply; cache adopted it; the client clicked through a TLS
warning.

### Constraints
- Defense ladder must use standard, real mechanisms (source-port randomization,
  DNSSEC, encrypted transports, client pinning) — no invented protocols.
- Ranking must be justified against this lab's constraints (lab clients are Python
  scripts and browsers; instructor controls both resolvers).

### Student questions
1. Which three fields must a forged reply match to be accepted, and which one did
   the attacker have to *guess*? What made the guess easy here?
2. Client A "loaded a page" from the wrong IP — why did the experience not hard-fail?
   What saved the session from silent credential theft (and who then broke it)?
3. For each rung — (a) stronger txid+port entropy already in place but beaten, (b)
   DNSSEC validation on the resolver, (c) DoT/DoH between client and resolver, (d)
   client-side cert pinning — state precisely what it stops and what it cannot stop.
4. Rank the rungs for this lab (effort vs benefit) and defend the last-place pick.

### Expected learning outcomes
- Read a poisoning attempt from capture fields (txid/port matching).
- Explain the layered defense model against cache poisoning.
- Rank defenses under real constraints rather than abstractly.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The forged reply knew the *question* (it saw it), needed the transaction ID, and
   had to land on the right outbound port. Which of those is random per query in a
   well-configured resolver?"
2. "The page loaded — TLS *did* complain. The attack's success required a human (or a
   script with verification disabled) to step over the last guard."

### Solution
1. Match: query name/type/class (attacker saw it — sniffing), destination port
   (resolver's outbound source port), transaction ID (random 16 bits per query). The
   attacker guessed txid; the *port* was easy here because the lab resolver used a
   fixed outbound port (40091 — misconfigured; well-behaved resolvers randomize
   source ports, multiplying the guess space by ~2^16 ⚠ per implementation). Fixed
   port + 16-bit txid ⇒ expected guesses ≈ 32k, trivially spammed in the 1 ms race
   window.
2. The attacker served content from 10.66.6.66; the page rendered because the
   attacker also presented *a* certificate (self-signed for the name) — the browser
   warned, the tester clicked through; a Python client using the default TLS
   verification would have hard-failed instead. The session's credentials were
   protected by certificate validation *until a human disabled it* — the classic
   last-guard failure.
3. (a) Source-port randomization (correctly configured): raises the forge space to
   ~2^32 per query — makes off-path poisoning impractical; cannot stop an *on-path*
   sniffer who reads both fields (as in this lab). (b) DNSSEC on the resolver:
   forged answers fail validation (no valid RRSIG) — stops poisoning of *signed*
   zones regardless of on/off-path; cannot protect unsigned zones (the lab's
   `.internal` zone must actually be signed for this rung to exist ⚠ setup cost).
   (c) DoT/DoH client↔resolver: encrypts the leg — stops sniffing of queries (so
   the attacker can't learn txid/port/context); does *not* stop poisoning at the
   resolver itself (the upstream leg remains). (d) Client pinning/validation:
   converts "wrong IP" from silent compromise into loud failure — the strongest
   *harm* reducer; does not fix resolution at all (the cache is still poisoned).
4. Ranking for this lab: (1) **(b) DNSSEC** — one resolver config + a signed test
   zone; kills the attack class outright (high benefit, moderate setup once). (2)
   **(d) client validation discipline** — near-zero effort, converts the failure
   mode from catastrophic to blocked; benefit:enforcement ratio is the best in the
   room. (3) **(a) fix the resolver's port randomization** — trivial config fix, but
   only raises the bar (on-path lab adversary still wins); necessary hygiene, limited
   ceiling. (4) **(c) DoT/DoH** — most operational work (certs, client support in
   the Python scripts) for partial benefit in this threat model; defensible last
   place because (b)+(d) already block the observed kill chain.

### Reasoning process
Facts: forged reply matched name+port, guessed txid, won a 1 ms race, cache adopted,
client clicked through TLS warning. Model: poisoning = forging an acceptable reply
(field matching) + human bypassing validation. Defense ladder mapped per rung to
what it breaks in the kill chain; ranked under lab constraints.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Random txid is enough" | The lab shows it beaten via the fixed port; entropy must span the *unpredictable* fields together |
| "DoH everywhere solves DNS security" | Encrypts the client leg only; the resolver's cache and upstream leg remain attackable |
| "Blame the tester's click-through as the root cause" | It's the last guard failing, not the mechanism; defense-in-depth exists because single guards fall |
| "Block all UDP/53 at the firewall" | Breaks the resolver's upstream leg entirely; not a defense, an outage |

### Extension question
The lab's attacker moves *on-path* (MITM position instead of sniffing). Which rungs
survive, and why does DNSSEC become the *only* resolution-integrity guarantee left?
(On-path sees and races everything: (a) irrelevant (no guessing needed), (c) shifts
the attack to the resolver↔upstream leg unless the resolver's own DoT is on; DNSSEC
validation at the resolver still rejects forged data because the attacker cannot
forge RRSIGs — signing keys are the trust anchor.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Field-matching analysis exact; per-rung stop/cannot-stop precision; ranking justified against lab constraints; on-path extension reasoned |
| 3 Proficient | Kill chain correct; rungs described generically |
| 2 Developing | "DNS is insecure" without field mechanics |
| 1 Beginning | Blames the firewall |

### References
- RFC 4033–4035 (DNSSEC) ⚠ verify; RFC 8310 (DoT), RFC 8484 (DoH) ⚠
- Kaminsky 2008 cache-poisoning context (source-port randomization history) — cite
  as background ⚠ verify citation details
