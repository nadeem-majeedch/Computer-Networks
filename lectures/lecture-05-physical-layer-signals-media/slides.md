# Lecture 05 — Physical Layer: Signals, Media & Transmission Basics — Slide Deck

| Field | Value |
|---|---|
| Slides | 17 (120 min: 10 open · 55 teach · 5 break · 40 GA-05 drills · 10 wrap) |
| Companions | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) (GA-05 capacity drills) |
| Style | [Course deck conventions](../../lectures/README.md#deck-conventions) |

## Deck outline

| # | Slide | # | Slide |
|---|---|---|---|
| 1 | Title | 10 | Media: copper vs fiber vs air |
| 2 | Hook: shouting a 1 across town | 11 | Encoding in one slide |
| 3 | From bits to signals | 12 | Worked example: capacity of a link |
| 4 | Bandwidth in Hz ≠ b/s | 13 | GA-05 drills brief |
| 5 | Nyquist: the noiseless ceiling | 14 | Classroom questions |
| 6 | Shannon: the noisy ceiling | 15 | Common misconceptions |
| 7 | Worked example: both laws | 16 | Summary |
| 8 | SNR & decibels | 17 | Exit question |
| 9 | dB table | | |

## Slides

### Slide 1 — Title
**Computer Networks — Lecture 5**
Physical layer: signals, media & transmission basics

> Notes — CLO2 anchor. The data link hands L1 a "1" and asks it to be shouted 10 km — how?

### Slide 2 — Hook: shouting a 1 across town
- "Shout this 1 so someone 10 km away hears it"
- Distance, noise, and hearing are the whole story
- Nyquist and Shannon are just that, in math

> Notes — 2 min. Keep physics honest: finite signal speed (≈5 µs/km fiber) and noise floors are the real villains.

### Slide 3 — From bits to signals
- L1 converts bits → **symbols** → waveforms
- Symbol rate (baud) vs bit rate = symbols × bits/symbol
- Modulation encodes bits into amplitude/phase/frequency

> Notes — One concrete wave sketch on the board (4-ASK). The baud≠b/s distinction feeds directly into Nyquist.

### Slide 4 — Bandwidth in Hz ≠ b/s
- **Bandwidth (Hz)**: width of frequencies the channel passes
- Bits/s depends on symbols/s *and* bits per symbol
- Two laws cap it: Nyquist (noiseless) and Shannon (noisy)

> Notes — The title IS the misconception. Preview: today ends with both formulas used on the same channel.

### Slide 5 — Nyquist: the noiseless ceiling
- **C = 2B·log₂M** (B = Hz, M = signal levels)
- Doubles the spectrum → doubles the rate
- More levels → more bits per symbol

> Notes — Work the formula's shape: 2B is the sampling insight; log₂M converts levels to bits. Noise enters on the next slide.

### Slide 6 — Shannon: the noisy ceiling
- **C = B·log₂(1 + SNR)**
- More noise → fewer distinguishable levels
- Fixes: more Hz or better SNR — nothing else

> Notes — The law's punchline: "re-encode with more levels" does NOT beat Shannon (worksheet drill 5 tests exactly this).

### Slide 7 — Worked example: both laws
- B = 4 kHz
- Nyquist, M = 16: 2·4000·4 = **32 kb/s**
- Shannon, SNR = 20 dB (×100): 4000·log₂101 ≈ **26.6 kb/s**

> Notes — Same channel, two ceilings: the *smaller* binds (26.6). This pairing is the lecture's core exam pattern.

### Slide 8 — SNR & decibels
- SNR = signal power ÷ noise power
- **dB = 10·log₁₀(SNR)** — 20 dB = ×100, 30 dB = ×1000
- +10 dB = ×10 power ratio

> Notes — Drill the two anchor conversions until reflexive; Shannon drills all term use them.

### Slide 9 — dB table

| dB | Ratio |
|---|---|
| 0 | 1 |
| 10 | 10 |
| 20 | 100 |
| 30 | 1000 |

> Notes — 60-second slide; keep it on screen during GA-05 drills as a crutch that fades by L30.

### Slide 10 — Media: copper vs fiber vs air

| | UTP copper | Fiber | Wireless |
|---|---|---|---|
| Distance | ~100 m | km | varies |
| EMI immunity | low | total | none (shared air) |
| Cost/port | lowest | higher | lowest install |

> Notes — Media choice is engineering trade-off, not fashion. The desk-level dominance of copper (cost) despite fiber's physics — exam-ready nuance.

### Slide 11 — Encoding in one slide
- Lines must self-clock: transitions carry timing
- Manchester (old Ethernet) vs 4B/5B vs modern scramblers — one idea: **transitions**
- DC balance matters on long runs

> Notes — Teaching model, not implementation detail — say so. Depth lives in the enrichment notes.

### Slide 12 — Worked example: capacity of a link
- Wi-Fi channel 20 MHz, SNR 25 dB (×316)
- Shannon: 20×10⁶ × log₂317 ≈ 20×10⁶ × 8.31 ≈ **166 Mb/s**
- Real 802.11ac delivers less — airtime contention, overheads

> Notes — Bridging slide: the law explains why "AC1200" marketing ≠ real throughput. Numbers desk-checked.

### Slide 13 — GA-05 drills brief
- Worksheet: 6 capacity drills, pairs
- Every answer: which law, which unit, stated assumptions
- 35 min + plenary of the two hardest

> Notes — Drill 4 (inverse Shannon: solve for B) and drill 5 (vendor-claim debunk) are the assessable stretch.

### Slide 14 — Classroom questions
1. Why can't new encoding beat a Shannon ceiling?
2. Fiber beats copper on distance — give the *physical* reason.
3. Your SNR drops 10 dB — what happens to capacity?

> Notes — Q3 answer: capacity roughly ÷3.4 (log₂(1+SNR) shrinks) — let students compute with the dB table.

### Slide 15 — Common misconceptions
- "Fiber is instant" → ≈2×10⁸ m/s, finite
- "More Hz always helps" → only if the band exists and passes
- "dB is absolute power" → it's a ratio

> Notes — Notes.md §6 gives counters for each; the dB one bites students all semester.

### Slide 16 — Summary
- Bits → symbols → signals; symbol rate × levels ≠ free
- Nyquist caps noiseless; Shannon caps noisy
- Media trade: distance, EMI, cost
- Next: framing and error detection (L06)

> Notes — Recap by formula recall, not slide reading.

### Slide 17 — Exit question
Channel 1 MHz, SNR 30 dB. Shannon ceiling in kb/s?
*(log₂1001 ≈ 9.97)*

> Notes — Answer: 1000 × 9.97 ≈ 9.97 → **≈ 9 970 b/s ≈ 10 kb/s**. Exit slips feed W03 quiz pool.

### Demonstration instructions (instructor)
- Optional 3-min demo: two signal-generator apps (or audio scope app) show a 1 kHz vs 4 kHz "channel" carrying the same melody — hearing degrades as bandwidth narrows
- No capture needed today; keep focus on the math drills
- ITI: verify worksheet arithmetic against `tools/scripts/verify_assessment_numbers.py` pattern before first use

### References for the deck
- PD §2.1–2.3 (bandwidth, Nyquist, Shannon, media)
- Tanenbaum & Wetherall physical-layer chapter (⚠ verify edition/section numbers)
- IEEE 802.3 (media standards home)
