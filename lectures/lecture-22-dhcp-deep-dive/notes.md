# Lecture 22 — Instructor Teaching Notes
## DHCP Deep Dive, BOOTP & Address Management (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4 primary; CLO3/CLO7 supporting |
| Textbook anchor | KR §4.4.5 (revisit); RFC 2131 |

---

## 1. Objectives hook
Board: **"Every device on this campus asks the same four questions daily: who am I,
what's my mask, where's the gateway, who resolves names? Four packets answer all
four — or an attacker answers them first."**

Hook (2 min): printout of a real (sanitized) DORA capture — "by hour's end you can
read this like a newspaper."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L14 DORA recall (3 items, fast); the capture printout |
| 6–28 | Concept 1 | Message anatomy: fields + the option zoo |
| 28–48 | Concept 2 | Lifecycle states, renew/rebind (deeper), conflict detection |
| 48–55 | Concept 3 | Scale design: scopes, reservations, relays, IPAM |
| 55–60 | Break | — |
| 60–82 | GA-22 | Live DORA dissection + IPAM mini-exercise, pairs |
| 82–100 | Concept 4 | Attack & defense: starvation, rogue server, snooping |
| 100–112 | Discussion | BOOTP/PXE lineage (5 min) + design Q&A |
| 112–118 | Summary + exit ticket | — |
| 118–120 | Preview | L23: HTTP/SMTP/SSH — CS-03 opens |

## 3. Concept walkthrough

