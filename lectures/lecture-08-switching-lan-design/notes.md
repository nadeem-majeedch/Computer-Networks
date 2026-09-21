# Lecture 08 — Instructor Teaching Notes
## Switching & LAN Design (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary; CLO6 design reasoning |
| Textbook anchor | PD §3.1–3.2 |

---

## 1. Objectives hook
Board: **"A switch has no configuration. Nobody tells it where anyone is. Yet it never
asks. How?"**

Hook (2 min): hold up a (virtual) letter with only a name, no address — "how does the mail
room deliver this? They *remember* which box that person collected from last time."
Self-learning is the magic; today we make it precise.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L07 hub/switch recall; letter analogy |
| 6–30 | Concept 1 | Switch algorithm: learn, forward, filter, flood — with a worked scenario |
| 30–48 | Concept 2 | LAN design: hierarchy, uplinks, domains; broadcast storms & loops |
| 48–55 | Concept 3 | STP purpose (concept only) |
| 55–60 | Break | — |
| 60–82 | GA-08 | FDB prediction worksheet, pairs → board reveal |
| 82–98 | Worked example | Broadcast storm walk-through; loop diagram |
| 98–110 | Design discussion | Campus LAN case: where do switches sit and why |
| 110–118 | Summary + exit ticket | — |
| 118–120 | Preview | VLANs fix the one-big-broadcast-domain problem (L09) |

## 3. Concept walkthrough

### 3.1 The switch algorithm (24 min, the lecture's core)
Per frame, a switch does exactly this (teach as state machine):
1. **Receive** the full frame (store-and-forward; some switches cut-through — enr note).
2. **Learn:** record (source MAC → ingress port, timestamp) in the **forwarding database
   (FDB / MAC table / CAM table)**. Learning is *always on*, from *every* frame's source.
