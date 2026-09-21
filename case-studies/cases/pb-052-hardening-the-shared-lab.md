# PB-052 — Hardening the Shared Lab (L26, Expert)

| Field | Value |
|---|---|
| Difficulty | **Expert** |
| Lecture(s) | L26 — Attack & Defense Case Workshop |
| CLOs | CLO3 (attack classes), CLO6 (defense-in-depth design under constraints) |
| In-class slot | Capstone-style workshop; 35 min, groups of 4 → review board |
| Case type | Design under constraints (multiple valid answers) · Topic: Security/enterprise design |
| Evidence policy | Synthetic requirements + constraints, labeled; every attack class must map to ≥2 defenses with failure-mode honesty; no offensive tooling instructions |

---

## Student version

### Scenario (isolated lab — defense design only)
Next semester, the networking lab hosts four classes sharing one switch fabric:
students get switch ports and VMs; exercises legitimately include ARP/NDP, DHCP, DNS
and routing labs. The course must survive *both* accidents (a student's NAT VM
bridged by mistake) and mischief (someone "borrowing" a lab exercise's attack script
outside its lab hour).

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Assets:    grade DB (10.20.80.10), instructor images (NFS 10.20.80.20), lab VLANs
           110–114 (one per class), shared services VLAN 120 (DHCP, DNS, NFS)
