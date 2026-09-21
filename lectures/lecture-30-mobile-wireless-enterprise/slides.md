# Lecture 30 — Mobile & Wireless Enterprise Networking — Slide Deck

| Field | Value |
|---|---|
| Slides | 17 (120 min: 10 open · 55 teach · 5 break · 40 case drill · 10 wrap) |
| Companions | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) · case bank PB-059…PB-061 |
| Style | [Course deck conventions](../../lectures/README.md#deck-conventions) |

## Deck outline

| # | Slide | # | Slide |
|---|---|---|---|
| 1 | Title | 10 | Cellular in one slide |
| 2 | Hook: the call that never dropped | 11 | Worked example: link budget |
| 3 | Enterprise WLAN = capacity design | 12 | The multi-technology campus |
| 4 | The airtime model revisited | 13 | Case drill: PB-059/060 rehearsal |
| 5 | Roaming engineering | 14 | Classroom questions |
| 6 | Fast transition & key caching | 15 | Common misconceptions |
| 7 | Voice-grade WLAN design | 16 | Summary |
| 8 | Worked example: hall of 400 | 17 | Exit question |
| 9 | Density vs coverage | | |

## Slides

### Slide 1 — Title
**Computer Networks — Lecture 30**
Mobile & wireless enterprise networking

> Notes — L10/L11 gave Wi-Fi's mechanics; today runs them at enterprise scale — 400 clients, voice, roaming, and the physics of link budgets.

### Slide 2 — Hook: the call that never dropped
- A phone walks the campus on a call: no drop
- Somebody *engineered* that: channel plan, overlap, key caching
- Design quality is invisible until its absence

> Notes — 2 min. The lecture's thesis: seamless = many correct small decisions. PB-059 is what happens when one is missing.

### Slide 3 — Enterprise WLAN = capacity design
- Coverage is table stakes; *capacity* is the design
- Per-cell client count, application mix, peak-hour demand
- The survey→model→place→validate loop (L11) at campus scale

> Notes — The L11 loop recurs deliberately — spaced retrieval. New at this scale: co-channel coordination across dozens of APs.

### Slide 4 — The airtime model revisited
- One radio = one shared airtime budget
- Per-client ≈ budget ÷ active clients (fair share, simplifications noted)
- Idle clients cost ~nothing; *active* ones divide

> Notes — L10's division math made operational (quiz W15 Q5's source). The active/idle distinction is where naive capacity math fails.

### Slide 5 — Roaming engineering
- Client decides; infrastructure *influences*: same-SSID design, balanced cells
- Roam gap = reassociation window; frames in flight may drop
- Design goal: overlap without co-channel contention

> Notes — Quiz W15 Q4's mechanism. The design tension (overlap helps roaming, hurts channels) is the lecture's central trade-off.

### Slide 6 — Fast transition & key caching
- 802.11r-class fast transition: fewer round trips at roam
- Key caching: no full re-authentication per AP
- Voice-grade WLANs require both — one line each

> Notes — Course-level treatment: what it fixes (the gap), not frame-by-frame mechanics. Notes.md has the mechanism sketch for the curious.

### Slide 7 — Voice-grade WLAN design
- Voice tolerates loss poorly and jitter worse
- Design: −67 dBm-class cell edges, ≤ ~20 active calls/cell, roaming overlap ≥ 15–20% (rule-of-thumb ranges, ⚠ verify per deployment guide)
- Admission control: refuse the call rather than degrade everyone

> Notes — The numbers are deployment-guide rules of thumb — flag for verification (speaker note does). Admission control is the "say no" design tool.

### Slide 8 — Worked example: hall of 400
- Lecture hall: 400 devices, 60% concurrently active
- One AP at 400 Mb/s goodput → 400×0.6 = 240 active → ≈ 1.7 Mb/s each
- Design answer: 6–8 APs, channel plan, 5 GHz steering

