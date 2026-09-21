# Lecture 20 — Instructor Teaching Notes
## Programming the Transport Layer: Reliability over UDP (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO5/CLO6 primary |
| Textbook anchor | KR §3.4 (principles of reliable transfer) |

---

## 1. Objectives hook
Board: **"In 18 and 19 you watched TCP do five things. UDP does none. Today you choose
which ones to rebuild — and write the document that will save you at 2 a.m. in week 12."**

Hook (2 min): show the project brief's evaluation matrix — "the spec you write today is
the *experiment design* you'll run in week 12. Writing it first is why some pairs will
demo calmly and others will demo panic."

## 2. Minute plan (workshop structure)

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | Recap + brief walk | L18/19 recall (2 items); project brief page-by-page |
| 8–25 | Concept 1 | The design method: requirements → mechanisms → states → timers → edge cases |
| 25–45 | Worked example | Instructor designs a stop-and-wait ARQ *live* (spec skeleton on board) |
| 45–55 | Concept 2 | Evaluation design: netem matrix; what each column proves |
| 55–60 | Break | — |
| 60–100 | **Workshop** | Pairs draft their specs (template in worksheet); instructor circulates |
| 100–110 | Peer swap | Two pairs exchange specs; red-team each other's edge cases |
| 110–118 | Common pitfalls + summary | Sliding-window traps; timer bugs; spec hygiene |
| 118–120 | Submission + preview | Spec collected; DNS next |

## 3. Concept walkthrough

### 3.1 The design method (17 min)
1. **Requirements first:** file transfer? chat? telemetry? Each implies different
   rungs: file transfer needs *all* rungs; chat needs ordering; telemetry may need
   neither (latest-wins). Writing "reliable" without naming what reliability *means*
   is the classic spec failure — force the definition.
2. **Choose mechanisms (the ladder from L17/18/19):**
   - Rung 1: **sequence numbers** (per-chunk).
   - Rung 2: **ACKs** (cumulative vs selective — show both ACK designs' costs).
   - Rung 3: **timeout + retransmit** (RTO shape from L18; backoff).
   - Rung 4: **in-order delivery** (reorder buffer) — *optional by requirement*.
   - Rung 5: **flow/congestion control** (window) — bonus tier.
3. **States & timers (the engineering heart):** sender: IDLE → SENDING(chunk i) →
   WAIT_ACK(i) → (timeout: resend) → …; receiver: EXPECTED(i) vs GOT(i). Timer
   granularity decisions (1 Hz vs 50 ms) change behavior dramatically — make
   students *choose and justify*.
4. **Edge cases (name them now, or meet them in week 12):** duplicate data (old
   chunk after timeout), ACK loss after data delivery (the classic two-army
   problem — your seq space answers it), reordering (did my retransmit race the
   original?), app closing mid-transfer, MTU (1,400 B chunks — L12/L17 discipline).

### 3.2 Worked design (instructor, live, 20 min)
Stop-and-wait ARQ for a 1 MB file, 1,400 B chunks (≈715 chunks):
- Header: [type:1][seq:2][len:2][crc16?] — walk why 16-bit seq is overkill and
  2–4 bits *plus* the alternating-bit trick suffices for stop-and-wait; why 32-bit
  for sliding window.
- States drawn on board (both endpoints); RTO = 300 ms fixed for v1; backoff v2.
- **Predicted throughput (L18/19 math):** 1,400×8/0.3 RTT ≈ 37 kbps — *the design
  is the bottleneck*; students compute it and immediately see why the window rung
  exists. This 60-second computation is the entire motivation for rung 5.

### 3.3 Evaluation design (10 min)
Matrix = the brief's required columns: loss {0, 2, 5, 10%} × reorder/delay settings ×
file size; per cell: completion time, retransmissions, correctness (checksum the file).
Predict *before* running (L04 discipline). The matrix converts "it works" into
evidence — the course's reproducibility rule applies to this project doubly.

### Reference diagram — Stop-and-wait sender state machine

```text
┌──────┐ send chunk n  ┌──────────┐ timeout  ┌───────────┐
│ IDLE │ ────────────→ │ WAIT_ACK │ ───────→ │ RESEND n  │
└──────┘ ←──────────── └──────────┘          └─────┬─────┘
       └──────────────── ack n ─────────────────────┘
```

## 4. Important definitions
Protocol spec · Stop-and-wait ARQ · Alternating-bit protocol · Sliding window ·
Cumulative vs selective ACK · Reorder buffer · RTO/backoff · Last-Mile edge cases
(dup data, ACK loss, reorder race) · Evaluation matrix.

## 5. Real-world examples
- **QUIC** rebuilt the whole ladder over UDP for the modern web — every design
  decision in today's workshop has a QUIC-shaped answer (name-drop, don't derive).
