# Lecture 06 — Instructor Teaching Notes
## Data Link Layer: Framing, Errors & Reliability (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary |
| Textbook anchor | PD §2.4–2.5 |

---

## 1. Objectives hook
Board: **"The wire gives you one long stream of bits. No spaces. No punctuation. Find the
words."**

Hook (2 min): write on the board `1101000110100111101001101100111011011` — "there's a
message in here. Where does one 'letter' end?" Let them squirm for 30 seconds, then
reveal: that is *exactly* the framing problem, solved billions of times per second.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L05 Shannon recall; framing puzzle on board |
| 6–26 | Concept 1 | Framing: sentinel, byte stuffing, bit stuffing |
| 26–50 | Concept 2 | Error detection: parity → checksum → CRC (with hand computation) |
| 50–55 | Break | — |
| 55–65 | Concept 3 | Error correction (FEC) vs detection+retransmission (ARQ) |
| 65–85 | GA-06 | CRC by hand, pairs (worksheet) |
| 85–100 | Worked example + discussion | Real frame walk: FCS verification; why Ethernet chooses detection |
| 100–112 | Problem-solving | Design questions (§11) in pairs |
| 112–118 | Summary + exit ticket | — |
| 118–120 | Preview | Ethernet & MAC next |

## 3. Concept walkthrough

