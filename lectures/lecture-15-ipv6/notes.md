# Lecture 15 — Instructor Teaching Notes
## IPv6 (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO3 primary; CLO4 supporting |
| Textbook anchor | KR §4.3.5; RFC 8200 |

---

## 1. Objectives hook
Board: **"1994 prediction: we run out of IPv4 addresses by ~2010. It's [current year].
Did we? What actually happened?"**

Hook (2 min): show your phone's Wi-Fi details — it likely has *several* addresses in
two families simultaneously. Dual stack is not the future; it's the present.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | NAT pain recall; phone's multiple addresses |
| 6–20 | Concept 1 | Why IPv6: exhaustion math & design goals |
| 20–40 | Concept 2 | Address structure, types, abbreviation rules |
| 40–55 | Concept 3 | Header changes vs IPv4; SLAAC/RA vs DHCPv6 |
| 55–60 | Break | — |
| 60–72 | LAB-06 briefing | Dual-stack topology + capture tasks |
| 72–105 | LAB-06 (in-class) | Pairs build/capture both families |
| 105–115 | Worked example | Abbreviation drills + prefix math (§6) |
| 115–120 | Summary + exit ticket + preview | Routing next |

## 3. Concept walkthrough

### 3.1 Why IPv6 (14 min)
- The math: 32 bits ≈ 4.3×10⁹ addresses vs tens of billions of devices; exhaustion
  arrived (RIR pools essentially exhausted; markets for IPv4 blocks exist). NAT (L14)
  was the pressure valve, not the cure.
- IPv6 design goals: **128-bit addresses** (not "more IPv4" — a redesign); restore
  end-to-end addressing (NAT66 is an anti-pattern except at edges); simplify headers
  (fixed 40 B; no per-hop checksum); hierarchical aggregation for routing-table
  sanity; built-in autoconfiguration; IPsec support (not "required" in practice —
  correct the myth).
- Adoption reality check: deployment varies hugely by country/ISP/mobile; students'
  own devices often have working v6 without knowing it. Have one `test-ipv6`-style
  live check (or pre-recorded) if the room has v6.

### 3.2 Addresses (20 min)
- **Structure:** 128 bits, 8 groups of 16 bits in hex; **abbreviation rules**: drop
  leading zeros per group; replace ONE run of all-zero groups with `::` (only once —
  ambiguity rule; drill it).
  - `2001:0db8:0000:0000:0000:ff00:0042:8329` → `2001:db8::ff00:42:8329`.
- **Types:**
  - **GUA** (global unicast, 2000::/3) — public; typically a /64 per link from an
    ISP delegation (often /48 or /56 to a site).
  - **Link-local (fe80::/10)** — mandatory per interface, no router needed; ARP's
    replacement (ND) runs here; you've seen them on every Linux box.
  - **ULA (fc00::/7, fd00::/8 practice)** — private, *not* NAT-ed by default (no
    NAT66 norm).
  - **Multicast (ff00::/8)** — replaces broadcast entirely; requested-node multicast
    (ff02::1:ffxx:xxxx) ties into ND below.
  - No broadcast: by design.
- **/64 is the standard subnet size** — bigger than every IPv4 network combined per
  *link*; planning changes philosophy: allocate generously, don't conserve.
- **EUI-64/privacy extensions (enr):** interface identifiers from MAC (ff:fe insert)
  vs temporary randomized addresses (RFC 4941) — privacy story in one minute.

### 3.3 Header changes & autoconfiguration (15 min)
- **Header table (IPv4 → IPv6):**
  - Fixed 40 B; IHL gone (no options in base header — extension headers instead).
  - **Checksum removed** (L2/L4 already check; per-router recompute was cost).
  - **No router fragmentation** — sender does PMTUD; routers return Packet Too Big
    (ICMPv6). Firewall note: blocking ICMPv6 breaks PMTUD — real-world footgun.
  - TTL → Hop Limit (same idea, honest name); Protocol → Next Header; addresses ×4
    in size.
- **ND (Neighbor Discovery)** replaces ARP: solicitations/advertisements over ICMPv6
  + multicast (show capture in LAB-06).
- **SLAAC (the star):** router advertisements (RA) announce the prefix; host builds
  address = prefix + interface ID; default route learned from RA. No server needed.
  Flags (M/O bits) decide: SLAAC-only, SLAAC+DHCPv6 for other options, or
  stateful DHCPv6. Compare with L14's DHCP: stateless vs stateful addressing.

### Reference diagram — IPv4 vs IPv6 fixed header

```text
v4 (20 B, variable): ver│IHL│len│id│frag│TTL│proto│cksum│src│dst
v6 (40 B, fixed):    ver│class│flow│len│next│hop│src(16 B)│dst(16 B)
 v6 drops: header checksum, in-header fragmentation
```

## 4. Important definitions
GUA · Link-local (fe80::/10) · ULA · Multicast (ff00::/8) · Solicited-node multicast ·
/64 subnet · Abbreviation (`::` rule) · Extension header · Hop Limit · Next Header ·
Neighbor Discovery (ND) · RA (Router Advertisement) · SLAAC · DHCPv6 (stateless/
stateful) · PMTUD · Dual stack · Privacy extensions (enr).

