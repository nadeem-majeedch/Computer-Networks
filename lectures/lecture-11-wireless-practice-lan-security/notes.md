# Lecture 11 — Instructor Teaching Notes
## Wireless in Practice + LAN Security Preview (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary; CLO6/CLO7 supporting |
| Textbook anchor | KR §6.3 (skim); instructor notes |

---

## 1. Objectives hook
Board: **"Two tickets arrived this morning: (1) 'Wi-Fi is slow in room 204 every day at
11:00.' (2) 'New laptop on the printer VLAN can reach payroll.' Same morning. Different
layers. Go."**

Hook (2 min): show both tickets as printed slips; today's class is exactly the toolkit
that turns each into a diagnosis. Ticket 2 is also the CS-02 seed and the semester's
security thread opener.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L10 airtime recall; the two tickets |
| 6–30 | Concept 1 | Wireless troubleshooting method (interference/RSSI/airtime/roaming) |
| 30–50 | Concept 2 | LAN attack surface: MAC flooding, ARP problems, rogue DHCP; defenses concept |
| 50–55 | Break | — |
| 55–75 | Activity | Ticket triage: pairs convert the two tickets into measurement plans |
| 75–100 | CS-02 kickoff + LAB-03 wrap | Brief walk-through; sketch work; write-up guidance |
| 100–115 | Worked example | 802.1X concept walk (supplicant/authenticator/AS) |
| 115–120 | Summary + exit ticket + preview | IP/ARP next |

## 3. Concept walkthrough