Attacks in scope (from real lab incidents, sanitized):
  A1  rogue DHCP (accidental bridged VM — happened twice last term)
  A2  ARP spoofing between student VMs (one "prank" hijacked a neighbor's DNS)
  A3  MAC/IP spoofing to grab a reserved grade-DB client identity
  A4  lab-hour mischief: attack script replayed at 2 a.m. against A2's target
Constraints (hard):
  C1  budget: existing L2+ switches; no new firewall; feature survey pending ⚠
      (assume DHCP snooping/DAI/802.1X *may* exist — design must state the survey
      questions)
  C2  pedagogy: exercises requiring broadcast/ARP/DHCP behavior must still work
      in scheduled lab hours
  C3  staffing: one admin; automation tolerated, toil not
  C4  students have local admin on their VMs
```

### Problem statement
Design the defense-in-depth plan: for each attack A1–A4, give at least two defenses at
different layers, mark which survive C1's "feature may not exist" risk, and resolve
the C2 tension explicitly (how does a blocked-by-default posture still let the ARP
lab run?). End with the survey's top three questions.

### Evidence pack
The labeled synthetic assets/constraints. Ambiguities are deliberate (feature survey
pending; lab-hour schedule granularity unspecified — you define it and defend it).

### Constraints
- Defense-in-depth: no single control may be the *only* thing standing between a
  student VM and the grade DB.
- Every "block" must name its scheduled "allow" path (C2) or be classed as always-on.
- The plan must be operable by one admin (C3): automation/templating, not manual
  per-port heroics.

### Student questions
1. A1 (rogue DHCP): two defenses at different layers + the C2 allowance. What does
   each not cover?
2. A2 (ARP spoofing): dynamic ARP inspection depends on snooping bindings — design
   the *student-VM* binding story given C4 (they control their VMs). What breaks
   when a student changes their IP?
3. A3 (identity spoofing): what does 802.1X (if present) give you that IP/MAC ACLs
   cannot, and what is the fallback if the survey says "no 802.1X"?
4. A4 (off-hours replay): design the time/scope control — what turns on, when, and
   how the same switch serves both locked-down and lab-open states without two
   configs?
5. Survey: your top three questions to the switch vendor — one per *risk* your plan
   carries if the feature is absent.

### Expected learning outcomes
- Layer defenses across L2 features, identity, time, and monitoring.
- Reason about control interdependence (DAI needs snooping bindings).
- Design around feature-availability uncertainty with explicit fallbacks.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Every defense you name must answer: what happens the day it's missing? That's
   the C1 discipline."
2. "The pedagogy tension (C2) is the design's crux: blocked-by-default with a
   *scheduled, bounded* exception beats always-open with warnings."

### Solution (one strong plan; alternatives acceptable if constraints honored)
1. **A1 rogue DHCP:** (i) DHCP snooping with only the uplink/120-server port
   trusted — drops OFFERs from student ports (layer: L2 switch; survives C1 only if
   survey says yes; fallback: VLAN-level isolation — lab VLANs have no route to
   120's DHCP, each class uses VLAN-local DHCP on the instructor's controlled host);
   (ii) templated port profile: student ports inherit `dhcp-snooping + guard` config
   from the class template (C3 automation). Does not cover: the *instructor* VLANs'
   own infrastructure mistakes (bridge your own VM → your own outages; accept and
   document). C2 allowance: DHCP *labs* run on a dedicated "attack VLAN" (115) where
   snooping is deliberately absent — students learn by doing inside a fence.
2. **A2 ARP spoofing:** (i) DAI on lab VLANs, bindings sourced from snooping +
   reservations for the fixed lab VMs (depends on (i)'s feature presence; fallback:
   static ARP entries for the *services* VMs only — students can still spoof each
   other inside the lab VLAN, which C2 tolerates *during lab hours*); (ii) the
   grade DB and NFS live on VLAN 120 where DAI + static ARP entries are always-on —
   students can fight each other but not the assets. Student-IP-change reality
   (C4): DHCP-snooping bindings go stale when students pick static IPs ⇒ define the
   lab contract: VMs must use the class DHCP (enforced by rejecting static ARP on
   unbound ports ⚠ survey question), and the worksheet teaches why. During *lab
   hours* on attack VLAN 115, nothing is enforced — bounded by time, not rules.
3. **A3 identity spoofing:** 802.1X (if present) authenticates the *port* (machine
   cert per lab VM, EAP-TLS ⚠ survey) — an IP/MAC claim without a valid port
   session fails before L3; ACLs bind 10.20.80.10 access to authenticated ports
   rather than to spoofable addresses. Fallback (no 802.1X): private-VLAN-style
   isolation on student ports (no student↔student L2 at all on asset VLANs) +
   asset VLANs reachable only via the instructor router where ACLs live (weaker:
   MAC/IP still spoofable *within* the student VLAN — state that residual honestly).
4. **A4 off-hours replay:** time-based port profiles: lab VLANs' student ports
   schedule to a "dormant" profile outside lab hours (ports stay up but are confined
   to a quarantine VLAN with only the class portal — no east-west traffic at all);
   attacks scheduled *inside* lab hours run in VLAN 115's fenced sandbox with
   DAI/snooping absent *there only*. One admin, one template, two states — automation
   flips profiles via the switch API at fixed times (C3 ✓). Uncovered: a student who
   stays *inside* the sandbox boundary — acceptable, the sandbox is the fence.
5. Survey questions (one per risk): (a) "Does the switch support DHCP snooping +
   dynamic ARP inspection per-VLAN, and are bindings scriptable via API?" (risk:
   A1/A2 fall back to weaker static ARP); (b) "Does 802.1X support EAP-TLS with
   dynamic VLAN assignment and MAB fallback for printers?" (risk: A3 falls back to
   isolation-only); (c) "Are time-based/CLI-scheduled port profiles supported natively,
   or do we need an external controller?" (risk: A4 needs a cron-driven SSH loop —
   workable but brittle).

### Reasoning process
Facts: assets, four attack classes, four hard constraints. Model: defense-in-depth =
each asset path crosses ≥2 independent controls; every control has a named failure
mode; every block has a bounded allow (time/scope). Design under feature uncertainty
= fallback pairs stated up front; the survey questions *are* the risk register.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Disable ARP/DHCP in student VLANs permanently" | Violates C2 — the curriculum *is* the traffic; fence it, don't forbid it |
| "One strong control: DAI everywhere" | Single point of failure (C1 risk); also needs bindings that C4 breaks — interdependence unaddressed |
| "Trust students; log everything" | Monitoring detects A2 after a prank succeeds; the grade DB exposure is preventable, not just detectable |
| "Air-gap the grade DB" | Breaks the legitimate pipeline (jobs read it); segmentation ≠ disconnection |

### Extension question
A new exercise requires students to run a *legitimate* DHCP server in their own lab
VLAN (to teach option 43). How does your A1 design accommodate it without opening
the rogue-DHCP door to VLANs 110–114? (Per-class DHCP-authorization window: the
template flips the snooping trust flag for *one designated port* in that VLAN for
the lab hour, via the same automation as A4 — bounded, auditable, and reverted
automatically. The pattern: exceptions inherit the same time/scope discipline as
blocks.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | ≥2 layers per attack; interdependence (DAI↔snooping↔C4) resolved; C2 fenced-exception design; three survey questions each tied to a named risk |
| 3 Proficient | Solid per-attack controls; fallbacks or C2 handling thin |
| 2 Developing | Feature-name laundry list without interdependence or constraints |
| 1 Beginning | "Use a firewall" |

### References
- PD §8 (security architecture context) ⚠ verify section mapping
- NIST SP 800-94 (IDS/monitoring framing) ⚠; vendor DAI/802.1X guides — survey-
  dependent ⚠
