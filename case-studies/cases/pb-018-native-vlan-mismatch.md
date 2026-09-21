# PB-018 — The Trunk That Speaks Two Languages (L09, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L09 — VLANs & L2 Segmentation |
| CLOs | CLO2, CLO6 (trunk semantics; diagnose partial failure) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: VLAN configuration |
| Evidence policy | Synthetic configs/logs, labeled; behavior per 802.1Q native-VLAN rules |

---

## Student version

### Scenario
After "routine" switch maintenance, phones (VLAN 12) stopped working between buildings,
but PCs (VLAN 20) on the same phones' PCs-pass-through ports still work. The uplink
between SW-A (HQ-A) and SW-B (HQ-B) is a trunk.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
SW-A uplink config:  trunk, allowed 12,20; native VLAN 12; mode trunk
SW-B uplink config:  trunk, allowed 12,20; native VLAN 20; mode trunk
Symptom map:         VLAN 20 traffic crosses fine; VLAN 12 phones dead across the link
                     (phones work locally within each building)
Switch logs:         SW-B: "native VLAN mismatch detected" (once, at maintenance time)
```

### Problem statement
Explain how a native-VLAN mismatch kills one VLAN while leaving the other untouched,
using 802.1Q tagging rules, and propose the fix plus a check that prevents recurrence.

### Evidence pack
The labeled synthetic configs. Key rule from lecture: on a trunk, frames in the *native*
VLAN are sent untagged; all others are tagged. Both ends must agree on which VLAN that
untagged traffic belongs to.

### Constraints
- Mechanism must cover the asymmetry (why 12 dies, 20 survives).
- One labeled hypothesis for why maintenance "caused" it (e.g., one end reconfigured to
  defaults) — distinguish from proven fact.

### Student questions
1. Trace a VLAN 20 phone frame across the trunk: tagged or untagged at each hop?
2. Trace a VLAN 12 phone frame. What does each switch *believe* the untagged frame is?
3. Why doesn't the mismatch affect VLAN 20 at all?
4. Fix + prevention: what exact config change is needed, and what setting makes this
   class of error fail loudly next time?

### Expected learning outcomes
- Apply native-VLAN/untagged-traffic rules across a trunk.
- Explain asymmetric symptoms from a symmetric-looking config error.
- Convert a silent mismatch into a loud failure (inconsistent-port checks).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "One VLAN travels untagged on this trunk. Which one at each end — and do the ends
   agree?"
2. "The frame leaves SW-A as a plain Ethernet frame. What VLAN does SW-B *assign* to a
   plain frame arriving on its trunk?"

### Solution
1. VLAN 20 ≠ native at either end → tagged with VLAN 20 at SW-A, SW-B reads tag →
   VLAN 20. Consistent both ways ✓.
2. VLAN 12 frame: SW-A sends it **untagged** (12 is SW-A's native). It arrives at SW-B
   as an untagged frame → SW-B classifies untagged trunk traffic into *its* native VLAN
   = 20. So the "VLAN 12" frame lands in VLAN 20's world on SW-B — phones in building B
   never see it; return traffic suffers the mirror-image fate (SW-B sends 12-untagged,
   SW-A reads it as 20). Effectively VLAN 12 leaks into VLAN 20 across the link —
   phones see nothing of their own VLAN.
3. Tagged traffic is self-describing: the tag carries the VLAN ID, so both ends agree
   regardless of native config. Only *untagged* traffic depends on shared
   configuration.
4. Fix: set native VLAN to match — e.g., make 12 native on both ends (or better:
   configure a dedicated unused native VLAN on both ends and force VLAN 12 to be
   tagged). Prevention: enable native-VLAN-mismatch detection as an *error* (log+err-
   disable rather than silent accept ⚠ verify platform behavior) and document trunk
   templates; the maintenance-time log line shows the tooling *did* speak — process
   must listen.

### Reasoning process
Facts: mirrored native-VLAN values (12 vs 20), VLAN 20 fine / VLAN 12 dead, one-time
mismatch log. Model: untagged = native at the *receiving* end. Mechanism explains
asymmetry without extra assumptions. Hypothesis (labeled): maintenance restored one
switch to default native VLAN (common default = VLAN 1; here 20 suggests an older
template — actually the asymmetry direction implies SW-A kept 12, SW-B moved to 20).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Trunk is down" | VLAN 20 crosses; the link is up and speaking |
| "Phones are tagged wrong" | Local phone traffic works within each building; the fault is the *crossing* |
| Allow both VLANs again | Already allowed — allowing isn't the issue; *classification of untagged* is |
| Set native to 1 on both ends | Works but puts phone traffic in the default VLAN — recreates the same design smell |

### Extension question
Why do many security guides say "never use VLAN 1 as native on trunks"? Frame the answer
in terms of this incident (untagged management traffic and default-classified frames all
share one domain; a mismatch or unmanaged device leaks frames into management space).

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both traces correct; asymmetry mechanism explicit; fix + loud-failure prevention; hypothesis labeled |
| 3 Proficient | Correct diagnosis; traces partially shown |
| 2 Developing | "VLAN mismatch" restated without the untagged-classification mechanism |
| 1 Beginning | Reboots the trunk |

### References
- PD §6.4.3 (VLAN trunking, 802.1Q)
- IEEE 802.1Q (tag format; native/untagged classification) ⚠ verify clauses
