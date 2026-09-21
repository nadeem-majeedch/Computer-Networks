# Lecture 25 — Instructor Teaching Notes
## Perimeter & Internal Defenses: Firewalls, Segmentation & VPNs (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO7 primary; CLO3/CLO6 supporting |
| Textbook anchor | KR §8.4–8.9 (selected); PD §8.3 |

---

## 1. Objectives hook
Board: **"Your firewall sees addresses, ports, flags, and sizes. It does NOT see
requests, users, intentions, or encrypted payloads. Design your defense knowing
exactly that."**

Hook (2 min): show two rulesets — a 40-rule pile vs a 6-line default-drop policy —
"which one survives an auditor? Which one survives a 3 a.m. incident?"

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | TLS recap (1 item); the two-rulesets contrast |
| 6–26 | Concept 1 | Firewall classes; statefulness; what's inspectable |
| 26–44 | Concept 2 | Policy design: zones, default-drop, rule ordering; Meridian zones |
| 44–55 | Concept 3 | IDS/IPS placement; VPN tunneling (site-to-site vs remote access) |
| 55–60 | Break | — |
| 60–72 | LAB-13 briefing | Topology + policy tasks |
| 72–105 | LAB-13 (in-class) | Pairs: nftables policy + verify; tunnel up |
| 105–115 | Findings | One pair demos the blocked/allowed matrix |
| 115–120 | Summary + exit ticket | CS-03 reminder |

## 3. Concept walkthrough

### 3.1 Firewall classes & visibility (20 min)
- **Packet filter (stateless):** per-packet 5-tuple decisions; cheap; can't see
  "reply to MY request" without explicit rules — the FTP-era pain that motivated
  state.
- **Stateful:** the firewall builds a **connection table** (L18's state concept,
  relocated): replies to outbound flows auto-allowed. This is also the honest
  answer to "isn't NAT a firewall?" (L14): NAT happens to track flows, but
  *policy* is the firewall's job — different mechanisms, sometimes co-located.
- **Application-layer (proxy/NGFW concept):** understands protocol semantics
  (URLs, methods) — heavier, placement-sensitive; encrypted traffic limits it
  (L24's boundary again: TLS hides payload — TLS inspection exists and is a
  governance minefield: name it, note the trade-off, move on).
- **What's inspectable vs not (the hook's payoff):** headers/flags/sizes/rates yes;
  intentions/identity(usually)/encrypted payload no. Defense design *starts*
  from this list.

### 3.2 Policy design (18 min)
- **Zones (Meridian):** inside-staff / inside-guest / DMZ (public services) /
  outside; VLANs (L09) *are* the internal zone borders — segmentation + policy
  = the system.