### 3.1 Framing (20 min)
- The link delivers bits; the link layer must agree on **frame boundaries**. Three classic
  approaches:
  1. **Sentinel/flag with stuffing** (flag = 01111110 in HDLC/PPP):
     - **Bit stuffing** (HDLC): sender inserts a 0 after any five consecutive 1s in the
       payload, so the flag pattern can never appear in data; receiver deletes a 0 after
       five 1s. Worked example on the board: payload `0111111…` → `0111110…`.
     - **Byte stuffing** (PPP with byte-oriented links): escape byte `0x7D` precedes a
       `0x7E` (flag) or `0x7D` (escape) appearing in payload.
  2. **Clock-based framing** (SONET): frames at fixed time intervals — no flag needed.
  3. **Length-based framing** (Ethernet's approach): explicit length/type field plus the
     physical-layer preamble+SFD for *finding the start* (L07 detail).
- Stuffing cost: worst case overhead; random data rarely hits worst case — a quick
  probability remark (1/32 of positions for bit stuffing on average).
- **Why the receiver must un-stuff before error-checking** — common exam trap.

### 3.2 Error detection (24 min, the heart)
- Noise flips bits. Detection adds **redundancy**: send extra bits computed from the data;
  receiver recomputes and compares.
- **Parity (1 bit):** catches odd numbers of bit errors; misses 2 flips. Cost 1/n. Teach
  with the 7-bit ASCII + parity example; then show the 2-flip miss on the board.
- **Internet checksum (16-bit 1's complement sum):** IP/TCP/UDP; cheap in software, catches
  most burst errors but misses some (compensating errors). Reason it survives: end-to-end
  cheap safety net, not the last line (TCP checksum subtleties acknowledged; strong
  verification happens at L18 via sequence numbers anyway).
- **CRC — cyclic redundancy check (the workhorse):**
  - Model the message as a polynomial over GF(2) (coefficients 0/1; addition = XOR).
  - Sender and receiver agree on a generator polynomial G (r+1 bits). Sender appends r
    zero bits, divides by G (mod-2 polynomial division), appends the r-bit remainder as
    the FCS. Receiver divides the whole thing by G: remainder 0 ⇒ (almost certainly) no
    error.
  - Hand computation: use G = 1101 (r=3), message 101101 → worked step-by-step in §6.
  - Properties (state, don't prove): detects all single- and double-bit errors (with
    suitable G), all odd errors if G has (x+1) factor, all burst errors ≤ r; Ethernet's
    FCS-32, Wi-Fi's FCS-32, HDLC's FCS-16 are all CRCs.
- **Detection ≠ correction:** detection says "throw it away"; the frame is dropped (link
  layer) and recovery is someone else's job (transport — L18; or application).

### 3.3 Error correction vs retransmission (10 min)
- **ARQ (retransmission):** detect → drop → sender resends (acknowledgments/timeout —
  formalized at L18). Good when return path exists and errors are rare.
- **FEC (forward error correction):** send enough redundancy to *repair* in place
  (Hamming code concept: parity bits at power-of-two positions; corrects single-bit
  errors). Good when return path is expensive: deep space, one-way links, storage, and —
  importantly — **modern Wi-Fi/cellular** where retransmission costs scarce airtime.
- **Hybrid (HARQ)** — one sentence; cellular uses it.
- Design rule of thumb: low error rate + bidirectional link → ARQ; noisy/unidirectional/
  latency-critical → FEC. This becomes a CLO6 "evaluate alternatives" exam favorite.

### Reference diagram — Byte stuffing around the flag 01111110

```text
sent:  01111110 ┃ 011111 0 10 011111010 ┃ 01111110
       flag     ┃ payload: a 0 follows ┃ flag
                ┃ every five 1s        ┃
 receiver deletes each 0 that follows five 1s → original payload
```

## 4. Important definitions
Frame · Flag/sentinel · Byte stuffing · Bit stuffing · Parity · Two's-complement vs 1's-
complement checksum · CRC · Generator polynomial (G) · FCS · Codeword · Hamming distance
(concept) · FEC · ARQ · Burst error · MTU (mentioned; detailed L07).

## 5. Real-world examples
- **Ethernet FCS-32** sits in every frame you've ever sent; Wireshark usually doesn't show
  it (NICs strip/verify in hardware) — mention the "FCS captured by some drivers" setting.
- **ECC RAM and SSDs** are Hamming/BCH/LDPC FEC — the same math class, different medium.
- **QR codes** survive a coffee stain because Reed–Solomon FEC repairs the block — the
  perfect everyday FEC story.
- **Deep-space probes** (Voyager/New Horizons) rely on FEC because a retransmission costs
  hours.

## 6. Mathematical/technical example (the worked CRC, board centerpiece)
Message M = 101101, generator G = 1101 (r = 3).
1. Append zeros: 101101000.
2. Mod-2 division (XOR, no borrows):
   ```
   101101000 ÷ 1101:
   101101000
   1101
   ----
   011001000        (101101 XOR 1101 down to first 4 bits: 1011^1101=0110)
   continue aligning at each leading 1...
   remainder = 010  (instructor: perform fully on board, students copy each XOR)
   ```
3. Transmitted codeword = 101101**010**.
4. Receiver divides 101101010 by 1101 → remainder 0 ⇒ OK.
5. Flip one bit (e.g., 1011010**1**0 → 101101000): remainder becomes 010 ≠ 0 ⇒ detected.
(QA 2026-09-20: remainder and codeword re-verified by machine computation — polynomial
division and an independent register model both give 010 / 101101010. Earlier versions
of this file carried an erroneous 100/101101100 pair; do not reintroduce it.)

## 7. GA-06: CRC by hand (20 min)
Worksheet: compute codeword for M = 110101, G = 1011; then flip bit 4 of your answer and
recompute to *see* detection; finally a 2-bit flip to discover that small-G CRCs can miss
multi-bit errors (drives home "detection is probabilistic guarantees by class of error").
Answer key at the end of the worksheet (kept for instructor; students tear off? — no:
solutions live in the instructor copy of the lab folder; worksheet here has blanks only).

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "CRC corrects errors" | Detects; correction is ARQ/FEC's job |
| "Checksum and CRC are the same thing with different names" | Weak additive check vs polynomial division with guaranteed error classes |
| "Parity is useless" | It's the cheapest; still used in serial links & memory scrubbing where anything better costs power |
| "Stuffed bits are part of the data" | Receiver un-stuffs before CRC; sequence numbers in transport are not affected by link stuffing |
| "If CRC passes, the data is correct" | Only certain error classes are guaranteed; tiny false-negative probability by design |
| "FEC is always better because no retransmit" | Costs bandwidth & compute always; ARQ costs only when errors occur |

## 9. Suggested practical demonstration
Wireshark on a captured frame: show the trailer/FCS field (enable "assume FCS present" if
the driver captured it), then *manually edit* a byte in a hex editor copy and show the FCS
no longer matching using a CRC verification tool (e.g., `pycrc`-style online calculator or
`crcmod` in Python — pre-verified script). If time is short, the board CRC is sufficient.
⚠ Pre-run the edit-and-verify flow on the VM once.

## 10. Classroom activities
- **Stuffing drill:** 3 payloads stuffed on the board by teams (30 seconds each), racing.
- **Parity grid magic square:** 8×8 grid of bits; add row/column parity; flip a hidden bit;
  class finds it (teaches 2-D parity → leads into Hamming intuition).

## 11. Problem-solving questions
1. Stuff (bit stuffing, flag 01111110): payload 011111101111110111110000.
2. Why must stuffing be undone before FCS verification?
3. G = 1101, r = 3: how many burst-error bits are guaranteed caught?
4. A link has BER 10⁻⁶ and 12,000-bit frames: estimate frame error probability
   (≈ 1 − (1−10⁻⁶)^12000 ≈ 1.2%) — and discuss what the link should do about it.
5. Wi-Fi uses FEC + link-layer retransmissions; Ethernet uses detection only. Give one
   property of each medium that explains the difference.

## 12. Formative assessment (with answers)
- MCQ: HDLC bit stuffing inserts a 0 after → **five consecutive 1s**.
- MCQ: Ethernet's FCS is a → **CRC-32**.
- MCQ: Two flipped bits with simple 1-bit parity → **undetected**.
- Short: why does Wi-Fi prefer FEC more than wired Ethernet? → airtime is scarce and
  shared; retransmission costs everyone on the channel.

## 13. Exit ticket
1. Bit stuffing rule in one line: ________
2. CRC remainder for M=1101, G=1011 (append 3 zeros): ________
3. Detection or correction: which does Ethernet's FCS do? ________

## 14. Anticipated difficulties
- Polynomial division scares students: emphasize it's XOR long division; keep the first
  example fully guided before pairs start.
- Students conflate link-layer drops with transport recovery — explicitly name who does
  what (sets up L18 beautifully).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify the worked CRC steps by hand (do the division yourself on paper!)
- [ ] Prepare the parity-grid handout; print GA-06 worksheets
- [ ] If using the FCS-verify demo: pre-run the tool and keep screenshots as backup
- [ ] Board pre-write: flag value; the division skeleton; "detect vs correct" two-column table

## 16. Timing fallbacks
Drop §10 activities; compress §3.3 to 6 minutes; GA-06 must survive intact (it is the
assessed artifact and quiz 1 preview).

## 17. References
- PD §2.4–2.5; Tanenbaum data-link chapter (⚠ verify section).
- Peterson & Davie's CRC treatment; standard CRC-32 polynomial (IEEE 802.3).
- RFC 1662 (PPP in HDLC-like framing — byte stuffing reference).
- ISO HDLC (bit stuffing reference) — cite via PD rather than buying the standard.
- ⚠ VERIFY edition/sections this semester.
