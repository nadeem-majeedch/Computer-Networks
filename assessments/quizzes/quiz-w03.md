# Weekly Quiz — Week 03 (L05, L06)

| Field | Value |
|---|---|
| Coverage | L05 — Physical layer: signals, media & transmission basics · L06 — Data link: framing, errors & reliability |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO2|L05]** State the difference between *bandwidth* in Hz and *throughput* in
b/s, and why a 1 MHz channel never automatically means 1 Mb/s.

**Q2 [I|CLO2|L05]** Using Shannon's capacity law, compute the maximum error-free bit
rate of a 3 kHz channel with SNR = 30 dB. (You may use log₂(1001) ≈ 9.97.)

**Q3 [I|CLO2|L05]** Nyquist check: a noiseless 4 kHz channel uses 4 signal levels. Max
symbol-independent bit rate? Show the formula.

**Q4 [B|CLO2|L06]** In one sentence each: what class of error does (i) 2-D parity,
(ii) an internet checksum, (iii) a CRC detect better than the previous one in the list?

**Q5 [I|CLO2|L06]** A data-link protocol must escape both a flag byte and an escaped
byte. Show what the transmitted byte sequence becomes for data `A ESC FLAG B`, and state
what the receiver reverses it to.

**Q6 [B|CLO2|L05]** You must run a 300 m link beside heavy industrial motors. Choose
copper UTP or fiber, and give the two physical-layer reasons from L05.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Bandwidth (Hz) is the width of frequencies the channel passes; throughput (b/s)
is delivered bits per second. Bits/s depends on encoding/symbol rate and SNR (Nyquist
caps symbols/s at 2B; Shannon caps b/s by noise), so Hz ≠ b/s. [B·CLO2]

**Q2.** 30 dB → SNR = 10³ = 1000. C = B·log₂(1+SNR) = 3000 × log₂(1001) ≈ 3000 × 9.97
≈ **29.9 kb/s** [MC]. [I·CLO2]

**Q3.** Nyquist: rate = 2B·log₂M = 2 × 4000 × log₂4 = 2 × 4000 × 2 = **16 kb/s** [MC].
Note for class: this is the noiseless ceiling — Shannon governs once noise exists. [I·CLO2]

**Q4.** (i) 2-D parity catches single-bit errors in two dimensions and many burst
patterns a single parity row misses; (ii) a checksum sums words and catches errors
parity misses on longer blocks (but is weak to compensating errors); (iii) a CRC's
polynomial division detects all burst errors shorter than the polynomial degree and
far more multi-bit patterns. [B·CLO2]

**Q5.** Canonical rule: every ESC in data → `ESC ESC`; every FLAG in data →
`ESC FLAG`. So data `A ESC FLAG B` transmits as **`A ESC ESC ESC FLAG B`** (the data
ESC doubles, then the data FLAG is escaped), and the receiver reverses exactly that
mapping. [I·CLO2]

**Q6.** Fiber: immune to electromagnetic interference (motors radiate noise UTP must
reject) and supports the distance — copper's channel limits/pair loss at 300 m exceed
typical UTP segment rules (100 m class channels), while fiber attenuation at 300 m is
far below budget. [B·CLO2]
