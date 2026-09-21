# LAB-06 — Instructor Guide

## Setup (before session)
- Verify the T0 block; the deliberate typo line (v4 address applied to `x-a` in v4v6b's
  netns context) is a designed debugging moment — keep it, but flag in session that it is
  intentional so it does not consume 20 minutes of panic. Students who document the fix
  (README troubleshooting row exists for it) earn the debugging note in their report.
- Pre-capture `lab06-nd.pcapng` for the offline route.

## Solutions / expected values
- **Pre-lab 1:** e.g. fd00:lab:1::/64 (or fd12:3456:789a::/64 — any fd00::/8 ULA); one host
  e.g. fd00:lab:1::a/64.
- **Pre-lab 2:** NS=135, NA=136; target = solicited-node multicast ff02::1:ffXX:XXXX
  (low 24 bits of the unicast).
- **Pre-lab 3:** fe80::/10; used for on-link control (NDP, RAs) and next-hop reachability.
- **T1:** ARP: L2 broadcast, all stations wake, Ethertype 0x0806, no IP header. NS:
  ICMPv6 inside v6, multicast MAC 33:33:xx:xx:xx:xx derived from the solicited-node group;
  only the interface owning that suffix listens.
- **T2:** forcing works; unforced depends on resolver/OS (RFC 6724) — the *recorded*
  behavior is the deliverable, no single right answer.
- **T3:** hop limit 64 on echoes (typical Linux default); NDP needs no ARP because it rides
  ICMPv6/multicast natively.
- **Post-lab 4:** fe80:: is required for NDP/RAs and as next-hop (gateway) addressing —
  it is the control plane of every IPv6 link.

## Common failure modes
1. Students delete the "typo" silently and never mention it — the report loses its
   debugging narrative (deduct clarity, not correctness).
2. `ping` unforced resolves nothing (no naming) and students claim v6 "lost" — guide to
   T2's forcing distinction.
3. Stale NDP cache hides NS — flush first (README covers).

## Grading notes
- Correct results (40): T0 four-address verification + T1 frame-number citations.
- Analysis (30): ARP-vs-NDP table with *structural* differences (not "one is v4, one v6").
- Reproducibility (20): command transcript + capture file.
- The typo diagnosis counts under analysis if documented (it is a listed row).
