# Lecture 13 — Instructor Teaching Notes
## IPv4 Subnetting & VLSM (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO3 primary |
| Textbook anchor | KR §4.3.3–4.3.4; PD §3.3 |

---

## 1. Objectives hook
Board: **"You are handed 192.168.10.0/24 and 5 buildings: 120, 60, 30, 10, 2 hosts.
Two rules: every subnet gets exactly one prefix; 20% growth headroom everywhere.
By the end of today you'll do this in under 10 minutes — and justify it."**

Hook (2 min): poll "how many of you could do this today?" — then promise the method.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–5 | Recap + hook | L12 notation recall; the challenge on the board |
| 5–20 | Concept 1 | The mask as a boundary; network/broadcast/host computation method |
| 20–40 | Concept 2 | Powers-of-two method for /25../30; the reference table |
| 40–55 | Concept 3 | VLSM: largest-first allocation; aggregation |
| 55–60 | Break | — |
| 60–95 | Guided practice | The 5-building challenge together, then pairs (LAB-04 start) |
| 95–110 | Design talk | Headroom, documentation, subnet↔VLAN pairing (L09 link) |
| 110–118 | Summary + exit ticket | — |
| 118–120 | Preview | DHCP/NAT next |

Concept 55 min + practice 35 min: this is the course's most computational lecture and is
structured accordingly (skills rehearsal dominates).

## 3. Concept walkthrough

### 3.1 The mask is a boundary (15 min)
- Prefix /n = first n bits network, rest hosts. The mask in binary is n ones then zeros —
  dotted decimal is just a rendering (255.255.255.0 = /24).
