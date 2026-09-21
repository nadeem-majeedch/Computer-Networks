# Lecture 26 — Instructor Teaching Notes
## Attack & Defense Case Workshop (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO7 primary; CLO4/CLO6 supporting |
| Textbook anchor | Instructor notes; BCP 38; RFC 2131 (defense context) |

---

## 1. Objectives hook
Board: **"Four attacks. Four capture signatures. Four defense stacks. One question:
what risk remains — and is it acceptable?"**

Hook (2 min): the semester's security sightings as a timeline on one slide (L11→L26):
"We've been assembling this workshop all term."

## 2. Minute plan (workshop structure)

| Minutes | Segment | What happens |
|---|---|---|
| 0–5 | Ethics gate restated (verbatim) + hook | Non-negotiable opener |
| 5–35 | Walkthrough block | 4 attacks: mechanism → signature → defenses → residual risk |
| 35–40 | GA-26 setup | Emulation lab brief (VM-only) |
| 40–75 | **Workshop rotation** | Teams rotate: emulate/observe → analyze → defend → re-test |
| 75–90 | CS-03 work block | Bundle-2 evidence; diagnosis drafting (due today) |
| 90–100 | CS-04 capstone brief | Scenario + stages + team formation |
| 100–112 | Defense-plan clinic | Teams draft; instructor circulates with the residual-risk prompt |
| 112–118 | Summary + exit ticket | CS-03 submission reminder |
| 118–120 | Preview | Cloud/SDN module |

## 3. Concept walkthrough (the four walkthroughs, 30 min)

### 3.1 ARP spoofing (L12's flaw, weaponized)
- **Mechanism:** forged gratuitous/reply ARP → victim caches poisoned → traffic
  flows through attacker (MITM) or blackholed (DoS).
- **Capture signature:** duplicate ARP replies with conflicting MAC↔IP mappings;
  gratuitous ARPs from a MAC that isn't the gateway's OUI; downstream: duplicated
  TCP ACKs (both paths transmit).
