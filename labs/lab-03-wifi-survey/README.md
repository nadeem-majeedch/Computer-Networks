# LAB-03 — Wi-Fi Survey & Association Analysis (passive, permission-only)

| Field | Value |
|---|---|
| Anchor lectures | L10 (Wi-Fi fundamentals), L11 (wireless in practice, security preview) |
| CLOs | CLO2 (physical/link), CLO7 (security awareness) |
| Assessment | Graded written findings (individual; 15% pool) |
| Mode / duration | Individual; 2-h session + 48-h window |
| Environment | **Host** Wireshark + your own Wi-Fi or the instructor-provided test SSID (VMs bridge Wi-Fi as Ethernet — this lab is deliberately host-side) |

## Learning outcomes
1. Conduct a passive RF survey: SSIDs, channels, signal strength (RSSI), band — and map
   channel occupancy in your room.
2. Explain beacon frames: what they carry (SSID, channel, capabilities) and why they exist.
3. Capture and interpret your own association/authentication exchange with the course test
   SSID (or your home router you own), naming the management frame sequence.
4. Recognize the security boundary: what a passive observer sees (everything in cleartext
   management; nothing from WPA2-encrypted data) and why.

## Safety & permission boundary (binding — syllabus-safety §3.3)
- Observe **only** networks you own or have written permission to observe; the instructor
  provides the course test SSID for association work.
- **No** deauthentication, injection, replay, or association attempts against any network
  that is not yours or the course test SSID. Every technique in this lab is passive.
- If the room/campus policy forbids scanning, use the offline bundle route (below) for the
  survey part.

## Pre-lab
1. L10: what frame type does an AP send ~10×/second, and what does it advertise?
2. Why can a VM not see Wi-Fi management frames? (How do VM NICs present wireless?)
3. 2.4 GHz non-overlapping channels: name them.

## Tasks

### T1 — Survey your environment (25 min)
On the host, start a monitor-mode capture with Wireshark (interface → enable Monitor Mode
in capture options ⚠ requires Npcap monitor-mode support on Windows / native support on
Linux) or use the text path:
```bash
sudo iw dev '<wifi-iface>' scan | egrep "SSID|freq|signal"   # one-shot survey (Linux host)
```
Build the room's channel-occupancy table (worksheet). **Expected observation:** most APs
cluster on 1/6/11; 5 GHz shows many more channels and typically weaker RSSI at distance.
Identify at least three co-channel APs — this is L10's contention problem made visible.

### T2 — Beacon anatomy (15 min)
From the monitor-mode capture, filter `wlan.fc.type_subtype == 8` (beacons). Pick the
course test SSID's beacon: record channel, RSSI trend, capabilities, and the timestamp
interval. **Expected observation:** beacons repeat at ~102.4 ms (verify with the capture's
delta times); SSID is plaintext in management frames.

### T3 — Your own association (25 min)
With permission (course test SSID or your own router), disconnect and reconnect while
capturing: filter `wlan.fc.type_subtype == 0x0c || wlan.fc.type_subtype == 0x0b || eapol`
(authentication/deauthentication/association family + EAPOL if WPA2).
**Expected observation:** authentication → association → (4-way EAPOL handshake, L11's
diagram) → data, all encrypted after the handshake. If your adapter/HW cannot produce a
clean sequence, use the provided `lab03-association.pcapng` and say so in the report —
do not fabricate.

### T4 — What the observer cannot see (15 min)
Compare two captures of the same transfer: your monitor-mode capture vs a course-provided
*cabled* capture of the same download. Note which fields are visible in each (MACs? IP?
ports? payload?). One paragraph: why WPA2 protects data but not management frames, and
what that means for a passive observer (links to LAB-15's ethics discussion).

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| No monitor-mode option in Wireshark | Npcap without monitor support (Windows) / managed-mode lock | use the offline bundle for survey; do association on the test SSID with a supported adapter |
| Beacons everywhere but your SSID missing | hidden SSID (beacon without SSID field) | that *is* a finding — record it; hidden ≠ secure (L11) |
| Capture full of data frames, no EAPOL | associated before capture started | disconnect first, then start capture, then reconnect |
| `iw dev` shows no wifi | VM (bridged as Ethernet) or missing driver | run on the host; VMs cannot do this lab |

## Post-lab questions
1. From your occupancy table: which two APs in your room contend most, and what would
   you change as the network's designer?
2. Beacons are plaintext. Name two fields an observer learns and one defense concept
   (L11) that reduces what management frames reveal.
3. Your association sequence: list the frame order you captured (or from the provided
   trace) and mark where encryption starts.
4. Why does "hidden SSID" not constitute security? (One sentence, mechanism-based.)

## Challenge (ungraded)
Compute the theoretical and observed beacon interval spread (deltas of 10 beacons),
and explain any drift you see (power save, chipset behavior ⚠ verify with your reference).

## Accessibility / low-resource alternatives
- Fully offline route: `lab03-survey.pcapng` + `lab03-association.pcapng` (instructor
  captures) + a channel-occupancy CSV. All questions answerable without RF access.
- tshark equivalents: `tshark -r lab03-association.pcapng -Y "eapol || wlan.fc.type_subtype==8" -T fields -e frame.number -e wlan.fc.type_subtype`.
- Color-independent: RSSI recorded as numbers (dBm), never interpreted by color alone.

## Safety notes
This lab is passive by design. The instructor's session reminder covers §3.3 explicitly.
