# Labs — Workbook for the Computer Networks Course

| Field | Value |
|---|---|
| Status | Draft v0.1 — awaiting instructor review |
| Scope | 16 progressively difficult labs aligned to the 32-lecture curriculum |
| Start here | [`syllabus-safety.md`](syllabus-safety.md) → [`setup-environment.md`](setup-environment.md) → `LAB-01` |
| Audit | `python3 tools/scripts/audit_labs.py` (structure, cross-references, graded-set consistency) · `python3 tools/scripts/check_lab_syntax.py` (fenced-command syntax) · `python3 tools/scripts/check_lab_env.py` (host tool inventory) |

## Package layout (uniform per lab)

```
labs/lab-NN-short-name/
├── README.md        # student-facing: outcomes, pre-lab, tasks, expected observations,
│                    # post-lab questions, challenge task, troubleshooting, alternatives
├── instructor.md    # solution guide, timing, rubric application notes, common failure modes
└── worksheet.md     # print/fill worksheet: pre-lab answers, task records, exit questions
```

Every lab README carries: lecture + CLO mapping · learning outcomes · prerequisites ·
estimated duration · accessibility/low-resource alternatives · safety notes · **expected
observations are described from tool semantics and named as such — never claimed as
executed output** (see the verification report).

## 1. Safety and ethics (read first)

All attack-technique work happens inside isolated course VMs/namespaces against course-owned
targets; passive captures on shared networks are observation-only; students sign the ethics
gate before LAB-01. Full rules: [`syllabus-safety.md`](syllabus-safety.md) §3.

## 2. Lab inventory

| ID | Lab | Lectures | CLOs | Environment | Tools | Difficulty | Graded |
|---|---|---|---|---|---|---|---|
| LAB-01 | [Latency & throughput](lab-01-latency-throughput/) | L04 | CLO5, CLO6 | Host + VM | ping, traceroute, iperf3, tcpdump | ● | Yes (15%) |
| LAB-02 | [Switched lab with VLANs](lab-02-switching-vlans/) | L08–L09 | CLO2, CLO6 | VMs/simulator | bridge, VLANs, Wireshark | ●● | Yes |
| LAB-03 | [Wi-Fi survey & association](lab-03-wifi-survey/) | L10–L11 | CLO2, CLO7 | Host + own Wi-Fi | Wireshark, `iw` | ●● | Yes (write-up) |
| LAB-04 | [Subnetting drills & design](lab-04-subnetting-design/) | L13–L16 | CLO3 | Paper + VM check | Python `ipaddress`, ip calc | ●● | Yes (5% instrument) |
| LAB-05 | [DHCP & NAT Linux router](lab-05-dhcp-nat-router/) | L14 | CLO3, CLO5 | VMs | dnsmasq, nftables, tcpdump | ●● | Yes |
| LAB-06 | [Dual-stack IPv4/IPv6](lab-06-dual-stack/) | L15 | CLO3, CLO4 | VMs/namespaces | ip, tcpdump, ping6 | ●● | Yes |
| LAB-07 | [Static routing & traceroute](lab-07-static-routing/) | L16 | CLO3, CLO6 | 3 namespaces (+GNS3 optional) | ip route, traceroute | ●●● | Yes |
| LAB-08 | [UDP client & server](lab-08-udp-sockets/) | L17 | CLO4, CLO5 | VM/namespace | Python sockets, tcpdump | ●● | Yes |
| LAB-09 | [TCP under netem](lab-09-tcp-netem/) | L19 | CLO5, CLO6 | Namespaces | iperf3, tc netem, ss | ●●● | Yes |
| LAB-10 | [Reliable transport — design](lab-10-reliable-design/) | L20 | CLO4–CLO6 | Paper + discussion | — | ●●● | Spec (10% milestone) |
| LAB-11 | [Reliable transport — implement](lab-11-reliable-implement/) | L20 (demo W12) | CLO4–CLO6 | VM/namespaces | Python sockets, netem | ●●●● | Code+demo (with LAB-10 = 10%) |
| LAB-12 | [HTTP/1.1 vs H2 vs H3 + SMTP/SSH](lab-12-app-protocols/) | L23 | CLO4, CLO7 | VM | curl, tshark, openssl s_client | ●● | Yes |
| LAB-13 | [Firewall policy & site-to-site VPN](lab-13-firewall-vpn/) | L25 | CLO7, CLO6 | 2 namespaces | nftables, OpenVPN | ●●● | Yes |
| LAB-14 | [Monitoring & fault injection](lab-14-monitoring-faults/) | L29 | CLO6, CLO7 | Namespaces | snmp/snmpget, netem, Python TSDB | ●●● | Yes |
| LAB-15 | [Security analysis, safely](lab-15-security-analysis/) | L24–L26 | CLO7 | Namespaces, offline captures | Python sockets, tshark | ●●● | **Optional (recognition)** |
| LAB-16 | [Design capstone rehearsal](lab-16-design-rehearsal/) | L31–L32 | CLO3, CLO6, CLO8 | Paper + namespaces | ip, python `ipaddress` | ●●● | **Optional (recognition)** |

Difficulty ●→●●●●. The 13 graded deliverables (drop lowest) and the 10% LAB-10/11 project
follow [`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) §3; LAB-15/16 are
this workbook's optional extensions with zero course weight unless the instructor changes
the assessment map first.

## 3. Topic coverage map (task requirement → labs)

| Required topic | Labs |
|---|---|
| Network inspection | 01, 03, 12, 14 |
| IP addressing & subnetting | 04, 05, 06, 07, 16 |
| Packet capture & protocol analysis | 01, 02, 03, 08, 09, 12 |
| Ethernet & ARP | 02, 05, 06 |
| DNS & DHCP | 05, 12 (DNS), 06 (RAs) |
| TCP & UDP | 08, 09, 10, 11 |
| Routing concepts | 06, 07 |
| VLANs & segmentation (simulation) | 02, 13, 16 |
| Network troubleshooting | 05, 07, 09, 14, 16 |
| Python client–server networking | 08, 10, 11 |
| Security analysis (safe) | 12 (TLS), 13 (policy), 15 |
| Network design | 04 (design exercise), 16 |

## 4. Session pattern, submission, rubric

Standard 2-hour pattern, uniform submission format, and the 100-point rubric live in
[`syllabus-safety.md`](syllabus-safety.md) §4–§6 (inherited unchanged from
[`../docs/lab-strategy.md`](../docs/lab-strategy.md) so the audit can check consistency).
