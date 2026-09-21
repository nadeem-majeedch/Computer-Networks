# PB-015 — Why Did the Reply Go Everywhere? (L08, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L08 — Switching & LAN Design |
| CLOs | CLO2 (switch learning/forwarding model), CLO6 (evidence vs assumption) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual trace · Topic: Ethernet and switching |
| Evidence policy | Synthetic frame trace, labeled; behavior checked line-by-line against learning-switch rules — one deliberate inconsistency for students to find |

---

## Student version

### Scenario
A brand-new switch powers up in the lab. Four PCs (A–D) hang off it. A student's
Wireshark notes record what each NIC saw during the first minute:

**Synthetic evidence — prepared for this case; internally consistent except where noted
in the instructor guide; not from a live system:**

```
t=0.1s  A→B (ARP request, broadcast):   B, C, D all receive it
t=0.2s  B→A (ARP reply — note says "unicast"):  A, C, D all receive it   ← odd?
t=0.3s  A→B (unicast):                  only B receives it
t=0.4s  C→A (unicast):                  A receives; B, D do not
t=0.5s  A→B (unicast):                  only B receives it
```

### Problem statement
Explain every line of the trace using the switch's learning/forwarding/flooding rules.
If any line cannot be explained by those rules, say so and propose the most plausible
correction.

### Evidence pack
The labeled synthetic trace. Assumption: the switch starts with an empty MAC table; no
other traffic. Note that "unicast" on line 2 is the *note-taker's label*, not a
captured field.

### Constraints
- One mechanism per line; show table state after each event.
- If model and evidence disagree, question the evidence before breaking the model.

### Student questions
1. After t=0.1 s: what does the MAC table contain, and why did everyone receive the
   request?
2. At t=0.2 s the note says "unicast", yet C and D saw it. Can the learning-switch
   rules produce this? Show why or why not.
3. The receive-set {A, C, D} is suspiciously familiar — which frame type produces
   exactly that set? What does that suggest about the note-taker's label?
4. Verify t=0.3 s–t=0.5 s against your table. Is the rest of the trace consistent?

### Expected learning outcomes
- Walk a learning switch's decisions: learn source → look up destination → forward or
  flood.
- Explain unknown-unicast flooding and broadcast flooding as distinct rules.
- Detect an evidence/model mismatch and reclassify an assumption as unverified.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Two things happen per frame: the switch *learns the source*, then *decides on the
   destination*. Track both separately."
2. "At t=0.2 s, A is already in the table from t=0.1 s. So what *should* the switch do
   with a unicast reply — and what actually happened on the wire?"

### Solution
1. A's frame arrives: source A learned on A's port. Destination = broadcast → flooded
   to all other ports (B, C, D) ✓. Table: {A → portA}.
2. No. With A already learned (t=0.1 s), a unicast reply B→A must be **forwarded to A
   only**. C and D receiving it contradicts the model — the trace as labeled is
   inconsistent with the rules.
3. {A, C, D} is exactly the receive-set of a **broadcast** (flood to all ports except
   the incoming one). So the frame was almost certainly a broadcast ARP reply — i.e.,
   the destination address was ff:ff:ff:ff:ff:ff — and the note-taker's "unicast" label
   was an *assumption* (they saw "reply" opcode and inferred unicast). This is a real
   behavior: some stacks send unsolicited/gratuitous-style ARP replies to broadcast ⚠
   (implementation-dependent; verify on the lab image with `tcpdump -e`).
4. Yes: t=0.3 s — B learned at t=0.2 s, A refreshed → forward to B only ✓; t=0.4 s — C
   learned, A known → A only ✓; t=0.5 s — B only ✓. One corrected label makes the whole
   trace consistent with zero changes to the switch model.

### Reasoning process
Facts: per-line receive sets (what Wireshark recorded). Model: learn-source → lookup →
forward/flood; broadcast always floods. Test each line; where the model contradicts a
line, examine *labels vs fields* in the evidence — the receive-set pattern identified
the frame type better than the note-taker's classification did. Lesson: facts
(receive sets) outrank assumptions ("unicast") in diagnosis.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The switch floods unicasts to be safe" | Flooding is only for *unknown* destinations; A was known at t=0.2 s |
| "The switch is buggy" | Deterministic rules + one mislabeled line explain everything; don't blame the model first |
| "ARP replies are always unicast" | Common but implementation-dependent ⚠; gratuitous/unsolicited replies are frequently broadcast |
| Accepting annotations as evidence | The label was an assumption; the capture fields were the facts |

### Extension question
Design the one-command experiment that settles line 2 on the real lab switch. (`tcpdump
-e -c 20 'arp'` on any host: the `-e` flag prints the *destination MAC* of each frame —
ff:ff:ff:ff:ff:ff vs B's MAC answers broadcast-vs-unicast definitively.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Line-by-line model application; identifies the impossible line; resolves it via receive-set pattern and separates fact from label |
| 3 Proficient | Correct model walk; accepts the "unicast" label uncritically |
| 2 Developing | Conflates flooding rules (broadcast vs unknown-unicast) |
| 1 Beginning | "The switch sends to everyone sometimes" |

### References
- PD §6.4.1 (self-learning switches), §6.4.2 (forwarding/filtering)
- Kurose & Ross §6.4.3 (switch self-learning walk-through)
