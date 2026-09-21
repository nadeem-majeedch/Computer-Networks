# LAB-13 — Firewalls & Site-to-Site VPN (nftables + OpenVPN)

| Field | Value |
|---|---|
| Anchor lectures | L25 (firewalls, segmentation, VPNs), L24 (TLS/crypto building blocks) |
| CLOs | CLO7 (threats/defenses), CLO6 (evaluate/troubleshoot) |
| Assessment | Graded lab deliverable (pairs; 15% pool) — report with policy justifications |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | Two namespace "sites" (route C) or 2 VMs; tools: `nftables`, `OpenVPN`, `tcpdump`, `iperf3` |

## Learning outcomes
1. Implement a default-deny stateful firewall policy (nftables) and verify each decision
   with an allowed *and* a blocked flow.
2. Explain stateful filtering from your own observations: the rule that lets replies in
   (established) and what happens without it.
3. Build a site-to-site OpenVPN tunnel between the two sites and demonstrate that the
   traffic between them is encrypted (capture shows TLS-like ciphertext, not your payload).
4. Argue policy trade-offs: your rule order, your logging choices, your VPN's scope.

## Pre-lab
1. Stateful vs stateless: which one needs the "established" rule, and why?
2. L25: what does a VPN add on an untrusted path, and what does it *not* protect against?
3. Why is default-deny preferred over default-allow with blocks? (One design sentence.)

## Topology (T0)

```
 siteA ns ── [fwA ns: nftables] ── (wan link) ── [fwB ns: nftables] ── siteB ns
 10.0.10.0/24        inside           wan 172.16.0.0/24        10.0.20.0/24
                        └──────── OpenVPN site-to-site (tun) ──────┘
```

## Tasks

### T0 — Build (20 min)
Standard veth/netns construction (LAB-07 pattern): two "firewall" namespaces with
`ip_forward=1`, hosts behind them, a WAN link between the firewalls. Record the exact
commands you used (course share script `lab13-build.sh` is allowed — cite it).

### T1 — Baseline: everything flows, everything is visible (10 min)
Ping + iperf3 across the WAN; capture the WAN link and identify your iperf3 payload
bytes in the clear. **This is the "before" picture.**

### T2 — Default-deny policy (25 min)
On fwA:
```bash
sudo ip netns exec fwA nft add table ip lab13
sudo ip netns exec fwA nft add chain ip lab13 input { type filter hook input priority 0 \; policy drop \; }
sudo ip netns exec fwA nft add chain ip lab13 forward { type filter hook forward priority 0 \; policy drop \; }
sudo ip netns exec fwA nft add rule ip lab13 forward ct state established,related accept
sudo ip netns exec fwA nft add rule ip lab13 forward ip saddr 10.0.10.0/24 ip daddr 10.0.20.0/24 icmp type echo-request accept
sudo ip netns exec fwA nft add rule ip lab13 forward ip saddr 10.0.10.0/24 ip daddr 10.0.20.0/24 tcp dport 5201 accept
```
fwB: mirrored rules (its side initiates nothing? your choice — *justify it*).
Verify: hostA→hostB ping works; hostB→hostA ping **fails** (no rule) — and explain the
asymmetry via the established rule for replies.
**Expected observation:** exactly the flows the rules name pass; everything else drops.
Add a counter rule (`counter drop`) and read the counters as your blocked-flow evidence.

### T3 — What statefulness buys (15 min)
Remove the established rule temporarily; ping again. **Expected observation:** the
request goes out, the reply dies at fwA — stateless-ish behavior restored. Restore it.
Two sentences: what `ct state established` checked to admit the reply.

### T4 — Site-to-site OpenVPN (25 min)
Minimal static-key tunnel between fwA and fwB (lab-only key, generated in session):
```bash
# on each firewall ns (adjust remotes/ips):
openvpn --dev tun0 --remote '<peer-wan-ip>' --ifconfig 10.0.99.1 10.0.99.2 \
        --secret lab13.key --cipher AES-256-GCM --daemon
```
Route siteA→siteB via the tunnel (`ip route add 10.0.20.0/24 via 10.0.99.2 dev tun0`
on fwA; mirrored on fwB). Capture the WAN during a hostA→hostB iperf3 run.
**Expected observation:** the WAN shows OpenVPN/UDP ciphertext between the *firewall*
addresses — no readable payload, no visible 10.0.x.x headers. The tunnel's inner packets
are invisible except by size/timing. (Static-key mode is a *teaching* simplification —
L25's TLS-based modes and key management are the production answer; say so in the report.)

### T5 — Policy justification (15 min)
Write the policy table: rule, purpose, what attack it mitigates, what it costs (usability
or perf). This table is the "justifications" deliverable the assessment names.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Everything drops after policy | forgot established rule or wrong inside interface | `nft list ruleset`; add counters to *see* where packets die |
| VPN up but sites unreachable | missing routes via tun0 on the firewalls | `ip route` in both fw ns; also fwB must forward between tun0 and inside |
| OpenVPN key errors | key file copied wrong / permissions | regenerate with `openvpn --genkey secret lab13.key`; copy verbatim to both sides |
| WAN capture shows plaintext payload | traffic is flowing outside the tunnel (route miss) | `ip route get 10.0.20.10` from hostA must show via tun0 |

## Post-lab questions
1. Your blocked-flow counters: which rule caught hostB's ping, and what evidence did you
   submit (counter + capture)?
2. The established rule: state the check it performs, and one attack it *cannot* stop.
3. What does the VPN hide from the WAN observer, and what remains visible (sizes, timing,
   endpoints)? — cite your own capture.
4. Static-key vs TLS-mode VPN: one advantage your lab mode had, one production weakness
   (L25 vocabulary).

## Challenge (ungraded)
Add rate-limiting to the policy (`ct state new limit rate 5/second`) and demonstrate the
limit with a ping burst — measure the drop pattern with the counter rule.

## Accessibility / low-resource alternatives
- Offline route: provided ruleset + capture pair (`lab13-before.pcapng`,
  `lab13-vpn.pcapng`); T1–T4 analysis-only; policy table unchanged.
- Screen-reader friendly: nftables and tcpdump are text tools throughout.

## Safety notes
Firewall changes exist only inside lab namespaces/VMs; never test policies against shared
networks (syllabus-safety §3.1/3.2). The VPN key is lab-internal, regenerated per session.
