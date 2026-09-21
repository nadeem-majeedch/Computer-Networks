# Lecture 10 — Instructor Teaching Notes
## Wireless Networking: Wi-Fi Fundamentals (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary; CLO6 supporting |
| Textbook anchor | PD §2.7–2.8 |

---

## 1. Objectives hook
Board: **"Your phone says 'connected, 866 Mbps'. A 100 MB file takes 40 seconds. Where did
the gigabits go?"** (100 MB = 800 Mb; 800/866 ≈ 0.9 s *if* PHY rate == throughput; the
gap is the lecture.)

Hook (2 min): walk to the window with the classroom's laptop, show Wi-Fi analyzer-style
RSSI dropping as you move — "the medium is now distance."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | VLAN pairing rule recall; RSSI walk |
| 6–24 | Concept 1 | 802.11 architecture: STA/AP/BSS/ESS/DS; association steps |
| 24–44 | Concept 2 | CSMA/CA: why not CD; IFS; ACKs; hidden node; collisions persist |
| 44–55 | Concept 3 | Channels & bands; PHY rates vs throughput math |
| 55–60 | Break | — |
| 60–72 | LAB-03 briefing | Survey method + ethics (passive only) |
| 72–105 | LAB-03 (in-class) | Survey nearby networks; analyze one association trace |
| 105–115 | Findings + summary | Groups report one observation each |
| 115–120 | Preview | LAN security preview next (L11) |

## 3. Concept walkthrough

### 3.1 802.11 architecture (18 min)
- Roles: **STA** (client), **AP** (access point), **BSS** (one AP + its STAs, one
  "cell"), **ESS** (multiple APs, one SSID — roaming), **DS** (distribution system —
  the wired backbone connecting APs). Ad-hoc/IBSS mentioned as legacy.
- **Association steps (simplified teaching model):** scan (active probe / passive
  beacon listen) → authenticate (open/WPA enterprise handshake — L11) → associate
  (join BSS, get association ID) → DHCP (L14). Beacons: APs announce presence ~every
  102.4 µs × 100 (≈ every 100 ms typical) with SSID, capabilities, timings.
- BSSID = the AP's radio MAC; SSID = the *name*; one AP with 2 radios = 2 BSSIDs, one
  SSID — disambiguate these three terms; students conflate them.
- Frames: management/control/data families; "everything is broadcast medium" — no
  wires, so every frame is heard by everyone in radio range (privacy implications:
  L11; capture ethics: prerequisites gate).

### 3.2 CSMA/CA (20 min, the conceptual core)
- Why not CD: a radio **cannot transmit and listen** simultaneously on the same channel
  (self-interference swamps the receiver) → collision *detection* impossible → must
  **avoid** and then *repair* with ACKs.