- **Defenses (layered):** Dynamic ARP Inspection (snooping's binding table — L22's
  system), 802.1X admission (L11), static ARPs (tiny nets), crypto (TLS makes
  *content* safe even on-path — L24's honest boundary).
- **Residual risk:** ARP-free protocols? No — ND (v6) has SEND (named, rarely
  deployed); residual = on-path *metadata* exposure even with TLS.

### 3.2 DNS poisoning (L21's threat, structured)
- **Mechanism:** forge replies (TXID/port guessing → Kaminsky-style flooding of
  fake referrals to cache a bogus record).
- **Signature:** many UDP/53 queries with incrementing TXIDs to odd ports;
  suspicious additional-section NS records; resolved IP ≠ known ranges.
- **Defenses:** source-port+TXID randomization (L17/L21), DNSSEC (signed chain —
  concept), DoH/DoT (transport privacy), resolver hygiene (no open recursion).
- **Residual:** DNSSEC adoption gaps; DoH moves the problem to resolver choice.

### 3.3 DHCP starvation (L22's math, weaponized)
- **Mechanism:** flood DISCOVERs with spoofed chaddr → pool exhaustion → legit
  clients starve; rogue server variant (L22) feeds *wrong* options.
- **Signature:** thousands of DISCOVERs, distinct chaddr values from one MAC/port;
  Option 82 port mismatch.
- **Defenses:** snooping rate-limit per port + port security (L11) + pool sizing
  (L22's arithmetic as *defense design*) + lease shortening during events.
- **Residual:** physical-port compromise; RF access on Wi-Fi VLANs (L10/L11).

### 3.4 TCP SYN flood (L18's half-open, industrialized)
- **Mechanism:** SYNs with spoofed sources → half-open backlog exhaustion →
  legit SYNs dropped (DoS on the *connection table*, not bandwidth).
- **Signature:** SYNs without completes; retransmitted SYN-ACKs; asymmetric
  flags in the flow table.
- **Defenses:** SYN cookies (stateless handshake — named), backlog tuning,
  upstream filtering (BCP 38 egress anti-spoof), CDN/anycast absorption (L01's
  architecture as defense).
- **Residual:** volumetric variants (reflection/amplification) — defense moves
  upstream; the honest limit of endpoint hardening.

### 3.5 The residual-risk frame (5 min, the C5 payoff)
Defense-in-depth ≠ perfection: each layer *reduces* likelihood/impact; the plan
must name what remains and why it's acceptable (or not). The worksheet's defense
plan has a mandatory residual-risk column — engineering honesty as a graded skill.

### Reference diagram — SYN flood and the backlog

```text
attacker ──SYN──→ server backlog [x][x][x] … full
            (handshake never completes)
 real clients: refused   │   defense: SYN cookies
                         │   (no state until the ACK arrives)
```

## 4. Important definitions
MITM · Poisoning · Starvation · Half-open connection · SYN cookies (named) ·
DAI (deployed) · Snooping rate-limit · Amplification (named) · Residual risk ·
Defense-in-depth · Incident response basics (detect → contain → eradicate →
recover → lessons; named at concept level).

## 5. Real-world examples
- **Mirai-class botnets** (named, concept): IoT default passwords → DDoS fleets;
  why the *defense* is device hygiene + upstream filtering, not just firewalls.
- **A university's DHCP outage during registration week** = starvation by
  popularity (L22's conference scenario at campus scale).

## 6. Mathematical/technical example
SYN-flood arithmetic: backlog 1,024 half-open, SYN retry window 60 s → ~17 SYN/s
exhausts it (trivially achievable from one host); SYN cookies make the handshake
stateless → the same flood becomes mere bandwidth noise. Compute with the class;
then the amplification math: DNS open resolver ×50 amplification (named ballpark)
— why reflection attacks beat brute force.

## 7. GA-26: benign emulation + defense (35-min rotation)
VM-lab only (ethics gate): (1) **benign SYN-flood pattern** via a provided script
against a VM-hosted test service — *rate-limited, course-owned, instructor-timed*
(not a real attack tool; the handout specifies the exact command and caps);
observe backlog exhaustion in `ss` output; (2) apply the defense (SYN-proxy rule
or backlog/cookie tuning per handout); (3) re-test; (4) log the before/after.
⚠ Pre-verify script + service + `ss` outputs on the image; the rotation's other
stations use *pre-captured evidence* for ARP/DNS/DHCP (no live spoofing anywhere).

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "A firewall stops these attacks" | Each attack's defense is a *stack*; no single box (the workshop's thesis) |
| "Encryption prevents MITM" | Prevents *reading/modifying*; connection still flows through (metadata leaks) |
| "DDoS defense = bigger pipe" | Upstream filtering/absorption beats capacity races |
| "Attackers are exotic" | Every attack today abuses *default-on* protocol behavior — hygiene is the frontier |
| "Residual risk = failure" | It's the honest accounting that makes plans fundable and auditable |

## 9. Suggested practical demonstration
The GA-26 station-1 emulation is the demo (before teams rotate): backlog filling
in `ss -s`, then the defense applied and the same command clean. 3 minutes, high
impact. ⚠ Pre-verify; abort criteria in the handout (instructor-only kill switch).

## 10. Classroom activities
The rotation *is* the activity. Add: **defense-plan peer challenge** — teams
attack each other's plans' residual-risk claims (one question each, written).

## 11. Problem-solving questions
1. Why does SYN cookies change the attacker's economics?
2. Your DNSSEC is deployed but one domain chain is broken — what happens?
   (validation failure → SERVFAIL; operational lesson)
3. Starvation defense: which *one* control helps most at a conference venue and
   why (rate-limit per port vs pool size)?
4. What metadata survives TLS for an on-path ARP attacker?
5. Rank the four attacks by *blast radius* for Meridian and justify in one
   sentence each.

## 12. Formative assessment (with answers)
- MCQ: SYN cookies work by → **stateless handshake encoding**.
- MCQ: DAI validates ARP against → **the snooping binding table**.
- Short: define residual risk in one sentence. → the risk remaining after
  controls, explicitly accepted/documented.

## 13. Exit ticket
1. Attack → signature pairs (any two): ________
2. The defense stack for ARP spoofing (three items): ________
3. My defense plan's biggest residual risk: ________

## 14. Anticipated difficulties
- Ethics-gate enthusiasm management: the rotation's rules are on the wall;
  instructor-only kill switch; restatement verbatim at minute 0.
- CS-03 time competition: the 15-minute block is *protected*; diagnosis drafting
  continues at home (due today via portal).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify GA-26 script/service/backlog observation on the image; abort switch
- [ ] Pre-capture evidence bundles for the other three stations
- [ ] Print worksheets + CS-04 briefs; rotation schedule posted
- [ ] Ethics-gate text verbatim; submission portal ready for CS-03

## 16. Timing fallbacks
If the rotation slips, stations 2–4 (evidence-based) compress to guided analysis;
station 1 (live emulation) is protected — it's the semester's only live defense
experiment.

## 17. References
- BCP 38 (RFC 2827, ingress filtering); RFC 4987 (SYN flooding countermeasures);
  RFC 2131 (DHCP context); RFC 4033-4035 (DNSSEC); instructor notes.
- Mirai-class botnet literature (named, concept citation ⚠ select one reputable
  reference per delivery).
- ⚠ VERIFY tooling and evidence bundles this semester.
