# Lecture 19 — Instructor Teaching Notes
## TCP Flow & Congestion Control (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO5/CLO6 primary; CLO4 supporting |
| Textbook anchor | KR §3.5.5, §3.6–3.7; RFC 5681 |

---

## 1. Objectives hook
Board: **"Receiver's window: 64 KB. RTT: 100 ms. The link is 1 Gbps and empty. Your
download runs at… 5 Mbps. Who's throttling you, and why does TCP *want* to?"**

Hook (2 min): two `iperf3` runs to a far VM — one with default window, one with
`-w 4M`: the difference *is* the lecture. (Set up in advance ⚠.)

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L18 RTO recall; the window-limited iperf reveal |
| 6–26 | Concept 1 | Flow control: receiver window; throughput = W/RTT; BDP |
| 26–50 | Concept 2 | Congestion control: slow start → AIMD → fast recovery |
| 50–55 | Break | — |
| 55–72 | Worked examples | BDP math; sawtooth sketch; bufferbloat arithmetic |
| 72–75 | LAB-09 briefing | Sweep matrix + report requirements |
| 75–105 | LAB-09 (in-class) | netem sweeps, pairs; start analysis |
| 105–115 | Early findings | One pair presents a curve; class interprets |
| 115–120 | Summary + exit ticket | Project spec reminder |

## 3. Concept walkthrough

### 3.1 Flow control — don't drown the receiver (20 min)
- **Receiver window (rwnd):** advertised in every segment (the Window field + window
  scale option); "my buffer has this much room".
- **Throughput = min(rwnd, cwnd) / RTT** — the single most useful formula of the
  module. The hook's arithmetic: 64 KB / 100 ms = 5.24 Mbps regardless of 1 Gbps.
