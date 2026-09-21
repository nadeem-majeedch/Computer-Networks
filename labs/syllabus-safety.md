# Laboratory Syllabus & Safety Rules

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Companion documents | [`setup-environment.md`](setup-environment.md) · [`../docs/lab-strategy.md`](../docs/lab-strategy.md) · [`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) |
| Status | Draft v0.1 — awaiting instructor review |
| Sessions | Weekly 2-hour supervised lab block (pattern in lab-strategy §4) + 48-h finish window |
| Tools | Wireshark, tcpdump, iproute2, netem, nftables, dnsmasq, iperf3, Python 3.10+, network namespaces; GNS3/Packet Tracer only where flagged optional |

## 1. Purpose and structure

The workbook operationalizes the *Do → observe → perturb → interpret* principle from
[`../docs/lab-strategy.md`](../docs/lab-strategy.md): every lab makes students run something,
observe it (on the wire or in measurements), change a variable, and explain what changed.
Labs are ordered to match the lecture sequence; each lab README names its anchor lectures and
CLOs. Sixteen labs ship in this workbook:

- **LAB-01…LAB-09, LAB-12, LAB-13, LAB-14** — the graded labs already scheduled in
  [`../docs/schedule-32-lectures.md`](../docs/schedule-32-lectures.md).
- **LAB-10, LAB-11** — the reliable-transport project (design + implementation), which the
  schedule shows combined as `LAB-10/11` and the assessment strategy weights at 10%.
- **LAB-15, LAB-16** — **optional, ungraded extension labs** (safe security analysis; network
  design capstone rehearsal), added by this workbook to reach the requested topic coverage
  (security analysis; design). Instructor may assign them for recognition or extra practice;
  they carry no course weight unless the instructor explicitly adds one *before* the semester
  starts (⚠ instructor decision — adding weight requires updating
  [`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) §3 first).

## 2. Grading at a glance

| Item | Weight | Where defined |
|---|---|---|
| 13 graded lab/GA deliverables (drop lowest) | 15% of course | assessment-strategy §3.2 |
| Subnetting problem set (LAB-04) | 5% (its own instrument) | assessment-strategy §3.3 |
| Reliable-transport project (LAB-10/11) | 10% | assessment-strategy §3.5 |
| LAB-15/LAB-16 | 0% (optional recognition) | this document |

Per-lab rubric (100 points, applies to every lab): Correct results & measurements 40 ·
Analysis & interpretation 30 · Evidence reproducibility 20 · Clarity & presentation 10 —
full text in [`../docs/lab-strategy.md`](../docs/lab-strategy.md) §6. Challenge tasks earn
recognition, never points.

## 3. Safety and ethics rules (binding)

> **The one-sentence version:** you may inspect, build, and perturb *only* inside the course's
> isolated lab environment or against captures the course provides; you never point tools at
> systems you do not own or have written permission to test.

1. **Isolation first.** All packet generation, address configuration, firewall changes, load
   generation, and fault injection happen inside course VMs or network namespaces. VMs use the
   host-only/NAT lab networks defined in [`setup-environment.md`](setup-environment.md) — never
   bridged to the campus/enterprise network unless a task explicitly says so.
2. **No scanning or probing of external systems.** Port scans, ping sweeps, ARP spoofing, SYN
   floods, and similar techniques are performed only against course-owned targets inside the
   lab. LAB-15's security analysis uses **benign, course-generated traffic** and offline
   captures only; no attack tooling against real networks, ever.
3. **Captures stay clean.** Passive Wireshark/tcpdump captures on shared networks (e.g., the
   host Wi-Fi in LAB-03) are **observation only** — no deauthentication, injection, or
   association attempts against networks you do not own; use only networks you own or have
   written permission to observe. If your lab room needs instructor-controlled APs, the
   instructor provides the test SSID.
4. **Credentials and data.** Lab exercises use course-created test accounts and synthetic
   data. Never capture or store real passwords, personal data, or institutional traffic;
   discard accidental captures of real traffic as instructed in session.
5. **System integrity.** Do not disable host firewalls/AV on machines outside your VM; do not
   install tools outside the ones listed in the setup guide without instructor approval.
6. **Acknowledgment gate.** Students sign the ethics acknowledgment (in
   [`../docs/prerequisites.md`](../docs/prerequisites.md) §5) before LAB-01. The instructor
   restates the two most relevant rules at the start of each lab block (5-minute reminder in
   the session pattern).
7. **Breakage is expected — hiding it is not.** If a lab technique makes something fail
   (that is the point of fault injection), report it; lab VMs are rebuilt from the image, so
   honest failure never costs marks, but fabricated or unreproducible evidence scores zero
   (assessment-strategy reproducibility rule).

## 4. Standard session pattern (2-hour supervised block)

1. **5 min** — objectives + safety/ethics reminder; log into the VM.
2. **15 min** — instructor walks the setup; students verify the environment (version checks
   printed and included in the submission).
3. **80 min** — the lab's tasks (each task = do → capture → question).
4. **15 min** — challenge task (stretch, ungraded) for fast finishers.
5. **5 min** — submission checklist; unfinished work becomes homework with a 48-h window.

## 5. Submission format (uniform, from lab-strategy §5)

One Markdown/PDF report per student or pair: environment table (tool versions), numbered
answers, screenshot or capture citation for every claim, and the **exact commands and
Wireshark display filters** used. Raw evidence alongside, named `LABxx-taskN-evidence.*`
(`.pcapng`, CSV, code). Reports state honestly what did not work.

## 6. Accessibility and low-resource alternatives

- **Low-spec machines:** every lab names a lighter path (offline captures instead of live
  capture; namespaces instead of extra VMs; text tools instead of GUI). A machine that runs a
  browser can complete most labs via offline `.pcapng` bundles + paper/`ipcalc` arithmetic.
- **Screen-reader/low-vision:** Wireshark is mouse-heavy; tshark equivalents are provided in
  each lab (`accessibility` note). Diagrams in these documents are ASCII so they survive text
  scaling and screen readers.
- **No lab room:** instructor can run any lab as a live demo while students predict-and-record
  on the worksheet; deliverables then grade prediction accuracy + interpretation (the
  instructor adapts the rubric's "correct results" row to "correct predictions" ⚠).
- **Color blindness:** all "expected output" descriptions name *textual* markers (counts,
  flags, numbers), never color alone.

## 7. Tool policy

Free/open-source only: Wireshark/tshark, tcpdump, iproute2 (`ip`, `ss`, `bridge`), netem,
nftables, dnsmasq, iperf3, bind9-utils (`dig`), OpenVPN, Python 3 standard library,
network namespaces. GNS3 is optional for multi-router topologies if kernel namespaces feel
too abstract (instructor decision, recorded per lab); Cisco Packet Tracer is an **optional
alternative** for visualization only where the institution already licenses it — no task
*requires* it, and deliverables never depend on PT file formats.
