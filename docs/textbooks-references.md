# Recommended Textbooks and Reference Sources

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companion | [`syllabus.md`](syllabus.md) (weekly reading map) |

All sources below are real, well-known, and verifiable. Nothing here is fabricated.
⚠ VERIFY: confirm the **latest available edition** of each print text when ordering —
new editions appear periodically and section numbers cited in this course refer to the
editions listed.

---

## 1. Required texts (choose per section)

| Text | Authors | Edition used in planning | Why | Notes |
|---|---|---|---|---|
| *Computer Networking: A Top-Down Approach* | J. Kurose, K. Ross | 8th ed., Pearson, 2021 | Primary text (KR). Application-first ordering suits our socket-early start; strong problems | Abbreviated **KR** in the syllabus reading map |
| *Computer Networks: A Systems Approach* | L. Peterson, B. Davie | 6th ed., Morgan Kaufmann, 2019 | Secondary text (PD). **Free to read online** at <https://systemsapproach.org> — guarantees every student access regardless of budget | Abbreviated **PD**; excellent for L2/L3 depth and the SDN chapter |

Both are used; if students may buy only one, KR is the primary and PD is freely available
online in full. ⚠ VERIFY: Kurose & Ross have released a newer edition more recently than
2021 — check before ordering and update the reading map's section numbers.

## 2. Recommended supplementary texts (instructor/library)

| Text | Authors | Use in this course |
|---|---|---|
| *Computer Networks* | A. Tanenbaum, N. Feamster, D. Wetherall, 6th ed., Pearson, 2021 (**T**) | Physical-layer and classic-perspective sections cited in Modules 2–3 |
| *Internetworking with TCP/IP, Volume 1* | D. Comer, 6th ed., Pearson, 2013 | Deeper IPv4/IPv6, routing, and ARP treatment for enrichment and instructor prep |
| *The TCP/IP Guide* | C. Kozierok | Free online reference (<https://www.tcpipguide.com>) for protocol minutiae; friendly explanatory style |
| *High Performance Browser Networking* | I. Grigorik, O'Reilly, 2013 | Free online (<https://hpbn.co>); good for HTTP/2-era performance chapters — note it predates HTTP/3/QUIC finalization, so pair with current sources |

## 3. Standards and primary documents (used as course materials)

These are the authoritative sources; lectures cite them directly.

### IETF RFCs (all free at <https://www.rfc-editor.org>)

| RFC | Topic | Used in |
|---|---|---|
| RFC 1122 | Requirements for Internet hosts — communication layers (layering overview) | L02 |
| RFC 791 | Internet Protocol (IPv4) | L12 |
| RFC 826 | ARP | L12 |
| RFC 792 / RFC 5925† | ICMP / ICMPv6 (with 4443) | L16 |
| RFC 768 | UDP | L17 |
| RFC 9293 | TCP — **note: obsoletes the classic RFC 793 (2022 consolidation)** | L18–L19 |
| RFC 1034, 1035 | DNS concepts and implementation | L21 |
| RFC 2131 | DHCP | L14, L22 |
| RFC 3022 | Traditional NAT | L14 |
| RFC 8200 | IPv6 specification (obsoletes RFC 2460) | L15 |
| RFC 4271 | BGP-4 | L16 (enr) |
| RFC 2328 | OSPFv2 | L16 (enr) |
| RFC 5321 | SMTP | L23 |
| RFC 9110 / 9112 | HTTP semantics / HTTP/1.1 | L23 |
| RFC 9113 / 9114 | HTTP/2 / HTTP/3 | L23 (enr) |
| RFC 9000 | QUIC | L17, L20, L23 (enr) |
| RFC 8446 | TLS 1.3 | L24 |
| RFC 4941 | IPv6 privacy extensions (enr) | L15 |

† Correction note: ICMPv6 is RFC 4443; the table row refers to ICMP (792) core use in L16.

### IEEE and other bodies

| Standard | Topic | Used in |
|---|---|---|
| IEEE 802.3 | Ethernet | L07 |
| IEEE 802.1Q | VLANs | L09 |
| IEEE 802.11 | Wi-Fi | L10 |
| IEEE 802.1X | Port-based access control | L11, L25 |
| IANA registries (<https://www.iana.org>) | Port numbers, address allocations | L02, L14, L17 |
| ICANN (<https://www.icann.org>) | Names/numbers governance | L01, L21 |

## 4. Tool documentation (labs)

| Tool | Official documentation |
|---|---|
| Wireshark | <https://www.wireshark.org/docs/> (user guide, sample captures) |
| Python sockets | <https://docs.python.org/3/library/socket.html> and howto |
| iproute2 (`ip`, `tc`) | man pages in the course VM; <https://wiki.linuxfoundation.org/networking/iproute2> |
| netem | <https://wiki.linuxfoundation.org/networking/netem> |
| iperf3 | <https://iperf.fr> (and GitHub releases) |
| nftables | <https://netfilter.org/projects/nftables/> and official wiki |
| tcpdump | <https://www.tcpdump.org/manpages/tcpdump.1.html> |
| dnsmasq | <https://dnsmasq.org> (man page) |
| BIND `dig` | <https://bind9.readthedocs.io> (arm man pages) |

## 5. Datasets and measurement sources (data-science segments)

| Source | Use |
|---|---|
| CAIDA (<https://www.caida.org>) public datasets & tools | L28, L31 telemetry/flow-analysis exercises (instructor-selected, license-checked) |
| M-Lab (<https://www.measurementlab.net>) | Internet measurement data for capacity/forecasting discussion |
| Wireshark sample capture library | GA and exam trace excerpts |

⚠ VERIFY: any dataset used for grading must be checked for license, size, and download
stability at semester start; record the exact file/version in the lab README.

## 6. Reading-map maintenance rules

1. The syllabus reading map uses the abbreviations KR/PD/T defined above.
2. When an edition changes, update section numbers in [`syllabus.md`](syllabus.md) in one
   pass and bump the course version.
3. Never cite a page number in exams without checking the edition in the reading map.
