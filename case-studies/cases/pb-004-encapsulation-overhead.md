# PB-004 — The Price of Wrapping a Message (L02, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L02 — Layered Architectures |
| CLOs | CLO2, CLO5 (quantify encapsulation overhead) |
| In-class slot | Closing consolidation; 12 min, pairs |
| Case type | Calculation (evidence-style reasoning) · Topic: OSI/TCP-IP reasoning |
| Evidence policy | Synthetic numbers, labeled; arithmetic desk-checked and internally consistent |

---

## Student version

### Scenario
The data-science team plans to push a **1 MiB model artifact** from a workstation to the
Meridian file server over Ethernet. A teammate claims "headers are tiny, we can ignore
them." Before the next lecture you want to know exactly how much wire time the wrapping
costs.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Application payload:      1 MiB = 1,048,576 bytes
Path MTU:                 1500 bytes (Ethernet)
TCP header:               20 bytes (no options)
IP header:                20 bytes
Ethernet frame overhead:  18 bytes (14 header + 4 FCS) per frame
Preamble + IFG:           8 + 12 = 20 bytes per frame on the wire
Link:                     1 Gb/s
Assumption (state it):    no TCP/IP options, payload fills every segment but the last
```

### Problem statement
Compute how many frames the transfer needs and the **total on-wire bytes**, then express
overhead as a percentage of payload. Is "headers are tiny, ignore them" a fair claim?

### Evidence pack
The labeled synthetic parameters above. All arithmetic flows from these numbers.

### Constraints
- TCP payload per segment = MTU − TCP header − IP header.
- The last segment may be partial; count frames correctly.
- Overhead percentage = (wire bytes − payload) ÷ payload.

### Student questions
1. Maximum TCP payload per segment (bytes).
2. Number of segments/frames for the 1 MiB payload.
3. Total on-wire bytes (payload + TCP/IP headers + Ethernet overhead + preamble/IFG).
4. Overhead percentage, and a one-sentence verdict on the teammate's claim.

### Expected learning outcomes
- Compute per-frame payload capacity from MTU and header sizes.
- Quantify protocol overhead across three layers at once.
- Judge a practical claim ("overhead is negligible") with arithmetic.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Per-frame budget: MTU minus everything below the payload. Which headers ride *inside*
   the frame?"
2. "Every frame pays the L2 tax too — even the short one at the end."

### Solution
1. Payload per segment = 1500 − 20 − 20 = **1460 B**.
2. Frames: 1,048,576 ÷ 1460 = 718.2 → **719 frames** (718 full + 1 partial of 1,016 B —
   check: 718×1460 = 1,048,280; remainder 296 B… recompute: 719×1460 = 1,049,740 ≥
   1,048,576, so 718 full frames carry 1,048,280 B and frame 719 carries 296 B).
3. Per-frame L3/L4 overhead = 40 B; per-frame wire overhead = 40 + 18 + 20 = 78 B.
   Total = payload 1,048,576 + 719×78 = 1,048,576 + 56,082 = **1,104,658 B**.
4. Overhead = 56,082 ÷ 1,048,576 = **5.35%**. Verdict: "tiny" is per-frame, but the cost
   is per-frame × thousands of frames — ~5% here, *more* if applications send small
   writes (each write can force a sub-MTU segment). A fair claim only for large,
   well-packed transfers.

### Reasoning process
Facts: MTU, header sizes, link framing. Model: payload/frame → frame count → overhead ×
frames → percentage. Assumption: no options, filled segments (state in answer).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| 1500 − 20 = 1480 payload | Forgets the TCP header is also inside the MTU |
| Rounding 718.2 → 718 frames | Truncation drops 296 B; ceiling is required |
| Counting L2 overhead once per transfer | Preamble/IFG/FCS are per-frame costs |
| Quoting 5.35% as universal | It's payload-size- and options-dependent; small writes are far worse |

### Extension question
The same 1 MiB is sent as 2 KiB application writes with TCP_NODELAY-style small-segment
behavior (each write becomes its own segment of ≤2048 B). Recompute frame count and
overhead percentage. (512 writes × 2048 B; each write exceeds the 1460 B MSS, so it splits into two segments
→ **1024 frames**; on-wire = 1,048,576 + 1024×78 = 1,088,448 B → overhead = 79,872 ÷
1,048,576 = **7.6%**, up from 5.35%. The teaching point: poor *application write
patterns* — not the headers themselves — inflate the tax.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Frame count correct (ceiling logic explicit); overhead 5.3–5.4%; verdict references per-frame × per-count scaling |
| 3 Proficient | Correct method, one arithmetic slip |
| 2 Developing | Uses 1500 as payload or forgets L2 tax |
| 1 Beginning | "Headers are tiny" accepted without computation |

### References
- PD §1.5.2 (encapsulation and header overhead)
- Kurose & Ross §1.5.2, §5.7 Ethernet framing (for the L2 tax)
