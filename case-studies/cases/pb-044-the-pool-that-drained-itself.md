# PB-044 — The Pool That Drained Itself (L22, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L22 — DHCP Deep Dive, BOOTP & Address Management |
| CLOs | CLO2 (lease state/relay), CLO6 (lease-table forensics) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: DNS/DHCP |
| Evidence policy | Synthetic lease table, labeled; randomization behavior per OS privacy features ⚠; internally consistent |

---

## Student version

### Scenario
The analytics VLAN's DHCP pool (10.20.30.100–10.20.30.199, 100 addresses) began
failing with "no leases available" at 10:30 daily — despite only ~35 real devices in
the VLAN. The lease table tells the story.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Lease table at 10:28 (100/100 leased):
  62 leases: MACs rotating daily per "device" — same hostnames as ~20 real phones
             (iOS/Android private-address randomization enabled ⚠)
  28 leases: RFC1918 192.168.x.x-looking hostnames ("lab-vm-01"...), all clients of
             ONE switch port (the student virtualization bench)
  10 leases: legitimate static-reservation-like devices
Rogue detail: the bench runs nested VMs with NAT — but one VM was bridged by mistake,
             exposing its DHCP *server* role on the analytics VLAN for 30 min daily
             (its scope: 192.168.122.0/24 — harmless addresses, harmful OFFERs)
Server logs: pool 100% by 10:28; oldest expiring leases: 12 h remaining
```

### Problem statement
Explain the two independent drain mechanisms (privacy MAC rotation; bridged lab
leases), reconcile why "35 devices" produced 100 leases, and design the fix set —
including the one that stops the rogue OFFERs from ever harming a client again.

### Evidence pack
The labeled synthetic lease table. Facts: rotating MACs for phone cohorts; 28 leases
from one port; one port intermittently offering DHCP. Assumptions must be labeled
(e.g., which OS randomizes at what cadence ⚠).

### Constraints
- Quantify: with daily MAC rotation and a 12-h lease, how many stale leases per phone
  per week (steady state)?
- Fixes at three layers (endpoint policy, lease hygiene, rogue containment) — each
  with what it does NOT fix.

### Student questions
1. Steady-state arithmetic: 20 phones × daily MAC rotation × 12-h leases — how many
   active + stale leases do the phones hold? Show the doubling logic.
2. The bench's 28 leases: why does a *NAT* design leak 28 leases onto the analytics
   VLAN? Which single misconfiguration turned NAT into bridging?
3. The rogue OFFER danger: the lab's scope is 192.168.122.0/24 — why is that *still*
   dangerous to analytics clients? (Think default-route and gateway options.)
4. Fix set: (a) endpoint policy for randomization, (b) lease hygiene (times/reserva-
   tions), (c) rogue containment. One line each + one limitation each.

### Expected learning outcomes
- Quantify lease inflation from identity rotation.
- Diagnose bridged-vs-NAT misconfigurations leaking leases.
- Layered remediation: endpoint, server policy, rogue containment (DHCP snooping).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Each rotation creates a *new identity* that must be served; the old lease only
   dies when it expires. Draw the two-lifecycle overlap."
2. "NAT translates; bridging *joins*. Which switch-port config change makes VM
   traffic look native on the analytics VLAN?"

### Solution
1. Each phone: rotation creates a new MAC daily → new lease (12 h). A phone active
   twice a day holds 2 leases; over 12 h of lease life, one phone with 2 rotations/
   day ≈ 2 live leases; with 12-h expiry and 24-h rotation ≈ steady state ≈ 2 leases/
   phone → 20 phones ≈ **40 leases** (up to 2× the device count). If rotation is
   per-network-rejoin (commute pattern), add one more per rejoin — the table's 62 is
   consistent with rotation + rejoin churn ⚠ exact OS cadence varies.
2. NAT hides VMs behind the host's address (1 lease). The mistake: one VM's vNIC was
   set to *bridged* mode instead of NAT — its frames (including its own DHCP server
   role) appear natively on the analytics VLAN. Each bridged VM requests its own
   analytics-VLAN lease → 28 leases from one port = a bench full of bridged VMs.
3. A DHCP OFFER can carry *any* options: the lab's scope is 192.168.122.x, but a
   client that accepts it gets gateway/DNS/NTP options pointing into the lab — the
   client's traffic is silently rerouted into the bench (blackholed or intercepted).
   The *addresses* don't matter; the *options* do. Also: the OFFERs race the real
   server (PB-027's selection problem — first acceptable offer wins).
4. (a) Endpoint: disable per-connection randomization on managed devices / use
   stable-per-SSID MACs (MDM policy ⚠) — does not fix unmanaged or guest devices.
   (b) Lease hygiene: shorten lease to match churn (e.g., 2–4 h for high-churn
   cohorts), reserve addresses for infrastructure — does not fix the rogue server.
   (c) Rogue containment: DHCP snooping (trust only the uplink port ⚠ switch
   feature), which drops OFFERs from the bench port entirely — the definitive stop;
   does not fix the *churn* problem (a+b still needed).

### Reasoning process
Facts: 62 rotating leases, 28 bench leases, intermittent rogue OFFERs, 12-h leases.
Model: identity lifetime × rotation rate = lease count; bridging = L2 join (leases
leak); OFFER options = the real risk. Layered fixes matched to each mechanism.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Buy a bigger pool" | Treats the count, not the causes; churn scales to fill any pool |
| "Ban phone randomization campus-wide" | Breaks privacy features users rely on; unenforceable for guests — MDM-scoped policy is the honest version |
| "Shut down the bench" | Removes the symptom and the pedagogy; snooping + proper port config contains it while the lab lives |
| "Ignore the 192.168.122 scope as harmless" | The options payload (gateway/DNS) is the danger, not the addressing |

### Extension question
DHCPv6 has no broadcast and uses multicast + different relay mechanics; RA-guard vs
snooping roles shift. In one paragraph: which of the three fix layers maps cleanly to
DHCPv6/RA-guard, and which needs rethinking? (Endpoint policy maps directly (SLAAC
privacy addresses have their own rotation knobs); lease hygiene maps to preferred/
valid lifetimes; rogue containment shifts from snooping to RA-guard + DHCPv6
snooping ⚠ — the *RA* becomes the rogue's favorite vector since SLAAC clients trust
unsolicited RAs.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both mechanisms quantified; bridging-vs-NAT precise; options-payload risk articulated; three-layer fixes with limitations |
| 3 Proficient | Both mechanisms found; quantification partial |
| 2 Developing | Blames "too many devices" without rotation/bridging analysis |
| 1 Beginning | Reboots the DHCP server |

### References
- RFC 2131 (lease management); RFC 7513 (snooping/option 82 context) ⚠ verify
- OS privacy-MAC behaviors are vendor-specific ⚠ (flag for instructor verification)
