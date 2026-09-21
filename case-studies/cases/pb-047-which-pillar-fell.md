# PB-047 — Which Pillar Fell? (L24, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L24 — Security Principles & Cryptographic Building Blocks |
| CLOs | CLO3 (CIA triad reasoning), CLO6 (control selection) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual classification · Topic: Security reasoning |
| Evidence policy | Synthetic incident summaries, labeled; each maps to one primary property plus one debatable secondary |

---

## Student version

### Scenario
Three incidents hit Meridian in one week. The ops channel wants "the security fix"
for each — but "security" isn't one thing. Your job: name what was *actually lost* in
each, then pick a proportionate control.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
I1  An intern's report with real customer emails was sent to a mailing list
    that includes a vendor partner. No alterations; recipients simply saw
    what they shouldn't.
I2  Overnight, someone re-pointed the training portal's "reset password" page
    to a look-alike page that captured credentials. Users' logins failed on
    the real site afterwards (accounts had new passwords).
I3  A disk failure destroyed 3 hours of telemetry writes; no copy existed in
    that window. Nobody unauthorized saw anything.
```

### Problem statement
For each incident: name the primary broken property (Confidentiality, Integrity, or
Availability), justify briefly, and select the *proportionate* control class (not a
product name — a class).

### Evidence pack
The labeled synthetic summaries. Facts per incident; the classification is the
reasoning task. I2 deliberately straddles two properties — that's the discussion.

### Constraints
- One primary property per incident; secondaries may be noted.
- Controls must match the property, not the loudest fear.

### Student questions
1. I1: property + why + control class.
2. I2: which property fell *first*, and which fell *as a consequence*? (Order
   matters.)
3. I3: property + why + control class. Why is encryption the wrong answer here?
4. Which incident needed *no* cryptography at all, and what does that teach about
   "add crypto" reflexes?

### Expected learning outcomes
- Apply the CIA triad to classify incidents precisely.
- Order compound incidents (primary vs consequential loss).
- Match control classes to properties, resisting one-tool reflexes.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Ask of each: was something *seen* that shouldn't be, *changed* that shouldn't
   have been, or *unavailable* that should be there?"
2. "I2 has a sequence: first the page lied, then credentials were harvested. The
   'lie' is the break-in point."

### Solution
1. I1 → **Confidentiality**: data reached unauthorized eyes; nothing altered, nothing
   lost. Control class: data-handling policy + distribution controls (labels/DLP-
   style review ⚠ class not product) — proportionate to disclosure, not tampering.
2. I2 → **Integrity first** (the reset page was falsified — users were shown content
   that lied about its origin); **confidentiality** fell as a consequence (captured
   credentials). Order matters because fixing confidentiality (password resets)
   without fixing integrity (the forged page) leaves the mechanism intact. Control
   class: authenticity/origin verification (TLS + domain hygiene; anti-phishing
   process).
3. I3 → **Availability** (data was lost; nothing seen, nothing altered). Control
   class: redundancy/backup (replication, snapshots). Encryption is the wrong tool:
   it protects against *seeing* or *altering* data — it does not prevent loss;
   encrypted-and-lost is still lost (and note: encrypted data *with no key
   escrow* can be *less* recoverable).
4. I1 and I3 need no cryptography (policy/backup). Lesson: crypto is a precision
   tool for specific properties — reflexively adding it to every incident wastes
   budget and can create new failure modes (key loss).

### Reasoning process
Facts: three incident narratives. Model: CIA as a lens — ask what was seen/changed/
lost. Compound incidents decomposed in time order. Controls chosen per property.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "I1 is a technical failure — encrypt the mail" | The data left legitimately-but-wrongly; encryption of the *channel* wouldn't stop an authorized send; classification/policy is the property match |
| "I2 is a password problem" | Resets treat the consequence; the forged page (integrity/authenticity) is the root |
| "I3 = ransomware" | No adversary present; don't import threat models the evidence doesn't show |
| One product for all three | Properties differ; one control cannot match three loss modes |

### Extension question
A fourth incident: telemetry is *believed* complete, but a week later a partner
disputes three records. Which CIA property is in question, and what control *class*
(e.g., auditability — logs, signatures, hashes) addresses disputes-after-the-fact?
(Integrity/accountability — non-repudiation flavor: hash chains or signatures give
*evidence* of integrity, distinct from prevention.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All three classified with ordered decomposition on I2; proportionate control classes; crypto-reflex lesson explicit |
| 3 Proficient | Classifications right; controls generic ("use security") |
| 2 Developing | Treats I3 as confidentiality or I2 as pure phishing |
| 1 Beginning | "Add encryption" uniformly |

### References
- PD §8.1 (security: CIA triad, threat taxonomy) ⚠ verify section mapping
- Kurose & Ross §8.1–8.2 (security principles, cryptography intro)
