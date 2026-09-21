# LAB-02 — Build a Switched Lab with VLANs

| Field | Value |
|---|---|
| Anchor lectures | L08 (switch learning/flooding), L09 (VLANs: access vs trunk) |
| CLOs | CLO2 (data link), CLO6 (evaluate/troubleshoot) |
| Assessment | Graded lab deliverable (pairs; 15% pool) |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | Linux namespaces + `bridge` with VLAN filtering (route C works fully; no external switch needed). Packet Tracer optional as a *sketch* tool only. |

## Learning outcomes
1. Configure a Linux bridge with VLAN filtering: access ports (untagged) and a trunk port
   (tagged), then verify with captures.
2. Observe switch learning and flooding: predict where an unknown-unicast frame goes,
   then verify from the capture and the bridge's FDB.
3. Demonstrate L2 segmentation: same-VLAN ARP/ICMP works, cross-VLAN does not — and
   explain which layer enforces it.
4. Read an 802.1Q tag in a frame capture (TPID 0x8100, VID) and distinguish tagged vs
   untagged frames on the same wire.

## Pre-lab
1. In L08's switch model: what does a switch do with a frame whose destination MAC is not
   yet in its table? (One line on the worksheet.)
2. Access ports send frames (tagged/untagged)? A trunk carries how many VLANs?
3. Predict: two hosts on different VLANs of the same switch — does ARP between them
   succeed? Why?

## Topology (T0)

```
        h1 (VLAN 10)   h2 (VLAN 20)   h3 (VLAN 10)   h4 (VLAN 20)
          |              |              |              |
        [br0 port 1]   [br0 port 2]   [br1 port 1]   [br1 port 2]
             \             |              |             /
              \         [trunk: br0 p3 ══ br1 p3]     /
               \             (tagged 10,20)          /
                +----------- br0 ═══════ br1 -------+
```

## Tasks

### T0 — Build (25 min, commands verified on Ubuntu 22.04/24.04)
```bash
# hosts as namespaces (root in the lab account):
for h in h1 h2 h3 h4; do sudo ip netns add $h; done
# two bridges acting as two switches:
sudo ip link add br0 type bridge vlan_filtering 1
sudo ip link add br1 type bridge vlan_filtering 1
# veth pairs: one end into the namespace ("host NIC"), other end = bridge port
for h in h1 h2 h3 h4; do
  sudo ip link add v-$h type veth peer name p-$h
  sudo ip link set v-$h netns $h
done
sudo ip link set p-h1 master br0; sudo ip link set p-h2 master br0
sudo ip link set p-h3 master br1; sudo ip link set p-h4 master br1
# trunk between the bridges:
sudo ip link add tr0 type veth peer name tr1
sudo ip link set tr0 master br0; sudo ip link set tr1 master br1
sudo ip link set br0 up; sudo ip link set br1 up
sudo ip link set p-h1 up; sudo ip link set p-h2 up
sudo ip link set p-h3 up; sudo ip link set p-h4 up
sudo ip link set tr0 up; sudo ip link set tr1 up
```
Port VLANs (access = untagged; trunk = tagged):
```bash
sudo bridge vlan del dev p-h1 vid 1
sudo bridge vlan add dev p-h1 vid 10 pvid untagged
sudo bridge vlan del dev p-h2 vid 1
sudo bridge vlan add dev p-h2 vid 20 pvid untagged
sudo bridge vlan del dev p-h3 vid 1
sudo bridge vlan add dev p-h3 vid 10 pvid untagged
sudo bridge vlan del dev p-h4 vid 1
sudo bridge vlan add dev p-h4 vid 20 pvid untagged
sudo bridge vlan add dev tr0 vid 10
sudo bridge vlan add dev tr0 vid 20
sudo bridge vlan add dev tr1 vid 10
sudo bridge vlan add dev tr1 vid 20
```
Addresses inside hosts:
```bash
sudo ip netns exec h1 ip addr add 192.0.2.11/24 dev v-h1
sudo ip netns exec h2 ip addr add 192.0.2.12/24 dev v-h2
sudo ip netns exec h3 ip addr add 192.0.2.13/24 dev v-h3
sudo ip netns exec h4 ip addr add 192.0.2.14/24 dev v-h4
for h in h1 h2 h3 h4; do sudo ip netns exec $h ip link set v-$h up; sudo ip netns exec $h ip link set lo up; done
```

