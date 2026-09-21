# Computer Networks

**A complete, open 4th-semester course for BS Computer Science and BS Data Science
students — 32 lectures × 2 hours = 64 instructional hours.**

You will learn how computer networks actually work — from a single Ethernet frame to
the global Internet — by building, measuring, capturing, and troubleshooting real
networks, not just reading about them. Every lecture pairs theory with hands-on work:
packet analysis in Wireshark, Python socket programming, Linux networking labs,
progressive problem-solving case studies, and a team capstone that designs and defends
a complete small network.

| | |
|---|---|
| **Level** | Undergraduate, semester 4 (no prior networking assumed) |
| **Format** | 32 lectures (2 h each) + a weekly 2-hour lab block |
| **Approach** | Theory → live demonstrations → labs → case studies → capstone |
| **Standards** | Vendor-neutral, open standards only (IETF RFCs, IEEE 802) |
| **Materials** | Free and open — the primary textbook is legally free online, and every lab tool is free software |

---

## 🚀 Start here

| I want to… | Go to |
|---|---|
| **See the whole course online** | 🌐 [**Course Website**](https://nadeem-majeedch.github.io/Computer-Networks/) |
| Understand the course, grading, and policies | [Course overview & syllabus](docs/syllabus.md) |
| See what I should already know | [Prerequisites](docs/prerequisites.md) |
| Browse all 32 lectures | [Lecture index](lectures/README.md) |
| Set up my lab environment | [Lab setup guide](labs/setup-environment.md) |
| Practice diagnosing network problems | [Case study bank](case-studies/README.md) |
| Find quizzes, assignments, and exams | [Assessment package](assessments/README.md) |
| Plan my semester | [Semester calendar](site-src/calendar.md) |
| Check a citation or read further | [References](docs/textbooks-references.md) |

Everything is readable directly here on GitHub — no special software needed. The
[course website](https://nadeem-majeedch.github.io/Computer-Networks/) presents the
same material with full-text search, clean navigation, and diagrams.

---

## What is this course about?

Computer networks are the connective tissue of modern computing: every web page, cloud
service, video call, and distributed dataset crosses a network. This course opens that
black box, layer by layer.

**Why it matters for Computer Science.** Debugging a stalled download, configuring a
firewall, or scaling a web service all require understanding what the network is doing
between your code and the user. You will finish able to *explain* what happens when a
packet travels from your laptop to a server — and *prove* it with a packet capture.

**Why it matters for Data Science.** Datasets live on other machines. Training jobs
push gigabytes through TCP; telemetry, logging, and monitoring systems are network
data streams. The course includes dedicated data-science cases: transfer-time and
overhead math for large datasets, TCP window limits on throughput, measurement bias,
and how monitoring turns networks into data you can analyze.

**How you'll learn.** Each week follows the same rhythm: concepts in lecture, then a
guided activity or lab where you *do* the thing — capture an ARP exchange, build a
VLAN, write a UDP protocol, watch TCP respond to congestion. Problem-solving case
studies (65 of them) train you to diagnose faults the way practitioners do: from
evidence to hypothesis to test.

---

## What you will be able to do

By the end of the course, you can (full CLO text in
[`docs/learning-outcomes-clos.md`](docs/learning-outcomes-clos.md)):

1. **Explain** layered network architecture — OSI and TCP/IP, encapsulation, PDUs, and
   the roles of the core protocols (CLO1)
2. **Describe** how bits physically move: media, framing, error detection, Ethernet
   switching, VLANs, and Wi-Fi (CLO2)
3. **Design** IPv4/IPv6 addressing plans — subnetting, VLSM, aggregation — and justify
   the trade-offs (CLO3)
4. **Capture and analyze** real traffic in Wireshark/tcpdump to explain ARP, ICMP, TCP,
   UDP, DNS, and DHCP behavior from packet evidence (CLO4)
5. **Build and measure** small networked systems with Python sockets and Linux tools,
   interpreting throughput, latency, loss, and jitter quantitatively (CLO5)
6. **Troubleshoot systematically** and evaluate design alternatives with a documented
   methodology (CLO6)
7. **Assess** common network threats and select layered, appropriate defenses (CLO7)
8. **Integrate** all of the above in a team capstone: design, build, secure,
   instrument, and defend a small multi-network solution (CLO8)

---

## Prerequisites

You're ready if you can (self-check details in
[`docs/prerequisites.md`](docs/prerequisites.md)):

- Write and debug a ~100-line Python program (functions, loops, dictionaries, files)
- Convert between decimal, binary, and hexadecimal
- Use a Linux shell: navigate, edit a file, run commands, read a man page
- Explain what an IP address and URL are at a user level

The course introduces networking concepts progressively — no networking background is
assumed. Recommended prior coursework: Programming Fundamentals, OOP/CS2, Discrete
Mathematics; Digital Logic and Operating Systems (completed or concurrent).

---

## Course map — 8 modules, 32 lectures

Full detail (per-lecture topics, labs, pacing, CLOs) lives in the
[lecture index](lectures/README.md) and the
[master schedule](docs/schedule-32-lectures.md).

### Module 1 — Foundations & Architecture · L01–L04
*How networks are organized and how to reason about them: switching, delay, layering,
sockets, and measurement.*

| # | Lecture | Materials |
|---|---|---|
| 1 | What Is a Network? Overview, History & the Internet Today | [Overview](lectures/lecture-01-what-is-a-network/) · [Worksheet](lectures/lecture-01-what-is-a-network/worksheet.md) |
| 2 | Layered Architectures: OSI & TCP/IP | [Overview](lectures/lecture-02-layered-architectures/) · [Worksheet](lectures/lecture-02-layered-architectures/worksheet.md) |
| 3 | Applications, Sockets & the First Packet Hunt | [Overview](lectures/lecture-03-applications-sockets-packet-journey/) · [Worksheet](lectures/lecture-03-applications-sockets-packet-journey/worksheet.md) |
| 4 | Performance Lab Foundations: Measuring the Network | [Overview](lectures/lecture-04-performance-measurement-foundations/) · [Worksheet](lectures/lecture-04-performance-measurement-foundations/worksheet.md) |

### Module 2 — Physical & Data Link Foundations · L05–L11
*Signals and media, framing and error detection, Ethernet and switching, VLANs, and
Wi-Fi.*

| # | Lecture | Materials |
|---|---|---|
| 5 | Physical Layer: Signals, Media & Transmission Basics | [Overview](lectures/lecture-05-physical-layer-signals-media/) · [Worksheet](lectures/lecture-05-physical-layer-signals-media/worksheet.md) |
| 6 | Data Link Layer: Framing, Errors & Reliability | [Overview](lectures/lecture-06-data-link-framing-errors/) · [Worksheet](lectures/lecture-06-data-link-framing-errors/worksheet.md) |
| 7 | MAC Protocols & Wired LANs: Ethernet | [Overview](lectures/lecture-07-mac-protocols-ethernet/) · [Worksheet](lectures/lecture-07-mac-protocols-ethernet/worksheet.md) |
| 8 | Switching & LAN Design | [Overview](lectures/lecture-08-switching-lan-design/) · [Worksheet](lectures/lecture-08-switching-lan-design/worksheet.md) |
| 9 | VLANs & L2 Segmentation | [Overview](lectures/lecture-09-vlans-l2-segmentation/) · [Worksheet](lectures/lecture-09-vlans-l2-segmentation/worksheet.md) |
| 10 | Wireless Networking: Wi-Fi Fundamentals | [Overview](lectures/lecture-10-wifi-fundamentals/) · [Worksheet](lectures/lecture-10-wifi-fundamentals/worksheet.md) |
| 11 | Wireless in Practice + LAN Security Preview | [Overview](lectures/lecture-11-wireless-practice-lan-security/) · [Worksheet](lectures/lecture-11-wireless-practice-lan-security/worksheet.md) |

### Module 3 — Internetworking with IPv4/IPv6 · L12–L16
*Addressing, ARP, subnetting, DHCP and NAT, IPv6, and routing.*

| # | Lecture | Materials |
|---|---|---|
| 12 | IP Fundamentals & ARP | [Overview](lectures/lecture-12-ip-fundamentals-arp/) · [Worksheet](lectures/lecture-12-ip-fundamentals-arp/worksheet.md) |
| 13 | IPv4 Subnetting & VLSM | [Overview](lectures/lecture-13-subnetting-vlsm/) · [Worksheet](lectures/lecture-13-subnetting-vlsm/worksheet.md) |
| 14 | IP Addressing at Scale: DHCP & NAT | [Overview](lectures/lecture-14-dhcp-nat/) · [Worksheet](lectures/lecture-14-dhcp-nat/worksheet.md) |
| 15 | IPv6 | [Overview](lectures/lecture-15-ipv6/) · [Worksheet](lectures/lecture-15-ipv6/worksheet.md) |
| 16 | Routing Fundamentals & ICMP | [Overview](lectures/lecture-16-routing-icmp/) · [Worksheet](lectures/lecture-16-routing-icmp/worksheet.md) |

### Module 4 — Transport Layer · L17–L20
*UDP, TCP connections and reliability, flow and congestion control, and programming
reliability yourself.*

| # | Lecture | Materials |
|---|---|---|
| 17 | UDP & the Transport Layer's Job | [Overview](lectures/lecture-17-udp-sockets/) · [Worksheet](lectures/lecture-17-udp-sockets/worksheet.md) |
| 18 | TCP Essentials: Connections & Reliable Delivery | [Overview](lectures/lecture-18-tcp-connections-reliability/) · [Worksheet](lectures/lecture-18-tcp-connections-reliability/worksheet.md) |
| 19 | TCP Flow & Congestion Control | [Overview](lectures/lecture-19-tcp-flow-congestion-control/) · [Worksheet](lectures/lecture-19-tcp-flow-congestion-control/worksheet.md) |
| 20 | Programming the Transport Layer: Reliability over UDP | [Overview](lectures/lecture-20-programming-transport-layer/) · [Worksheet](lectures/lecture-20-programming-transport-layer/worksheet.md) |

### Module 5 — Application Layer & Network Services · L21–L23
*DNS, DHCP in depth, and the application protocols: HTTP/1.1 → HTTP/3, SMTP, SSH.*

| # | Lecture | Materials |
|---|---|---|
| 21 | DNS: The Internet's Directory | [Overview](lectures/lecture-21-dns/) · [Worksheet](lectures/lecture-21-dns/worksheet.md) |
| 22 | DHCP Deep Dive, BOOTP & Address Management | [Overview](lectures/lecture-22-dhcp-deep-dive/) · [Worksheet](lectures/lecture-22-dhcp-deep-dive/worksheet.md) |
| 23 | Core Application Protocols: HTTP/1.1 → HTTP/3, SMTP & SSH | [Overview](lectures/lecture-23-application-protocols/) · [Worksheet](lectures/lecture-23-application-protocols/worksheet.md) |

### Module 6 — Network Security · L24–L26
*Cryptographic building blocks and TLS, firewalls/segmentation/VPNs, and an
attack-and-defense workshop in a safe, isolated lab.*

| # | Lecture | Materials |
|---|---|---|
| 24 | Security Principles & Cryptographic Building Blocks | [Overview](lectures/lecture-24-security-crypto-tls/) · [Worksheet](lectures/lecture-24-security-crypto-tls/worksheet.md) |
| 25 | Perimeter & Internal Defenses: Firewalls, Segmentation & VPNs | [Overview](lectures/lecture-25-firewalls-vpns/) · [Worksheet](lectures/lecture-25-firewalls-vpns/worksheet.md) |
| 26 | Attack & Defense Case Workshop | [Overview](lectures/lecture-26-attack-defense-workshop/) · [Worksheet](lectures/lecture-26-attack-defense-workshop/worksheet.md) |

### Module 7 — Operations, Monitoring & Cloud · L27–L29
*Cloud and virtual networking, software-defined networking, and systematic monitoring
and troubleshooting.*

| # | Lecture | Materials |
|---|---|---|
| 27 | Cloud & Virtual Networking | [Overview](lectures/lecture-27-cloud-virtual-networking/) · [Worksheet](lectures/lecture-27-cloud-virtual-networking/worksheet.md) |
| 28 | Data-Plane & SDN: Programmable Networks | [Overview](lectures/lecture-28-sdn/) · [Worksheet](lectures/lecture-28-sdn/worksheet.md) |
| 29 | Monitoring, Telemetry & Systematic Troubleshooting | [Overview](lectures/lecture-29-monitoring-operations/) · [Worksheet](lectures/lecture-29-monitoring-operations/worksheet.md) |

### Module 8 — Integration & Capstone · L30–L32
*Enterprise wireless and mobile networking, full-network design, and the capstone
workshop and defense.*

| # | Lecture | Materials |
|---|---|---|
| 30 | Mobile & Wireless Enterprise Networking | [Overview](lectures/lecture-30-mobile-wireless-enterprise/) · [Worksheet](lectures/lecture-30-mobile-wireless-enterprise/worksheet.md) |
| 31 | Enterprise Design & the Data-Science Connection | [Overview](lectures/lecture-31-enterprise-design-capstone-kickoff/) · [Worksheet](lectures/lecture-31-enterprise-design-capstone-kickoff/worksheet.md) |
| 32 | Capstone Workshop, Presentations & Course Synthesis | [Overview](lectures/lecture-32-capstone-clinic-synthesis/) · [Worksheet](lectures/lecture-32-capstone-clinic-synthesis/worksheet.md) |

---

## Lecture materials

Every lecture package contains:

| File | What's in it |
|---|---|
| **Overview** (`README.md`) | Learning outcomes, prerequisites, how the lecture connects to labs and cases |
| **Worksheet** (`worksheet.md`) | In-class exercises and an exit ticket — print or copy and work through |
| **Notes** (`notes.md`) | Concept explanations, definitions, worked examples, diagrams, and the instructor's 120-minute plan — the fullest treatment of each topic, and your best friend when you miss a lecture |
| **Slides** (`slides.md`) | The deck used in class; each slide is followed by speaker notes |

- **Instructor-only material** (answer keys, exercise solutions, exam papers) lives in
  separate files (`instructor.md`, `*-instructor.md`, fenced key sections, case-study
  instructor halves). The published course website excludes it automatically; on GitHub
  it is always clearly labeled. Teaching plans and prep checklists are embedded in each
  `notes.md` alongside the student-readable explanations.

Self-study aids:

- [Module review questions with answers](assessments/README.md#1-what-lives-here) — self-check after each module
- [65 practice case studies](case-studies/README.md) — diagnostic reasoning practice
- [Question banks](assessments/README.md#1-what-lives-here) — extra practice by question type

---

## 🧪 Practical laboratories

A 16-lab workbook runs alongside the lectures in a weekly 2-hour block — reproducible,
safe, and entirely on free software:

- **Measure** latency and throughput (`ping`, `traceroute`, `iperf3`) — [LAB-01](labs/lab-01-latency-throughput/)
- **Build** switched networks with VLANs and verify with Wireshark — [LAB-02](labs/lab-02-switching-vlans/)
- **Survey** real Wi-Fi networks (passive, permission-based) — [LAB-03](labs/lab-03-wifi-survey/)
- **Design** subnets and address plans — [LAB-04](labs/lab-04-subnetting-design/)
- **Configure** DHCP and NAT on a Linux router — [LAB-05](labs/lab-05-dhcp-nat-router/)
- **Run** dual-stack IPv4/IPv6 and static routing labs — [LAB-06](labs/lab-06-dual-stack/) · [LAB-07](labs/lab-07-static-routing/)
- **Write** UDP client/server programs in Python, then measure TCP under
  induced delay and loss (`netem`) — [LAB-08](labs/lab-08-udp-sockets/) · [LAB-09](labs/lab-09-tcp-netem/)
- **Implement** your own reliable transport protocol over UDP — [LAB-10](labs/lab-10-reliable-design/) · [LAB-11](labs/lab-11-reliable-implement/)
- **Dissect** HTTP/1.1 vs HTTP/2 vs HTTP/3, SMTP, and SSH — [LAB-12](labs/lab-12-app-protocols/)
- **Configure** firewalls and a site-to-site VPN — [LAB-13](labs/lab-13-firewall-vpn/)
- **Monitor** a network and inject faults to practice diagnosis — [LAB-14](labs/lab-14-monitoring-faults/)
- Optional extensions: [security analysis](labs/lab-15-security-analysis/) and a
  [capstone design rehearsal](labs/lab-16-design-rehearsal/)

**Before your first lab:** read the [safety and ethics rules](labs/syllabus-safety.md)
(all experimentation happens in isolated VMs/namespaces against course-owned targets;
captures on shared networks are observation-only) and follow the
[setup guide](labs/setup-environment.md) — three supported routes, including a
no-VM namespaces-only option. Every lab lists expected observations, troubleshooting
tips, and low-resource alternatives.

---

## 🧩 Problem-solving case studies

Real network work is diagnosis: given symptoms and evidence, form hypotheses, test
them, and justify a conclusion. This course trains that explicitly with **65 practice
cases** ([PB-001…PB-065](case-studies/README.md)), two or more per lecture, in four
difficulty levels:

- **Beginner** — single-mechanism reasoning from given facts
- **Intermediate** — weigh 2–3 candidate causes, do the math, spot the red herring
- **Advanced** — incomplete or conflicting evidence: decide *what to measure next*
- **Expert** — open-ended design and trade-off defense

Each case gives you a scenario, labeled evidence, constraints, and questions; work
them in pairs in lecture slots, in tutorials, or as exam preparation (the later
cases deliberately mirror exam-style vignettes). Data-science–flagged cases rehearse
transfer math, telemetry reasoning, and measurement bias.

Browse by lecture, difficulty, or topic in the [case study index](case-studies/README.md#6-index--by-lecture).
The four **graded** Meridian cases (CS-01…CS-04) run across the semester as part of
the assessment plan (see [`docs/case-study-strategy.md`](docs/case-study-strategy.md)).

---

## 📝 Assessments and assignments

Full structure and the marking conventions: [Assessment package](assessments/README.md).
All weightings are the **proposed plan** pending institutional approval.

| Instrument | Where |
|---|---|
| Weekly formative quizzes (16, with self-check value) | [quizzes/](assessments/quizzes/) |
| Module review questions (self-study, with answers) | [review/](assessments/review/) |
| Subnetting problem set (assignment) | [assignment brief](assessments/assignments/subnetting-problem-set-student.md) |
| Reliable-transport project (pair project) | [assignment brief](assessments/assignments/reliable-transport-project-student.md) |
| Midterm and final exam preparation | [exams/](assessments/exams/) — student papers; instructor versions withheld |
| Practical work & capstone rubrics | [rubrics/](assessments/rubrics/) — know how you're graded |
| Rules on collaboration and AI use | [academic integrity](assessments/academic-integrity.md) |

The **capstone** (Modules 7–8) ties the course together: teams design, build, secure,
and instrument a small multi-network solution, then defend it — graded with the
[capstone rubric](assessments/rubrics/capstone-rubric.md). Solutions and marking keys
are instructor-only and are not published on the course website.

---

## 📅 Semester calendar

The 32-lecture schedule, modules, lab and assessment milestones — configurable per
semester, with **no invented institutional dates**:

- Online: [Semester calendar](site-src/calendar.md) on the course website (printable;
  downloadable `calendar.ics` / `calendar.csv` for your own calendar app)
- Configuration and maintenance: [`site-src/_calendar.yml`](site-src/_calendar.yml),
  documented in the [calendar guide](docs/calendar-guide.md)

---

## 🗺️ Recommended learning path

**Studying with this repository (independently or in a course):**

1. **Read the [course overview](docs/syllabus.md)** and check the
   [prerequisites](docs/prerequisites.md) — remediation links are there if you need them.
2. **Work through the lectures in order.** Start each with the overview, read the
   notes, then attempt the worksheet *before* looking anything up.
3. **Do the labs.** Set up your environment once ([setup guide](labs/setup-environment.md)),
   then run each lab when the matching lecture appears in the
   [calendar](site-src/calendar.md). Doing is where networking sticks.
4. **Solve the case studies** for each lecture — pairs work best. Struggle first; the
   reasoning process in each case teaches the method.
5. **Self-check with review questions and quizzes** ([review/](assessments/review/),
   [quizzes/](assessments/quizzes/)) after every module.
6. **Attempt the assignments** ([subnetting set](assessments/assignments/subnetting-problem-set-student.md),
   [reliable-transport project](assessments/assignments/reliable-transport-project-student.md))
   — they're the course's two signature skills.
7. **Finish with the capstone**: design, build, and defend a small network, using the
   [rubric](assessments/rubrics/capstone-rubric.md) as your checklist.
8. **Go deeper with the [references](docs/textbooks-references.md)** — the primary
   textbook (Peterson & Davie) is free to read online in full.

---

## 🛠️ Tools and environment

All free; full install guidance in the [lab setup guide](labs/setup-environment.md),
with a self-check script (`tools/scripts/check_lab_env.py`).

| Tool | Used for | Where |
|---|---|---|
| [Wireshark](https://www.wireshark.org/) | Packet capture and dissection — the course's microscope | Nearly every lab and many lectures |
| Linux (Ubuntu LTS) + `iproute2` | Namespaces, bridges, VLANs, routing — the course's laboratory bench | Most labs |
| Python 3.10+ (standard library) | Socket programming, measurement scripts, subnet tooling | LAB-08…LAB-11, GA-03 |
| `iperf3`, `ping`, `traceroute`, `mtr` | Measurement — throughput, latency, path | LAB-01, LAB-09 |
| `tcpdump` / `tshark` | Command-line captures | Capture-heavy labs |
| `dnsmasq`, `nftables`, `netem (tc)` | DHCP/NAT services, firewall policy, induced delay/loss | LAB-05, LAB-13, LAB-09 |
| VirtualBox or VMware Player (free tiers) | Running the course VM | VM-route labs |
| GNS3 / Cisco Packet Tracer *(optional)* | Multi-router visualization where licensed/available | Optional alternatives only |

**Platform note:** the namespaces-based labs need Linux (via the course VM on
Windows/macOS). Every lab lists a documented alternative if hardware or licensing is
missing — no paid software is required.

---

## 📚 References and further reading

Full annotated list with verification flags: [`docs/textbooks-references.md`](docs/textbooks-references.md).

- **Primary text:** Peterson & Davie, *Computer Networks: A Systems Approach* —
  **free to read online** at <https://systemsapproach.org>
- **Also used:** Kurose & Ross, *Computer Networking: A Top-Down Approach* (8th ed.)
- **Free references:** [The TCP/IP Guide](https://www.tcpipguide.com) ·
  [High Performance Browser Networking](https://hpbn.co)
- **Primary standards:** [IETF RFCs](https://www.rfc-editor.org) — cited per lecture
  (e.g., RFC 9293 for TCP, RFC 8200 for IPv6, RFC 9110–9114 for HTTP) — and IEEE 802
  standards for LAN/wireless
- Every standards-sensitive claim in the course cites one of these sources; nothing
  fabricated, and edition-check items are flagged ⚠ for the instructor

---

## 🧑‍🏫 For instructors

The repository is a complete teaching package, not just student notes:

- **Teaching structure:** [`docs/teaching-methodology.md`](docs/teaching-methodology.md)
  (lecture pattern, two-audience design, misconception register) and the
  [120-minute plans](docs/schedule-32-lectures.md#teaching-pattern)
- **Instructor-only material:** per-lab solution guides (`labs/<lab>/instructor.md`),
  exam/assignment instructor papers (`assessments/**/*-instructor.md`), and fenced
  `INSTRUCTOR KEY` sections in quizzes/banks/cases. Teaching plans, misconceptions
  registers, and prep checklists live inside each lecture's `notes.md`.
- **Semester setup:** [calendar configuration](docs/calendar-guide.md),
  [assessment strategy](docs/assessment-strategy.md), and the
  [review workflow](docs/contributing-instructor-review.md) — including the
  ⚠-flagged items that need verification each semester
- **Quality record:** audit reports under [`docs/audit-reports/`](docs/audit-reports/)
- **Adapting the course:** lecture packages are self-contained and sequenced
  dependency-first (see the [schedule's dependency map](docs/schedule-32-lectures.md#progression--dependency-map));
  the site build ([`tools/scripts/build_site_docs.py`](tools/scripts/build_site_docs.py))
  publishes student-facing pages and excludes instructor-only files
- **Reporting issues:** open a GitHub issue or a pull request (see
  [Contributing](#contributing-and-usage))

---

## Contributing and usage

- **Corrections and improvements are welcome** — typo fixes, clearer explanations,
  better exercises. Open an issue describing the problem, or submit a pull request;
  technical claims should carry a named source (RFC, standard, or textbook), and no
  fabricated evidence (captures, logs, measurements) may be introduced.
- **Status:** this is a draft v0.1 course under active instructor review. Content is
  sound and machine-audited (see the audit reports), but institutional decisions
  (weightings, calendar dates, editions) remain flagged ⚠ pending instructor approval.
- **License:** no license has been chosen yet. All rights reserved by default —
  reuse beyond reading requires the author's permission until a license is added.
- **Attribution:** diagrams are original to this course (Mermaid/ASCII) and must not
  be replaced with copyrighted textbook figures; cited sources are credited on the
  [References page](site-src/references.md).

---

## Repository & website

| | |
|---|---|
| **Course website** | <https://nadeem-majeedch.github.io/Computer-Networks/> — all student-facing materials, searchable, with diagrams and a printable calendar |
| **Repository** | <https://github.com/nadeem-majeedch/Computer-Networks> — every source file, including instructor materials |

**How the site is built:** a generator ([`tools/scripts/build_site_docs.py`](tools/scripts/build_site_docs.py))
mirrors the course sources into the MkDocs Material site — student-visible pages only —
and GitHub Actions builds and deploys it on push to `main`
([workflow](.github/workflows/deploy-pages.yml)). To rebuild locally:
`pip install -r requirements.txt`, then `python tools/scripts/build_site_docs.py && mkdocs build --strict`.

<details>
<summary><strong>For maintainers: deployment reference</strong> (click to expand)</summary>

1. Commit and push to `main` (the workflow does the rest).
2. GitHub → Settings → Pages → Source: **GitHub Actions**.
3. Watch the *Deploy GitHub Pages* workflow run (Actions tab); it must finish green.
4. Verify <https://nadeem-majeedch.github.io/Computer-Networks/> in a private window.
Full details and the validation record:
[`docs-meta/github-pages-deployment-report.md`](docs-meta/github-pages-deployment-report.md).

</details>

---

*Course materials prepared as an open educational resource for undergraduate
Computer Science and Data Science teaching. Standards cited: IETF RFCs and IEEE 802
series — see the [References](site-src/references.md) page for full attribution.*
