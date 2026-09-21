# Case Study Strategy

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`schedule-32-lectures.md`](schedule-32-lectures.md) · [`assessment-strategy.md`](assessment-strategy.md) · [`lab-strategy.md`](lab-strategy.md) |

## 1. The narrative device: Meridian Systems

**Meridian Systems** is a fictional mid-size company (~250 staff): a two-building
headquarters campus, a small branch office, cloud-hosted services, and a growing fleet of
wireless devices. Students act as the junior network engineering team; the instructor plays
the IT manager and, later, the incident commander. All scenario evidence (captures, configs,
logs, tickets) is instructor-prepared, course-owned, and synthetic — no real organization's
data is used.

The narrative gives every technical topic a *reason*: students are never solving an abstract
exercise; they are solving Meridian's next problem.

## 2. The four case studies

| ID | Title | Kickoff | Resolution | Focus | CLOs |
|---|---|---|---|---|---|
| CS-01 | "The morning the network felt slow" | L03 | L04 | Layered reading of an incident; measurement vocabulary | CLO1, CLO4 |
| CS-02 | Designing Meridian's segmented LAN | L11 | L16 | LAN design, VLANs, addressing plan, routing | CLO2, CLO3, CLO6 |
| CS-03 | "The service outage" | L23 | L29 | Packet-evidence diagnosis, security incident, RCA writing | CLO4, CLO6, CLO7 |
| CS-04 | Meridian multi-site redesign (capstone) | L26 (brief due) | L32 | Full design → build → secure → instrument → defend | CLO3–CLO8 |

### CS-01 — The morning the network felt slow (in-class, ungraded exercise)
A one-page incident vignette plus a small provided capture. In lecture teams, students
classify every observed symptom by layer (the "Layer 1–7 of the incident" exercise) and
list what they would measure first. Deliberately low-stakes: it calibrates the
evidence-based mindset before any graded work.

### CS-02 — Designing Meridian's segmented LAN (graded, 4%)
Meridian is growing; the flat LAN has become a broadcast storm with mixed trust zones.
Deliverable: a segmentation design (VLANs, trunk plan, L2/L3 boundary choices) **and** a
complete IPv4 addressing plan with VLSM, growth headroom, and a written justification of
trade-offs. Evidence requirement: simulations/captures that demonstrate the design works
(switch FDB, inter-VLAN routing). Due L16; feeds directly into the capstone scenario.

### CS-03 — The service outage (graded, 6% across three milestones)
Meridian's internal web service fails intermittently for one building. Instructor provides
three evidence bundles across the lectures:
1. **Evidence log** (L23): initial captures and syslog — students open a structured
   evidence log with hypotheses (due as part of the L26 diagnosis).
2. **Diagnosis** (L26, 3%): from later bundles (DNS, DHCP, TCP retransmission, and an
   ARP-anomaly trail), students identify the failure chain and the security incident
   embedded in it.
3. **Root-cause analysis report** (L29, 3%): professional RCA — timeline, contributing
   factors, what monitoring would have caught it, remediation plan. Uses the LAB-14
   dashboard as supporting evidence.

### CS-04 — Capstone: multi-site redesign (graded, 15%; team)
See §4.

## 3. Progressive skills rehearsed across the case-study thread

1. Read an incident through the layered model (CS-01)
2. Measure before diagnosing; record evidence honestly (CS-01 → CS-03)
3. Turn requirements into designs with justified trade-offs (CS-02)
4. Attribute observed behavior to specific protocol mechanics (CS-03)
5. Write professional documents: design doc, evidence log, RCA (CS-02 → CS-03)
6. Defend decisions under questioning (CS-04)

## 4. Capstone (CS-04) design

**Scenario:** Meridian acquires a second site and must integrate it: branch ↔ HQ ↔ cloud.
**Team size:** 3–4, mixed CS/DS encouraged. **Instructor role:** design-review board and
acceptance tester.

| Stage | Due | Deliverable | Weight (of 15%) |
|---|---|---|---|
| 1. Design document | W13 (L26) | Topology, VLAN & IP plan (v4+v6), routing, security zones & firewall policy intent, monitoring plan; capacity estimates with shown math | 25% |
| 2. Build & demo | W15 (L31 clinic) | Working VM-lab build demonstrating inter-site routing, a security control, and one application flow; live demo checklist | 20% |
| 3. Instrumentation | W16 (L32) | Monitoring dashboard (metrics that matter, alert rationale) + measurement data from a fault-injection run | 20% |
| 4. Final report | W16 (L32) | Design-vs-built comparison, evidence appendix, limitations, future work | 20% |
| 5. Defense | W16 (L32) | 15-min presentation + individual Q&A (each member defends a component) | 15% |

**Data-science component (required in every capstone):** the telemetry dataset the team
collects (flow records or dashboard metrics) must be analyzed for at least one pattern
(e.g., baseline vs fault-injection traffic profile) with a short methodological note.

## 5. Capstone rubric highlights

| Dimension | Points (of 100) | What good looks like |
|---|---|---|
| Design quality & justification | 25 | Requirements traced to design; alternatives considered; math shown |
| Build correctness | 25 | Demo matches design; flows work; controls demonstrably active |
| Measurement & instrumentation | 20 | Meaningful metrics; fault injection interpreted; honest error bars |
| Documentation & reproducibility | 15 | Commands, configs, and data included; another team could rebuild it |
| Defense & individual understanding | 15 | Every member explains their component; graceful "we don't know yet" |

Peer contribution factor ±10% (documented peer evaluation + instructor observation) applied
to individual marks within the team score; disputes resolved by evidence of contribution
(commit history, section authorship).

## 6. Instructor preparation for the case-study thread

- [ ] ⚠ VERIFY all CS-03 evidence bundles produce the intended conclusions when re-analyzed
      (run the model answer against the packets each semester)
- [ ] ⚠ VERIFY synthetic captures contain no real usernames/hosts (sanity scan)
- [ ] Refresh the Meridian scenario "next problem" so it stays plausible with current tools
- [ ] Prepare the CS-04 acceptance-test checklist before the W15 clinic