### 3.1 Wireless troubleshooting method (24 min)
A repeatable ladder (mirrors L29's general method but wireless-specific):
1. **Locate** — one user? one room? one AP? (blast-radius reasoning from L08).
2. **Measure** — RSSI/SNR at the complaint spot; channel occupancy (analyzer); retransmit
   %; airtime utilization. Numbers, not vibes: −55 dBm good / −75 dBm poor; SNR < 20 dB
   hurts.
3. **Classify** the dominant cause:
   - **Coverage:** weak RSSI at the spot → AP placement/power.
   - **Interference/co-channel:** overlapping channels or non-Wi-Fi sources (microwave
     ovens ≈ 2.45 GHz!) → channel plan (1/6/11), band shift to 5 GHz.
   - **Capacity/airtime:** strong signal, slow speeds, many clients → slow-client tax
     (L10), too many clients per AP.
   - **Config:** wrong VLAN, roaming sticky-client issues, DFS pauses on 5 GHz.
4. **Fix one variable; re-measure** — the scientific habit that carries to L29.
- The 11:00 ticket resolves as: adjacent classroom's microwave + channel-6 overlap +
  40 clients on one AP — a composite diagnosis; each cause maps to one measurement from
  step 2 (this is the worked example in §7).

### 3.2 LAN attack surface (20 min — the security thread opens)
Frame every attack as *abuse of a mechanism you already know* (L07–L09):

| Attack | Mechanism abused | Symptom | Defense concept |
|---|---|---|---|
| MAC flooding | L08 unknown-unicast flooding | FDB fills → switch becomes "hub-like", traffic leaks | Port security: limit MACs/port, shut/drop on excess |
| ARP problems (spoofing/MITM preview) | L12's ARP (trusted, unauthenticated) | Traffic redirected through attacker; "intermittent logout" symptoms | Dynamic ARP inspection (name + idea only), L12 full treatment |
| Rogue DHCP | L14's DHCP (anyone can answer) | Wrong gateway/DNS handed out → MITM | DHCP snooping: trusted ports only (concept), L22 details |
| Rogue AP | Physical/ESS trust | "Free Wi-Fi" harvesting | 802.1X, WPA-Enterprise, RF monitoring |

- **Port security (concept):** per-port MAC allow-list/count limits; violation modes
  (protect/restrict/shutdown) named, mechanics deferred to lab courses.
- **802.1X (concept walk, §7):** who are you (supplicant credentials) → is the port
  open (authenticator = switch/AP relays) → says the RADIUS authentication server (AS).
  Three roles on the board; the punchline: *authentication before the port forwards*.
- **WPA2/WPA3 personal vs enterprise (enr, 2 min):** PSK = one shared secret (one user
  leaves → everyone rotates); enterprise = per-user 802.1X. Foreshadows L24's crypto.

### 3.3 Bridging to CS-02 (6 min)
The ticket-2 attack works because Meridian's flat LAN mixes trust zones. CS-02 asks:
segment it (VLANs), address it (next module's subnetting), defend it (ACLs later).
Hand out the brief; point at the deliverable table (due L16).

### Reference diagram — WPA2-PSK 4-way handshake (EAPOL)

```text
AP                                          client
   │──── M1: ANonce ────────────────────────────→│
   │←─── M2: SNonce + MIC ───────────────────────│  proves client holds PMK
   │──── M3: GTK + MIC, install keys ──────────→│
   │←─── M4: MIC ────────────────────────────────│  proves AP holds PMK
```

## 4. Important definitions
RSSI/SNR · Channel plan · Co-channel contention · Airtime utilization · MAC flooding ·
Port security · ARP spoofing (named; detailed L12) · Rogue DHCP · DHCP snooping (named;
L22) · Rogue AP · 802.1X roles (supplicant/authenticator/AS) · RADIUS (named) ·
PSK vs enterprise.

## 5. Real-world examples
- **Microwave vs Wi-Fi:** the 2.45 GHz oven band is the same as channel 6–10; a leaking
  door seal is a portable jammer — measured, not folkloric.
- **Hotel "oops":** a guest plugs their travel router into the room port → rogue DHCP for
  the whole floor; the fix (port security + DHCP snooping) is on every real switch.
- **MAC randomization:** phones rotate MACs per network; port-security allow-lists on
  student ports now fight privacy features — policies must catch up with devices.

## 6. Mathematical/technical example
Airtime/utilization threshold reasoning (simplified): a survey shows 65% channel
utilization, 22% retransmission, SNR 24 dB at the desk — classify: retransmissions with
good SNR ⇒ interference (not coverage); utilization 65% with 40 clients ⇒ capacity.
Each number kills one hypothesis — teach "numbers discriminate hypotheses" explicitly;
it's the intellectual core of troubleshooting.

## 7. Worked example: the 11:00 ticket (in §3.1; formalized here)
Measurement plan students build: (1) ping gateway every 10 s from 10:45–11:15 (RTT
spikes?); (2) channel analyzer screenshot at 11:00 (microwave burst pattern — periodic
gulps); (3) AP client count + utilization export. Diagnosis: composite (interference +
capacity). Remediation: move to 5 GHz, rechannel 2.4 GHz, or add AP. Answer: numbers
first, folklore never.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "MAC flooding is a switch bug" | It's correct behavior (L08 flooding) abused; defenses are policy features |
| "802.1X replaces the need for VLANs" | It *authenticates into* a VLAN; segmentation still needed |
| "Port security stops ARP spoofing" | Different mechanism (limits MAC count, doesn't validate ARP) |
| "Hiding SSID is security" | Beacons/probes still leak it; clients broadcast probes; theater |
| "Strong signal = good network" | Capacity/interference hurt at full bars (L10) |
| "Enterprise Wi-Fi needs only good passwords" | PSK shares one secret with everyone; enterprise binds identity per user |

## 9. Suggested practical demonstration
Two 5-minute captures, projected: (1) a beacon/probe dump showing a "hidden" SSID still
leaking via probe requests; (2) a (pre-built, course-VM) ARP table before/after an ARP
spoof *simulation diagram* — no live spoofing in class; the ethics gate is absolute.
⚠ The second demo is a **diagram + pre-captured evidence** only; state that aloud.

## 10. Classroom activities
- **Ticket triage (pairs):** for each of the two tickets, write the 3 measurements you'd
  take first and the hypothesis each discriminates. Compare across pairs — divergence
  itself is the lesson (there are defensible orders).
- **802.1X role-play:** three volunteers (supplicant/authenticator/AS) walk the flow
  with cards; the switch repeats "I'm just the bouncer" until it isn't (policy).

## 11. Problem-solving questions
1. Room 204: SNR 26 dB, utilization 70%, retrans 3% — coverage, interference, or
   capacity? Which number rules out which?
2. Why does MAC flooding *increase* visibility for the attacker? (FDB overflow →
   flooding → frames leave the port they shouldn't.)
3. A floor's devices get gateway 10.9.9.9 (not the real one). Which attack, which
   defense?
4. Why is SSID hiding not security? Cite the frame type that leaks it.
5. Sketch the 802.1X flow with the three roles and one sentence each.

## 12. Formative assessment (with answers)
- MCQ: Which defense limits MACs per switch port? → **port security**.
- MCQ: 802.1X's three roles → **supplicant / authenticator / authentication server**.
- Short: why is the ticket-2 scenario possible on a flat LAN? → no trust boundaries;
  any host ARPs/reaches any other — segmentation (CS-02) is the fix.

## 13. Exit ticket
1. The three Wi-Fi measurement numbers I'd collect first: ________
2. MAC flooding abuses the switch's ________ behavior.
3. 802.1X decides ________ before the port ________.

## 14. Anticipated difficulties
- Students want to *do* the attacks; hold the line: the ethics gate restricts all
  active techniques to the course VM lab (GA-26, L26) — say it explicitly and kindly.
- Ticket triage can sprawl; cap at 8 minutes with a strict 3-measurement limit.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify both ticket demos (beacon capture; pre-captured ARP evidence)
- [ ] Print CS-02 briefs and ticket slips; LAB-03 write-up template ready
- [ ] Prepare 802.1X role cards
- [ ] Re-read the ethics gate language from prerequisites.md to quote it exactly

## 16. Timing fallbacks
Drop the 802.1X role-play (keep the 2-minute diagram); CS-02 kickoff must keep ≥20 min
(teams need the brief context to start well).

## 17. References
- KR §6.3 (skim, ⚠ verify section); instructor notes (this document).
- IEEE 802.1X (port-based access control) — concept citation.
- Wi-Fi Alliance WPA2/WPA3 overview publications.
- Course ethics gate: [prerequisites.md](../../docs/prerequisites.md) §5.
- ⚠ VERIFY editions/sections this semester.
