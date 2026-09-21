# LAB-07 — Static Routing & Traceroute Dissection (3-router topology)

| Field | Value |
|---|---|
| Anchor lectures | L16 (routing, ICMP), L13 (longest-prefix match) |
| CLOs | CLO3 (addressing), CLO6 (evaluate/troubleshoot) |
| Assessment | Graded lab deliverable (pairs; 15% pool) |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | Three router namespaces + two host namespaces (route C); GNS3 optional alternative |

## Learning outcomes
1. Build a 3-router, 2-host topology with forwarded namespaces acting as routers.
2. Configure static routes (and a default) so end-to-end forwarding works — and predict
   each router's decision before testing it.
3. Capture TTL decrements across hops and dissect a traceroute's ICMP/time-exceeded
   mechanism end to end.
4. Apply longest-prefix-match reasoning to a routing table and predict its choice.

## Pre-lab
1. What single `sysctl` turns a Linux namespace into a router?
2. Traceroute (UDP variant): which ICMP message do routers send back, and what field
   makes hop 2 different from hop 1?
3. Two routes match a destination: 10.0.0.0/8 via A and 10.1.0.0/16 via B — which wins,
   and what is the rule called?

## Topology (T0)

```
 hostA ─ [R1: 10.0.1.1 | 10.0.12.1] ── [R2: 10.0.12.2 | 10.0.23.2] ── [R3: 10.0.23.3 | 10.0.2.1] ─ hostB
```

## Tasks

### T0 — Build (25 min)
```bash
for n in R1 R2 R3 hostA hostB; do sudo ip netns add $n; done
# links: a-r1, r1-r2, r2-r3, r3-b
sudo ip link add a1 type veth peer name r1a; sudo ip link set a1 netns hostA; sudo ip link set r1a netns R1
sudo ip link add r12a type veth peer name r12b; sudo ip link set r12a netns R1; sudo ip link set r12b netns R2
sudo ip link add r23a type veth peer name r23b; sudo ip link set r23a netns R2; sudo ip link set r23b netns R3
sudo ip link add b3 type veth peer name r3b; sudo ip link set b3 netns hostB; sudo ip link set r3b netns R3
sudo ip netns exec hostA ip addr add 10.0.1.10/24 dev a1
sudo ip netns exec R1 ip addr add 10.0.1.1/24 dev r1a
sudo ip netns exec R1 ip addr add 10.0.12.1/24 dev r12a
sudo ip netns exec R2 ip addr add 10.0.12.2/24 dev r12b
sudo ip netns exec R2 ip addr add 10.0.23.2/24 dev r23a
sudo ip netns exec R3 ip addr add 10.0.23.3/24 dev r23b
sudo ip netns exec R3 ip addr add 10.0.2.1/24 dev r3b
sudo ip netns exec hostB ip addr add 10.0.2.10/24 dev b3
for i in a1 r1a r12a r12b r23a r23b r3b b3; do sudo ip link set $i up; done
for n in R1 R2 R3; do sudo ip netns exec $n sysctl -w net.ipv4.ip_forward=1; done
for n in hostA hostB; do sudo ip netns exec $n ip link set lo up; done
```
Routes (predict-then-apply; record your predictions first):
```bash
sudo ip netns exec hostA ip route add default via 10.0.1.1
sudo ip netns exec R1   ip route add 10.0.2.0/24 via 10.0.12.2
sudo ip netns exec R3   ip route add 10.0.1.0/24 via 10.0.23.2
sudo ip netns exec hostB ip route add default via 10.0.2.1
# R2 is directly connected to both links — needs nothing extra. Verify that claim.
```

### T1 — Connectivity + the R2 question (15 min)
`sudo ip netns exec hostA ping -c3 10.0.2.10`
**Expected observation:** works. The "R2 needs nothing" claim holds because both its
links are *directly connected* routes (from the /24s). Write R2's two relevant table
entries from `ip netns exec R2 ip route`.

### T2 — TTL on the wire (20 min)
Capture on the R1–R2 link while pinging hostB:
```bash
sudo tcpdump -i r12a -nn -c 6 'icmp' &
sudo ip netns exec hostA ping -c3 10.0.2.10
```
**Expected observation:** TTL 64 (typical Linux default) leaving hostA, 63 on the wire
after R1 (captured on r12a, the *ingress* side of R2 sees 63 — discuss which side shows
what). One paragraph explaining the decrement point per hop (L16).

### T3 — Traceroute dissection (20 min)
```bash
sudo tcpdump -i r12a -nn -c 20 'icmp or udp' -w lab07-tr.pcapng &
sudo ip netns exec hostA traceroute -n 10.0.2.10
```
**Expected observation:** probe 1 (TTL 1) dies at R1 → ICMP time-exceeded (type 11)
sourced from 10.0.1.1; probe 2 (TTL 2) dies at R2 → time-exceeded from 10.0.12.2;
probe 3 reaches hostB. Record each probe's TTL and the returned source — the mechanism,
not just the hop list.

### T4 — Longest-prefix-match drill (15 min)
Add a more-specific route: `sudo ip netns exec R1 ip route add 10.0.2.10/32 via 10.0.12.2`
(then a *wrong-path* variant via a scratch host to prove specificity wins over a working
default). Predict, apply, verify with `ip route get`:
```bash
sudo ip netns exec R1 ip route get 10.0.2.10
```
**Expected observation:** the /32 wins over any shorter match — table shows the chosen
route explicitly.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Ping dies at hop 1 | missing default route on hostA | `ip netns exec hostA ip route` — default present? |
| Ping dies after hop 1 | R1 lacks the 10.0.2.0/24 route | add it; `ip route get` from R1 to verify |
| Forwarding off (silent drop) | `ip_forward=0` in a router ns | re-run the sysctl for all three routers |
| Traceroute shows `*` at hop 2 but ping works | time-exceeded rate-limited/filtered | rerun; rate limiting is itself a reportable observation |

## Post-lab questions
1. Where exactly did the TTL decrement in your T2 capture (which device, which step)?
2. Why must R2 know nothing about 10.0.1.0/24 *here*, and what changes if hostA's subnet
   grows to two /25s?
3. Traceroute's time-exceeded message: who generates it and how does traceroute know to
   stop (three probe lines per hop — what does it look for)?
4. In T4, what made the /32 win — and name one operational *risk* of more-specific routes.

## Challenge (ungraded)
Symmetry check: run traceroute from hostB to hostA. Does the reverse path match? If not,
explain asymmetric routing using your tables (routes are per-direction).

## Accessibility / low-resource alternatives
- Offline bundle `lab07-tr.pcapng` + full command transcript; T2–T4 analysis-only.
- GNS3 alternative (if the class already uses it): same topology with the provided
  addressing; the observations and answers are identical.
- Screen-reader friendly: all text tools.

## Safety notes
Isolated namespaces; documentation ranges only (syllabus-safety §3.1). No external
network involved.