- **Game netcode:** "reliable-when-it-matters" layers (chat reliable, position
  unreliable-latest-wins) — the requirements-first step in industry form.

## 6. Mathematical/technical example
Stop-and-wait throughput ceiling: W=1 chunk: T = chunk_size/RTT (37 kbps example).
Sliding window: T = W×chunk_size/RTT until bandwidth binds — students compute the
window size needed to saturate their lab path (e.g., 100 Mbps × 5 ms / 11.2 kb ≈ 45
chunks) — that single number tells them which rung their project must reach for full
marks trajectory. (Connects L19's BDP to their own protocol.)

## 7. Workshop logistics (the 40-minute block)
Spec template (worksheet): goal & reliability definition; chunk format table; state
diagrams (both endpoints); timer table; edge-case list (≥5 from §3.1); evaluation
matrix (≥6 cells with predictions); milestone plan (W11 mid-check, W12 demo).
Instructor circulates with two questions per pair: "what does your receiver do when
the ACK is lost?" and "which rung did you skip and why?" — those two questions surface
90% of design flaws.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Reliable = TCP rebuilt in full" | Requirements decide the rungs; full rebuild is over-engineering (and won't beat TCP) |
| "The spec is paperwork after coding" | Here the spec *is* the deliverable's first graded stage; design-first is the lesson |
| "Timers can be added later" | Timer behavior *is* the protocol; underspecified timers are where demos die |
| "Sequence numbers must be huge" | Seq space serves the *mechanism*: stop-and-wait needs 1 bit; window needs more — size to design |
| "Testing = it worked once" | The evaluation matrix with predictions is the standard (reproducibility rule) |

## 9. Suggested practical demonstration
5-minute teaser: the reference stop-and-wait implementation under `netem loss 5%`
completing *slowly but correctly* — then the same with a 2 MB file showing the
throughput ceiling from §6. Students see both the correctness and the cost. ⚠
Pre-verify the reference implementation on the image; keep it instructor-only.

## 10. Classroom activities
The workshop *is* the activity; the peer swap (red-team) is the second. Keep the
red-team prompts concrete: "find the case where the receiver hangs forever."

## 11. Problem-solving questions
1. Your ACK for chunk 5 is lost. Walk both endpoints' states until recovery.
2. Why does stop-and-wait need only 1 bit of sequence?
3. Compute the window needed to reach 100 Mbps on your 5-ms lab path (1,400 B chunks).
4. Which edge case is unfixable by retransmission alone? (ACK-loss-after-delivery —
   needs idempotency/duplicate handling.)
5. Reorder arrives: chunk 7 before 6. What must the receiver hold, and what must it
   *not* deliver yet?

## 12. Formative assessment (with answers)
- MCQ: Stop-and-wait's ceiling is set by → **1 chunk per RTT**.
- MCQ: Which rung fixes the "37 kbps" problem? → **sliding window**.
- Short: two edge cases your spec must name. → dup data after timeout; ACK loss
  after delivery; reorder race (any two).

## 13. Exit ticket (submission checkpoint)
1. My protocol's reliability definition (one sentence): ________
2. Rungs I include / deliberately skip: ________ / ________
3. The evaluation cell I most fear: ________

## 14. Anticipated difficulties
- Perfectionism on chunk formats burns workshop minutes; cap format work at 10 min
  (state diagrams matter more).
- Pairs that skip the evaluation matrix will invent one in W12 — the brief makes it
  required; today's template makes it easy.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify reference implementation + netem demo on image
- [ ] Print project briefs + spec templates; plan red-team pairings
- [ ] Board pre-write: ladder rungs; stop-and-wait state diagram; throughput formula
- [ ] Submission portal ready (spec due at end of session)

## 16. Timing fallbacks
Shrink the worked design to the state diagram + one computation; workshop time is
sacrosanct — it's the graded deliverable's birthplace.

## 17. References
- KR §3.4; RFC 9293 (for mechanism citation in specs); RFC 9000 (QUIC — named).
- Project brief (labs/lab-10-11-reliable-transport/).
- ⚠ VERIFY image tooling; keep reference implementation out of student paths.
