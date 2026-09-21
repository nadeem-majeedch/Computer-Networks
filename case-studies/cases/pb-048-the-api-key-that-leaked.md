# PB-048 — The API Key That Leaked (L24, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L24 — Security Principles & Cryptographic Building Blocks |
| CLOs | CLO3 (least privilege, credential design), CLO6 (trade-off evaluation) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Design/trade-off · Topic: Security reasoning |
| Evidence policy | Synthetic incident + design options, labeled; every consequence derivable from the credential model |

---

## Student version

### Scenario
A dataset-pipeline service authenticates to the analytics API with **one shared API
key**, embedded in the pipeline config and reused by every job. This week, a public
repository briefly contained a build log that printed the key. The key is valid for
"the pipeline" — which can read *every* dataset and delete *any* file.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Credential:     one static key, all pipeline jobs, full read+delete scope
Leak window:    the build log was public for 6 days before removal
Usage logs:     no anomalous calls detected *so far* (log retention: 7 days)
Options on the table:
  A) Keep one key; rotate it now and every 90 days; monitor harder
  B) Per-job credentials (each job gets its own key, least-privilege scopes)
  C) Short-lived tokens issued per run (minutes-to-hours TTL), no static secret
  D) mTLS client certificates per job
Constraints:  14 pipeline jobs; CI system rotates configs on deploy; the API
              supports per-credential scopes, TTLs, and mTLS (all four options
              implementable)
```

### Problem statement
Evaluate options A–D against the *properties that failed* (compromise blast radius,
detection, revocation), pick a primary design (with one hybrid allowed), and write
the incident-response sequence for the *current* leak (today's actions, in order).

### Evidence pack
The labeled synthetic facts. The 6-day leak window and 7-day log retention are the
detection problem; the full-scope key is the blast-radius problem. Both must be
addressed.

### Constraints
- Every option needs: blast radius if leaked, revocation story, operational cost.
- The IR sequence must be ordered by *risk-reduction per hour*, not by ease.
- Least privilege must be explicit: what can each credential do after your design?

### Student questions
1. What is the blast radius of the *current* design during the 6-day window? Name
   three concrete harms possible with this scope.
2. Option A's rotation cadence: why does 90-day rotation *not* solve this incident
   class? (What does it limit, and what doesn't it?)
3. Compare B, C, D on: revocation speed, per-leak blast radius, operational cost.
   One sentence each — no product evangelism.
4. Your pick (one primary + allowed hybrid) and the ordered IR sequence for today.

### Expected learning outcomes
- Reason about credentials via blast radius, detection, and revocation.
- Distinguish rotation cadence from scope reduction.
- Sequence incident response by risk reduction.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The leaked credential can read everything and delete anything. What is the
   *ceiling* of harm while it lives — and how long did it live?"
2. "Rotation changes *when* a leaked key dies. Scope changes *what it can do* while
   alive. Those are different axes — the incident had failures on both."

### Solution
1. Blast radius during 6 days: (a) exfiltrate every dataset (confidentiality), (b)
   delete/corrupt any file (integrity — including backups if same credential), (c)
   write as the pipeline (attribution poisoning — forged telemetry looks legitimate).
   All three were *possible* for 144 hours; detection (log-based) covers only the
   last 7 days — the incident may never be provably resolved.
2. A's 90-day rotation limits a leaked key's *lifetime* (≤90 days), not its *power*
   (still read-all/delete-all while valid) and not the *window before discovery*
   (could leak on day 89). It's a mitigation for persistence, not a fix for scope;
   and 6-day public exposure shows detection lag dominates any cadence.
3. **B (per-job keys)**: revocation = disable one key (fast, surgical); blast radius
   = that job's scope (small if least-privilege); cost = credential lifecycle × 14
   jobs (config plumbing, rotation bookkeeping). **C (short-lived tokens)**: blast
   radius = job scope × minutes (tiny); revocation mostly unnecessary (expiry);
   cost = an issuing service + per-run plumbing — the strongest detection/revocation
   story, moderate ops cost. **D (mTLS certs)**: cryptographic client identity,
   strong mutual auth and revocation via CRL/OCSP ⚠ (infra-dependent); cost = PKI
   operations — heavy for this team size; overkill unless jobs live in untrusted
   networks.
4. Pick: **B as primary with C for the two highest-risk jobs** (the delete-capable
   pipeline) — or pure C if the issuing service is a week's work. IR sequence
   (risk-per-hour): (1) **revoke the leaked key now** (kills the 6-day ceiling) —
   deploy B-style scoped keys immediately after; (2) **audit logs for the leak
   window** + extend retention before it lapses (the 7-day horizon is about to
   erase evidence); (3) **rotate secrets in config/CI** (the old key may be cached
   in more build logs); (4) scope-reduction rollout; (5) post-mortem: forbid secret
   printing in build logs (the *vector*).

### Reasoning process
Facts: shared full-scope key, 6-day exposure, 7-day logs, four implementable
options. Model: credential risk = scope × lifetime × detection lag. Compare options
on those axes; sequence IR by marginal risk reduction. Hybrid allowed where jobs
differ in risk.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Rotate and move on" (A as full answer) | Leaves read-all/delete-all scope; next leak has the same ceiling |
| "Revoke and rotate, skip the log audit" | Destroys the only evidence trail before its natural expiry; you'll never know what happened |
| "mTLS everywhere" (D by default) | PKI cost without a threat model needing it; B/C achieve the risk reduction cheaper here |
| "Least privilege later, after the rewrite" | Scope is the *first* axis to fix — it needs config, not code |

### Extension question
The API team proposes *signed requests* (HMAC over method+path+body with a per-job
secret) instead of bearer keys. What does signing add (replay/protection scope ⚠)
and what does it *not* change about this incident? (Adds request-integrity/replay
binding ⚠ details per scheme; does not change blast radius of a *leaked secret* —
the HMAC key is equally leakable; scope/rotation/short-TTL reasoning is unchanged.
Crypto upgrades the channel, not the authorization model.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Three harms named; rotation-vs-scope distinction crisp; B/C/D on all three axes; ordered IR with retention-timer insight |
| 3 Proficient | Correct pick; axes partially compared; IR unordered |
| 2 Developing | "Rotate the key" as the plan |
| 1 Beginning | Ignores the leak; adds monitoring |

### References
- PD §8.2 (authentication/integrity building blocks) ⚠ verify section mapping
- Kurose & Ross §8.3–8.4 (authentication, integrity) context; NIST SP 800-207
  (zero-trust/least-privilege framing) ⚠
