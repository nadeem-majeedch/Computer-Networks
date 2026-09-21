# PB-001 — Meridian's First Inventory (L01, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L01 — What Is a Network? |
| CLOs | CLO1 (identify components and their roles) |
| In-class slot | Opening hook or closing consolidation; 10 min, pairs |
| Case type | Conceptual diagnostic · Topic: Network fundamentals |
| Evidence policy | Synthetic evidence, labeled below; internally consistent; no live-system data |

---

## Student version

### Scenario
Meridian Systems occupies two buildings (HQ-A and HQ-B) connected by a fiber link between
their basement comms rooms. Each floor of each building has one wall-cabinet switch; staff
PCs and phones plug into floor switches; each building has a server room and a Wi-Fi
network; the branch office reaches HQ over the internet; cloud services run in a public
cloud. **Synthetic evidence** (prepared for this case, not from a live system):

```
HQ-A: 4 floors × 1 switch = 4 access switches
HQ-B: 3 floors × 1 switch = 3 access switches
1 fiber uplink HQ-A ↔ HQ-B; 1 edge router to the internet; 1 cloud tenant (VPC)
Branch office: 1 router + 1 switch, consumer-grade
Wi-Fi: 6 APs total across both HQ buildings; branch has 1 consumer AP
Servers: 12 on-prem (HQ-A server room), rest in cloud
```

### Problem statement
New IT-manager memo: *"Before we fix anything, I need to know what 'the network' actually
is. Inventory it by role — what moves bits across a room, across campus, between
buildings, and off-site — and tell me which parts our staff never see."*

### Evidence pack
See the labeled synthetic inventory above; treat every line as a **given fact** for this
case.

### Constraints
- Use only the inventory facts; do not invent extra equipment.
- If something is ambiguous (is the branch's consumer router a router? a switch? both?),
  say so and state what one clarification question you would ask.

### Student questions
1. Group the inventory into: links, forwarding devices, and end systems. Count each group.
2. Which single component, if it failed, disconnects the branch from HQ? Which single
   component disconnects *both buildings from the internet*?
3. Staff never see most of this equipment. Name the pieces that are "invisible" to users
   and explain in one sentence why that invisibility is *by design*.
4. The memo asks you to draw the network as a picture with buildings, the fiber, the
   router, and the cloud. Sketch it and label every link with what it connects.

### Expected learning outcomes
- Identify end systems vs. forwarding devices vs. transmission links in a concrete deployment.
- Reason about network *reachability* (what disconnects what) from a topology description.
- Distinguish user-visible from user-invisible network elements.

### Extension question
The branch router is a consumer all-in-one. List two roles it plays at once and why that
dual role is acceptable at a 4-person branch but risky at HQ.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Sort the lines by what each thing *does*, not where it sits."
2. "For Q2, trace the branch's path to HQ on your sketch — the failure point is on that path."

### Solution
- **Links:** fiber HQ-A↔HQ-B; internet link at HQ-A edge router; branch's internet link;
  cloud connectivity (via the same edge router); each AP's radio link; each patch cable.
  **Forwarding devices:** 7 floor switches, 1 edge router, branch router, (cloud VPC
  forwarding handled by the provider). **End systems:** 12 on-prem servers + staff
  PCs/phones/printers + cloud VMs.
- Q2: **branch's internet link** (its only path); **HQ-A edge router** (sole default path
  for both buildings — the fiber hangs off the campus side, not the internet side, per the
  inventory's "1 edge router to the internet"). If a student instead answers "the fiber,"
  accept it *only* if they state it disconnects HQ-B's staff from HQ-A, not the branch —
  reward the reachability reasoning, not the exact object.
- Q3: switches, APs, the fiber, patch panels — invisible because each is designed to be
  self-sufficient (forwarding learned automatically; radios unattended); users interact
  only with end systems. Accept any answer that separates *operation* from *oversight*.
- Q4 sketch: HQ-A (4 sw) —fiber— HQ-B (3 sw); both buildings up to the single edge router;
  branch router via internet cloud-symbol; VPC behind the same edge. Label every link.

### Reasoning process (for class debrief)
Inventory → classify by function (link/forward/end) → trace paths → ask "what single
failure breaks which reachability" → sketch and re-check against the inventory.

### Common incorrect approaches
| Approach | Why it's wrong / what to do instead |
|---|---|
| Counting the cloud as "not part of the network" | The VPC is networked; it's reachable, so it's in scope |
| Treating the AP as an end system | It forwards for others → forwarding device |
| "The branch router is the edge router" | One edge router is inventoried; branch has its own consumer router — a *different* device |
| Sketch with unlabeled links | Reachability questions can't be answered from an unlabeled sketch |

### Assessment rubric (per question, 0–2 each; 8 → convert to 4-level)
| Level | Descriptor |
|---|---|
| 4 Exemplary | All groups correct; both Q2 answers with correct reachability reasoning; sketch labeled |
| 3 Proficient | Minor misclassification (e.g., AP), reachability reasoning sound |
| 2 Developing | Classifies correctly but reachability answers guess; sketch partial |
| 1 Beginning | Groups by location rather than function; no reachability reasoning |

### References
- PD §1.2 (network components); Kurose & Ross §1.2 (access networks, physical media overview)
