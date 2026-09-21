# LAB-06 — Dual Stack: IPv4 + IPv6 Side by Side

| Field | Value |
|---|---|
| Anchor lectures | L15 (IPv6), L12 (ARP → NDP contrast) |
| CLOs | CLO3 (addressing), CLO4 (packet analysis) |
| Assessment | Graded lab deliverable (pairs; 15% pool) |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | Namespaces (route C) or two VMs; tools: `ip`, `tcpdump`, `ping` (v4+v6) |

## Learning outcomes
1. Configure dual-stack interfaces (IPv4 + IPv6 ULA + link-local) and verify both
   protocols coexist on one wire.
2. Observe Neighbor Discovery (NS/NA) and contrast its packet shape with ARP.
3. Demonstrate address *selection*: when both stacks work, which one does the OS pick,
   and how you force the other.
4. Capture and explain an ICMPv6 echo exchange including its hop limit behavior.

## Pre-lab
1. Write a valid ULA prefix (fd00::/8 family) for a lab net and one host address in it.
2. NDP replaces ARP: which ICMPv6 types do NS/NA use, and what *is* the neighbor-solicit
   target (hint: not a broadcast)?
3. What does a link-local address begin with, and when is it used?

## Tasks

### T0 — Build dual-stack pair (20 min)
```bash
sudo ip netns add v4v6a; sudo ip netns add v4v6b
sudo ip link add x-a type veth peer name x-b
sudo ip link set x-a netns v4v6a; sudo ip link set x-b netns v4v6b
sudo ip netns exec v4v6a ip addr add 192.0.2.21/24 dev x-a
sudo ip netns exec v4v6b ip addr add 192.0.2.22/24 dev x-a   # (typo guard: use x-b)
sudo ip netns exec v4v6b ip addr add 192.0.2.22/24 dev x-b
sudo ip netns exec v4v6a ip addr add fd00:lab:1::a/64 dev x-a
sudo ip netns exec v4v6b ip addr add fd00:lab:1::b/64 dev x-b
for i in x-a x-b; do sudo ip link set $i up; done
for n in v4v6a v4v6b; do sudo ip netns exec $n ip link set lo up; done
```
Verify both planes: `sudo ip netns exec v4v6a ip -br addr` shows four addresses
(v4, v6 ULA, v6 link-local fe80::, loopback).

### T1 — NDP vs ARP (25 min)
```bash
sudo tcpdump -i x-b -nn -c 8 'arp or icmp6' -w lab06-nd.pcapng &
sudo ip netns exec v4v6a ping -c1 192.0.2.22           # triggers ARP
sudo ip netns exec v4v6a ping -c1 fd00:lab:1::b        # triggers NS/NA
```
**Expected observation:** ARP is a raw L2 broadcast (Ethertype 0x0806) with no IP header;
NS is ICMPv6 type 135 sent to a **solicited-node multicast** (`ff02::1:ffXX:XXXX`) —
Wireshark names the layers for you. Record the multicast MAC the NS maps to and explain
why only interfaces with that address suffix wake up.

### T2 — Address selection (20 min)
```bash
sudo ip netns exec v4v6a ping -c2 '<peer-name>' 2>/dev/null || true
sudo ip netns exec v4v6a getent hosts v4v6b || true     # naming may resolve either family
sudo ip netns exec v4v6a ping -c2 192.0.2.22            # force v4
sudo ip netns exec v4v6a ping -c2 fd00:lab:1::b         # force v6
```
**Expected observation:** forcing by address family works directly; without forcing,
selection follows the resolver/OS policy (RFC 6724 preferences ⚠ behavior varies by OS —
record yours). One paragraph: why "dual stack" ≠ "IPv6 wins by default" everywhere.

### T3 — ICMPv6 details (15 min)
From your capture: hop limit on the echo request (compare with L15's TTL→HL rename),
and the fact that NDP runs *without* ARP even though ICMPv4's ping needs ARP first.
Record both observations with frame numbers.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| `ping` v6 fails: Network unreachable | no route/link-local not up | check `ip -br addr` inside ns; link-local appears automatically when the link is UP |
| NS/NA not in capture | NDP entries cached from a previous run | `sudo ip netns exec v4v6a ip -6 neigh flush all` first |
| Typo guard: v4 address on the wrong veth | the T0 command list intentionally includes one; README notes it | verify with `ip -br addr` in both ns; fix and note it in your report (debugging is a skill) |
| `ping fd00...` resolves via getent to v4 | hosts file entry | use literal addresses for T2/T3 |

## Post-lab questions
1. ARP vs NS/NA: two structural differences (who is woken, where it rides) and one
   similarity (the question being asked).
2. Your OS picked a family for the unforced ping — which, and per what preference?
3. Why does IPv6 not need a separate ARP protocol at all (one sentence, mechanism)?
4. Where did you see fe80:: addresses used, and why can't they just be removed?

## Challenge (ungraded)
Add a third namespace and a bridge; verify solicited-node multicast on the shared segment
only wakes the right interface (capture the multicast MAC mapping for both peers).

## Accessibility / low-resource alternatives
- Offline bundle `lab06-nd.pcapng` + a command transcript; every question answerable
  without root. tshark: `tshark -r lab06-nd.pcapng -Y "icmp6.type==135 || arp"`.
- All CLI text; no GUI dependency.

## Safety notes
ULA + documentation ranges only; isolated namespaces (syllabus-safety §3.1).
