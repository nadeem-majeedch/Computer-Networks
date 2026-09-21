# PB-017 — Same Switch, Different Universe (L09, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L09 — VLANs & L2 Segmentation |
| CLOs | CLO2 (VLAN isolation semantics) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual diagnostic · Topic: VLAN configuration |
| Evidence policy | Synthetic port table, labeled; isolation behavior per 802.1Q model |

---

## Student version

### Scenario
A student-technician moves the analytics printer to a different wall port — same switch,
same room. Now the print server can't reach it. Both devices ping their own defaults
fine; the switch is otherwise untouched.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Switch port table:
  Port 3  (print server)   VLAN 20, access
  Port 17 (printer, new)   VLAN 30, access   ← old port 14 was VLAN 20
Inter-VLAN routing: exists for staff VLANs (20↔30 via the L3 switch), but
  the printer's policy ACL (from the print vendor's hardening guide) denies
  inbound connections on its print port from other subnets
Everything else on VLAN 20 can still print.
```

### Problem statement
Explain why moving the printer to port 17 broke printing even though both devices are
on the same physical switch, and identify the two cooperating causes.

### Evidence pack
The labeled synthetic port table and ACL note. Assumption: no other changes were made.

### Constraints
- Explain at L2 first (what VLANs do to a switch's forwarding), then note the L3/ACL
  wrinkle.
- Do not propose "put everything in VLAN 1".

### Student questions
1. Why can't two devices on the same switch in different VLANs exchange frames at L2?
2. The L3 switch *does* route VLAN 20↔30 — so why doesn't routing save the day here?
3. Name the two cooperating causes in this incident.
4. The technician wants printing to work from the analytics VLAN only. Give a fix that
   satisfies both the isolation policy and the users.

### Expected learning outcomes
- Explain VLANs as separate broadcast/forwarding domains inside one switch.
- Recognize that inter-VLAN routing exists but is subject to policy (ACLs).
- Match a fix to the *policy*, not just to connectivity.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A VLAN tag (or access-port assignment) decides which *forwarding table* your frame
   lives in. Same box, different table."
2. "Routing moves packets across VLANs — then who else gets a vote? Look at the ACL
   note."

### Solution
1. Each VLAN is a distinct broadcast/forwarding domain: the switch forwards frames only
   within the VLAN determined by the port's assignment (untagged access traffic is
   classified into that VLAN). A frame from VLAN 20 is never delivered out a VLAN 30
   port at L2 — ARP requests don't cross, so the printer's MAC is never even learned
   by the server's ARP process.
2. Routing exists, so packets *can* cross VLANs — but the printer's hardening ACL
   rejects inbound print-protocol connections from other subnets (the routed path
   arrives as "other subnet"). So L3 reachability succeeds but the application-level
   policy refuses the connection.
3. (a) The move reclassified the printer into VLAN 30 (L2 separation); (b) the printer
   ACL denies cross-subnet print connections (L3/policy) — each alone would *not* have
   broken printing (old setup was same-VLAN; a printer without the ACL would print via
   routing).
4. Move the printer back to a VLAN 20 access port (or create a dedicated "printers"
   VLAN with the routing/ACL policy the vendor guide expects). The point: the correct
   fix restores the *intended segmentation*, it doesn't delete segmentation.

### Reasoning process
Facts: port table change (VLAN 20→30), ACL policy note, "everything else still prints."
Model: VLAN = forwarding domain (L2 isolation) + routed inter-VLAN with policy (L3).
Two independent causes compose into the symptom.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Same switch = same network" | VLANs deliberately violate that intuition; that's their purpose |
| "Routing is broken" | Routing works; the printer's ACL refuses the routed path |
| "Delete the VLANs" | Destroys the segmentation policy that exists for a reason |
| Swap cables again | The port assignment, not the cable, defines membership |

### Extension question
The print vendor's guide insists printers be in their own VLAN. What two infrastructure
elements must exist for that design to work from the analytics VLAN? (Inter-VLAN routing
for the print VLAN + an ACL/permit for exactly the print protocols/subnets — policy,
not reachability, is the design task.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | L2 isolation mechanism precise; identifies both cooperating causes; fix respects the policy |
| 3 Proficient | Explains VLAN isolation; misses the ACL's role |
| 2 Developing | "VLANs are like different networks" without mechanism |
| 1 Beginning | Recables until it works |

### References
- PD §6.4.3 (VLANs and trunking concept)
- IEEE 802.1Q (tag structure, port VLAN classification) ⚠ verify clauses