- Mechanism (simplified model): sense channel idle → wait **DIFS** → random backoff
  window (like Ethernet's backoff but *before* sending) → transmit → **immediate ACK**
  from receiver on success. No ACK ⇒ sender assumes collision/loss ⇒ retransmit (link-
  layer retransmissions! L06's ARQ in the wild).
- **Hidden node:** A and B both in range of AP but not each other; both sense idle,
  both send, collision *at the AP only*. Mitigation: **RTS/CTS** (short reserve frames)
  — optional, overhead-priced. Draw it; it's the classic exam diagram.
- **Exposed node** (enr, one line): the mirror case where CSMA/CA is *over*cautious.
- Collisions still happen (the A stands for avoidance, not abolition) — PHY partially
  detects via energy, and the ACK timeout catches the rest.
- Airtime is the scarce resource: *one* slow device (say 20 Mbps-capable at the edge)
  consumes as much airtime sending its bits as a fast one — the "slow client taxes
  everyone" phenomenon; LAB-03 observes it.

### 3.3 Channels, bands, PHY vs throughput (17 min)
- Bands: 2.4 GHz (3 non-overlapping 20 MHz channels: 1/6/11), 5 GHz (many channels,
  DFS radar-sharing), 6 GHz (Wi-Fi 6E; clean but range-limited). Higher band = more
  spectrum, more attenuation through walls.
- **PHY rate ≠ throughput.** Take a 866 Mbps PHY rate: it's a *shared, half-duplex*,
  best-case modulation number. Real single-client TCP throughput typically lands at
  40–60% of PHY rate: management/beacon overhead, ACK frames, backoff idle time,
  preamble/PHY overhead per frame, retransmissions, aggregation shortfalls.
- Worked math (board): PHY 866 → effective ~400 Mbps half-duplex air ceiling → one
  client's share with 6 active clients ≈ 67 Mbps → TCP goodput after overheads ≈
  45–55 Mbps. Now the opening question answers itself.
- Security preview (1 line): open networks vs WPA2/WPA3 — L11.

### Reference diagram — Hidden terminal problem

```text
            ┌──────┐
            │  AP  │        A and B each hear the AP,
            └──┬───┘        but not each other:
         ┌─────┴─────┐      both sense idle, both send
       ┌─┴─┐       ┌─┴─┐    → collision happens AT the AP
       │ A │       │ B │
```

## 4. Important definitions
STA · AP · BSS/ESS/BSSID/SSID · DS · Beacon · Scanning (active/passive) ·
Authentication vs association · CSMA/CA · DIFS · Backoff · ACK · Hidden node ·
RTS/CTS · Channel · Non-overlapping channels · DFS · PHY rate vs throughput · Airtime.

## 5. Real-world examples
- **Stadium/lecture-hall Wi-Fi:** hundreds of clients per AP → airtime, not capacity, is
  the limiter; "more APs on the same channel" makes it *worse* (co-channel contention).
- **2.4 GHz at home:** neighbors on channel 6 — the classic; spectrum is unlicensed and
  shared with microwaves/Bluetooth.
- **Slow-printer effect:** one ancient 802.11b-era device on a modern network drags the
  cell (slow-client tax).

## 6. Mathematical/technical example
Airtime arithmetic (simplified): 1500 B frame at PHY 866 Mbps vs at 54 Mbps —
transmission time ≈ 13.9 µs vs 222 µs (plus ~50–100 µs protocol overhead each). The
slow frame occupies ~16× the airtime: compute with the class, then connect to the
"tax" phenomenon and to L01's transmission-delay concept — same L/R, real radio.

## 7. LAB-03 briefing (12 min)
Method (passive-only, ethics gate restated): use a scanning app (or `nmcli dev wifi
list` / Wireshark beacon capture in monitor mode where permitted) to map: SSIDs, bands,
channels, RSSI of 6+ networks; identify overlapping channels in 2.4 GHz; measure RTT to
the AP at 3 distances (ping the gateway); record in the handout table. Analysis task:
one provided association trace — identify beacon/probe/auth/assoc/DHCP steps.
⚠ Verify the room's Wi-Fi has ≥3 visible networks; have a recorded beacon capture as
backup; monitor-mode capability is NOT required for the graded task.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Wi-Fi is wireless Ethernet" | Different MAC (CSMA/CA, ACKs), half duplex, shared airtime |
| "Connected at 866 Mbps = 866 Mbps speed" | PHY rate ≠ goodput; overheads + sharing (worked math) |
| "More APs = more capacity, always" | Co-channel contention; planning beats quantity |
| "Collisions are eliminated by CSMA/CA" | Avoided/repaired; ACK timeouts catch what sensing misses |
| "5 GHz always beats 2.4 GHz" | Range/wall loss; 2.4 GHz penetrates better |
| "The AP is a switch" | It bridges Wi-Fi↔wired; airtime management adds a whole layer |

## 9. Suggested practical demonstration
The RSSI walk (opening) plus live scan: `nmcli dev wifi list` projected, then a Wireshark
beacon capture (3 minutes) — identify SSID/channel/RSSI fields in one beacon. ⚠ Verify
wireless adapter capture permissions on the podium machine; use recorded backup if not.

## 10. Classroom activities
- **Hidden-node diagram puzzle:** draw A-B-AP with ranges; ask who collides with whom;
  then add RTS/CTS and ask what changes.
- **Airtime auction:** 8 "clients" get PHY rates on cards; a 1-second "air clock" is
  divided — each student claims their transmission time; the class watches the fast
  clients starve. Loud, quick, memorable.

## 11. Problem-solving questions
1. Why can't 802.11 use CSMA/CD? (physics: can't listen while transmitting)
2. PHY 1200 Mbps, 4 active clients, one at 60 Mbps: estimate the slow client's effect on
   the others (qualitative + one number using airtime logic).
3. Two APs, same channel, same room: what happens to throughput and latency?
4. Why do beacons exist and what happens if they're missed? (Timings/power save;
   eventual loss of sync — re-scan.)
5. A user reports "great signal, terrible speed" at a café: give three distinct causes.

## 12. Formative assessment (with answers)
- MCQ: 802.11 uses CSMA/CA because → **radios can't detect collisions while
  transmitting**.
- MCQ: One BSS is identified by its → **BSSID**.
- MCQ: The frame sent by the receiver after a successful data frame is → **ACK**.
- Short: why is one slow client everyone's problem? → airtime is shared; slow frames
  occupy the channel proportionally longer.

## 13. Exit ticket
1. CSMA/CA replaces detection with ________ + ________.
2. Hidden node = ________.
3. PHY 866 Mbps is (per-client guaranteed / shared best-case): ________

## 14. Anticipated difficulties
- Students conflate authentication (L11's topic) with association; keep the separation
  explicit but brief today.
- RSSI dBm numbers seem backwards (−50 > −80): emphasize "closer to zero is stronger";
  tie to L05's dB recipe.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify ≥3 visible networks in the room; recorded beacon capture as backup
- [ ] Test `nmcli dev wifi list` on podium; print LAB-03 handouts
- [ ] Prepare airtime-auction rate cards; hidden-node diagrams
- [ ] Restate ethics gate (passive capture only) at briefing

## 16. Timing fallbacks
Trim §3.3 bands to 5 minutes (readings cover); the CSMA/CA section and LAB-03 survey are
protected.

## 17. References
- PD §2.7–2.8 (⚠ verify); IEEE 802.11 standard family (cite only).
- Wi-Fi Alliance publications for band/feature naming (6/6E/7).
- LAB-03 handout for the survey method.
- ⚠ VERIFY editions/sections; verify wireless demo permissions.
