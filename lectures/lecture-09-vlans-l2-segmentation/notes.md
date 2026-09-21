# Lecture 09 — Instructor Teaching Notes
## VLANs & L2 Segmentation (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary; CLO6/CLO7 supporting |
| Textbook anchor | PD §3.2 (VLAN section) |

---

## 1. Objectives hook
Board: **"One switch, 48 ports, 500 users. Accounting's PCs, the guest phones, and the
lab printers all share one broadcast domain. You can't buy 3 switches for 3 departments.
Now what?"**

Hook (2 min): show the Meridian CS-02 one-pager (flat LAN problems) — the class is
looking at the problem VLANs were invented for.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L08 flood/learn recall; Meridian problem statement |
| 6–28 | Concept 1 | VLAN model, 802.1Q tag, access vs trunk |
| 28–46 | Concept 2 | Trunk operation worked example; native VLAN; inter-VLAN routing options |
| 46–55 | Concept 3 | Security benefits & limits; L2 vs L3 segmentation |
| 55–60 | Break | — |
| 60–72 | LAB-02 briefing | Topology, tasks, verification commands |
| 72–108 | LAB-02 (in-class start) | Pairs build the VLAN lab |
| 108–118 | Early findings + summary | 2 pairs demo; exit ticket |
| 118–120 | Preview | Wi-Fi next |

## 3. Concept walkthrough

### 3.1 The VLAN model (22 min)
- A **VLAN = one broadcast domain configured on switches**: frames flood only within the
  VLAN; MAC learning is per-VLAN; each VLAN is one IP subnet (the pairing rule — repeat
  it twice).
- Two kinds of ports:
  - **Access port:** belongs to exactly one VLAN; frames in/out are *untagged* (hosts
    neither know nor care).
  - **Trunk port:** carries *multiple* VLANs between switches; every frame is **tagged**
    with a 4-byte **802.1Q header** inserted after Source MAC: TPID 0x8100 + TCI
    (3-bit priority/PCP + 1-bit DEI + 12-bit **VLAN ID**, 1–4094).
- Mechanics of a tagged frame: EtherType moves into the 802.1Q-encapsulated header —
  i.e., tag sits *between* Source MAC and original EtherType; receiver strips the tag
  before delivering to the host. Show the byte layout; have students mark it on the
  worksheet.
- **Native VLAN** (on trunks): the one VLAN sent untagged — a historical compatibility
  convenience and a security footgun (mismatched native VLANs leak frames between
  VLANs); best practice: set native to an unused VLAN or tag everything.
- Two switches, one trunk: switch adds tag on egress per VLAN, strips on delivery to
  access ports. FDB learning becomes (VLAN, MAC) → port — connect to L08's FDB.

### 3.2 Trunk operation + inter-VLAN routing (18 min)
Worked example (board): SW1 and SW2, trunk carries VLANs 10/20; PCs A1,B1 in VLAN 10
(SW1), A2 in VLAN 10 (SW2), C1 in VLAN 20 (SW2). Frame A1→B1: tagged 10 crosses trunk,
untagged delivery. Frame A1→C1: **same switch, different VLAN → cannot bridge; must be
routed** — the crucial insight: VLANs isolate at L2; communication needs L3.
- Inter-VLAN options: (1) legacy "router-on-a-stick": one router interface, subinterfaces
  per VLAN over one trunk; (2) L3 switch doing routing internally (modern default);
  (3) physical router ports per VLAN (history). Trade-offs: bandwidth through the trunk
  vs integrated speed; ACL placement.
- Design pairing rule: VLAN ↔ subnet 1:1 keeps routing/ACLs sane. Violations (two
  subnets in one VLAN) create asymmetric-routing mysteries — name the rule.

### 3.3 Security benefits and limits (9 min)
- Benefits: blast-radius reduction (ARP/DHCP storms contained — L22 shows DHCP
  starvation), trust-zone separation (users vs printers vs cameras vs guests), smaller
  unknown-unicast flooding scope, a place to hang policies (later: DHCP snooping, 802.1X).
- **Limits (state loudly):** VLANs are *not* firewalls — traffic between VLANs flows
  wherever routing allows; tags can be forged by on-path hosts in the same VLAN;
  misconfigurations (native VLAN) undo isolation. Security value = segmentation
  hygiene + policy anchor, not confidentiality boundary. (Full defense-in-depth: L25.)

### Reference diagram — Access vs trunk ports with 802.1Q

```text
H1 ── p1(access, V10) ┤          ├ p4(access, V10) ── H3
                      ┤ SW1 p3   ── trunk ── SW2 p5
H2 ── p2(access, V20) ┤          ├
 trunk frame: │ dst │ src │ 0x8100 │ VID=10 │ payload │ FCS │
```

## 4. Important definitions
VLAN · VLAN ID (12-bit) · 802.1Q tag (TPID/PCP/DEI/VID) · Access port · Trunk port ·
Native VLAN · Inter-VLAN routing · Router-on-a-stick · L3 switch · Per-VLAN MAC learning.