- Given IP a.b.c.d/n:
  - **Network** = IP AND mask (all host bits → 0).
  - **Broadcast** = network + all host bits → 1.
  - **Usable hosts** = 2^(32−n) − 2 (network + broadcast excluded) — *except* /31 and /32
    (RFC 3021 point-to-point: /31 has 2 usable; /32 is a host route — mention, don't drill).
- Worked: 192.168.10.77/26 → last octet 77 = 01001101; /26 → last 6 bits host →
  network 192.168.10.64, broadcast 192.168.10.127, hosts .65–.126 (62 usable).
- **The method to teach (and drill):** find the octet where the boundary lives; compute
  the *block size* = 256 − (mask octet) = number of addresses in that octet's steps;
  multiples of block size bound the subnet. /26 → block 64 → networks at 0/64/128/192.

### 3.2 The reference table (20 min — build it WITH the class, don't project it finished)
| Prefix | Block (addresses) | Usable hosts | Mask last octet |
|---|---|---|---|
| /25 | 128 | 126 | .128 |
| /26 | 64 | 62 | .192 |
| /27 | 32 | 30 | .224 |
| /28 | 16 | 14 | .240 |
| /29 | 8 | 6 | .248 |
| /30 | 4 | 2 | .252 |
- Rule: *usable hosts* needs 2 extra for network/broadcast → pick the smallest block
  with block ≥ hosts+2. Students who memorize "which /n fits 60 hosts?" (→ /26) are
  doing it wrong; teach "60+2=62 ≤ 64 → /26".
- Speed drills (2-minute sprints, 3 rounds): "50 hosts? 300? 2? 1000?" → /26, /23, /30,
  /22. Sprint culture here pays for the whole semester (this is a *skill*, not knowledge).

### 3.3 VLSM and aggregation (15 min)
- **VLSM:** variable-length subnets from one parent block — allocate **largest first**,
  aligned to their own block size, no overlaps:
  192.168.10.0/24 → B1 (120+2→/25): 10.0–10.127; B2 (60→/26): 10.128–10.191;
  B3 (30→/27): 10.192–10.223; B4 (10→/28): 10.224–10.239; links (2→/30s): 10.240+.
- **Aggregation:** the four /26s inside 172.16.4.0–172.16.7.255 summarize as 172.16.4.0/22
  — because they're *contiguous and aligned*. Route-table motivation: core routers
  carrying one /22 instead of four /26s; the global Internet's ~1M routes exist because
  aggregation isn't universal (enr: routing-table growth discussions).
- Common VLSM trap: alignment (a /26 must start at a multiple of 64) — show one broken
  plan and let the class find the overlap.

### Reference diagram — Borrowing bits: /24 into four /26s

```text
11000000.10101000.00000100.│00│000000   ← borrowed bits
 ┌─────────┬──────────┬───────────┬──────────┐
 │ .0–.63  │ .64–.127 │ .128–.191 │ .192–.255│   four /26s
 └─────────┴──────────┴───────────┴──────────┘
 64 addrs each; 62 usable (network + broadcast)
```

## 4. Important definitions
Subnet mask · Prefix (/n) · Network address · Broadcast address · Usable hosts ·
Block size · VLSM · CIDR · Aggregation/summarization · RFC 3021 (/31) · Host route (/32).

## 5. Real-world examples
- A campus plan: one /16, buildings get /24s, buildings' floors /26s — readable,
  printable, memorable. (Bad real-world plans leak: "why is room 204 in the finance
  subnet?" — address plans encode org structure.)
- Cloud subnets: AWS/VNet force explicit CIDR choices at creation; resizing later is
  painful — VLSM discipline is a career skill, not an exam trick.

## 6. Mathematical/technical example
The 5-building challenge fully worked on the board (see hook). Include the headroom
step: B1 120 hosts → +20% = 144 → 144+2=146 ≤ 256 → /24? No — /24 exceeds the /24
parent when 5 subnets needed… deliberately let the class hit the contradiction, then
reveal: *the parent is too small for that growth* — real design means escalating to
10.0.0.0/23 and saying so in the justification. Teach that "not enough space" is a
legitimate, professional finding.

## 7. Guided practice + LAB-04 start (35 min)
Phase 1 (instructor-led, 15 min): challenge above. Phase 2 (pairs, 20 min): LAB-04
problem set part A (6 computation problems) + start of the design exercise; instructor
circulates. LAB-04 due L16 (weights: 5% instrument per assessment strategy).

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Subnetting is memorizing tables" | It's powers-of-two + alignment; the table is a byproduct |
| "/24 always means 254 hosts I must use" | VLSM slices further; waste is a design failure |
| "Broadcast address is usable" | 2 reserved addresses per subnet (network+broadcast) |
| "Any start address works for a /26" | Alignment to block size is mandatory |
| "Aggregation is just 'use a shorter mask'" | Must be contiguous AND aligned |
| "IPv6 removes the need for this skill" | IPv6 uses prefixes everywhere (L15); the *skill* transfers directly |

## 9. Suggested practical demonstration
Python as a calculator (2 min, optional): `ipaddress` module:
```bash
python3 - <<'EOF'
import ipaddress
net = ipaddress.ip_network("192.168.10.77/26", strict=False)
print(net, net.broadcast_address, net.num_addresses)
print([str(s) for s in ipaddress.ip_network("192.168.10.0/24").subnets(new_prefix=26)])
EOF
```
Framing matters: "the tool *checks* your hand work, it doesn't replace it" — exam is
closed-device.

## 10. Classroom activities
- **Sprint ladder:** 3 rounds of 5 rapid fit-the-prefix questions; score on the board.
- **Find the overlap:** one deliberately broken VLSM plan; first pair to name the
  overlapping subnet pair wins.

## 11. Problem-solving questions
1. 10.4.35.77/22 → network, broadcast, usable range. (10.4.32.0, 10.4.35.255, .33.1–.35.254)
2. Need 300 hosts → prefix? (/23) Need 2 hosts on a WAN link → (/30 or /31)
3. Aggregate 172.16.4.0/24 + 172.16.5.0/24 + 172.16.6.0/24 + 172.16.7.0/24 → /22.
4. You have 10.9.0.0/22 and need 4 equal /24-class departments: possible? (No — /22
   holds 1024 addresses = 4 × /24 exactly: yes! check alignment: 10.9.0.0/22 contains
   10.9.0.0–10.9.3.255 → four /24s. Good trap: "22 vs 23" confusion.)
5. A plan assigns 10.0.64.0/26 and 10.0.64.32/28. Overlap? (Yes: /28 inside /26.)

## 12. Formative assessment (with answers)
- MCQ: Usable hosts in /28 → **14**.
- MCQ: Network address of 172.16.19.7/22 → **172.16.16.0**.
- Short: why largest-first in VLSM? → smaller blocks fit into gaps; reverse order
  fragments the space.

## 13. Exit ticket
1. /26 block size + usable hosts: ________ / ________
2. Network address of 192.168.1.100/28: ________
3. The two alignment rules for aggregation: ________

## 14. Anticipated difficulties
- Wide skill variance is the biggest risk: sprints + pair work + the `ipaddress`
  checker keep both fast and slow students engaged; early finishers get the /22 trap
  question.
- Octet-boundary blindness (only the *boundary octet* matters): drill with /22, /23,
  /21 examples that break the last-octet habit.

## 15. Instructor preparation checklist
- [ ] Print LAB-04 handouts; verify `ipaddress` demo runs on image
- [ ] Board pre-write: reference table skeleton; challenge requirements table
- [ ] Prepare 3 sprint rounds (15 Qs) + the broken-plan slide
- [ ] Timekeeper: this lecture dies without pacing discipline

## 16. Timing fallbacks
Cut §5 real-world examples entirely and aggregation to 6 minutes; the computation
method + VLSM + guided practice are the irreducible core (CLO3's primary artifact
grows from here).

## 17. References
- KR §4.3.3–4.3.4; PD §3.3.
- RFC 950 (subnetting, historical), RFC 1519 (CIDR), RFC 3021 (/31 links).
- Python `ipaddress` module docs (checker tool only).
- ⚠ VERIFY editions/sections this semester.
