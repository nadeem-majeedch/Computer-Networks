# PB-042 — The Migration That Lagged for Hours (L21, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L21 — DNS: the Internet's Directory |
| CLOs | CLO5 (TTL arithmetic), CLO6 (migration planning) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Calculation + diagnostic · Topic: DNS |
| Evidence policy | Synthetic logs/records, labeled; caching semantics per DNS standard (TTL honored by resolvers) |

---

## Student version

### Scenario
Meridian moved the analytics portal to new hardware. The cutover plan said "DNS
change at 09:00, done by 09:05." At 13:00, a quarter of HQ users still hit the old
server; the rest hit the new one.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Zone record:  portal.meridian.example  A 203.0.113.77   TTL 21600  (6 h — legacy)
New record:   portal.meridian.example  A 203.0.113.90   TTL 300    (set at 09:00)
Client reports by hour (HQ, ~800 clients):
  09:00–10:00:  ~15% on old server
  11:00–12:00:  ~8% on old
  13:00:        ~4% on old (then decaying toward zero)
Resolver path: clients → internal resolver 10.20.5.53 (caching) → public DNS
The internal resolver had cached the OLD record (TTL 6 h) as recently as 08:58
```

### Problem statement
Explain the lag with TTL arithmetic (who cached what, when, and for how long), predict
when the *last* straggler clears, and produce the migration playbook that makes the
next cutover clean.

### Evidence pack
The labeled synthetic records and report curve. Facts: old TTL 6 h; change at 09:00;
decay curve consistent with expiry. Assumptions to state: resolvers honor TTLs; no
negative caching involved (A existed before and after).

### Constraints
- Arithmetic: last possible stale-cache origin = a cache fill just *before* 09:00 →
  expiry time; show it.
- The playbook must include the TTL pre-lowering step and the verification step.

### Student questions
1. A client resolver cached the old A at 08:58 with TTL 21,600 s. When does its entry
   expire? When does it *ask again*, and what will it receive?
2. Explain the decay curve shape (15% → 8% → 4%) using cache-fill timing — why is the
   tail long rather than everyone flipping at 09:05?
3. The ops team proposes "flush the internal resolver at 09:00". Which stragglers
   remain even after that flush, and why?
4. Write the three-line migration playbook (TTL step, cutover step, verification
   step) with timings.

### Expected learning outcomes
- Compute cache lifetime and re-query timing from TTL values.
- Explain population-level decay from per-client cache diversity.
- Design a migration that respects caching rather than fighting it.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "TTL is measured from when the resolver *cached* the record, not from when the
   zone changed. Find the latest-possible stale fill."
2. "Every client's recursive resolver has its own fill time. The change date doesn't
   synchronize them — each cache expires on its own schedule."

### Solution
1. Fill at 08:58 + 21,600 s = expires **14:58**. Until then the resolver serves the
   cached 203.0.113.77 without asking; at expiry the next query goes upstream and
   receives 203.0.113.90 (TTL 300).
2. Each client's resolver filled the old record at some time ≤ 08:58 (some days
   earlier, refreshed on access). Expiry = fill + 6 h → the last fillers clear last.
   The fraction-on-old at time t ≈ fraction of resolvers whose last fill was within
   (t − 6 h, 09:00) — a decaying tail as you move past 09:00, emptying by ~15:00.
   The shape is determined by *when clients last looked*, i.e., traffic patterns —
   hence the smooth decay instead of a synchronized flip.
3. Flushing the internal resolver clears *its* cache (the big one), but clients may
   run their own stub caching (OS/browser DNS caches, DoH resolvers!) that also hold
   the old record — the flush reaches only 10.20.5.53. Remaining stragglers: any
   client with an OS/browser-level cache filled before 09:00. Also: any *other*
   recursive path (VPNs, public resolvers configured on some hosts, e.g., 8.8.8.8)
   caches independently.
4. Playbook: (1) T−24 h: lower the record's TTL to 300 s (so all caches now hold
   short-TTL data; the 6 h tails from *before* still drain — that's why this is a day
   early, not an hour); (2) T=09:00: change the A record; caches expire within ≤5 min
   of their fill; (3) T+1 h: verify — query several vantage points (`dig @resolver
   portal...` + one client outside the corporate resolver), watch old-IP connections
   drop to zero on the old server's logs; keep old hardware answering (read-only) for
   the max-TTL window as the safety net.

### Reasoning process
Facts: TTLs, change time, decay curve. Model: per-cache expiry = fill-time + TTL;
population decay = superposition of independent expiries. Playbook = make TTL small
*before* the flip; verify from multiple vantage points; keep a rollback surface.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "DNS changes take up to 48 h to propagate" | Propagation is a myth: caches expire per TTL; 48 h reflects *some* people's huge TTLs, not a law |
| "Flush everything at 09:00" | You control one cache in a chain; stub/DoH caches persist |
| "Set TTL to 0 forever" | Kills legitimate caching load; TTL is a tuning knob, not an enemy |
| Blaming the 4% clients' PCs | Their resolvers simply filled late; the *plan* failed, not the clients |

### Extension question
The portal also publishes HTTPS records (SVCB) with `alpn=h2,h3`. What new TTL-
planning consideration does a *service-mode* HTTPS record introduce during migration
(vs a plain A move)? (SVCB/HTTPS records carry service parameters (ALPN, ECH, port)
cached like any RRset — parameter changes inherit the same TTL discipline; a stale
HTTPS record can leave clients attempting h3 against a server that no longer offers
it until expiry ⚠ deployment-specific — plan TTLs for *both* record types.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Fill-time arithmetic exact; decay mechanism; flush-limitation insight (stub/DoH caches); three-step playbook with verification and rollback |
| 3 Proficient | TTL math right; playbook missing the pre-lowering lead time |
| 2 Developing | "Propagation delay" as an unexplained force |
| 1 Beginning | Blames client machines |

### References
- RFC 1035 §3.2.2/§4 (TTL semantics) ⚠ verify sections; PD §2.5 (DNS caching)
- Kurose & Ross §2.4.3 (DNS records & caching)
