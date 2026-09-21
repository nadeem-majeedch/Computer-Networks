# PB-031 — Which Route Wins? (L16, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L16 — Routing Fundamentals & ICMP |
| CLOs | CLO2 (forwarding model: longest-prefix match) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual trace (calculation-lite) · Topic: Routing |
| Evidence policy | Synthetic routing table, labeled; match rule per standard forwarding behavior |

---

## Student version

### Scenario
A junior admin proposes deleting "redundant" routes to "simplify" the branch router.
Before approving, you test the table by hand against five destinations.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Branch router routing table (relevant entries):
  0.0.0.0/0        via 198.51.100.1   (ISP)           metric 10
  10.20.0.0/16     via 10.100.0.1     (HQ uplink)     metric 5
  10.20.70.0/24    via 10.100.0.1     (HQ staff VLAN) metric 5
  10.20.70.0/26    via 192.0.2.9      (new micro-datacenter link) metric 5
  10.20.90.128/25  via 10.100.0.1     (HQ VoIP range) metric 5

Destinations to test:
  D1  10.20.70.10     (staff PC)
  D2  10.20.70.70     (micro-datacenter server)
  D3  10.20.90.200    (VoIP phone)
  D4  10.20.120.5     (HQ guest VLAN)
  D5  8.8.8.8         (internet)
```

### Problem statement
For each destination, pick the matching route by longest-prefix match and name the next
hop. Then evaluate the junior's deletion plan: which entries are truly redundant, and
which deletion would break a destination?

### Evidence pack
The labeled synthetic table. The rule: the *most specific* (longest) matching prefix
wins; ties broken by metric. Note the deliberate /24 vs /26 split of 10.20.70.0/24.

### Constraints
- Justify each pick by showing the matching prefixes and their lengths.
- "Redundant" must be judged per-destination, not per-entry aesthetics.

### Student questions
1. D1–D5: for each, list *all* matching table entries and the winner + next hop.
2. Which two entries overlap, and how does the router divide traffic between them?
3. The junior wants to delete "10.20.70.0/24" as a duplicate of "/16". What breaks?
4. Which entry *is* safely deletable, and what must you confirm first?

### Expected learning outcomes
- Apply longest-prefix match across overlapping prefixes.
- See how a /26 carve-out steers a subset differently from its parent /24.
- Judge route redundancy by behavior, not by appearance.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Convert each candidate IP and ask: which prefixes *contain* it? Then pick the
   longest containing one."
2. "10.20.70.0/26 covers only the first 64 addresses of the /24. Where does .70 sit?"

### Solution
1. D1 10.20.70.10: matches /16, /24, /26 (70.10 < 70.64 ⇒ inside the /26) → **/26
   wins** → 192.0.2.9. D2 10.20.70.70: matches /16, /24 (70.70 ≥ 70.64 ⇒ outside the
   /26) → **/24** → 10.100.0.1. D3 10.20.90.200: matches /16 and /25 (90.200 ≥
   90.128 ⇒ inside) → **/25** → 10.100.0.1. D4 10.20.120.5: matches /16 only → /16 →
   10.100.0.1. D5 8.8.8.8: matches only 0.0.0.0/0 → default → 198.51.100.1.
2. /24 and /26 (and /16 as their ancestor): the /26 steers 10.20.70.0–10.20.70.63 to
   the micro-datacenter link; the rest of the /24 rides the HQ uplink.
3. Deleting the /24 sends 10.20.70.64–10.20.70.254 (including D2) to the /16 — which
   has the *same* next hop here, so behavior survives... **but only accidentally**: the
   /24 exists to be more specific than a future /16-level change or a different-metric
   ancestor; deleting it couples two route policies. Verdict: not redundant *in
   intent*; today's traffic unchanged, tomorrow's refactor breaks silently. (Accept
   "traffic unchanged today" answers — reward the nuance over a flat "breaks".)
4. The /16 is safely deletable *only if* every 10.20.x destination has a more specific
   entry — false here (D4 relies on it). So: nothing is deletable without adding
   specifics; the honest answer: confirm coverage for all 10.20.0.0/16 subnets first;
   otherwise keep it. (If the instructor wants a deletable line in class, the /25 is
   removable *if* its traffic pattern matches the /16's next hop and policy — same
   accident-dependence as #3.)

### Reasoning process
Facts: five destinations, five prefixes. Model: containment test → longest prefix →
next hop; ties by metric. Redundancy judged per-destination *and* per-intent.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| First-match-in-table | Forwarding is by specificity, not listing order |
| "Shorter prefix = fallback only" | The default is the fallback; specific always beats general regardless of metric |
| 70.70 "probably also in the /26" | /26 ends at 70.63; boundary arithmetic is the whole game |
| Deleting entries that "look duplicated" | Same next hop today ≠ same policy tomorrow |

### Extension question
A sixth route appears: `10.20.70.0/26 via 10.100.0.1 metric 1`. What changes for D1 and
why does metric matter *now* but not before? (A tie in prefix length between two /26s —
metric breaks it; before, lengths differed so metric never got consulted. Teaching
point: metric is a tiebreaker within equal specificity.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All five correct with prefix-length arithmetic; overlap split explicit; deletion verdicts with intent-vs-accident nuance |
| 3 Proficient | Four correct; one boundary slip |
| 2 Developing | Picks by metric or table order |
| 1 Beginning | "The default route handles it" for everything |

### References
- PD §4.2 (forwarding tables, longest-prefix matching) ⚠ verify section
- Kurose & Ross §4.2.1 (forwarding), §5.2 context (routing algorithms)