## 5. Real-world examples
- Guest Wi-Fi: same APs, separate VLAN → guests can't see printers (classic 802.1Q).
- Voice VLAN: IP phones tag their own traffic (voice VLAN ID) so PC + phone share one
  access port but two VLANs — real, everywhere, and explains "why is there a phone port
  on my desk switch".
- IoT containment: cameras/TVs on an isolated VLAN with no internet route — the
  "smart TV phoning home" mitigation.

## 6. Mathematical/technical example
Tag overhead: 1500 B payload + 4 B tag still fits MTU 1500? No — the *frame* becomes
1504; standard practice keeps payload at 1500 and vendors accept the 4 B or use
"baby giants". Trunk capacity math: 1 Gbps trunk shared by 3 VLANs at 300/300/300 Mbps
is fine; at 900/50/50 the numbers VLAN vs capacity debate. Quick exercise: 4094 usable
VLAN IDs; how many for a 3-building campus with 12 departments × 3 roles? (108 + spares
— ID plan discipline, feeding CS-02's addressing plan.)

## 7. LAB-02 briefing (12 min)
Topology (VM/simulator): 2 "switches" (Linux bridges or simulator switches), 4 hosts,
trunk between switches, VLANs 10/20. Tasks: build, tag trunk, assign access ports,
verify isolation (ping across VLANs fails; within VLAN works), capture a tagged frame
and identify the 802.1Q fields, configure inter-VLAN routing (stretch task).
Verification commands (Linux-bridge variant) listed in the LAB-02 handout; simulator
variant uses the simulator's CLI. ⚠ Verify both variants on the current image before
class; the handout records which variant this semester uses.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "VLANs encrypt or secure traffic" | No confidentiality at all; segmentation + policy anchor only |
| "Trunks carry 'special' traffic" | They carry ordinary tagged frames for many VLANs |
| "Tagged frames reach hosts" | Hosts see untagged; switch strips at access egress |
| "Native VLAN is required everywhere" | Compatibility relic; tag-everything is cleaner |
| "One VLAN can hold many subnets" | Breaks the VLAN↔subnet pairing; asymmetric-routing pain |
| "VLAN = firewall" | Routing between VLANs is unrestricted unless policies are added |

## 9. Suggested practical demonstration
5-minute tag-view: on the LAB-02 topology, capture on the trunk (Wireshark) and show one
tagged frame's 802.1Q expansion (TPID 0x8100, VID=10); then the same logical flow on an
access-port capture — no tag. Side-by-side is the "aha". ⚠ Pre-build the topology and
keep it running; capture filters `vlan`.

## 10. Classroom activities
- **Tag/untag relay:** two rows of students = two switches; paper "frames" move between
  rows; a "trunk" student adds/removes colored sticky tags per VLAN announced — physical
  802.1Q.
- **Design debate (3 min):** "Separate staff/students by VLAN or by physical switches?"
  Pairs argue; reveal the cost/maintenance winner (VLANs) *and* the edge cases (high-
  security labs may justify physical separation).

## 11. Problem-solving questions
1. Hosts in VLAN 10 and VLAN 20 share one switch. Why can't they ARP each other?
2. A trunk's native VLAN is 1 on SW1 and 20 on SW2. What misbehavior follows?
3. Where would you put an ACL to control staff→finance traffic? (Inter-VLAN routing
   point — precise answer: the L3 switch/router doing inter-VLAN routing.)
4. 4094 VIDs: how would you allocate for 12 departments × (staff/students/devices)?
5. Why does a two-subnet-one-VLAN design cause asymmetric paths? (ARP resolves across
   subnets; router may hairpin; explain in class if time.)

## 12. Formative assessment (with answers)
- MCQ: The 802.1Q TPID value is → **0x8100**.
- MCQ: An access port carries → **exactly one VLAN, untagged**.
- MCQ: Inter-VLAN traffic requires → **an L3 device**.
- Short: two security benefits of VLANs, one limit → containment/policy anchor; not a
  confidentiality boundary.

## 13. Exit ticket
1. Tag TPID + VID field size: ________ / ________ bits.
2. Access vs trunk in one line each: ________
3. True/false + why: "VLANs stop all attacks between departments."

## 14. Anticipated difficulties
- The tag's *position* in the frame confuses; the byte-layout diagram + relay activity
  fix it.
- In LAB-02, students confuse "isolation failed" (wrong port assignment) with "routing
  works" (stretch task) — the handout's verification checklist orders the checks.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify LAB-02 topology boots on the image (bridge *and* simulator variants)
- [ ] Pre-build the demo topology with tagged capture ready
- [ ] Print LAB-02 handouts; Meridian CS-02 one-pager at hand
- [ ] Sticky notes in two colors for the relay activity

## 16. Timing fallbacks
If lab startup drags: instructor runs the tag capture demo while pairs finish build;
stretch task (inter-VLAN routing) moves to homework. Protect the isolation-verification
task — it's the assessed observation.

## 17. References
- PD §3.2 (VLAN section, ⚠ verify); IEEE 802.1Q (tag format).
- LAB-02 handout (labs/lab-02-vlans/) for build variants.
- ⚠ VERIFY edition/sections and lab-image compatibility this semester.
