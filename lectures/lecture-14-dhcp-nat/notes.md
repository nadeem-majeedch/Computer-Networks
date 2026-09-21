# Lecture 14 — Instructor Teaching Notes
## IP Addressing at Scale: DHCP & NAT (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO3 primary; CLO4 supporting |
| Textbook anchor | KR §4.3.4, §4.4.5; RFC 2131; RFC 3022 |

---

## 1. Objectives hook
Board: **"A new phone joins the campus Wi-Fi. Nobody configures anything. Ten seconds
later it has an address, a gateway, DNS, and a route to the world. Who did what?"**

Hook (2 min): connect to the guest Wi-Fi live; show the address that appears. "Four
packets did that. Let's meet them."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L13 subnet recall (1 item); live DHCP join |
| 6–30 | Concept 1 | DHCP: DORA, message anatomy, relay, lease lifecycle |
| 30–52 | Concept 2 | NAT: the problem it solves, mechanics, flavors |
| 52–55 | Break | — |
| 55–70 | Worked example | NAT translation table walk + hairpin/edge cases |
| 70–75 | LAB-05 briefing | Topology + tasks |
| 75–108 | LAB-05 (in-class) | Pairs configure DHCP+NAT on Linux router VMs |
| 108–118 | Findings + summary | 2 pairs demo their router; exit ticket |
| 118–120 | Preview | IPv6 next — "what if addresses never ran out?" |

## 3. Concept walkthrough

### 3.1 DHCP (24 min)
- **The problem:** static addressing doesn't scale (manual errors, moves, exhaustion);
  hosts need address + mask + gateway + DNS + more (options!).
- **DORA** (simplified RFC 2131 flow):
  1. **Discover** — client broadcasts (255.255.255.255, still address-less: 0.0.0.0
     source) "any DHCP servers?"
  2. **Offer** — server(s) offer lease (yiaddr, options, lease time).
  3. **Request** — client broadcasts its chosen offer (others may stand down).
  4. **Ack** — server confirms + full option set. Client may then do ARP probe/gratuitous
     ARP (duplicate detection).
- **Message anatomy (key fields):** yiaddr (your address), siaddr/server-identifier,
  transaction ID, options (53 = message type; 1 = mask; 3 = router; 6 = DNS; 51 = lease
  time; 12 = hostname; vendor-specific…).
- **Relay agents:** DHCP is broadcast; servers can't hear other subnets' broadcasts —
  relay (ip helper-address) converts to unicast toward the server with giaddr marking
  the subnet. This is why one DHCP server serves a whole campus.
- **Lease lifecycle:** T1 = 50% of lease → client renews with the original server
  (unicast Request); T2 = 87.5% → rebind (broadcast, any server); expiry → must stop
  using the address. Real numbers: 1–24 h leases typical; "infinite" leases are a
  management mistake.
- **LAB-05's tool:** dnsmasq (DHCP+DNS in one, ideal for labs) on the Linux router VM.

### 3.2 NAT (22 min)
- **Why:** IPv4 exhaustion — ~4.3 billion addresses vs tens of billions of devices;
  private space (RFC 1918: 10/8, 172.16/12, 192.168/16) is reused everywhere; NAT
  stitches private nets to the public Internet.
- **Many-to-one (NAPT/PAT — what everyone actually runs):** the router rewrites
  (source IP, source port) → (public IP, *new source port*), records the mapping, and
  reverses it for replies. Port reuse is what makes thousands of hosts share one IP:
  the port space (16 bits) is the resource, not the address.
- **Translation table walk (board):**

| Inside 192.168.1.20:51000 → 8.8.8.8:53 | Public view | Return path |
|---|---|---|
| 192.168.1.20:51000 | 203.0.113.7:40001 | 8.8.8.8:53→203.0.113.7:40001 → table → back inside |

- **Flavors:** static NAT (1:1, for servers), dynamic pool (legacy), NAPT (dominant);
  CGNAT (carrier-grade, shared 100.64/10 space — two NAT layers, the "double NAT"
  complaints).
