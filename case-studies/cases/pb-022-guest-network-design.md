# PB-022 — Design Under Debate: The Guest Network (L11, Expert)

| Field | Value |
|---|---|
| Difficulty | **Expert** |
| Lecture(s) | L11 — Wireless in Practice + LAN Security Preview |
| CLOs | CLO6 (design + defend under ambiguity), CLO3 (security reasoning preview) |
| In-class slot | Extended activity; 25 min, groups of 3–4 → structured debate |
| Case type | Design/trade-off with incomplete evidence · Topic: Enterprise design (LAN security preview) |
| Evidence policy | Synthetic requirements + meeting minutes, labeled; ambiguities deliberate; multiple defensible designs exist |

---

## Student version

### Scenario
Meridian must offer guest Wi-Fi in both buildings. The requirements meeting went badly;
the minutes survive but so do the disagreements.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Requirements (agreed):
  R1  Guests must reach the internet only — never internal subnets
  R2  No guest may see another guest's traffic at L2
  R3  Provisioning must survive the IT admin being on leave
  R4  Budget: reuse existing switches; no new firewall this quarter
Meeting minutes (disputed):
  D1  CTO: "Put guests in VLAN 30 like the printers VLAN — VLANs are isolation."
  D2  Security consultant: "VLAN-only guest access on shared switching is not
      acceptable isolation for untrusted devices."
  D3  Facilities: "The printer VLAN already crosses buildings; guest must too."
  D4  Finance: "What does 'not acceptable' cost to fix?"
Unknowns: switch capability details (local ACLs? per-port policing?) — survey pending
```

### Problem statement
Design the guest network for *this quarter* (constraints honored) and *next* (upgrade
path). For each disputed claim, rule: agree/disagree with reasoning. Be explicit about
what the pending survey must answer.

### Evidence pack
The labeled requirements and minutes. All capability details are unknown-by-design:
this case trains *design under incomplete evidence* — every assumption must be listed
with its consequence if wrong.

### Constraints
- R1–R4 are hard constraints; you may not add hardware beyond what R4 allows.
- At least two designs must be compared; pick one and defend it.
- Every disputed claim (D1–D4) gets a ruling.

### Student questions
1. Rule on D1: is "VLAN = isolation" adequate for untrusted guests? Give the specific
   threat that defeats it.
2. Rule on D2: what does the consultant's objection concretely require (name the
   control class), and what is the *minimum* version of it available without new
   hardware?
3. Design A (this quarter) and Design B (next): sketch each with the trust boundary
   drawn; where does guest traffic first touch Meridian-owned policy?
4. Rule on D3/D4: does the printer-VLAN precedent matter for guests? What cost figure
   should Finance actually request?

### Expected learning outcomes
- Distinguish segmentation (L2 isolation) from policy enforcement (L3+/security
  controls) for untrusted devices.
- Design under explicit constraints with an honest upgrade path.
- Evaluate meeting claims as claims — not as requirements.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Two guest laptops on the same VLAN share a broadcast domain. What can one do to the
   other before any router/firewall is involved?"
2. "The threat is *lateral*, and the chokepoint must be *somewhere Meridian owns
   policy*. Without a new firewall — what existing box can enforce a permit-internet-
   deny-internal rule for VLAN 30?"

### Solution (one strong design; alternatives acceptable if constraints honored)
1. **D1 — disagree (mostly).** A shared guest VLAN gives untrusted devices L2 adjacency
   with each other: ARP spoofing, sniffing of broadcast/multicast, and attacks on any
   misconfigured guest. VLAN isolation is *between* VLANs, not *within* one. If guest
   devices are isolated per-port (client isolation / private-VLAN-style per-port
   filtering — capability = survey question), VLAN 30 becomes workable; that
   conditional is the precise resolution of the dispute.
2. **D2 — agree, with a floor.** The objection names the right threat class (untrusted
   lateral access). The minimum control without new hardware: a guest VLAN whose only
   routed egress is an ACL on the *existing* L3 switch permitting DNS/HTTP(S)/DHCP to
   the internet and denying RFC1918 destinations ⚠ (verify the L3 switch supports the
   needed ACL breadth — that's survey question #1), plus per-port client isolation on
   the APs/switches if supported (survey question #2).
3. **Design A (this quarter):** Guest SSID → VLAN 30 → L3 switch ACL (permit DNS/DHCP/
   HTTPS out, deny RFC1918) → NAT at the existing internet edge. Trust boundary first
   touched: the L3 switch ACL (weak but real), with AP client isolation as the L2
   stopgap. Known gaps (stated): no rate limiting per guest, ACL change requires IT,
   lateral protection depends on survey results. **Design B (next):** dedicated guest
   edge (firewall/VRF or cloud-hosted) with captive portal, per-client isolation
   mandatory, bandwidth policing, logging. Boundary moves to a dedicated policy
   enforcement point.
4. **D3 — disagree as precedent.** Printers are *managed Meridian devices* with a
   defined protocol set; guests are untrusted. A VLAN that works for one is not
   evidence for the other; the shared *cross-building transport* is fine, the trust
   class is not. **D4 — the right cost question:** not "what does 'not acceptable'
   cost" but "what is the exposure if survey answers come back 'no client isolation,
   no ACL'?" — ask Finance for the Design B line item *and* the interim risk
   acceptance in writing.

### Reasoning process
Facts: R1–R4; minutes = claims, not requirements. Model: trust classification → control
selection → chokepoint placement under constraints. Two designs, staged; every unknown
mapped to a survey question with consequence-if-wrong. Rulings distinguish precedent
(printer VLAN) from principle (trust class).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "VLAN 30 and done" (D1 accepted) | Lateral exposure between untrusted devices; R2 violated unless per-port isolation exists |
| "Refuse until the firewall arrives" | Ignores R4/R3 — a defensible interim design exists; refusing isn't designing |
| "NAT is the security" | NAT is not a policy boundary; R1 is about *destinations*, not translations |
| Designing only Design B | Ignores the quarter's constraint; staging is the assignment |

### Extension question
Write the two survey questions whose answers *flip* your Design A choice, and state for
each what Design A becomes if the answer is "no". (E.g., "Does the L3 switch support
source-address-based ACLs at line rate?" — no → guests ride a dedicated uplink to a
cheap internet drop with zero internal routes, trading convenience for isolation.
"Does the AP support per-client isolation on this SSID?" — no → R2 is unmet; document
risk acceptance or enable MAC-randomizing-hostile portals... discuss.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both designs staged; trust boundaries drawn; all four rulings reasoned; survey questions with flip conditions |
| 3 Proficient | Sound Design A + rulings; Design B thin or survey questions missing |
| 2 Developing | Accepts D1 or refuses to design under constraints |
| 1 Beginning | Single design, no ruling structure |

### References
- PD §6.4.3 (VLAN limitations), §8 security chapters preview (context)
- NIST SP 800-94 (wireless security guidance) ⚠ section for guest/BYOD framing
