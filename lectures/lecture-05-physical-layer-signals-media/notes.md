# Lecture 05 — Instructor Teaching Notes
## Physical Layer: Signals, Media & Transmission Basics (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary; CLO1 reinforced |
| Textbook anchor | PD §2.1–2.3; Tanenbaum physical-layer chapter (⚠ verify edition/section) |

---

## 1. Objectives hook
Board: **"The data link layer hands the physical layer a 1 and asks it to shout it 10 km.
What does 'shouting a 1' even mean?"**

Hook (2 min): play a 4-minute-old dial-up handshake recording (or a spectrogram video).
Students hear bits becoming sound. "Modulation is not magic; it's just agreed symbols."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L04 measurement recall; dial-up audio |
| 6–22 | Concept 1 | Signals, bandwidth (Hz), symbols, modulation basics |
| 22–40 | Concept 2 | Channel limits: Nyquist (noiseless) & Shannon (noisy) |
| 40–55 | Concept 3 | Media: twisted pair, coax, fibre, wireless — with numbers |
| 55–60 | Break | — |
| 60–75 | Worked examples | Capacity calculations, instructor-led (§6) |
| 75–95 | GA-05 | Pairs: calculation drills (worksheet part A) |
| 95–108 | Concept 4 | Encoding basics; connectors; why fibre won the backbone |
| 108–118 | Summary + exit ticket | — |
| 118–120 | Preview | Errors & framing next (L06) |

## 3. Concept walkthrough

### 3.1 Signals, symbols, modulation (16 min)
- The physical layer's job: convert bits into **signals** that survive a medium, and back.
- **Bit rate vs symbol rate (baud):** a symbol is a distinguishable state (voltage level,
  phase, frequency); with M distinct symbols each symbol carries **log₂M bits**. Simplified
  teaching model: real systems add coding/spreading (constellations like QAM, OFDM
  subcarriers); the logic of "more distinguishable states = more bits per symbol" is what
  we teach here.
- **Bandwidth in Hz vs data rate in b/s — the L01 tension resolved:** analogue bandwidth
  (frequency span the medium passes) bounds how *fast symbols can change*; Nyquist gives the
  noiseless ceiling.
- Modulation menu (one slide each, intuition only): amplitude, frequency, phase;
  **QAM** as the workhorse (amplitude + phase = constellation points); spread-spectrum/
  OFDM mentioned as "how Wi-Fi really does it" — details deliberately out of scope.

### 3.2 The two great limits (18 min)
- **Nyquist (1928, noiseless):** C = 2B·log₂M, where B = channel bandwidth in Hz, M = signal
  levels. Message: *you cannot clock symbols faster than the channel's frequency response
  allows* (inter-symbol interference appears beyond it). Example: B = 3 kHz telephone
  channel, M = 2 → 6,000 b/s — the old modem world.
- **Shannon (1948, noisy):** C = B·log₂(1 + S/N). Message: noise sets the *information*
  ceiling regardless of cleverness. Decibels: SNR(dB) = 10·log₁₀(S/N); convert back with
  S/N = 10^(dB/10). Example: 30 dB → S/N = 1000 → log₂(1001) ≈ 9.97 bits/symbol.
- **How they combine in practice:** Nyquist caps symbol rate (≈2 symbols/s per Hz in the
  simple model); Shannon caps bits per second. Engineering = push M (constellation size)
  until you approach Shannon, never past it. Modern Wi-Fi/cable modems are exactly this
  trade at scale (adaptive modulation: good SNR → big constellation; bad → small).
- Why both matter: a noiseless 4 kHz channel could carry infinite bits by making M huge —
  noise is what makes information scarce. This is the punchline of the lecture.

### 3.3 Media (15 min)
| Medium | Typical use | Data rates (order of magnitude) | Key strengths / limits |
|---|---|---|---|
| Twisted pair (Cat 5e/6/6A) | Office LANs, 100 m runs | 1–10 Gbps (2.5/5/10G on Cat6A) | Cheap, easy; distance-limited; crosstalk managed by twisting |
| Coax | Cable broadband, legacy CCTV | ~1–10 Gbps shared (DOCSIS) | Good shielding; bus heritage |
| Fibre (SM/MM) | Backbone, FTTH, DCs | 10G–400G+ per lambda; many lambdas via WDM | Distance + bandwidth king; no EMI; costlier ends |
| Wireless (2.4/5/6 GHz) | Mobility, last metres | 100 Mbps–few Gbps shared, *half duplex* | Mobility; shared airtime, interference, physics penalties |