- **Consequences (the honest list):**
  - Inbound connections impossible without explicit mapping (port forwarding) —
    P2P/game hosting pain.
  - IP-passthrough assumptions break: protocols embedding addresses in payloads
    (legacy FTP/SIP) need helpers (ALGs) — fragile.
  - IPsec complications (address rewriting breaks some integrity expectations — L25
    returns to this).
  - **NAT is not a firewall** (misconception #1 in the register): it has no policy
    engine; unidirectional-initiation is a side effect, not a control (L25).
  - Geolocation/logging: many users behind one IP (CGNAT law-enforcement story).
- **Address management context:** IANA → RIRs (AfriNIC/APNIC/ARIN/LACNIC/RIPE NCC)
  → ISPs; IPv4 markets exist because exhaustion is real (enr, one slide).

### Reference diagram — DHCP DORA + NAT translation

```text
C ──Discover (broadcast)──→ S      inside 10.0.0.5:51322
C ←─Offer─────────────────  S
C ──Request (broadcast)───→ S     NAT: 10.0.0.5:51322
C ←─Ack───────────────────  S          ⇄ 203.0.113.7:40001
            ↑ rewritten per packet at the edge
```

## 4. Important definitions
DHCP · DORA · Lease (T1/T2/rebinding) · Options · Relay agent (giaddr) ·
NAT/NAPT/PAT · Translation table · Static NAT · CGNAT · Port forwarding ·
ALG · RFC 1918 space · Public/private split · IANA/RIR.

## 5. Real-world examples
- **Café/airport Wi-Fi** = DHCP handing 10.x addresses + NAT to one uplink; the
  169.254.x.x address from L12 is precisely DHCP failure.
- **"Can you open port 25565 for my Minecraft server?"** — port forwarding request =
  asking to punch through NAT; an everyday artifact of the addressing shortage.
- **Double NAT at home** (ISP modem + own router): game consoles complain; the fix is
  bridge mode — CGNAT shrunk to a household.

## 6. Mathematical/technical example
Port-space arithmetic: one public IP, 65,536 ports per protocol — minus well-known/
reserved; realistic ~60 k concurrent mappings per protocol; a CGNAT serving 1,000
subscribers with 100 mappings each = 100,000 mappings ≈ 2 public IPs (with
ephemeral-port reuse constraints). Then the reverse question: how many *bits* of
state must the NAT box look up per packet? (≈ a hash lookup on the 4-tuple —
mention flow-state cost; links to L19's middlebox discussions.)

## 7. LAB-05 briefing (5 min)
Topology: 3 VMs — router (2 NICs: internal 192.168.50.1/24, external via NAT/WAN),
client-A, client-B on the internal net. Tasks: configure dnsmasq DHCP pool; enable
IPv4 forwarding + nftables MASQUERADE; verify DORA on the wire (Wireshark filter
`bootp`); verify internet reachability through NAT; observe the translation table
(`conntrack` if present). Full handout in labs/. ⚠ Verify VM image's dnsmasq/nftables
presence before class; pre-configure one complete router as the demo/reference.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "NAT is a security feature" | No policy engine; blocks *unsolicited inbound* as a side effect only — firewalls (L25) do policy |
| "DHCP assigns your MAC address" | It assigns IPs/options; MAC is the client's identity in the exchange |
| "One subnet = one DHCP server" | Relays let one server serve many subnets |
| "NAT helps IPv6" | IPv6 aims to restore end-to-end addressing; NAT64 exists for v6↔v4 transition (L15) |
| "Port forwarding = DMZ = safe" | It's an inbound pinhole to a host; exposure discipline is L25's topic |
| "Leases renew at expiry" | T1 at 50% — clients that disappear at expiry vs renew quietly behave differently |

## 9. Suggested practical demonstration
Before students start: the pre-built router VM demonstrates the finished state —
`nft list ruleset` (MASQUERADE line), `dnsmasq` config, a client's DORA capture, and
the conntrack entry during one curl. 5 minutes, then students replicate. ⚠
Pre-verify the reference VM; screenshot backup for projector failure.

## 10. Classroom activities
- **DORA role-play:** four volunteers (client/server-a/server-b/relay) act the exchange
  with cards; the "relay" must convert broadcast→unicast (physically walk the card to
  the server row) — makes giaddr visceral.
- **NAT table completion:** 3 packet pairs on the worksheet; students fill the
  translation entries and return paths.

## 11. Problem-solving questions
1. Client boots in a new subnet; no reply to Discover. Name two causes and one test for
   each. (No DHCP in subnet / relay missing — capture on both sides.)
2. Why must the client *broadcast* Request even after choosing an Offer?
3. Two clients get 192.168.50.100 simultaneously (different scopes, different
   servers): is conflict possible? What mechanism prevents it within one scope?
4. NAT box receives inbound packet to 203.0.113.7:40001 with no table entry. What
   happens, and what would make it work?
5. An app breaks through NAT but works on the LAN. Give two mechanisms that explain it
   (embedded addresses; inbound initiation).

## 12. Formative assessment (with answers)
- MCQ: DHCP messages travel initially as → **broadcasts**.
- MCQ: Renewal begins at T1 = → **50% of lease**.
- MCQ: NAPT maps (IP, port) → → **(public IP, new port)**.
- Short: why is CGNAT worse than single NAT? → two layers of state; logging ambiguity;
  port exhaustion per public IP shared by more subscribers.

## 13. Exit ticket
1. The four DORA steps: ________
2. NAT translates the pair ( ________, ________ ) → ( ________, ________ ).
3. True/false + why: "NAT protects me from attacks."

## 14. Anticipated difficulties
- LAB-05's two NICs confuse students (which interface is "inside"?); the handout
  labels them and the briefing projects the topology.
- nftables syntax is error-prone; provide the exact MASQUERADE rule in the handout
  (copying ≠ thinking here — the thinking is the verification).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify dnsmasq/nftables/conntrack on the image; reference router pre-built
- [ ] Print LAB-05 handouts; test the DORA capture filter (`bootp`)
- [ ] Prepare DORA role-play cards; NAT-table worksheet answers
- [ ] Verify the room allows outbound from the lab subnet (or scope the lab to
      VM-internal NAT only)

## 16. Timing fallbacks
Trim §6 port-space math to 3 minutes; if lab startup drags, clients configure while
instructor demos the router; relay-agent discussion (§3.1) can compress to 2 minutes.

## 17. References
- KR §4.3.4 (DHCP), §4.4.5 (NAT, ⚠ verify section); RFC 2131 (DHCP); RFC 3022 (NAT);
  RFC 1918 (private space).
- dnsmasq man page; nftables wiki (MASQUERADE); conntrack tools documentation.
- ⚠ VERIFY editions/sections and image tooling this semester.