> Notes — The arithmetic that justifies budgets (quiz W15 Q5's structural upgrade). Desk-checked: 400×0.6 = 240; 400/240 ≈ 1.67.

### Slide 9 — Density vs coverage

| Design | Cells | Per-cell load | Roam frequency |
|---|---|---|---|
| Coverage-first | few | heavy | rare |
| Density-first | many | light | frequent |

- You choose the *failure* you prefer

> Notes — The 2×2 trade-off. Roam frequency cost appears only if roaming engineering (slide 5–6) is done — otherwise density-first = roam-problems.

### Slide 10 — Cellular in one slide
- Same MAC problem, licensed spectrum, provider-managed cells
- Handover: the network *assists* more actively than Wi-Fi roaming
- Concepts transfer; ownership and spectrum differ

> Notes — 90 seconds: the point is conceptual continuity, not cellular engineering. 5G/Wi-Fi6 convergence = enrichment pointer.

### Slide 11 — Worked example: link budget
- Outdoor bridge: TX 20 dBm, both antennas 10 dBi, cable loss 2 dB
- Received ≈ 20 + 10 + 10 − 2 − 2 − path-loss(5 km, 5 GHz)
- Path loss ≈ 120 dB → received ≈ −84 dBm → workable only with high-gain + low-noise (⚠ figures illustrative — verify with a real calculator in class)

> Notes — The link-budget *shape* is the lesson (PB-060's case rehearses it fully). The numbers are teaching values — the speaker note must say so; run a real budget calculator live if available.

### Slide 12 — The multi-technology campus
- Wi-Fi + cellular + wired: one design, three radios
- Policy: which traffic goes where (voice → Wi-Fi calling, bulk → wired)
- The design-review question: "what happens when one fails?"

> Notes — The capstone-facing slide (L31/L32 preview). Redundancy thinking from L16's design vocabulary returns.

### Slide 13 — Case drill: PB-059/060 rehearsal
- PB-059: wrong-AP attachment (roaming gone wrong) — diagnose the design flaw
- PB-060: outdoor link budget — is the bridge viable?
- 20 min each, pairs, instructor keys sealed

> Notes — The two cases map to slides 5 and 11. PB-061 (campus upgrade review) is tonight's reading.

### Slide 14 — Classroom questions
1. Why does adding APs *not* add airtime to a single cell?
2. Your roam gap drops calls: two engineering suspects?
3. Where does the client's decision-making show up in a site survey?

> Notes — Q1: airtime is per-radio — new AP = new budget, same cell unchanged. Q3: the survey shows *client-side* attachment logs — the surveyor must capture them (PB-059's evidence type).

### Slide 15 — Common misconceptions
- "−50 dBm everywhere = done" → capacity lives elsewhere (L11's hook, now with budget math)
- "More power = better" → bigger cells worsen contention/roam asymmetry
- "Cellular and Wi-Fi roam the same way" → different ownership; assisted vs client-decided

> Notes — The power misconception is the most common field error; the contention argument (slide 4) is the counter.

### Slide 16 — Summary
- Enterprise WLAN = capacity + roaming engineering
- Airtime math sizes APs; link budgets size links
- The design loop with load validation
- Next: enterprise design & capstone kickoff (L31)

> Notes — Recap by the two worked examples; students re-derive one airtime number cold.

### Slide 17 — Exit question
One AP, 300 Mb/s airtime goodput, 50 active clients, fair share. Per-client rate?
*(PB-061 reading tonight.)*

> Notes — Answer: 6 Mb/s. Exit slips feed W15 pool.

### Demonstration instructions (instructor)
- Case drills are paper-first; keys sealed per the bank's convention
- Live beat (optional): roam between two lab APs with continuous ping (ITI: two APs + configured SSID; else narrate the L11 figure with PB-059's timeline)
- Link budget: run a free web budget calculator live if outbound is allowed; else the worksheet's printed table (labeled illustrative)

### References for the deck
- IEEE 802.11r/k/v (fast transition, radio management — concept citations)
- Vendor deployment guides for the −67 dBm/overlap rules of thumb (⚠ verify before printing numbers in student handouts)
- Case bank: PB-059…PB-061
