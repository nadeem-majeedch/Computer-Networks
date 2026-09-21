# PB-049 — The Rule That Ate the Subnet (L25, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L25 — Perimeter & Internal Defenses: Firewalls, Segmentation, VPNs |
| CLOs | CLO3 (ruleset semantics), CLO6 (diagnose policy faults) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: Security and firewall reasoning |
| Evidence policy | Synthetic ruleset + symptom, labeled; first-match semantics and stateful return behavior per standard firewall models |

---

## Student version

### Scenario
A "cleanup" added one rule to the analytics-zone firewall. Within the hour, the
metrics agent (runs on every analytics host, pushes to 10.20.60.10:8443) stopped
reporting; SSH *into* the analytics hosts from the jump box kept working; SSH *out*
to GitHub for updates started failing.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (ruleset in evaluation order):**

```
Zone: analytics (10.20.30.0/24) → policies evaluated top-down, first match wins
  1  permit tcp 10.20.30.0/24 → 10.20.60.10 port 22      (host mgmt)
  2  permit tcp 10.20.30.0/24 → 10.20.60.10 port 8443    (metrics collector)  ← NEW
  3  deny   tcp 10.20.30.0/24 → any port 22              ("block SSH egress" cleanup)
  4  permit ip 10.20.30.0/24 → 10.20.60.0/24             (backend services)
  5  deny   ip any → any                                 (default)
Firewall is stateful (return traffic auto-allowed).
Jump box (10.20.60.5) → analytics hosts :22  → still works
Analytics host → 10.20.60.10:8443            → fails
Analytics host → github.com:443              → fails
Analytics host → 10.20.60.10:22 (mgmt API)   → works
```

### Problem statement
Explain each symptom with the ruleset's first-match semantics, identify the cleanup
rule's actual effect vs its intent, and rewrite the ruleset so the intent ("analytics
hosts may SSH only to the jump box") is enforced without breaking the metrics agent.

### Evidence pack
The labeled synthetic ruleset and symptom matrix. Facts: stateful firewall; order
shown; all five symptoms reproducible.

### Constraints
- Every symptom must trace to a specific rule number (or to stateful return).
- The rewrite must preserve the *stated intent* (SSH only to jump box) — not merely
  re-permit everything.

### Student questions
1. Trace "analytics → 10.20.60.10:8443" through the ruleset. Which rule fires, and
   why?
2. Trace "analytics → github.com:443". Which rule fires? (Careful: is it rule 3?)
3. Why does jump-box → analytics:22 still work? (Two mechanisms — one is rule order,
   one is statefulness.)
4. Rewrite: minimal change set that enforces the intent without collateral damage.
   State what your rule 3 becomes.

### Expected learning outcomes
- Apply first-match evaluation to a real ruleset symptom matrix.
- Distinguish destination-based egress control from direction misconceptions.
- Rewrite policy to match intent with minimal collateral.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Walk each flow top-down and stop at the first match. The *destination port* in
   rule 3 is the trap."
2. "Rule 3 denies port 22 to *any* destination — including the jump box's *return*
   path? No — statefulness handles returns. So what does rule 3 actually block?"

### Solution
1. As written, rule 2 *permits* analytics→10.20.60.10:8443 — and nothing above it
   matches — so the ruleset shown cannot produce symptom 1. **The evidence is
   internally inconsistent, and that's the lesson**: either the ruleset in the ticket
   isn't the ruleset running (the cleanup also *displaced* an old broader permit —
   e.g., an existing `permit → 10.20.60.10 any` that used to sit above rule 3 was
   replaced by the narrower 8443 rule while the deny moved up), or a second policy
   layer sits in the path (the collector host's own firewall, or the wrong zone-pair
   — analytics→mgmt vs analytics→backend naming). The next diagnostic follows
   directly: dump the *running* config and check the host firewall on 10.20.60.10.
   Reward students who catch the inconsistency above those who force a mechanism
   onto contradictory evidence.
2. github.com:443: matches no permit → falls to rule 5 default deny. Rule 3 (port
   22) is *not* what blocks HTTPS — common wrong answer; the cleanup's SSH rule is
   irrelevant to 443.
3. Jump box → analytics:22: the *inbound* direction (backend→analytics zone pair)
   isn't governed by this analytics→backend ruleset; and return traffic to the jump
   box rides the state table anyway. Two distinct mechanisms; students often
   conflate them.
4. Rewrite: replace rule 3 with a *destination-scoped* deny that matches the intent —
   e.g., `permit tcp 10.20.30.0/24 → 10.20.60.5 port 22` (jump box only) placed
   *above* a `deny tcp 10.20.30.0/24 → any port 22`. Rule 2 stays (and verify it's
   actually loaded in the right zone-pair — the symptom-1 investigation). The
   general lesson: egress intent = permit-the-allowed + deny-the-rest *scoped to the
   port/destination pair*, and test each legitimate flow after cleanup.

### Reasoning process
Facts: ruleset order, five symptoms, statefulness. Model: first-match walk-through
per flow; stateful returns exempt from explicit rules. Symptom 1's inconsistency
itself becomes the lesson: rulesets-as-documented vs rulesets-as-running, and
multi-layer policy.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Rule 3 blocks GitHub" | Rule 3 is port 22; 443 falls through to the default deny |
| "Stateful firewalls don't need outbound rules" | Statefulness handles *returns*; new outbound flows still need permits |
| "Delete rule 3" | Restores SSH egress to everywhere — violates the stated intent; scope it instead |
| Trust the ticket's ruleset blindly | Symptom 1 proves the running config differs — verify before editing |

### Extension question
Add a rule-order failure mode of your own: write a two-line ruleset where the *same
two rules in swapped order* produce opposite outcomes for one flow, and explain which
order enforces least privilege. (Classic: `deny any→any` then `permit A→B` = A→B
blocked (first-match); swapped = allowed. Least privilege = denies *after* explicit
permits, with a final deny — the deny-all must be last, not first.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Per-flow rule traces; catches symptom-1 inconsistency and names the next diagnostic; intent-preserving rewrite |
| 3 Proficient | Correct traces for 2–3; misses the inconsistency |
| 2 Developing | Attributes all symptoms to the new rule |
| 1 Beginning | Deletes rules until it works |

### References
- PD §8.4/§8.9 (firewalls, ACLs) ⚠ verify section mapping
- Kurose & Ross §8.9 (firewalls); zone-pair/stateful semantics per vendor docs ⚠