- **Default-drop discipline:** `policy drop` + explicit allows; rule order
  matters (first-match semantics in nftables); logging the drop chain (you can't
  troubleshoot what you don't record — L29 preview).
- **Worked micro-policy (board, becomes LAB-13's skeleton):**
  ```
  allow established/related          # statefulness
  allow tcp dport 443 to DMZ-web     # the service
  allow icmp echo (rate-limited)     # diagnostics without discovery-fests
  allow staff→internals per matrix   # segmentation policy
  drop + log                         # the default
  ```
  Each line gets a *justification sentence* in the lab report — the CLO6/Evaluate
  muscle.
- **Egress filtering (BCP 38 spirit):** filtering *outbound* spoofs/steps —
  named as the good-citizen rule; connects to L12's spoofing thread.

### 3.3 IDS/IPS & VPNs (17 min)
- **IDS/IPS:** signature vs anomaly detection; placement (mirror/span port for
  IDS; inline for IPS); encrypted-traffic reality (metadata detection, TLS
  termination points); false-positive economics (why alert tuning is a job).
- **VPNs:** **tunneling = IP-in-IP + crypto**: site-to-site (router-to-router,
  LANs merge) vs remote-access (host joins the network conceptually);
  IPsec/IKE named for site-to-site (L14's NAT-vs-IPsec friction revisited),
  WireGuard/OpenVPN as modern choices (named, one line each).
- **What a VPN changes / doesn't:** path privacy & membership yes; endpoint
  hygiene, *post-connect* lateral movement no — the honest boundary again
  ("VPN ≠ safety", the register's line).

### Reference diagram — Stateful firewall decision path

```text
pkt in (ext→int) ──→ state table: established?
        │                       │yes → forward
        │ no                    ▼
        ▼                 rule match? ──yes→ forward (+ state entry)
        no → drop (+ log)
```

## 4. Important definitions
Packet filter · Stateful inspection · Connection table · Zones/DMZ ·
Default-drop (whitelist) · Rule ordering/first match · Egress filtering (BCP 38,
named) · IDS vs IPS · Signature vs anomaly · Span port · VPN tunneling ·
Site-to-site vs remote access · IPsec/IKE (named) · WireGuard (named) ·
Encapsulation overhead.

## 5. Real-world examples
- **The DMZ web server breach that *didn't* become a domain breach** — because the
  staff→DMZ direction had no allow rules: segmentation earning its keep.
- **"The VPN is slow"** = MTU/overhead mismatch (tunnel adds headers → fragments →
  PMTUD pain, L15's ICMP-blocking footgun at work): the fix is MSS clamping —
  named, and demonstrated in LAB-13.
- **Firewall change freezes at midnight** — because the drop chain had no log;
  the next morning's debugging was archaeology.

## 6. Mathematical/technical example
Tunnel overhead: IPv4+ESP+outer-IP ≈ 60–80 B per packet (mode-dependent); on
1500-MTU path the inner payload shrinks to ~1420 → why the lab sets MSS clamp
1360 (safe) and why throughput dips ~5% — quantified honesty about "free security".
State-table arithmetic: 10,000 active flows × ~300 B state = 3 MB — why a small
router state-tracks fine and why SYN floods (L18/L26) attack exactly this memory.

## 7. LAB-13 briefing (12 min)
Topology: 3 VMs — "outside" client, "firewall" router (2 NICs), "DMZ" server; plus
an internal net. Tasks: (1) default-drop nftables policy on the firewall with
justified allows (443→DMZ; staff→internal matrix; rate-limited ICMP); (2) verify
with the allowed/blocked matrix (curl + ping tests); (3) bring up a site-to-site
tunnel between two nets (WireGuard per handout; IPsec alternative documented);
(4) measure MTU/MSS effect (ping -s sweep + MSS clamp) — connect to §6's math.
⚠ Verify WireGuard (or IPsec) modules + nftables on the image; handout carries the
exact key-generation steps; the *policy justification text* is the graded thinking.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "NAT is my firewall" (register line) | Flow-tracking side effect vs policy engine; firewalls state-track *for policy* |
| "Default-allow with block rules is fine" | Negative-listing inverts the burden; one forgotten service is the breach |
| "The firewall stops insiders" | Internal zones need internal policy; perimeter-only thinking fails (CS-04 brief) |
| "VPN = anonymous" | Membership + path privacy; identity and endpoints still known |
| "IDS sees everything" | Encrypted payload limits signatures; placement decides |
| "More rules = more secure" | Rule surface = audit surface; minimal policies win |

## 9. Suggested practical demonstration
5 minutes: pre-built LAB-13 firewall, run the allowed/blocked matrix live (curl to
443 allowed; port 80 blocked *with the logged drop shown* via `journalctl`) —
policy + logging as one demo. ⚠ Pre-verify; keep config as backup slide.

## 10. Classroom activities
- **Policy drafting sprint:** Meridian's staff→guest scenarios on cards; teams
  write 6-line policies; two are traded between teams for critique (the
  justification sentence is the rubric).
- **Zone sorting:** 8 services (guest printer, staff file share, public web,
  database...) → zone + direction of allowed initiation; defends CS-04's design
  work.

## 11. Problem-solving questions
1. Why does statefulness fix the FTP-reply problem stateless filters can't?
2. Your DMZ web server is compromised. Which rules decide whether it becomes a
   beachhead? (egress/direction policy)
3. MSS clamp math: why 1360 for the tunnel in §6?
4. IDS on a span port sees TLS: what *can* it still detect? (metadata, SNI,
   sizes, rates — L24's boundary)
5. Two identical policies, one logs drops. Which is more secure? (neither — but
   one is *operable*; security = operations)

## 12. Formative assessment (with answers)
- MCQ: Stateful firewalls track → **connection state to auto-allow replies**.
- MCQ: Default-drop means → **deny unless explicitly allowed**.
- MCQ: A site-to-site VPN connects → **two networks**.
- Short: why log the drop chain? → troubleshooting + incident evidence;
  unlogged drops are invisible failures (L29).

## 13. Exit ticket
1. Firewall sees: ________ ; never: ________
2. The first rule in a policy is usually: ________
3. VPN provides ________ and ________, not ________.

## 14. Anticipated difficulties
- nftables syntax friction in LAB-13: the handout's skeleton + the briefing's
  live edit keep pairs moving; justification text, not syntax, is graded.
- Students conflate VPN *product* vs *architecture* — keep site-to-site vs
  remote-access crisp; LAB-13 does the former.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify nftables + WireGuard/IPsec on image; pre-run the full lab once
- [ ] Print handouts + policy-sprint cards; prepare the logging demo
- [ ] Board pre-write: inspectable/not table; micro-policy; tunnel overhead math
- [ ] CS-03 due-date reminder prepared (next session)

## 16. Timing fallbacks
Compress IDS/IPS to placement + signature/anomaly (5 min); the policy design and
LAB-13 start are protected; tunnel MTU measurement can move to the report.

## 17. References
- KR §8.4–8.9 (selected); PD §8.3; RFC 6092 (ipv6 firewall advice, concept);
  BCP 38 (egress/ingress filtering, named); WireGuard whitepaper (named).
- nftables wiki; LAB-13 handout.
- ⚠ VERIFY editions/sections and image tooling this semester.
