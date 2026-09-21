# Prerequisites and Entry Skills

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companion | [`syllabus.md`](syllabus.md) |

## 1. Required prior coursework

| Prior course | Requirement level | Why it matters here |
|---|---|---|
| Programming Fundamentals (CS1) — Python or C | **Required (completed)** | Labs are in Python; students must write functions, use dictionaries/lists, read files, and follow a program skeleton without step-by-step hand-holding |
| Object-Oriented Programming / CS2 | **Required (completed)** | The reliable-transport project and socket labs involve multiple cooperating classes/modules; students need basic program decomposition skills |
| Discrete Mathematics | **Required (completed)** | Subnetting and CIDR are binary-arithmetic and set reasoning; counting, powers of two, and modular thinking are used weekly from L13 onward |
| Digital Logic / Computer Organization (concurrent OK) | **Required (completed or concurrent)** | Bits, bytes, endianness, binary/hex conversion, and basic signal intuition are assumed in Module 2 |
| Operating Systems (concurrent OK) | **Recommended (concurrent acceptable)** | Process/socket concepts, file descriptors, and virtualization help in Modules 4–5; only basic familiarity is needed by L17 |

## 2. Entry skills checklist (student self-assessment)

A student is ready for this course if they can, without help:

- [ ] Convert between decimal, binary, and hexadecimal for 8- and 32-bit values
- [ ] Write, run, and debug a ~100-line Python program (functions, loops, dicts, file I/O)
- [ ] Use a Linux shell: navigate directories, edit a file, run a command with flags, read a man page
- [ ] Explain what an IP address and a URL are at a user level (no technical depth required)
- [ ] Install software on their own laptop or administer their own VM

Students weak on the first three items should complete the remediation resources below in
week 0. The course does **not** teach programming or Linux basics.

## 3. Remediation resources (week 0, optional, ungraded)

- Python refresher: the official tutorial, chapters 1–5 — <https://docs.python.org/3/tutorial/>
- Linux shell basics: any of the standard intro tutorials; the lab environment ships with a
  cheat sheet. ⚠ VERIFY: pin the specific tutorial and shell version at first delivery.
- Binary arithmetic drills: any reputable practice site; the L13 problem set includes a
  warm-up section.

## 4. Environment requirements

| Requirement | Minimum | Notes |
|---|---|---|
| Laptop | 8 GB RAM, 40 GB free disk, admin rights | Needed for VM labs (Modules 3, 6, 7) |
| Virtualization | VirtualBox or VMware Workstation Player (free tiers) | ⚠ VERIFY: confirm the approved hypervisor and version for your lab image before semester start |
| Wireshark | Current stable release | Used from L01 onward; download from <https://www.wireshark.org/> |
| Python | 3.10+ | Socket and measurement labs |
| Linux VM image | Course-provided Ubuntu LTS image | Ships with `iperf3`, `tcpdump`, `dnsmasq`, `nftables`, `tc/netem`, `dig`, `iproute2` preinstalled |
| Wi-Fi access | A network the student may scan *passively* | LAB-03 uses only passive observation on a network the student controls or has permission to observe — see the ethics note in [`lab-strategy.md`](lab-strategy.md) |
| Cloud account | Free tier (Module 7 GA-27) | Optional if the campus provides an equivalent sandbox; ⚠ VERIFY provider and cost ceiling before promising this |

## 5. Ethics and legality gate (required acknowledgment, week 1)

Students sign an acknowledgment that they will:

1. Capture traffic only on networks they own or have explicit permission to monitor;
2. Never attempt attacks against systems they do not own; all attack-technique exercises run
   inside the course VM lab against course-owned targets;
3. Follow the university's acceptable-use policy at all times.

This gate is a prerequisite for participating in Labs 03, 08–14 and the GA-26 workshop.
