---
title: References
icon: material/library
---

# References & Attribution

Nothing on this site is a fabricated reference. Every standards-sensitive claim in
the course traces to one of the sources below, and instructor-verify items are
flagged in place with ⚠.

## Primary textbooks

| Abbrev. | Work | Used for |
|---|---|---|
| **PD** | Peterson & Davie, *Computer Networks: A Systems Approach* (5th/6th ed.) | Course spine: layering, internetworking, transport, applications |
| **KR** | Kurose & Ross, *Computer Networking: A Top-Down Approach* (7th/8th ed.) | Application-layer, transport, and security treatments |
| **TW** | Tanenbaum & Wetherall, *Computer Networks* (5th ed.) | Physical layer, data link, classic examples |

!!! warning "Edition verification"

    Section numbers cited in lectures and decks (e.g., "PD §4.3") must be
    re-verified against the instructor's chosen edition before publication —
    they are flagged ⚠ in place for exactly this reason.

## Standards & official documentation

| Body / series | Where the course relies on it |
|---|---|
| **IEEE 802.3** | Ethernet frame formats, media, speeds (L07–L08) |
| **IEEE 802.1Q / 802.1D / 802.1X** | VLAN tagging, STP purpose, port authentication (L09, L11) |
| **IEEE 802.11 / 802.11r·k·v·i** | Wi-Fi fundamentals, fast transition, WPA (L10–L11, L30) |
| **IETF RFCs** | Protocol behaviors throughout — the RFC series cited per lecture: |
| RFC 791 / 792 / 826 / 950 | IPv4, ICMP, ARP, subnetting (L12, L16) |
| RFC 1918 / 3022 | Private address space, NAT (L14) |
| RFC 2131 / 3046 | DHCP semantics and relaying (L14, L22) |
| RFC 4291 / 4861 / 4862 / 5952 / 7348 | IPv6 addressing, NDP, SLAAC, text representation; VXLAN for overlay concepts (L15, L27) |
| RFC 3021 | /31 point-to-point links (L12, L13) |
| RFC 768 / 9293 | UDP; TCP (consolidated) (L17, L18–L20) |
| RFC 5681 / 6298 | TCP congestion control; RTO (L19–L20) |
| RFC 1034 / 1035 / 2181 | DNS and TTL semantics (L21) |
| RFC 9110 / 9112 / 7540 / 9000 | HTTP semantics; HTTP/2; QUIC (L23) |
| RFC 5321 / 4251 | SMTP; SSH architecture (L23) |
| RFC 8446 / 5280 | TLS 1.3; certificates (L24) |
| RFC 7011 | IPFIX/flow records concept (L29) |
| RFC 1958 | Internet architectural principles (L01) |
| **NIST** | SP 800-41 (firewall policy concepts), Cybersecurity Framework (control categories) (L25–L26) |
| **ONF** | SDN architecture primer (concepts) (L28) |

## Tools & software

Wireshark, tcpdump, iperf3, Python's standard library, Linux networking
(`iproute2`), nftables, dnsmasq, and netem are used in labs; each lab package
documents its own tool list and version-verification item. Tool documentation is
linked from [the lab index](labs/README.md).

## Attribution policy

- Course materials are original; diagrams are drawn for this course (Mermaid/ASCII)
  and must not be replaced with copyrighted textbook figures.
- Short quotations remain within fair-use norms and name their source.
- When reusing this course, keep these attributions and the ⚠ flags that mark what
  an instructor must verify.
- Instructor-facing references policy (no fabricated references, no invented
  results): [docs/contributing-instructor-review.md](docs/contributing-instructor-review.md).
