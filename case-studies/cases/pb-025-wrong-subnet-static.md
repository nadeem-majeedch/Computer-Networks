# PB-025 — Plugged Into the Right Wall, Wrong Subnet (L13, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L13 — IPv4 Subnetting & VLSM |
| CLOs | CLO5 (subnet arithmetic), CLO6 (diagnose addressing faults) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Calculation + diagnostic · Topic: Subnetting/VLSM |
| Evidence policy | Synthetic configs, labeled; all arithmetic desk-checked |

---

## Student version

### Scenario
A workstation in the analytics VLAN "has network but no internet". Its settings were
copied from an old sticker. The VLAN's router interface is 10.20.70.1/24.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Workstation:   IP 10.20.71.40, mask 255.255.255.0, gateway 10.20.70.1
Router (VLAN 70 interface): 10.20.70.1/24
Local tests:
  ping 10.20.71.53 (neighbor, same sticker-era /24) → replies        (odd?)
  ping 10.20.70.1 (the gateway itself) → "Destination host unreachable"
                                    (reported by the workstation itself)
Internet test: ping 8.8.8.8 → "Destination host unreachable" (from workstation)
Teammate's PC (same VLAN): IP 10.20.70.53, mask /24, gateway 10.20.70.1 → everything works
```

### Problem statement
Compute the workstation's subnet from its IP and mask, explain the
"neighbor works, gateway unreachable" split, and give the corrected configuration.

### Evidence pack
The labeled synthetic configs. All subnet logic follows from the /24 mask.

### Constraints
- Show the network/broadcast computation explicitly.
- Explain *mechanically* how the router is reachable at all (hint: same link, different
  subnet beliefs).

### Student questions
1. Network address, broadcast address, and usable host range for the workstation's
   10.20.71.40/24.
2. Is the gateway 10.20.70.1 inside that subnet? What does the workstation *intend* to
   do with a packet to 8.8.8.8?
3.Explain the split: why can the workstation reach 10.20.71.53 but not the router a few
meters away on the same switch, and why does the router never even get asked?
(Two different delivery decisions, both made by the workstation.)
4. Give the corrected IP and justify it against the usable range from Q1.

### Expected learning outcomes
- Compute network/broadcast/host ranges from an address + mask.
- Explain why a same-subnet gateway mismatch breaks only off-link traffic.
- Translate diagnosis into a correct config.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Mask 255.255.255.0 slices at the third octet. What does 10.20.71.40 belong to?"
2. "The router replies because *it* decides the workstation is on-link. The workstation
   decides 8.8.8.8 is not on-link — and then can't use its gateway. Whose belief
   matters for each direction?"

### Solution
1. 10.20.71.40/24 → network **10.20.71.0**, broadcast **10.20.71.255**, usable
   10.20.71.1–10.20.71.254.
2. Gateway 10.20.70.1 is **not** in 10.20.71.0/24. For 8.8.8.8, the workstation wants
   to send to its default gateway 10.20.70.1 — which it also computes as off-link, so
   it has no on-link next hop at all → packets never leave; the host itself reports
   unreachable.
3. Belief model: the workstation's mask says its universe is 10.20.71.0/24. To
   10.20.71.53 → on-link → ARP within the shared broadcast domain → L2 delivers (the
   two hosts' *beliefs agree*, so this works even without any router). To 10.20.70.1
   → off-link per its own mask → must be sent via a gateway; but the configured
   gateway is 10.20.70.1, which is *itself* off-link → the stack has no usable next
   hop, never sends anything (not even an ARP for the router), and reports unreachable
   from its own address. The router is never consulted for off-link traffic because
   the next hop toward it is unreachable. (Strict-stack behavior; some OSes add
   last-resort on-link routes ⚠ — the evidence here is consistent with strict
   behavior, which is the default on mainstream stacks.)
4. Corrected: **10.20.70.53-style address within 10.20.70.1–10.20.70.254** excluding
   the router — e.g., 10.20.70.40/24, gateway 10.20.70.1 (inside the /24 ✓). Better:
   stop copying stickers — use DHCP reservations.

### Reasoning process
Facts: workstation in .71, router/gateway in .70, teammate .70 works, neighbor .71
works. Model: each host's mask defines its on-link universe; on-link needs only ARP+L2
(shared broadcast domain), off-link needs an *on-link* gateway. Diagnosis: gateway
outside the host's subnet ⇒ no usable next hop. Fix: re-address into the router's
subnet.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Ping to the neighbor works, so the network is fine — blame the ISP" | On-link L2 works; every off-link conversation needs a usable gateway, which is exactly what's broken |
| "Change the mask to /16 to make the gateway fit" | Widens the guest's belief — works by accident, wrecks the plan; also /16 would place 10.20.70.1 on-link — but it violates the VLAN design |
| Copy the sticker without checking VLAN | The sticker *was* the failure mode |
| Assume DHCP is broken | Teammate on DHCP/static works; this is a static config error |

### Extension question
Why do strict host models refuse to send traffic for off-link destinations without a
usable gateway? Name one protection this provides. (Loose/last-resort models let a
host blast frames for any destination onto the local segment — e.g., a compromised
host in 10.20.71.x could attack 10.20.70.x hosts directly, bypassing the assumption
that inter-subnet traffic crosses a policy-enforcing router. Strict models force
everything inter-subnet through the router where ACLs can see it ⚠ platform-
dependent.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Subnet math correct; asymmetry explained via belief model; OS-dependent behavior flagged; clean config fix |
| 3 Proficient | Math correct; asymmetry partly explained |
| 2 Developing | Computes the subnet but can't explain why ping worked |
| 1 Beginning | "Bad cable" |

### References
- PD §4.3 (IPv4 addressing and subnetting) ⚠ verify section mapping
- Kurose & Ross §4.3.4/§5.6 (addressing; broadcast domains) ⚠ verify
