# Lecture 30 — Worksheet (GA-30) & Exit Ticket

Name: ________________  Date: ______  Pair: ________________

## Part A — RF drills (10 min)
Show your work; round dB to whole numbers. Use FSPL(dB) ≈ 100 + 20·log₁₀(d_km)
on 2.4 GHz; TX +20 dBm, antenna gains +2 dBi total (EIRP +22 dBm).

1. FSPL at 100 m in free space: ________ dB; received power: ________ dBm.
2. Pass/fail vs the −67 dBm cell-edge target at 100 m? Margin: ________ dB.
3. Same link through one wall (add −12 dB): ________ dBm. Verdict?
4. Your client's sensitivity is −82 dBm. State the margin at the −67 dBm
   design target: ________ dB.
5. A hall needs 25 concurrent clients per AP with usable per-client rate;
   airtime, not signal, is the constraint. Coverage-first or capacity-first?
6. In one sentence: why do walls, not open-space distance, dominate
   in-building design? Use your drill numbers in the answer.

## Part B — GA-30: Meridian Building B wireless design (25 min)
Design the wireless plan for the floor plan provided: ~35 staff devices,
up to 60 guest devices at events, one SSID per group.

Fill the design grid; every row needs a *because*.

| Row | Design decision | Your choice | Because (evidence/rule) |
|---|---|---|---|
| 5 | AP count + placement rationale | | |
| 6 | 5 GHz channel plan (and 2.4 GHz fallback) | | |
| 7 | SSIDs + VLANs (staff/guest) | | |
| 8 | Authentication per SSID (802.1X vs PSK; guest isolation) | | |
| 9 | Capacity estimate for the event hall | | |
| 10 | One failure mode of your own plan + early detection (L29) | | |

## Part C — Findings (5 min)
Two pairs defend rows 5–6 aloud; the class critiques with the rubric
(coverage reasoning · channel legality · auth/isolation · capacity).

## Exit ticket (3 items)
1. Roaming within one enterprise SSID keeps your ________ unchanged.
2. The three non-overlapping 2.4 GHz channels: ________, ________, ________.
3. "Coverage ≠ capacity" in one sentence, using airtime in your answer: ________