- **Bandwidth–delay product (BDP):** capacity × RTT = bytes "in flight" to fill the
  pipe: 1 Gbps × 100 ms = 12.5 MB. Window < BDP ⇒ the pipe can never fill — no
  amount of link speed fixes a small window. (This resolves L04's "single-stream
  iperf underestimates long paths" caveat from the measurement lecture.)
- Practical: window scaling option (why the 16-bit field needed an extension — 64 KB
  cap would strangle long-fat networks); autotuning in modern OSes (mention; the
  *math* is what we teach).

### 3.2 Congestion control — don't drown the network (24 min)
- Distinction (L18 planted it): flow control protects the *receiver*; congestion
  control protects the *network* (routers' queues). Two independent mechanisms, one
  min() in the sender's math.
- **cwnd — the sender's belief about network capacity.** Not advertised; learned.
- **Slow start (misnamed — it's exponential):** cwnd starts small (≈10 MSS, IW10 per
  modern stacks); +1 MSS per ACK → doubling per RTT. Purpose: find capacity *fast*
  without dumping a BDP into an unknown network on byte one.
- **ssthresh:** slow start → congestion avoidance when cwnd ≥ ssthresh.
- **Congestion avoidance (AIMD):** +1 MSS per RTT (linear); on loss:
  - **Timeout-loss (believed congestion, serious):** ssthresh = cwnd/2; cwnd resets
    to initial window; slow start again.
  - **3-dup-ACK loss (fast retransmit, L18) → fast recovery:** ssthresh = cwnd/2;
    cwnd ≈ ssthresh (+3, then per dup-ACK) and continue in congestion avoidance —
    the sawtooth without the cliff.
- **The sawtooth** (draw it): probes up linearly, halves on loss — AIMD's AJM+
  MD (additive increase, multiplicative decrease) is *deliberately* unstable at the
  top and forgiving on loss; it's how N senders share a bottleneck fairly-ish
  (sketch the two-flow convergence diagram — equalization over time).
- **Simplified-model flags:** modern variants (CUBIC's cubic growth; BBR's
  model-based bandwidth/RTT estimation instead of loss) exist — one slide, name and
  *one-sentence* distinction; ECN (routers mark instead of drop; L19-enr) named.
  Loss ≠ congestion always (wireless L10!) — honest caveat; CUBIC tolerates it
  better; BBR sidesteps loss-as-signal.

### 3.3 Bufferbloat (worked example block, 17 min)
- From L01: queueing delay explodes as ρ→1. *Bigger buffers make it worse*: a 1-GB
  buffer on a 10-Mbps link holds 800 s of data — a filled one means every packet
  waits minutes. Interactive traffic dies while throughput tests look *great*.
- The modern answer set (named): smart queue management (FQ-CoDel/AQM — name only),
  ECN, BBR's avoidance of queue buildup. Tie to L04's "loaded latency": students
  *measured* bufferbloat in LAB-01; now they can explain it.

### Reference diagram — AIMD congestion sawtooth

```text
cwnd │        ╱╲        ╱╲
     │       ╱    ╲     ╱    ╲     loss → multiplicative cut,
     │      ╱      ╲   ╱      ╲    then linear increase
     │     ╱        ╲ ╱        ╲   (+1 MSS per RTT)
     └─────────────────────────────→ time
```

## 4. Important definitions
rwnd/cwnd · BDP · In-flight data · Slow start (IW10) · ssthresh · AIMD ·
Sawtooth · Fast recovery · Timeout-loss vs dup-ACK-loss · Window scaling ·
CUBIC/BBR (named variants) · ECN (named) · AQM/FQ-CoDel (named) · Bufferbloat.

## 5. Real-world examples
- **Satellite/long-fat links** need huge windows — the BDP math explains why VPN
  users on high-RTT links get "slow downloads at low CPU".
- **Bufferbloat at home:** router defaults + a test rig = 300 ms loaded latency;
  fixing it (SQM/firmware) is a consumer-actionable consequence of this lecture.
- **Convergence:** two iperf3 flows started 30 s apart share roughly fairly within
  a couple of minutes — AIMD's promise made visible (LAB-09 optional task).

## 6. Mathematical/technical examples
1. BDP: 1 Gbps × 50 ms = 6.25 MB → window must exceed it for full speed.
2. Sawtooth numbers: 10-Mbps RTT 40 ms pipe, MSS 1460: loss-free period for AIMD
   from W/2 to W: W = throughput×RTT/MSS ≈ 10⁷×0.04/1460 ≈ 274 segments; recovery
   to 137→274 takes 137 RTTs ≈ 5.5 s — compute with class; the sawtooth is *slow*
   by design.
3. Bufferbloat: 10-Mbps link, 4-MB queue: 3.2 s queueing delay when full — compare
   to the 40 ms RTT floor: 80× worse.
4. LAB-09 prediction columns: students *predict* throughput for each netem setting
   before running (estimate discipline from L04, now with a formula that works).

## 7. LAB-09 briefing (3 min — extended in handout)
Sweep matrix on a VM pair: baseline; RTT {10, 50, 100 ms}; loss {0, 0.5, 2%};
bandwidth cap {100, 10 Mbps}; record throughput + retransmissions + RTT under load;
plot and interpret (expected: throughput ∝ 1/RTT at fixed window; loss cliffs;
bufferbloat in the RTT-under-load column). Report: graphs + interpretation per the
lab rubric. ⚠ Verify netem + iperf3 on image; pre-run the matrix once; note the
approximate runtimes so pairs finish in class.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Slow start is slow" | It's *exponential*; the name means "start small", not "start slow" |
| "Loss = broken network" | AIMD *requires* loss as its signal; wireless loss just makes that signal noisy (L10 tie-in) |
| "Bigger buffers always help" | Bufferbloat: they help throughput tests and destroy latency |
| "The receiver's window is the bottleneck" | min(rwnd, cwnd); the network's belief (cwnd) usually binds first |
| "Congestion control is in the routers" | It's endpoint behavior (cwnd); routers only queue/mark (AQM aside) |
| "TCP throughput is independent of RTT" | W/RTT: RTT is *in* the formula; long pipes need big windows |

## 9. Suggested practical demonstration
The hook's two-iperf comparison, then one live netem loss sweep with the throughput
number projected as it changes (iperf3 -i 1 prints per-second lines — watch the
sawtooth in real time). ⚠ Pre-verify; keep rates modest on shared teaching networks.

## 10. Classroom activities
- **Sawtooth sketch relay:** pairs draw cwnd through: start, slow start to 64 MSS,
  dup-ACK loss, recovery, timeout loss — compare boards; the *shape* is the
  understanding.
- **Bufferbloat role play:** one student is the queue (arms filling), two are flows,
  one is a ping packet trying to squeeze past — arms full = the latency tax.

## 11. Problem-solving questions
1. rwnd 64 KB, RTT 100 ms, 1 Gbps link: throughput? Which term binds?
2. Window to fill 1 Gbps × 50 ms? (BDP: 6.25 MB)
3. cwnd 200 MSS, loss via 3 dup-ACKs: new ssthresh and cwnd? (100/≈103-100 then AIMD)
4. Why does AIMD converge to fair sharing where pure "decrease by half of *your*
   share" might not? (qualitative — sketch the two-flow diagram)
5. 10-Mbps/40-ms link, MSS 1460: segments in flight at capacity? (≈274)

## 12. Formative assessment (with answers)
- MCQ: Throughput = → **min(rwnd, cwnd)/RTT**.
- MCQ: On timeout, cwnd → **resets to initial; ssthresh = cwnd/2**.
- MCQ: AIMD increase is → **+1 MSS per RTT (linear)**.
- Short: why does the sawtooth exist? → probing beyond capacity is how TCP
  *finds* the limit; loss is the feedback.

## 13. Exit ticket
1. Throughput formula: ________
2. BDP = ________ × ________
3. Timeout loss: cwnd does ________; dup-ACK loss: cwnd does ________.

## 14. Anticipated difficulties
- The min(rwnd,cwnd) algebra is fine; the *congestion* half being "imaginary
  receiver" (cwnd) is the leap — the role play and the loss-trigger contrast
  anchor it.
- LAB-09 reports overwhelm if started late: briefing includes the plot checklist;
  analysis can finish at home.

## 15. Instructor preparation checklist
- [ ] ⚠ Pre-run the full LAB-09 sweep; note runtimes; verify netem/iperf3
- [ ] Set up the two-window hook demo (`iperf3 -w` comparison)
- [ ] Print LAB-09 handouts + plot checklist
- [ ] Board pre-write: throughput formula; BDP; sawtooth axes; loss-trigger table

## 16. Timing fallbacks
Compress §3.1 by 5 minutes (rwnd is the easier half); the AIMD walkthrough and
LAB-09 start are protected; bufferbloat example can shrink to the one number.

## 17. References
- KR §3.5.5, §3.6–3.7; RFC 5681 (TCP congestion control); RFC 9293.
- iperf3 + netem documentation (LAB-09 handout).
- FQ-CoDel / bufferbloat literature (bufferbloat.net) — for the bufferbloat slide.
- ⚠ VERIFY editions/sections and image tooling this semester.
