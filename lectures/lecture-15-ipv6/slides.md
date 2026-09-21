# Lecture 15 — IPv6 — Slide Deck

| Field | Value |
|---|---|
| Slides | 17 (120 min: 10 open · 55 teach · 5 break · 40 LAB-06 · 10 wrap) |
| Companions | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) · [LAB-06](../../labs/lab-06-dual-stack/README.md) |
| Style | [Course deck conventions](../../lectures/README.md#deck-conventions) |

## Deck outline

| # | Slide | # | Slide |
|---|---|---|---|
| 1 | Title | 10 | NDP: IPv6's ARP |
| 2 | Hook: 340 undecillion addresses | 11 | SLAAC (diagram) |
| 3 | The 128-bit address | 12 | Worked example: read a prefix |
| 4 | Writing it: RFC 5952 rules | 13 | LAB-06 brief |
| 5 | Worked example: compress | 14 | Classroom questions |
| 6 | Address types table | 15 | Common misconceptions |
| 7 | Link-local fe80::/10 | 16 | Summary |
| 8 | No broadcast — multicast | 17 | Exit question |
| 9 | Global unicast anatomy | | |

## Slides

### Slide 1 — Title
**Computer Networks — Lecture 15**
IPv6 (LAB-06 today)

> Notes — Same Internet architecture; new address plane. Focus: reading, classifying, and auto-configuring addresses.

### Slide 2 — Hook: 340 undecillion addresses
- IPv4: 4.3 billion — exhausted (L14's NAT was the patch)
- IPv6: 2¹²⁸ ≈ 3.4×10³⁸ — every grain of sand gets a /62
- Why didn't we switch in 1998? (Answer: the waist is sticky — L02)

> Notes — The sand figure: 2^128 ÷ 7.5×10^18 grains ≈ 4.5×10^19 per grain — even /64-sized to each. The switch *cost* is the honest answer to the delay.

### Slide 3 — The 128-bit address
- 8 groups × 4 hex digits, colon-separated
- **/64 is the standard host boundary** (huge!)
- Prefix /48–/56 to a site; /64 per link

> Notes — The /64 convention is the design keystone: it makes SLAAC possible (next slides). "Huge on purpose" — interface IDs are 64-bit by design.

### Slide 4 — Writing it: RFC 5952 rules
1. Drop leading zeros in each group
2. Replace the **longest** run of zero groups with `::` — **once**
3. Lowercase hex

> Notes — Three rules, quiz W08 Q1 tests all. The "once" is where students slip (ambiguity is why).

### Slide 5 — Worked example: compress
- `2001:0db8:0000:0000:0000:ff00:0042:8329`
- Drop leading zeros: `2001:db8:0:0:0:ff00:42:8329`
- `::` the 3-group run: **`2001:db8::ff00:42:8329`**

> Notes — Do it live, three steps, no skipping. LAB-06 drills the reverse (expansion) too.

### Slide 6 — Address types table

| Type | Prefix | Scope |
|---|---|---|
| Global unicast | 2000::/3 | Internet-routable |
| Link-local | fe80::/10 | one link only |
| Multicast | ff00::/8 | many (scope in nibble) |
| Unique local | fc00::/7 | site-private |

> Notes — Quiz W09-adjacent vocabulary; link-local and multicast get their own slides. Documentation prefix 2001:db8::/32 appears in all our examples — say why (RFC 3849).

### Slide 7 — Link-local fe80::/10
- Self-configured on every interface, always
- Protocol workhorse: NDP, next-hop for routers
- Never routed between links

> Notes — "Every interface has one, even with a global address" — LAB-06 shows both on one interface. Quiz W08 Q2 tests the never-routed clause.

### Slide 8 — No broadcast — multicast
- IPv4's ff:ff:ff:ff:ff:ff has no IPv6 equivalent
- Replaced by scoped multicast: ff02::1 (all nodes), ff02::2 (all routers)
- Solicited-node multicast makes NDP efficient

> Notes — Quiz-prep: "IPv6 removed broadcast; name the replacement class" (review-M3 Q10). Efficiency story: solicited-node reaches *few* NICs, not all.

### Slide 9 — Global unicast anatomy

```text
2001:db8:0000:1234:/48 site → 0005:/64 link → interface ID
|--- routing (site) ---||--- subnet ---||--- interface ---|
```

- Site gets /48; 16 bits of subnetting room inside (65 536 links)

> Notes — Subnetting *inverts*: the host side is fixed at /64; all design freedom is the middle. Preview L31's enterprise plan.

### Slide 10 — NDP: IPv6's ARP
- Same job: IP → MAC on one link
- Multicast-based (solicited-node), not broadcast
- Also does router discovery (RS/RA) — IPv4 needed DHCP for that

> Notes — The RS/RA clause is the SLAAC setup. NDP spoofing mirrors ARP spoofing (L26 defense parity — DAD-guard / RA-guard named, not dissected).

### Slide 11 — SLAAC (diagram)

```mermaid
sequenceDiagram
  H->>Link: Router Solicitation (RS)
  R->>H: Router Advertisement (RA: prefix, flags)
  H->>H: address = prefix + interface ID
  H->>Link: Duplicate Address Detection probe
  Note over H: address usable
```

- Hosts build addresses from RAs — no server needed

> Notes — The "stateless" in SLAAC: no server keeps state. DAD closes the loop (quiz-level: why DAD — review-M3 Q11).

### Slide 12 — Worked example: read a prefix
- RA advertises `2001:db8:1::/64`; MAC `aa:bb:cc:dd:ee:01`
- Interface ID: flip bit 7 → `a8bb:ccff:fedd:ee01` (EUI-64 style)
- Address: `2001:db8:1::a8bb:ccff:fedd:ee01`

> Notes — Modern stacks randomize the interface ID for privacy — say so; EUI-64 is the *teaching* mechanism (notes.md has both).

### Slide 13 — LAB-06 brief
- Pairs: dual-stack namespace; observe link-local + global; SLAAC via RA
- Verify DAD; test IPv6 ping between neighbors
- Deliverable: address table with type labels + one capture of an RS/RA pair

> Notes — 40 min. The deliverable's type labels are the assessable vocabulary (slide 6's table in action).

### Slide 14 — Classroom questions
1. Why exactly one `::`?
2. fe80::1 exists on two of your machines — collision?
3. What does IPv6 do to NAT's job security?

> Notes — Q2: none — link-local is per-*link* scope, different links may reuse. Q3: honest answer — removes the *scarcity* motive; policy NAT survives (course-level framing).

### Slide 15 — Common misconceptions
- "IPv6 = IPv4 with longer addresses" → ND/SLAAC/no-broadcast are *different machinery*
- "IPv6 has no broadcast so nothing floods" → multicast still floods (scoped)
- "You need DHCPv6" → SLAAC usually suffices; DHCPv6 is optional stateful mode

> Notes — The first misconception is the deepest: the *protocols around* the address changed too.

### Slide 16 — Summary
- 128 bits, /64 host side, three writing rules
- Types: global, link-local, multicast, ULA
- NDP + SLAAC = self-configuring links
- Next: routing & ICMP — the layer that moves it all (L16)

> Notes — Recap: compress one address on call, classify one address on call.

### Slide 17 — Exit question
Compress `2001:0db8:0000:0001:0000:0000:0000:00ff` per RFC 5952.
*(LAB-06 due next session.)*

> Notes — Answer: `2001:db8:0:1::ff`. Exit slips feed W08 pool (midterm week — keep the wrap brisk).

### Demonstration instructions (instructor)
- LAB-06: dual-stack namespaces; `ip -6 addr`, `ping -6` — ITI: verify RA daemons (radvd or kernel) on the teaching image
- Capture beat: one RS/RA exchange + one solicited-node multicast — the two "new machines" of IPv6
- Fallback: worksheet prints both exchanges, labeled synthetic where edited

### References for the deck
- RFC 4291 (addressing), RFC 5952 (text representation), RFC 4861 (NDP), RFC 4862 (SLAAC)
- PD §4.3 (IPv6)
- LAB-06 package: [`../../labs/lab-06-dual-stack/README.md`](../../labs/lab-06-dual-stack/README.md)