### T1 — Verify L2 connectivity pattern (15 min)
```bash
sudo ip netns exec h1 ping -c3 192.0.2.13    # same VLAN 10, across the trunk
sudo ip netns exec h1 ping -c3 192.0.2.12    # VLAN 10 → VLAN 20
```
**Expected observation:** h1↔h3 works (same VLAN, trunk carries tagged frames between the
bridges); h1↔h2 fails — ARP gets no answer. Explain the failing ARP specifically: broadcast
is confined to the VLAN's broadcast domain, so h2 never hears the request.

### T2 — Watch learning and flooding (15 min)
Start a capture on the trunk and on p-h2, then from h1 ping h3 (clear ARP first:
`sudo ip netns exec h1 ip neigh flush all`).
```bash
sudo tcpdump -i p-h2 -nn -c 8 ether broadcast &   # does h2 hear h1's ARP?
sudo tcpdump -i tr0 -nn -e -c 10 'vlan'           # tagged frames on the trunk
```
**Expected observation:** h2 hears *nothing* (segmentation). On tr0 you see frames with
`vlan 10` in tcpdump's `-e` output. Bridge FDB check: `sudo bridge fdb show | grep -E "p-h1|p-h3"`.
The first packet of a flow after `neigh flush` shows flooding behavior *within* VLAN 10 only.

### T3 — Tag anatomy (10 min)
Capture one cross-trunk frame in Wireshark (capture on tr0 from the host, filter
`vlan`) — identify EtherType 0x8100 (TPID), VID field, and note that the host-side capture
of an *access* port shows the same frame **without** the tag (hosts see untagged frames).
Cross-check with the GA-30/L09 lesson: access = untagged, trunk = tagged.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Nothing pings, even same-bridge | forgot `ip link set ... up` (host end) | `ip netns exec h1 ip link` — v-h1 UP? lo UP? |
| Same-VLAN works, cross-bridge fails | trunk veths not in the bridge / VLANs not added on trunk | `bridge vlan show dev tr0` must list 10 and 20 |
| h1 hears h2's ARP (should not) | VLAN filtering off (`vlan_filtering 0` default when created?) | recreate bridge with `vlan_filtering 1`; `ip -d link show br0` |
| `RTNETLINK answers: Operation not permitted` | lab account lacks sudo/root | use the course VM route (A) or ask for the netns-enabled account |

## Post-lab questions
1. Where exactly does a cross-VLAN ping die — which layer answers (or doesn't), and why?
2. What did the FDB show before/after the first ping? Relate to L08's learn/forward/flood.
3. Your trunk capture shows VID 10 frames. What would break if the trunk only carried VID 20?
4. Why do hosts never see 802.1Q tags on access ports? What that buys the designer.

## Challenge (ungraded)
Move h2 to VLAN 10 via two commands (no cabling changes), then *without* flushing, explain
why h1→h2 now works on the first try (ARP cached? flooded?). Verify with capture.

## Accessibility / low-resource alternatives
- **No root available:** offline bundle `lab02-tagged.pcapng` + `lab02-untagged.pcapng` —
  T2/T3 become guided Wireshark/tshark analysis; T1 answers from a provided command log.
- Packet Tracer alternative (optional, where licensed): build the same two-switch topology
  with two 2960s; the *observations* translate, but you must still answer T3 from the
  provided captures (PT's simulated frames are not a substitute for a real capture).
- tshark equivalents: `tshark -i tr0 -c 10 -Y vlan -T fields -e vlan.id`.

## Safety notes
Entirely inside namespaces (isolated by design — syllabus-safety §3.1). No external
network involvement.
