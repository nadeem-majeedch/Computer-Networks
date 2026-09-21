# LAB-03 — Instructor Guide

## Setup / logistics (before session)
- ⚠ Verify the room's RF policy (lab-strategy §7). Prepare the course test SSID on a local
  AP you control; print the permission statement students must cite in their reports.
- Capture `lab03-survey.pcapng` and `lab03-association.pcapng` yourself from the test SSID
  the week before (also the accessibility route's source).
- Student adapter variability is the #1 issue: publish a known-good USB adapter model for
  students whose laptops cannot do monitor mode.

## Solutions / expected values
- **Pre-lab 1:** beacon (~10/s, e.g. 102.4 ms default); advertises SSID, channel, supported
  rates/capabilities.
- **Pre-lab 2:** VM NICs present wireless as wired Ethernet; management frames never reach
  the guest — this lab is host-side.
- **Pre-lab 3:** 1, 6, 11.
- **T1:** occupancy table shows 1/6/11 clustering; 5 GHz weaker at distance. "Three
  co-channel APs" is normally easy in a building — the contention insight is the point.
- **T2:** delta ≈ 102.4 ms; SSID plaintext; RSSI trend with movement.
- **T3:** Open: auth → assoc → data. WPA2: auth → assoc → EAPOL M1–M4 → encrypted data.
  Encryption begins after M4 (keys installed); from there the observer sees MACs + frame
  sizes only.
- **T4:** cabled capture: MAC/IP/ports/payload. Monitor capture of WPA2: radiotap + MACs +
  sizes, no IP/ports/payload. The paragraph must separate "data confidentiality" from
  "management visibility" (map to L11's WPA2-PSK 4-way diagram and LAB-15's ethics).
- **Post-lab 4:** hiding the SSID just removes it from beacons; probes/associations still
  reveal it, and nothing about the encryption changes — mechanism, not policy.

## Common failure modes
1. Students capturing on their home network *without* permission language in the report —
   require the citation line ("I own/operate this network" or instructor test SSID).
2. Windows Npcap installed without monitor-mode support — the offline route is the fix,
   not an excuse to skip.
3. EAPOL frames missed because capture started post-association (see README T3 note).
4. Students quoting RSSI as "good/bad" — require dBm numbers (rubric: units).

## Grading notes
- This lab's deliverable is *written findings* (no pair work). Evidence = the two capture
  files or the offline bundle + command log.
- The permission statement is mandatory; a technically perfect report without it scores 0
  on reproducibility (20 pts) until resubmitted.