### 3.1 Message anatomy (22 min)
- **BOOTP bones (DHCP inherits them):** op (1=request/2=reply), htype/hlen/chaddr
  (client MAC), **xid** (transaction ID — L17/L21's randomization story returns),
  **flags** (broadcast bit — why some clients can't unicast early), **ciaddr/yiaddr/
  siaddr/giaddr** (the four addresses: client's current, server's offer, next-server
  (TFTP for PXE!), relay's), sname/file, and the **magic cookie** (99.130.83.99)
  that marks where options begin.
- **The option zoo (teach the ones that matter, name the concept):**
  - 53 message type (DISCOVER/OFFER/REQUEST/ACK/NAK/RELEASE/INFORM/DECLINE)
  - 1 subnet mask; 3 router; 6 DNS; 15 domain name; 51 lease time;
    58/59 T1/T2 (renewal/rebinding — L14's lifecycle gets its wire encoding)
  - 12 host name; 61 client identifier (MAC or DUID — reservation keys!)
  - 82 relay agent information (Option 82: which physical port asked — the snooping
    foundation); vendor-encapsulated 43 (VoIP provisioning et al.)
- **Parameter vs address lease:** DHCP hands *more than addresses* — it's a
  configuration protocol; the "inform" flow (address known, options wanted) shows
  the protocol's second personality.

### 3.2 Lifecycle, deeper (20 min)
- **State machine (client):** INIT → SELECTING → REQUESTING → BOUND → RENEWING
  (unicast to leasing server) → REBINDING (broadcast; any server) → re-INIT on
  failure/expiry. Map each state onto which message flows — students label a blank
  state diagram on the worksheet.
- **Renewal arithmetic (beyond L14):** T1/T2 are *absolute* fractions (50%/87.5%);
  servers *may* shorten a lease at renewal (T1 recalculation); lease *shrinking* is
  the standard trick for reclaiming pools during migrations — an admin's daily tool.
- **Conflict detection (DECLINE + ping probe):** server pings offered address;
  client ARPs it; either party can reject — duplicate addresses are *prevented*
  (mostly), which is why misconfigured static hosts cause the failures they do.
- **NAK semantics:** moving between scopes/subnets → NAK forces re-DISCOVER; students
  who have seen "stuck on 169.254" have met the failure of this step (L12's link-
  local signature connects).

### 3.3 Scale design & IPAM (20 min)
- **Scopes/superscopes; pools & exclusions; reservations** (chaddr/client-id → fixed
  address): printers, APs, cameras — anything with a *service* identity wants a
  reservation, not DHCP-randomness.
- **Relay revisited with giaddr discipline:** one server, many subnets; Option 82
  carries the physical origin; ACL the relay path (only relays may unicast to the
  server) — the first brick of the defense wall (§3.5).
- **IPAM (IP address management) as a discipline:** the *plan* (VLAN↔subnet, per
  CS-02), the *inventory* (who has what, when), and the *audit trail* (leases are
  legal evidence in incident response). Mini-exercise in GA-22: allocate scopes for
  a 3-VLAN building with growth margins (L13/L15 planning habits combine).
- **BOOTP/PXE lineage (5 min in §10/here):** DHCP is BOOTP extended; PXE boots
  bare machines via DHCP options 66/67 (next-server/filename) — the lab imaging
  story; legacy but alive in every enterprise depot.

### 3.5 Attack & defense (18 min)
- **Rogue server:** attacker answers faster than the real one; hands out *themselves*
  as gateway/DNS (L11's floor-of-hotel story, now with fields). Defense: **DHCP
  snooping** — switch marks trusted (toward real server) vs untrusted ports;
  DROPs OFFER/ACK from untrusted ports; builds the binding table (MAC↔IP↔port↔VLAN)
  that feeds **Dynamic ARP Inspection** (L12's named defense) and IP Source Guard.
  The three features are *one system* — say it as a system.
- **Starvation (DoS):** flood DISCOVERs with spoofed chaddr → exhaust the pool;
  legit clients starve. Defense: snooping's rate limit per port + port security
  (L11) + small pools per VLAN (blast radius).
- **Lease hijacking (named, concept):** CLAIM the victim's reservation via client-id
  forgery — requires sniffing; snooping + 802.1X raise the floor.
- Ethics gate restated: starvation/rogue experiments run only in the course VM lab
  (GA-26 territory), never on teaching networks.

### Reference diagram — DHCP lease lifecycle

```text
INIT ──DORA──→ BOUND ──T1 (50%)──→ RENEWING ──Ack──→ BOUND
                 │                        │
                 │ no reply by T2 (87.5%) │
                 ▼                        ▼
             (keep using)            REBINDING ──fail──→ INIT
```

## 4. Important definitions
BOOTP · chaddr/yiaddr/siaddr/giaddr · Magic cookie · Options (53/1/3/6/51/58/59/61/82)
· Client states (INIT…REBINDING) · DECLINE/NAK/INFORM · Reservation · Scope/
superscope · Exclusion pool · IPAM · Relay (Option 82) · DHCP snooping ·
Binding table · DAI/IPS G (named systems) · Starvation · PXE (66/67).

## 5. Real-world examples
- **Printer on a reservation stops printing after a "network refresh":** someone
  changed the reservation's IP; DNS still points at the old one — the IPAM/inventory
  lesson wearing work clothes.
- **Conference-room flood:** 300 attendees, /24 pool, 2-h leases → starvation by
  popularity, not malice — lease-time engineering as capacity planning.
- **VoIP phones booting blank:** Option 43/66 provisioning missing after a server
  migration — options are load-bearing.

## 6. Mathematical/technical example
Pool arithmetic (mini-design): /24 VLAN, 20 static reservations, 25% exclusion for
infrastructure → usable pool ≈ 256−2(network/bcast)−20−64 = 170; lease 2 h;
arrival rate 60 clients/h steady state ⇒ average leases outstanding ≈ 60×2 = 120 —
comfortable; conference burst to 300 ⇒ starvation — the moment the math makes the
security topic concrete (shorten lease to 30 min during events: 300×0.5 = 150 — fits).

## 7. GA-22: dissection + IPAM (22 min)
(a) Live capture of a full DORA (VM lab: restart dnsmasq client on one VM, filter
`bootp`); label every field from §3.1 incl. the magic cookie; mark T1/T2 encodings.
(b) IPAM mini-exercise: 3-VLAN building (staff/students/devices), growth margins,
2 reservations each, write the scope table. Answer key: instructor copy only. ⚠
Pre-verify the lab's dnsmasq restart path and capture filter.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "DHCP = just an IP address" | Configuration protocol: options carry the network's whole onboarding |
| "Reservations guarantee nothing else changes" | Reservation pins the IP; options still come from the scope config |
| "Snooping inspects DHCP payloads for malware" | It enforces *port trust* for OFFER/ACK and builds bindings — a policy feature, not antivirus |
| "NAK means the server is broken" | NAK is protocol-honest scope migration; the client's re-DISCOVER follows |
| "Expiring leases free addresses instantly" | Expiry frees; *shortened renewals* is how admins reclaim fast |
| "BOOTP is dead" | PXE (its child) boots half the world's servers annually |

## 9. Suggested practical demonstration
Live: `journalctl -u dnsmasq` (server view) side-by-side with the Wireshark capture
(client view) during one fresh lease — two perspectives of one conversation. Then
flip a scope's lease to 5 minutes and watch renewal cadence change. ⚠ Pre-script
both; keep the capture as backup.

## 10. Classroom activities
- **State-machine labeling race:** blank client state diagram; first correct table
  wins (ties L14's lifecycle to today's precision).
- **Scope-design honey pot:** the conference-room scenario; teams re-plan leases —
  the math exercise with stakes.

## 11. Problem-solving questions
1. chaddr vs option 61: why can two reservations collide if 61 is DUID-based?
2. giaddr = 10.20.0.1: which scope answers, and who set that field?
3. Why must the broadcast bit exist? (Client without IP can't hear unicast.)
4. Starvation at 2-h leases vs 30-min leases: which survives a 300-client burst,
   and why (show the arithmetic)?
5. Snooping sees OFFER on an untrusted port: what happens next, and what table grows?

## 12. Formative assessment (with answers)
- MCQ: Option 53 carries → **the DHCP message type**.
- MCQ: REBINDING state uses → **broadcast Request (any server)**.
- MCQ: DHCP snooping builds → **the MAC↔IP↔port↔VLAN binding table**.
- Short: two defenses against starvation. → per-port rate limiting; port security;
  small per-VLAN pools (any two).

## 13. Exit ticket
1. The four address fields (ciaddr/yiaddr/siaddr/giaddr) mean: ________
2. Options 51/58/59 encode: ________
3. Snooping + DAI + IP Source Guard form: ________

## 14. Anticipated difficulties
- Field-density fatigue: the capture printout with annotations *pre-drawn* for the
  first two fields anchors the rest — then GA-22's blank version tests transfer.
- IPAM exercise sprawl: cap at 12 minutes with the template (3 scopes, margins,
  2 reservations).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify dnsmasq restart + `bootp` filter; annotate one capture as the key
- [ ] Print worksheets + state-diagram blanks; IPAM templates
- [ ] Board pre-write: field table; option zoo; state diagram blank
- [ ] Ethics-gate language ready for the attack section

## 16. Timing fallbacks
Drop PXE/BOOTP lineage to a reading pointer; GA-22 part (b) (IPAM) can compress to
homework if the dissection runs long — dissection is the protected core.

## 17. References
- RFC 2131 (DHCP); RFC 1532/1533-era BOOTP lineage via RFC 2131 §history; RFC 3046
  (Option 82); RFC 2308 not relevant here (DNS) — avoid cross-citation errors.
- dnsmasq man page (lab server); LAB-05 handout (build context).
- ⚠ VERIFY editions/sections; verify lab behavior this semester.
