# Laboratory Strategy

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`schedule-32-lectures.md`](schedule-32-lectures.md) · [`assessment-strategy.md`](assessment-strategy.md) · [`prerequisites.md`](prerequisites.md) |

## 1. Principles

1. **Do → observe → perturb → interpret.** Every lab makes students run something, watch
   it on the wire or in measurements, change a variable, and explain what changed and why.
   Interpretation is always graded, never just output.
2. **One environment, many uses.** A single course VM image (Ubuntu LTS) serves all labs;
   no lab requires paid software or cloud spend.
3. **Realism over simulation.** Packet-level labs use real captures and real VMs; simulators
   (e.g., GNS3) are used only where kernel networking cannot reach (multi-router L3
   topologies in LAB-07). ⚠ VERIFY simulator licensing and image availability each semester.
4. **Ethics by design.** All attack-technique work happens inside the VM lab against
   course-owned targets; see the acknowledgment gate in [`prerequisites.md`](prerequisites.md).
5. **Skeleton-first programming.** Python labs ship with working scaffolds; students
   implement protocol logic, not boilerplate.

## 2. Environments

| Environment | Used for | Notes |
|---|---|---|
| Course VM (Ubuntu LTS, provided image) | LAB-04…LAB-14, all GA work | Ships with Wireshark, Python 3.10+, `iperf3`, `tcpdump`, `dnsmasq`, `nftables`, `tc/netem`, `dig`, `iproute2`, OpenVPN ⚠ VERIFY image build each semester; publish hash |
| Host Wireshark | LAB-01, LAB-03, GA-01/02/07/12/18/21/22 | Passive captures only, on networks the student owns or has permission to observe |
| Network simulator (GNS3 or equivalent) | LAB-07 multi-router topology (if kernel namespaces are insufficient) | Free tier; instructor decision recorded in lab README |
| Free cloud tier | GA-27 mini-VPC | Optional campus sandbox alternative; ⚠ VERIFY provider, quota, and cost ceiling |

## 3. Lab inventory (14 numbered labs + in-lecture GAs)

| ID | Title | Lecture | Mode | Environment | Deliverable (graded) |
|---|---|---|---|---|---|
| LAB-01 | Measuring latency & throughput: ping, traceroute, iperf3 | L04 | Individual | Host + VM | Worksheet: estimates vs measurements |
| LAB-02 | Build a switched lab with VLANs | L09 | Pairs | VMs/simulator | Lab report |
| LAB-03 | Wi-Fi survey & association analysis | L10–L11 | Individual | Host + own Wi-Fi | Written findings |
| LAB-04 | Subnetting drills & design exercise | L13–L16 (due) | Individual | Paper + VM check | Problem set (5% instrument) |
| LAB-05 | DHCP & NAT on a Linux router | L14 | Pairs | VMs | Lab report |
| LAB-06 | Dual-stack IPv4/IPv6 lab | L15 | Pairs | VMs | Lab report |
| LAB-07 | Static routing & traceroute dissection (3-router topology) | L16 | Pairs | VMs (+simulator if needed) | Lab report |
| LAB-08 | UDP chat/file transfer client & server (Python) | L17 | Pairs | VM | Working code + demo |
| LAB-09 | TCP performance under netem | L19 | Individual | VM | Report with graphs & interpretation |
| LAB-10/11 | Reliable transport over UDP (design + implement) | L20 (assign) → W12 demo | Pairs | VM | Spec (milestone) + code + demo (10% instrument) |
| LAB-12 | Capture & compare HTTP/1.1 vs HTTP/2 vs HTTP/3; SMTP & SSH dissection | L23 | Individual | VM | Worksheet |
| LAB-13 | Firewalls & VPN (nftables policy + site-to-site tunnel) | L25 | Pairs | VMs | Lab report with policy justifications |
| LAB-14 | Monitoring dashboard & fault-injection drill | L29 | Pairs | VMs | Report + dashboard |
| GA-xx | In-lecture guided activities (GA-01…GA-31 per schedule) | Various | Individual | Host/VM/paper | Exit tickets & worksheets (lab-component credit) |

Thirteen of these produce the graded lab-component deliverables described in
[`assessment-strategy.md`](assessment-strategy.md) §3.2 (lowest dropped).

## 4. Standard lab session pattern (2-hour supervised block)

1. **5 min** — objectives and safety/ethics reminder; everyone logs into the VM.
2. **15 min** — instructor walks the setup; students verify their environment (version
   checks printed and included in submissions).
3. **80 min** — work through the lab's tasks (each task = do → capture → question).
4. **15 min** — challenge task (stretch, ungraded) for fast finishers.
5. **5 min** — submission checklist; anything unfinished becomes homework with a 48-h window.

## 5. Submission format (uniform)

- One PDF or Markdown report per pair/student containing: environment table (tool
  versions), answers to numbered questions, embedded screenshots/captions for every claim,
  and the **exact commands and Wireshark filters** used.
- Raw evidence (`.pcapng` files, measurement CSVs, code) submitted alongside, named
  `LABxx-taskN-evidence.*`.
- Reproducibility rule from the assessment strategy applies: fabricated or unreproducible
  evidence scores zero on the instrument.

## 6. Rubric (100 points, all labs)

| Criterion | Points | Notes |
|---|---|---|
| Correct results & measurements | 40 | Right answers, sane numbers, units stated |
| Analysis & interpretation | 30 | Explains *why*; connects to lecture concepts; notes anomalies |
| Evidence reproducibility | 20 | Commands/filters included; another person could repeat it |
| Clarity & presentation | 10 | Organized, readable, honest about failures |

Challenge tasks earn recognition (badge/mention), never points — keeps grading fair.

## 7. Environment-dependent items — instructor verification list

- [ ] ⚠ VERIFY VM image boots on the teaching lab's hypervisor version; publish SHA-256
- [ ] ⚠ VERIFY Wi-Fi survey lab is feasible in the local room/campus RF environment (LAB-03)
- [ ] ⚠ VERIFY simulator (if used) images and licensing for LAB-07
- [ ] ⚠ VERIFY cloud sandbox quotas for GA-27 or substitute the VM-lab alternative
- [ ] ⚠ VERIFY HTTP/3 test endpoints used by LAB-12 are still reachable; keep a local
      fallback server in the VM image
- [ ] ⚠ VERIFY any external dataset downloads (LAB-14, L28/L31 exercises) for stability
