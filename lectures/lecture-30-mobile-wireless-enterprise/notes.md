# Lecture 30 — Instructor Teaching Notes
## Mobile & Wireless Enterprise Networking (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO6 primary (design + evaluation); CLO2 physical-layer thread |
| Textbook anchor | KR 6.3–6.4 (skim); PD 2.7 |

---

## 1. Objectives hook
Board: **"Your phone never dropped a call crossing campus. Somebody designed
that — with power budgets and channel numbers."**

Hook (3 min): replay a short L10 spectrum shot, then show two APs on a floor
plan and ask: "why these two spots and not two others?" Collect guesses —
the lecture answers them with arithmetic.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | Recap + hook | L10/L11 recall; the "why these AP spots" puzzle |
| 8–30 | Concept 1 | Mobility: roam/reassociate, L3 problem, Mobile IP framing |
| 30–45 | Concept 2 | RF planning: link budget, FSPL, cell-edge target, channel reuse |
| 45–60 | Concept 3 | Enterprise auth & guest isolation; 4G/5G service classes |
| 60–65 | GA-30 briefing | Deliverables + rubric |
| 65–72 | Break | — |
| 72–105 | GA-30 (design) | Pairs design Meridian Building B wireless plan |
| 105–115 | Findings | Two pairs defend AP counts/channels; class critiques |
| 115–120 | Summary + exit ticket | — |

## 3. Concept walkthrough

