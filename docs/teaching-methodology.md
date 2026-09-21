# Teaching Methodology

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`schedule-32-lectures.md`](schedule-32-lectures.md) · [`lab-strategy.md`](lab-strategy.md) · [`case-study-strategy.md`](case-study-strategy.md) |

## 1. Instructional approach

The course teaches each protocol **three times in different registers**:

1. **Conceptually** — why it exists, what problem it solves, how it fits the layered model;
2. **Analytically** — on the wire: students read real packets (Wireshark) and compute
   real numbers (delays, capacities, windows);
3. **Operationally** — in the lab: students configure, program, perturb, and measure it.

A topic is not considered "covered" until all three registers have been exercised. This
is the course's core pedagogical commitment and drives the schedule's Lab/GA column.

## 2. The 120-minute lecture pattern

Fixed skeleton per lecture (see the M&C column in the master schedule):

| Segment | Minutes | Techniques used |
|---|---|---|
| Recap + objectives + hook | 10 | 2-question recall poll; a real failure story or screenshot as the hook; today's driving question on the board |
| Concept block | 40–75 (per module) | Slides + whiteboard derivation + **live demo**; think-pair-share at each mini-milestone |
| Break | 5 | — |
| Activity block | 30–55 (per module) | GA worksheet, packet hunt, Python demo, or lab briefing — students work, instructor circulates |
| Wrap-up | 10 | Exit ticket (2–3 items), preview with a question to think about, pointers to reading/lab |

The pattern is uniform so students build a stable learning rhythm; module-level minute
allocations differ (listed in each module's overview in the schedule).

## 3. Lecture types

| Type | Lectures | Emphasis |
|---|---|---|
| Foundation lectures | L01–L02, L05–L06 | Conceptual clarity; vocabulary; no lab software beyond Wireshark basics |
| Protocol-analysis lectures | L07, L12, L18, L21–L24 | Wireshark-centric; packet walks and dissection drills |
| Design lectures | L09, L13–L16, L25, L27, L31 | Worked design problems; heuristics and trade-offs; calculation practice |
| Build lectures | L17, L20 | Programming model of the layer; project scaffolding |
| Workshop lectures | L26, L29 (drill part), L31 (review part), L32 | Team work with instructor coaching; rubric-aligned critique |

## 4. Live demonstration standards

Every demo must be **reproducible and pre-verified** by the instructor the same morning
(configs and commands live in the lecture folder). Standard demo kit:

- Laptop + course VM; backup pre-recorded terminal session in case of failure;
- Wireshark mirrored to the projector with 14pt+ fonts and colorized filters;
- One "what do you predict?" question posed to the room before every demo runs.

⚠ VERIFY: projector/display port, presenter view, and network access in each teaching room
before week 1; document the room setup in the instructor log.

## 5. Active-learning techniques used

- **Packet hunts:** "find the packet that proves X" exercises on provided traces.
- **Predict-observe-explain:** predict switch/route/protocol behavior, then run it.
- **FDB/routing-table races:** short timed table-completion contests (GA-08, LAB-07).
- **Whiteboard design critiques:** students defend an addressing or segmentation plan.
- **Error taxonomies:** students classify a failure story by layer before diagnosing it.
- **Exit tickets:** graded-for-participation only; used to tune the next lecture's recap.

## 6. Programming integration

Python is used from L03 (socket tour) and becomes central at L17–L20. Rules:

- All lab code targets **Python 3.10+** and the standard library plus `scapy` only where a
  lab explicitly says so (LAB-12 packet crafting optional; never required for passing);
- Students always receive a **working skeleton**; the intellectual work is protocol logic,
  not boilerplate;
- Code review of one student pair per week (rotating, 5 minutes) normalizes reading others'
  network code;
- The reliable-transport project (LAB-10/11) is the course's programming capstone for the
  transport module and feeds directly into capstone tooling reuse.

## 7. Serving two audiences (CS and Data Science)

- **Shared core:** everything in the master schedule labeled core.
- **Data-science emphasis points:** L04 (measurement bias), L28 (telemetry as data),
  L29 (flow records as datasets), L31 (traffic classification, anomaly-detection framing,
  capacity forecasting, ethics).
- **CS emphasis points:** deeper socket/kernel mechanics in L17–L20 enrichment, L28 SDN.
- Both audiences sit in the same lectures and teams; differentiation happens in the *depth
  of the analysis questions*, not in separate content tracks. This is deliberate — mixed
  teams mirror real industry practice.

## 8. Common misconceptions register (address explicitly)

| Misconception | Where debunked |
|---|---|
| "The OSI model is a protocol suite" (vs a reference model) | L02 |
| "Layers strictly correspond one-to-one to headers in every real packet" | L02, L07 |
| "Bandwidth == throughput" | L01, L04, L19 |
| "A switch is just a smarter router" | L08, L16 |
| "NAT is a firewall / provides security" | L14, L25 |
| "TCP is always better than UDP" | L17, L20 |
| "Wi-Fi is just wireless Ethernet" (ignores CSMA/CA, half duplex, airtime) | L10 |
| "Ping proves the network is fine" | L16, L29 |
| "Encryption == VPN == anonymity" | L24–L25 |
| "The cloud is a different kind of network" | L27 |

## 9. Inclusive teaching commitments

- All example names, scenarios, and case-study characters are region-neutral and respectful;
- No lab requires hardware a student cannot run free on a mid-range laptop (VM images
  provided; lab machines available on campus — ⚠ VERIFY lab-room booking each semester);
- Slides use colorblind-safe palettes; every color-coded trace also has a text label;
- All videos/demos have captions or an equivalent live narration script;
- The two-audience design (§7) explicitly legitimizes both CS and DS backgrounds in teams.

## 10. Instructor preparation checklist (per semester)

- [ ] Verify editions in [`textbooks-references.md`](textbooks-references.md) and update the
      syllabus reading map
- [ ] Rebuild and test the course VM image; record image hash in the lab README
- [ ] Re-verify every demo and lab solution on the current image (⚠ each one)
- [ ] Confirm teaching-room AV/network and book the lab room for the 11 staffed labs
- [ ] Refresh case-study packet bundles and re-run all analysis answers against them
- [ ] Complete the PLO mapping in [`clo-mapping.md`](clo-mapping.md) and submit the syllabus
- [ ] Confirm exam dates against the university calendar (⚠ syllabus calendar note)
- [ ] Review the misconception register against last semester's exit-ticket data
