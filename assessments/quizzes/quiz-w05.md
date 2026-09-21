# Weekly Quiz — Week 05 (L09, L10)

| Field | Value |
|---|---|
| Coverage | L09 — VLANs & L2 segmentation · L10 — Wi-Fi fundamentals |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO2|L09]** What does an 802.1Q tag add to a frame, which two fields matter most
to a switch, and where in the frame is it inserted?

**Q2 [I|CLO2|L09]** Explain in two sentences why splitting one physical switch into two
VLANs reduces both broadcast load and attack surface.

**Q3 [I|CLO2|L09]** A printer on port 7 must serve VLAN 20 clients only; the switch's
port 1 uplink to the router carries all VLANs. Classify both ports (access/trunk) and
state the tagging behavior of each.

**Q4 [B|CLO2|L10]** Give the classic 2.4 GHz vs 5 GHz trade-off pair (range vs
capacity/interference) and one reason from physics for each side.

**Q5 [I|CLO4|L10]** Distinguish SSID from BSSID. Which one does a client actually
associate to, and what does the AP's beacon advertise?

**Q6 [I|CLO6|L09]** Two PCs on the same switch are configured into different VLANs but
share the same IPv4 subnet. Predict the exact failure at Layer 2 and name the correct
fix (one sentence each).

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** A 4-byte 802.1Q header (TPID 0x8100 + TCI: PCP/DEI + **VLAN ID**) inserted after
the source MAC field; VLAN ID selects the frame's VLAN, PCP drives priority handling. [B·CLO2]

**Q2.** Broadcast frames are confined per-VLAN, so VLAN 10's ARP/DHCP chatter no longer
reaches VLAN 20 hosts. Attack surface shrinks because Layer-2 attack traffic (e.g.,
flooding, sniffing of others' frames) is similarly confined; reaching the other VLAN now
requires passing a router/firewall. [I·CLO2]

**Q3.** Port 7: **access** port — sends/receives untagged frames, all mapped to VLAN 20.
Port 1: **trunk** — carries tagged frames for multiple VLANs (untagged arrivals map to
its native VLAN). [I·CLO2]

**Q4.** 2.4 GHz: better range/wall penetration (lower frequency attenuates less) but
fewer non-overlapping channels and more interference (crowded band, microwave/ISM
noise). 5 GHz: more channels and wider channels → higher capacity, shorter range
(higher path loss through obstacles). [B·CLO2]

**Q5.** SSID is the logical network name advertised; BSSID is the AP radio's MAC address
for one cell. The client associates to the **BSSID** (an AP radio) after choosing an
SSID; beacons advertise SSID, supported rates/capabilities, and carry the BSSID. [I·CLO4]

**Q6.** Failure: the switch will not bridge frames across VLANs, so ARP requests from
one PC never reach the other — no Layer-2 path exists even though IPs look "same
network." Fix: either place both in one VLAN, or keep VLANs and give each VLAN its own
subnet with a router (L3) path between them. Accept either with correct reasoning. [I·CLO6]