## 5. Real-world examples
- **fe80:: addresses** on every Linux/Mac `ifconfig`/`ip addr` output in this room —
  the protocol is running whether or not the room "has IPv6".
- **Mobile carriers** run large v6 networks (many national carriers are majority-v6);
  students can check their phone's cellular status page.
- **The "no broadcast" design:** a building full of IPv6 hosts generates no ARP-style
  broadcast storms — L08's problem class engineered out.

## 6. Mathematical/technical example
Abbreviation drills (do 4 live): `fe80:0000:0000:0000:02aa:00ff:fe28:9c5a` →
`fe80::2aa:ff:fe28:9c5a`; `2001:0db8:0000:0000:ab00:0000:0000:0001` →
`2001:db8::ab00:0:0:1` (why not `2001:db8::ab00::1`? — `::` twice is illegal).
Address-space arithmetic: 128 bits ≈ 3.4×10³⁸; Earth's surface ≈ 5.1×10¹⁴ m² →
~6.6×10²³ addresses per square metre — the abundance that *justifies* /64-per-link
philosophy. Prefix math: ISP delegates /48 → 65,536 /64 subnets.

## 7. LAB-06 briefing (12 min)
Topology (2 VMs, dual-stack): add v6 addresses (LLA + ULA or GUA via RA using radvd
on one VM — handout provides configs); tasks: verify ping over both families; capture
ICMPv6 ND exchange (filter `icmpv6`) and identify NS/NA; capture an RA (filter `icmpv6
type 134`) and read the prefix; disable v4 on one host and confirm apps still work
(stretch). ⚠ Verify radvd/ndisc6 presence on the image; pre-built reference topology
as demo.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "IPv6 is IPv4 with longer addresses" | Redesigned header, ND, no broadcast, SLAAC, no router fragmentation |
| "IPv6 has no NAT, so my LAN is exposed" | Default-forwarding still requires routing/firewall policy (L25); v6 changes addressing, not policy existence |
| "`::` can replace any zeros, anywhere" | Once per address — ambiguity; drill it |
| "Link-local addresses mean broken networking" | They're mandatory and functional; ND runs over them |
| "IPv6 removes the need for DHCP forever" | SLAAC covers addresses; DHCPv6 still used for options/some policies |
| "You can't memorize IPv6 addresses" | Nobody memorizes hosts; you memorize *prefixes* — plan accordingly (CS-02 extension) |

## 9. Suggested practical demonstration
On the podium VM: `ip -6 addr` (show LLA + any GUA), `ping -6` a neighbor, capture ND
(NS/NA) in Wireshark, then `radvd` config + a captured RA dissected field by field.
5 minutes before LAB-06. ⚠ Pre-verify all commands; recorded fallback if the room's
virtual switches strip multicast RA behavior unexpectedly.

## 10. Classroom activities
- **Abbreviation race:** 6 addresses on the board, first correct per row scores;
  include one illegal-`::` trap.
- **Address-type sorting:** 10 addresses (GUA/LLA/ULA/multicast/IPv4-mapped) — teams
  classify in 90 seconds.

## 11. Problem-solving questions
1. Abbreviate: `2001:0db8:0000:0000:0000:0000:0000:0042`.
2. Why is `2001:db8::ab00::1` illegal?
3. A host has only fe80:: on an interface. Can it ping the host next to it? The one
   across a router? Why?
4. Your firewall blocks all ICMPv6. What breaks? (ND + PMTUD — explain both.)
5. Site gets 2001:db8:aaaa::/48. How many /64 subnets? Plan two for VLANs 10/20.

## 12. Formative assessment (with answers)
- MCQ: IPv6 link-local prefix is → **fe80::/10**.
- MCQ: The IPv6 header checksum → **does not exist**.
- MCQ: SLAAC addressing is configured by → **Router Advertisements**.
- Short: why no broadcast in IPv6? → multicast solves the need (solicited-node,
  all-nodes) without flooding every host.

## 13. Exit ticket
1. Abbreviate `fe80:0:0:0:0:0:0:1` → ________
2. SLAAC is configured by ________ messages from ________.
3. IPv6's ARP-replacement is called ________ and runs over ________.

## 14. Anticipated difficulties
- Abbreviation rules take reps; the race drill covers it — don't skip it.
- Students conflate "no NAT in IPv6" with "no firewalls in IPv6" — L25 will re-fix,
  but preempt today (misconception table).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify radvd + ND capture works on the image; reference topology ready
- [ ] Prepare abbreviation drill set (incl. illegal trap); print LAB-06 handouts
- [ ] Board pre-write: abbreviation rules; header comparison table skeleton
- [ ] Check room v6 availability for the live adoption demo; else use recorded data

## 16. Timing fallbacks
Drop EUI-64/privacy to reading; compress §3.1 to 8 minutes; LAB-06 and the
abbreviation drills are protected.

## 17. References
- KR §4.3.5; RFC 8200 (IPv6 spec); RFC 4861 (ND); RFC 4862 (SLAAC); RFC 4941
  (privacy extensions); RFC 4193 (ULA).
- radvd documentation; LAB-06 handout.
- Google/APNIC IPv6 adoption statistics (for the adoption slide; cite the tracker
  used). ⚠ VERIFY editions/sections and adoption numbers are current when shown.
