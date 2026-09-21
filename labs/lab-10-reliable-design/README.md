# LAB-10 — Reliable Transport over UDP: Design & Specification

| Field | Value |
|---|---|
| Anchor lectures | L20 (programming the transport layer), L18–L19 (TCP mechanisms to borrow) |
| CLOs | CLO4, CLO5, CLO6 |
| Assessment | Spec milestone of the 10% project (assessment-strategy §3.5); pair work |
| Mode / duration | Pairs; in-session design clinic + out-of-class drafting; **spec due before LAB-11 coding** |
| Environment | Paper + this document; no code required yet |

## Learning outcomes
1. Define reliability *for a workload*: which guarantees (ordering, dedup, ack, retry)
   a file-transfer design actually needs, and which it explicitly drops.
2. Design the protocol mechanics: chunk format, sequence numbers, sender/receiver state
   machines, timers — borrowing consciously from TCP (L18) where justified.
3. Build a prediction-driven evaluation matrix: what you expect to happen under loss,
   delay, and reorder *before* implementing (LAB-09's caveat: reorder fakes congestion).
4. Write a testable specification another pair could implement — the deliverable is the
   spec, not code.

## Pre-lab
1. List TCP's reliability rungs (L17/L18) in order: ack, retransmit, ordering, dedup,
   flow control, congestion control.
2. LAB-09's T4 lesson: why is *reorder tolerance* a design requirement here?
3. Your app moves a 1 MB file over UDP. Why is stop-and-wait painful on a 50 ms link?
   (One number: window math.)

## Tasks

### T1 — Reliability definition (15 min, worksheet)
Choose and justify: which rungs your protocol implements for a file transfer over a
lossy/reordering link. Write the guarantee as a testable sentence: "The receiver's
output file is byte-identical to the sender's input when loss ≤ X% and reorder ≤ Y ms;
no guarantee beyond that."

### T2 — Protocol mechanics (35 min)
Specify, in the worksheet's table format (from L20's GA):
- **Chunk format:** `magic|seq|flags|length|payload` — field sizes and endianness
  (fixed 8-byte header is enough; say why your header is unambiguous when bytes repeat).
- **Sender state machine:** SEND → WAIT_ACK(n) → (timeout→resend, cap 3) / (ack→n+1)
  or your windowed design — draw both endpoints' diagrams in the worksheet.
- **Timers:** timeout value and *why* (2× your measured LAB-09 RTT? state it).
- **Termination:** explicit FIN-style chunk or quiet-period rule — pick one, defend it.

### T3 — Evaluation matrix (20 min)
Reproduce L20's matrix with *predictions*: transfer time + retransmit count for
(0% loss, no reorder), (2% loss), (5% + 50 ms ± 25 ms reorder), × 1 MB file, on a
50 ms RTT, 10 Mbit/s link. These numbers are graded in LAB-11 against reality —
the *comparison* is the assessment, not the prediction's accuracy.
**Expected observation (design stage):** every matrix cell contains *numbers*, and the
ack-path question (are your ACKs lossless?) is answered explicitly — the classic gap.

### T4 — Spec document (30 min clinic + homework)
Assemble T1–T3 into a 2–3 page spec: guarantee sentence, format table, both state
machines, timers, termination, evaluation matrix, and a test plan (which netem settings
prove which rung). Exchange specs with another pair for a 10-minute red-team review;
record their two hardest questions and your answers in an appendix.

## Troubleshooting (design-stage)
| Symptom | Likely cause | Action |
|---|---|---|
| Spec says "TCP but in UDP" | borrowing everything, justifying nothing | for each borrowed mechanism, one line: what breaks if omitted |
| No termination rule | forgot the end-of-file problem | FIN chunk vs quiet-period; state dedup consequences |
| Matrix assumes lossless ACKs | ACK path is also lossy! | predict ACK-retransmission behavior explicitly |

## Post-lab questions (append to spec)
1. Which rung did you *reject* and what workload would make that rejection wrong?
2. Your red-teamers' hardest question — and why your spec survives (or what you changed).
3. Where exactly could your protocol deadlock? (Both sides waiting — or both giving up.)

## Challenge (ungraded)
Design cumulative ACKs (ack = highest in-order seq) vs per-packet ACKs: predict which
survives ACK loss better and why. LAB-11's evaluation will test the prediction.

## Accessibility / low-resource alternatives
- Entirely paper-based; diagrams may be ASCII or described verbally (rubric-neutral).
- Remote pairs: the red-team review works over any text chat; paste the Q&A into the spec.

## Safety notes
No traffic in this phase — design only (ethics gate still applies to the spec's
failure-injection plans: syllabus-safety §3.2).
