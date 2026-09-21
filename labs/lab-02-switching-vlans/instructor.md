# LAB-02 — Instructor Guide

## Setup (before session)
- Test the T0 script on the teaching image **the week before**; netns + bridge + vlan_filtering
  is the exact stack LAB-06/07/13 reuse. Keep a teardown helper ready:
  `for h in h1 h2 h3 h4; do sudo ip netns del $h; done; sudo ip link del br0; sudo ip link del br1; sudo ip link del tr0`
- Offline bundle `lab02-tagged.pcapng`: capture ~10 tagged + ~10 untagged frames yourself from
  the working topology and save for the no-root route (label them clearly).
- ⚠ Verify on the teaching kernel: some older kernels need `bridge vlan del vid 1` handled
  differently; if `del vid 1` errors, it is non-fatal for this lab — note it in session.

## Solutions / expected values
- **Pre-lab 1:** flood — copy out all ports in the same VLAN except the ingress port.
- **Pre-lab 2:** untagged; trunk carries many (here 2: 10 and 20).
- **Pre-lab 3:** fails — ARP broadcast confined to VLAN 10; h2 (VLAN 20) never receives it.
- **T1:** h1↔h3 succeeds; h1↔h2 fails at ARP (no reply). The failing *packet* is the ARP
  request; there is no reply to time out on — capture proves silence.
- **T2:** p-h2 capture: empty (broadcast did not cross VLANs). tr0 capture: `vlan 10` frames
  during h1→h3; FDB shows h1's MAC on p-h1 (and h3's on p-h3) after the exchange.
- **T3:** Wireshark on tr0 shows `802.1Q Virtual LAN` layer, TPID 0x8100, VID 10; host-side
  access-port capture shows the frame without that layer.
- **Post-lab 4:** tags are added/removed at the edge (access ports) so end hosts stay simple;
  keeps the tag hop-count/VLAN logic inside the switched core.

## Common failure modes
1. Students skip `lo up` inside netns — ping to own IP fails, panic ensues. (Add to setup.)
2. Trunk veths created but never enslaved to the bridges → "same-bridge works, cross-bridge
   doesn't." Diagnose with `ip link show master br0`.
3. Capturing on the wrong end: tcpdump on `v-h1` (inside netns) vs `p-h1` (bridge port) see
   different tagging — a *feature* worth 2 minutes of discussion (egress untagging).
4. Two pairs per machine forgetting teardown → stale netns names; run the teardown helper
   between groups.

## Grading notes
- Correct results (40): T1 pattern table + T2 capture evidence (named files).
- Analysis (30): post-lab 1–2 must cite *their* captures; "broadcast domain" language from L09.
- Reproducibility (20): exact `bridge vlan add` lines present (not "configured VLANs").
- Pairs submit one report; both names; individual viva question at demo time optional.
