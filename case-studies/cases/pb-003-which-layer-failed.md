# PB-003 — Which Layer Failed? (L02, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L02 — Layered Architectures (OSI & TCP/IP) |
| CLOs | CLO1, CLO2 (layered model as diagnostic tool) |
| In-class slot | Opening hook; 10 min, pairs |
| Case type | Conceptual · Topic: OSI/TCP-IP reasoning |
| Evidence policy | Synthetic symptom list, labeled; each symptom maps to exactly one defensible layer |

---

## Student version

### Scenario
Monday morning at Meridian, the help desk collects six reports in ten minutes:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
S1  "My monitor shows 'no signal'."                       (monitor cable unplugged)
S2  "Wi-Fi icon shows connected, but nothing loads."      (laptop, HQ-A 2nd floor)
S3  "I can open the intranet site but my network drive won't map."  (desktop, HQ-B)
S4  "ping 10.20.30.1 works; ping meridian-file01 fails."  (same desktop as S3)
S5  "The fiber patch panel LED for floor 3 is dark."      (HQ-A basement)
S6  "My app says 'connection refused' on port 8080."      (dev VM, cloud)
```

### Problem statement
For each symptom, name the **lowest OSI layer that could plausibly be the cause**, and
justify with one sentence referencing what that layer is *responsible for*.

### Evidence pack
The labeled synthetic reports above. Treat each report's parenthetical note as a
**given fact** (help-desk confirmation), not an assumption.

### Constraints
- One layer per symptom; if two layers are defensible, pick the lowest and say why.
- No configuration fixes — this is a *classification* exercise.

### Student questions
1. Assign a layer (1–7) to S1…S6, lowest defensible layer each.
2. Which two symptoms can be ruled out as "not actually a network problem at all" — and
   what distinguishes them from the rest?
3. S3 and S4 come from the same machine. In one sentence: what does the *combination*
   tell you that neither alone does?
4. Order S1…S6 from "most physical" to "most application" and comment on whether the
   help desk's arrival order is any guide to the cause.

### Expected learning outcomes
- Use the layer model as a classification tool for symptoms.
- Recognize that not every "network is down" report is a network fault.
- Combine two observations to narrow the layer (S3+S4 pattern).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Each layer answers one question: bits on a medium? local delivery? end-to-end path?
   naming? the conversation? the data itself?"
2. "S4 working tells you the path to the host exists — so what is S3's drive-mapping
   problem about?"

### Solution
| Symptom | Lowest plausible layer | One-sentence justification |
|---|---|---|
| S1 | L1 (or L7 of the *monitor* system — accept "not a computer network") | Video signal, not network; the classic non-network fault |
| S2 | L3 (routing/IP reachability) or L7 (DNS/app) | "Connected" is link-layer association (L2 OK); failure is above — lowest defensible is L3 if IP fails, but with nothing loading, L7/DNS is common; either accepted with justification |
| S3 | L7 | Intranet (HTTP) works → path and naming work; drive mapping is an application-layer service (e.g., SMB) |
| S4 | L7 (name resolution) | IP ping by address works; failure to resolve/reach *by name* = naming/application issue |
| S5 | L1 | Dark LED on a patch panel is a physical signal problem |
| S6 | L7 | "Connection refused" means the packet *reached* the host and the OS replied — L1–L4 path works; the server isn't listening |

- Q2: S1 (monitor cable) and arguably S6's *server-side* cause — neither indicates a
  network-path fault; what distinguishes them is that the network did its job (or wasn't
  involved).
- Q3: same machine, ping-by-IP OK + name-based service fails → points at name resolution
  or the service, *not* the path — the combination localizes the layer.
- Q4: physical → application ordering is S5, S1(monitor, excluded), S2, S4, S3, S6.
  Arrival order is not a guide; reports are a *set*, not a sequence.

### Reasoning process
Fact per symptom → what each layer is responsible for → lowest layer that could produce
the observed message → combination effects (same machine) → classify, then revisit the
two non-network items.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Calling S6 an L4 problem | Refused = RST came back; transport path works, nobody is listening (L7/service) |
| Calling S3 an L3 problem | HTTP to the intranet proves L3 reachability to that server; drive mapping fails above |
| Treating "Wi-Fi connected" as L1–L7 OK | Association is L2; everything above is still open |
| Fixing first, classifying never | Without the layer habit, diagnosis is guesswork at scale |

### Extension question
The S6 VM is in a cloud VPC. Name one *cloud-platform* control (not the OS) that produces
"connection refused"-like behavior, and which layer you would then assign.
(Expected: security group / firewall at L3–L4 drops or rejects; if it *rejects*, the
refusal behaves like a transport-layer rejection — discuss reject-vs-drop semantics.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | 5–6 correct lowest-layer assignments with correct responsibility justifications; Q3 combination insight |
| 3 Proficient | 4 correct; one layer off but justified |
| 2 Developing | Classifies by surface keyword ("refused = port = transport") without responsibility reasoning |
| 1 Beginning | Random assignment; no model used |

### References
- PD §1.5 (protocol layers and their responsibilities)
- Kurose & Ross §1.5 (layered architectures)