### 3.1 Mobility: what roams, what doesn't (22 min)
- **Roam = reassociate:** the client drops one AP's link and attaches to
  another *on the same SSID*; open-standard exchanges (the 802.11
  reassociation, then security in L11's terms) make it fast. ⚠ Exact
  handshake message names vary by security mode — verify against 802.11
  before testing this on students.
- **Why enterprises care:** a client re-associating *within one VLAN/subnet*
  keeps its IP → TCP sessions (L18) survive; roam across subnets breaks
  every connection. The enterprise pattern: one big L2 domain per user
  group (or controllers tunneling traffic to a central anchor).
- **The L3 problem, framed:** Mobile IP's idea — a *home address* stays
  stable while a *care-of address* changes, with a home agent forwarding —
  taught as the classic framing, not as deployed reality; say plainly that
  enterprises usually solve it by avoiding the problem (keep the L2 domain
  seamless) rather than by deploying Mobile IP.

### Reference diagram — Seamless roaming: same subnet, IP survives

```text
        ┌──── AP-1 ────┐      ┌──── AP-2 ────┐
        │  ch 36       │      │  ch 36       │   same SSID;
        └──────┬───────┘      └──────┬───────┘   client re-associates
             ┌─┴─────────────────────┴─┐         without losing L3:
             │  WLC / gateway (RADIUS) │         802.11 roam,
             └─────────────────────────┘         IP stays
```

### 3.2 RF planning: the arithmetic of coverage (15 min)
- **Link budget in one line:** received power = TX power + antenna gains −
  free-space path loss (FSPL); teach FSPL(dB) = 32.44 + 20·log₁₀(f_MHz) +
  20·log₁₀(d_km), i.e. ≈ 100 + 20·log₁₀(d_km) at 2.4 GHz (⚠ verify against
  your reference), and the design habit: margin ≥ 15 dB above sensitivity
  at the *cell edge*, aiming for the common −67 dBm target.
- **Coverage vs capacity:** one AP covers a floor at low density; a lecture
  hall needs many small cells because *airtime*, not signal, is the
  scarce resource (L10's CSMA intuition returns).
- **Channel reuse:** 2.4 GHz gives 3 non-overlapping channels (1/6/11) —
  adjacent APs never share one; 5 GHz has many more, so plan 5 GHz
  primary and treat 2.4 GHz as legacy.

### 3.3 Auth and the cellular headlines (15 min)
- **Enterprise wireless = 802.1X:** each user authenticates individually
  (RADIUS), so one stolen PSK cannot compromise the SSID (L11 revisit);
  guest: separate SSID/VLAN + internet-only policy (L25's zones).
- **4G/5G as service classes:** eMBB (broadband), URLLC (low-latency),
  massive IoT (many devices) — headline numbers depend on spectrum,
  distance, and load (L01's shared-medium lesson); handover exists in
  cellular too, managed by the carrier, not the user.

## 4. Important definitions
Handover / reassociation · Seamless L2 roaming · Cell edge (−67 dBm design
target) · Link budget & margin · FSPL · Coverage vs capacity · Channel
reuse plan (1/6/11) · 802.1X/RADIUS · Guest isolation · eMBB / URLLC /
massive IoT · (Mobile IP: home address, care-of address, home agent).

## 5. Real-world examples
- **The campus tour test:** walk L01's route during a call; the design that
  keeps it alive is today's worksheet.
- **The warehouse deployment story:** coverage-first design failed at
  peak — capacity cells and channel reuse fixed it (both GA-30 rubric rows).

## 6. Mathematical/technical example
Cell-edge link budget (worked): TX +20 dBm, antenna gains +2 dBi total →
EIRP +22 dBm. FSPL at 50 m on 2.4 GHz ≈ 100 + 20·log₁₀(0.05) ≈ 74 dB →
received ≈ 22 − 74 = −52 dBm: far above the −67 dBm target, so open-space
distance is not the constraint. Add one wall (−12 dB): ≈ −64 dBm — still
inside the target but with almost no margin. The lesson in three numbers:
*walls, not distance, dominate in-building design.* Second: an 80 MHz-wide
5 GHz channel shares airtime across ~30 active clients — per-client
expectation arithmetic straight into GA-30.

## 7. GA-30 mechanics (in-lecture, 40 min total)
Worksheet: RF drills (10) + Building B design grid (25) + findings (5).
Rubric rows: coverage reasoning, channel plan legality, auth/isolation
choices, capacity estimate. ⚠ No live RF work in the classroom unless the
room is instrumented — use LAB-11's captured spectrum instead; the design
is pencil-and-paper by intent.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Roaming = getting a new IP" | Seamless roaming is *within* one L2 domain; the IP survives — that's the design goal |
| "More APs always means better Wi-Fi" | Overlap on a channel is contention; coverage ≠ capacity |
| "Full signal bars = fast network" | Bars measure one direction of one link, not airtime sharing or backhaul |
| "5G means phones only" | The service classes (URLLC, massive IoT) aim far beyond handsets |
| "Mobile IP is how enterprise Wi-Fi works" | It's the classic L3 framing; enterprises avoid the problem with seamless L2 |

## 9. Suggested practical demonstration
- LAB-11's captured spectrum view (no live RF in class ⚠): identify channel
  overlap from the trace.
- Roam test recording (if the room allows): client on a call walking
  between two APs — show the reassociation moment in a packet capture.
  ⚠ Verify tooling and permissions beforehand; otherwise show the trace.

## 10. Classroom activities
- **"Spot the reuse violation":** a floor plan with channel numbers — teams
  find the two adjacent same-channel APs (30 s, whiteboards).
- **Link-budget speed round:** three distance/target combos; teams estimate
  pass/fail before computing (estimation habit from L04).

## 11. Problem-solving questions
1. A floor is 40 m × 20 m; target −67 dBm at the edge. Estimate AP count
   and justify (FSPL + wall assumption stated).
2. Two APs on channel 6, 15 m apart, both busy: what do clients experience,
   and which plan change fixes it?
3. A TCP download survives a roam between AP-1 and AP-2. What must have
   been true at L2/L3? What breaks if AP-2 is a different subnet?
4. Why does a lecture hall of 200 students need more APs than a warehouse
   of the same size?
5. Your campus SSID uses WPA2-PSK; IT wants per-user accountability. Which
   architecture change delivers it, and what does it cost?

## 12. Formative assessment (with answers)
- MCQ: Seamless roaming keeps → the IP address (same L2 domain).
- MCQ: Three non-overlapping 2.4 GHz channels → 1, 6, 11.
- Short: −67 dBm at cell edge is → the design target ensuring ≥ ~15 dB
  margin above a typical client sensitivity (accept equivalent phrasings).
- Exit diagnostic: one GA-30 grid row re-defended aloud.

## 13. Exit ticket
1. Roaming inside one enterprise SSID keeps your ________ unchanged; the
   802.11 event that moves you is ________.
2. The three non-overlapping 2.4 GHz channels are ________, ________, ________.
3. The two capacity numbers a design must state for a lecture hall:
   ________ and ________.

## 14. Anticipated difficulties
- Students conflate roaming (L2) with handover (cellular) and Mobile IP
  (L3) — the definitions table separates them; keep naming which layer.
- Link-budget dB arithmetic intimidates; the worked example plus speed
  rounds keep it to subtraction and one log lookup.
- GA-30 over-designing (APs everywhere): the rubric's capacity row and the
  channel-legality row constrain it.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify FSPL constant + −67 dBm target against your reference before class
- [ ] Meridian Building B floor plan printed (1 per pair); rubric visible
- [ ] LAB-11 spectrum trace loaded; roam-trace ready or fallback stated
- [ ] Channel-reuse floor plan for the 30-second activity on the board

## 16. Timing fallbacks
The 4G/5G segment may compress to the three service classes in one slide;
findings may shrink to one pair; the second activity drops first. Do not
cut the GA-30 briefing — the rubric is the assessment artifact.

## 17. References
- Kurose & Ross, *Computer Networking* 8th ed., §6.3–6.4 (skim) ⚠ verify
  section numbers against your edition.
- Peterson & Davie, *Computer Networks: A Systems Approach* 6th ed. (open
  edition), §2.7 wireless background.
- IEEE 802.11 (WLAN) and IEEE 802.1X (port-based access control) —
  standards family references, read for terminology not test prep.
- Meridian Building B plan (CS-01 bundle); LAB-11 spectrum captures.