3. **Look up** destination MAC in the FDB:
   - **Hit** → **forward** out that port only (**filtering** if that port == ingress port:
     don't send it back).
   - **Miss** → **flood** out all ports except ingress (unknown unicast).
4. Special cases: broadcast/multicast → always flood (within the broadcast domain);
   FDB entries age out (typically 300 s default) — relearned on next frame.

Worked scenario (board, 4 hosts/2 switches — draw it):

```
HostA [p1] ──── SW1 [p1..p4] ══ trunk-link ══ SW2 [p1..p2] ──── HostC [p1]
```
Frame sequence and FDB states (table on board, one row per event):

| Event | SW1 FDB after | SW2 FDB after | Out where? |
|---|---|---|---|
| A→C (A unknown to SW1) | A→p1 | (nothing: floods, learns nothing — C's frame not yet seen) | flooded to link+others |
| C→A (reply) | A→p1, C→p2(link) | C→p1 | SW2 floods to link; SW1 forwards to p1 |
| A→C (again) | (same) | (same) | SW1 has C on link → forwards only there |

The punchline: **learning is free and automatic; flooding is the price of ignorance**;
unknown-unicast flooding is also a security topic (L11's MAC-flooding attack *abuses*
this exact mechanism).

### 3.2 LAN design & domains (18 min)
- **Hierarchy:** access switches (hosts) → distribution/uplink → core. Reasons: cable
  economics, failure isolation, predictable paths.
- **Domains, counted:** each switch port = 1 collision domain (full duplex now makes this
  moot but the vocabulary stays); **one broadcast domain per VLAN/LAN** — all flooded
  frames go everywhere. Broadcast % of traffic grows with hosts (ARP, DHCP — L12/L14
  make this concrete), which is the scaling problem VLANs solve.
- **Loops:** two links between switches (redundancy = good) + flooding = a frame copies
  itself forever: **broadcast storm**. Also FDB thrashing (same MAC seen on two ports).
  Draw the 2-switch-2-link storm; count copies doubling per traversal.
- **STP purpose (concept, 7 min):** spanning tree protocol logically *blocks* redundant
  links, keeping a loop-free active topology while preserving physical redundancy as
  standby; re-converges on failure. Mechanics (bridge IDs, root election, timers) =
  enrichment; purpose is core. Modern relevance: it's why "plug both cables in" usually
  works instead of melting the network.

### 3.3 What good LAN design looks like (design discussion seed, 12 min)
- Predictable traffic paths; sized uplinks (aggregate ratio); no accidental loops
  (STP handles it, but don't rely on it); management access plan; documentation.
- Meridian Systems teaser (CS-02): two buildings, one flat LAN — ask class to name three
  problems (broadcast scale, security zones, fault blast radius). Their answers ARE the
  motivation slide for L09.

## 4. Important definitions
Forwarding/learning/filtering/flooding · FDB (MAC/CAM table) · Aging time · Unknown
unicast · Broadcast storm · Spanning tree (purpose) · Access/distribution/core ·
Uplink · Collision domain · Broadcast domain · Store-and-forward vs cut-through (enr).

## 5. Real-world examples
- **"It's always the second cable":** a user plugs a second cable into the same switch
  for "speed" → loop → storm → whole-floor outage. STP usually saves you; "usually"
  matters. This is the most common real L2 incident.
- **FDB age-out confusion:** device moves desks; traffic to it floods for seconds until
  it speaks or ARP refreshes — explains "new desk, weird slowness for a minute".
- **Mac OS/phone roaming between APs** reappears in FDBs of multiple switches — fine, but
  explains flapping entries on busy wireless networks.

## 6. Mathematical/technical example
Storm growth (simplified model): 2 switches, 2 parallel links, one broadcast frame —
each switch duplicates every received broadcast onto both links; population roughly
doubles each traversal: 1→2→4→8…; gigabit links fill in well under a second, CPU follows.
Contrast: with STP blocking one link, the same broadcast is delivered once per link on
the tree. Numbers make "why loops are forbidden at L2" visceral.

## 7. GA-08: FDB prediction (22 min)
Worksheet: 3 scenarios on a fixed 2-switch topology; students fill FDB tables after each
frame and mark forward/flood/filter decisions, then answer two design questions (where
would you add a second uplink; what breaks if a host MAC is spoofed — teaser L11).
Debrief: one scenario on the board, pairs self-mark.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "A switch is a smart hub" (L07 relapse, deeper now) | Per-port forwarding with FDB vs electrical repetition; demonstrate with flood-vs-forward table |
| "Switches need configuration to know MACs" | Learning is automatic and source-driven |
| "Redundant links are always good" | Loops at L2 without STP = storms; redundancy needs protocol management |
| "Flooding is an error condition" | It's the correct behavior for unknown/broadcast; *persistent* flooding is the smell |
| "STP creates the loop-free paths by removing redundancy" | Physical links stay; logical blocking; failover uses the standby |
| "Full duplex made broadcast domains irrelevant" | Collision domains died; broadcast domains absolutely did not (ARP/DHCP storms still floor buildings) |

## 9. Suggested practical demonstration
Linux bridge on the VM as a visible switch:
```bash
sudo ip link add br0 type bridge
sudo ip link set br0 up
# attach two veth pairs as "hosts" and show learning:
ip link show br0
bridge fdb show
```
Generate traffic between the two veth endpoints, re-run `bridge fdb show`, and watch
entries appear — the FDB is now *visible*. ⚠ Pre-script this; veth setup is fiddly live.
Backup: static diagram + FDB table reveal.

## 10. Classroom activities
- **Human switch:** 6 students = 6 ports; instructor whispers "frame from MAC-A on port
  2 to MAC-C"; they pass a paper card according to a drawn FDB on the whiteboard; errors
  are instructive and loud.
- **Domain counting sprint:** 4 increasingly nasty topologies projected; teams count
  collision and broadcast domains in 60 s each.

## 11. Problem-solving questions
1. After the worked scenario (§3.1), what does SW1 do with a frame to MAC-D (never seen)?
2. Why does aging time exist? What breaks with no aging? (Stale entries after moves.)
3. Two switches, one link: which frames cross the link? (Only those whose FDB lookup
   points across it — i.e., unknowns + cross-traffic.)
4. Your redundant uplink was "blocked by STP" — does it carry traffic? When?
5. Broadcast traffic share is 4% and rising with 500 hosts. Two options: bigger pipes or
   VLANs. Argue both, then pick (preview L09).

## 12. Formative assessment (with answers)
- MCQ: A switch learns by reading the frame's → **source MAC**.
- MCQ: Unknown unicast is → **flooded** to all ports except ingress.
- MCQ: STP's job is to → **block redundant links logically to prevent loops**.
- Short: why is one big broadcast domain a scaling problem? → flooded broadcast/multicast
  and unknown-unicast load grows with hosts; blast radius of storms.

## 13. Exit ticket
1. The four switch actions in order: ________
2. Learning uses the ________ MAC; lookup uses the ________ MAC.
3. Loops at L2 are dangerous because of ________.

## 14. Anticipated difficulties
- Students want STP mechanics immediately; park it (enr) with one sentence of promise.
- FDB tables on paper go wrong when a host *replies* (students forget C→A teaches SW1 the
  link port). The human-switch activity is the fix.

## 15. Instructor preparation checklist
- [ ] ⚠ Pre-script and test the Linux-bridge FDB demo; keep static backup
- [ ] Print GA-08 worksheets (3 scenarios); prepare the reveal deck
- [ ] Board pre-write: 2-switch topology used by all scenarios; FDB blank tables
- [ ] Prepare domain-count topologies for the sprint

## 16. Timing fallbacks
Drop the design discussion (§3.3) to 5 minutes; protect §3.1 and GA-08 entirely.

## 17. References
- PD §3.1–3.2 (switching basics; LAN design).
- IEEE 802.1D (STP) — cited for purpose; mechanics out of scope.
- Linux bridge documentation (bridge/fdb) for the demo.
- ⚠ VERIFY edition/sections; verify `bridge fdb show` on the VM image.