- Fibre intuition: light, total internal reflection; single-mode (laser, long haul) vs
  multi-mode (LED/VCSEL, short runs); WDM = many colours = many channels on one strand.
- Wireless physics penalties preview (full treatment L10): path loss, interference,
  half-duplex airtime — "the air is a party everyone shouts over".

### 3.4 Encoding basics & connectors (13 min)
- **Encoding** = mapping bit sequences to signal patterns. Motivations: clock recovery
  (receiver must know where bits begin), DC balance (transformers/AC coupling), error
  detection (L06). Sketch: NRZ (simple, DC-drifting) → Manchester (clock in every bit,
  50% overhead, classic Ethernet) → 4B/5B & line codes with controlled transitions
  (Fast Ethernet) — the trend: *trade raw efficiency for receiver friendliness*, then win
  it back with faster electronics.
- Connectors/cabling reality (2 min, pictures): RJ45, T568A/B (say "pick one, be
  consistent"), LC/SC fibre connectors, PoE existence.

### Reference diagram — NRZ waveform for bits 1 0 1 1 0

```text
+V   ────┐      ┌────────
         │      │        │  1 = high, 0 = low
  0V     └──────┘        └────
       t0     t1   t2  t3   (one bit per clock tick)
```

## 4. Important definitions
Signal · Symbol (baud) · Bit rate vs symbol rate · Modulation · QAM (concept) ·
Channel bandwidth (Hz) · SNR & decibel · Nyquist limit · Shannon capacity ·
Baseband vs broadband · Encoding · Line coding · Twisted pair / coax / single-mode /
multi-mode fibre · WDM · Attenuation · Crosstalk · EMI.

## 5. Real-world examples
- **Your Wi-Fi "signal strength" bars** are SNR storytelling: −60 dBm excellent, −80 dBm
  suffering — adaptive modulation drops constellation size (Shannon at work) before drops
  become drops.
- **DOCSIS 3.1 cable modems** = QAM on many narrow channels; ISP marketing "gigabit" is
  Shannon arithmetic on shared coax.
- **Submarine fibre cables** carry terabits on a few fibre pairs using WDM + coherent
  optics: Shannon limited, and you can look up the *actual* capacity per cable — engineering
  at the limit.
- **ADSL vs fibre to the home:** same copper pair, frequency span and noise decide — why
  "fibre everywhere" replaced "faster DSL".

## 6. Mathematical/technical examples (worked on the board)
1. Telephone channel: B = 3 kHz, SNR = 30 dB → Shannon: C = 3000·log₂(1+1000) ≈ 30 kbps —
   matches dial-up modems' ceiling (they hit it).
2. Wi-Fi 40 MHz channel at 20 dB: C = 40×10⁶·log₂(1+100) ≈ 40×10⁶×6.66 ≈ 266 Mbps —
   *before* overheads; real 802.11n achieves ~150 Mbps — overheads & half duplex are real.
3. dB conversions: 20 dB = ×100; 30 dB = ×1000; −3 dB = half power; signal at −70 dBm and
   noise floor −90 dBm → SNR = 20 dB.
4. Nyquist then Shannon on the same channel: B = 1 MHz, M = 4: Nyquist = 2×10⁶×2 = 4 Mbps;
   if SNR = 15 dB (≈31.6): Shannon = 10⁶×log₂(32.6) ≈ 5 Mbps → Shannon permits 5, Nyquist
   with M=4 gives 4: increase M to approach 5 but noise forbids M beyond ~32 levels:
   log₂32.6 ≈ 5.02 → M=32 is already at the edge. Interlock the two laws concretely.

## 7. GA-05: Nyquist/Shannon calculation drills (20 min)
Worksheet part A (pairs): 6 problems escalating from plug-in to design judgment
(reverse problems: "what SNR does this claim require?"). Emphasize units and the
noiseless/noisy distinction. Debrief two problems on the board.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Bandwidth (Hz) and data rate (b/s) are the same" | Nyquist/Shannon connect but distinguish them; Hz is a property of the channel, b/s of the achieved encoding |
| "Bigger M is always better" | Noise floor punishes big constellations; adaptive modulation exists precisely for this |
| "Fibre is always better than copper" | Ends cost more; for 5 m runs copper wins on cost; fibre wins distance/EMI/aggregate capacity |
| "Wi-Fi Gbps numbers are throughput" | PHY rates; shared airtime, half duplex, management frames eat half or more (L10) |
| "dB is a unit of power" | It's a *ratio*; dBm is the absolute reference (1 mW) |
| "Light in fibre travels at c" | ~2×10⁸ m/s in glass — L01's propagation number was already this |

## 9. Suggested practical demonstration
Option A (cheap, reliable): function generator or phone tone + microphone oscilloscope app
showing a sine wave; increase frequency until the "channel" (a low-pass filter app) smears
it — ISI made visible.
Option B (VM): none needed — this lecture is deliberately tool-free; keep it that way to
protect the 20-minute drill block.
⚠ If using audio demos, test room speakers beforehand.

## 10. Classroom activities
- **Constellation intuition:** draw 4-QAM vs 64-QAM on the board; ask which survives a
  noisy room (gestures get loud — literally demonstrate with noise).
- **Media triage (pairs):** 5 scenarios (dorm wiring, 100 km backbone, factory floor with
  motors, heritage building, stadium event) → choose medium + justify in one line.

## 11. Problem-solving questions
1. B = 4 kHz, M = 16, noiseless → max b/s? (32 kbps)
2. B = 3 kHz, SNR = 20 dB → Shannon ceiling? (≈20 kbps: 3000×log₂101≈19,975)
3. B = 20 MHz, SNR = 25 dB → ceiling? (≈166 Mbps: log₂(1+316)≈8.31)
4. Need 1 Gbps at SNR 30 dB → minimum B? (≈100 MHz: 10⁹/log₂1001 ≈ 10⁹/9.97)
5. Vendor claims 5 Gbps on 100 MHz: required SNR? (5×10⁸/10⁸ = 5 b/sym → SNR ≈ 2⁵−1 = 31
   ≈ 15 dB — plausible!) — then in a noisy gym at 8 dB? (Not plausible.)

## 12. Formative assessment (with answers)
- MCQ: Shannon capacity depends on → **bandwidth and SNR**.
- MCQ: Doubling SNR (×2, linear) adds about → **1 bit/symbol** (log₂(2S/S+N)≈1).
- MCQ: Which medium for a 80 km inter-campus link? → **single-mode fibre**.
- Short: why do modems drop speed as signal degrades? → adaptive constellation shrink to
  stay under Shannon; errors otherwise explode.

## 13. Exit ticket
1. The two channel-limit formulas and what each assumes: ________
2. 20 dB SNR = S/N ratio of ________; −3 dB means ________.
3. Which medium for: 2 m patch cable? 60 km between towns? ________ / ________

## 14. Anticipated difficulties
- Logarithms: give the 3-line dB conversion recipe on the board and keep it there all
  lecture; scientific calculators/phones permitted for GA-05 (say so explicitly).
- Hz vs b/s relapse from L01: every formula written with explicit units on the board.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify audio demo (or skip; lecture is tool-free by design)
- [ ] Print GA-05 sheets (with the dB recipe at top)
- [ ] Board pre-write: the two formulas + dB recipe + media table skeleton
- [ ] Calculators permitted — announce at start (avoid covert phone use)

## 16. Timing fallbacks
Drop §3.4 encoding to a 3-minute sketch (readings cover it); protect §3.2 and GA-05 —
they carry the quiz and the assessed worksheet.

## 17. References
- PD §2.1–2.3 (physical layer, media); Tanenbaum physical-layer chapter (⚠ verify section).
- C. Shannon, "A Mathematical Theory of Communication" (1948) — historical citation for the
  capacity theorem; H. Nyquist (1928) — sampling/levels result.
- IEEE 802.3 (media standards families); ITU-T G-series recommendations (DSL/optical).
- ⚠ VERIFY edition/section numbers this semester.
