# Lecture 12 — Instructor Teaching Notes
## IP Fundamentals & ARP (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4 primary; CLO2/CLO7 supporting |
| Textbook anchor | KR §4.3.1–4.3.2; RFC 791; RFC 826 |

---

## 1. Objectives hook
Board: **"Ethernet speaks MAC addresses. IP speaks IP addresses. Your packet needs both.
Who introduces them — and why doesn't IP just use MAC addresses?"**

Hook (2 min): show a captured packet with both address families visible: "two postal
systems on one envelope. Today: what each one is for and who translates."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | Module 2 recap quiz (2 items); two-addresses hook |
| 6–20 | Concept 1 | The IP service model: best effort, hop-by-hop, why it won |
| 20–40 | Concept 2 | IPv4 header field-by-field (with packet to project) |
| 40–55 | Concept 3 | ARP: the translator — flow, cache, gratuitous ARP |
| 55–60 | Break | — |
| 60–80 | GA-12 | ARP resolution walk on a real trace, pairs |
| 80–95 | Concept 4 | Addressing notation primer: dotted decimal, binary, prefix preview (L13 runway) |
| 95–108 | Security preview | ARP spoofing: mechanism, symptom, defenses (thread) |
| 108–118 | Summary + exit ticket | — |
| 118–120 | Preview | Subnetting (L13): the math module |

## 3. Concept walkthrough

### 3.1 The IP service model (14 min)
- **Best-effort, connectionless, packet-switched:** IP promises to *try*: no delivery
  guarantee, no ordering, no duplicate protection, no bandwidth guarantee. Everything
  hard (reliability, ordering) is a higher layer's job — TCP (L18) or the app (QUIC etc.).
- **Why so dumb on purpose (end-to-end argument in one slide):** keep the core simple;
  complexity at edges. This is the design decision that let the Internet scale past
  every smarter-looking alternative (telephone world included).
- **Hop-by-hop model:** each router makes an *independent* forwarding decision per
  packet using only the destination address and its own table (L16 formalizes the
  table). TTL exists precisely because loops among independent deciders were expected.
- Addresses identify *interfaces*, not machines (a router has many IPs; your phone has
  Wi-Fi and cellular IPs simultaneously).

### 3.2 IPv4 header, field by field (20 min)
Project one real header (Wireshark dissection) and walk:

| Field | Bits | Job |
|---|---|---|
| Version | 4 | 4 (or 6 → different header entirely, L15) |
| IHL | 4 | Header length in 32-bit words (options exist; usually 5 → 20 B) |
| DSCP/ECN | 8 | Quality marking / congestion signaling (L19 mentions ECN) |
| Total Length | 16 | Datagram bytes (header+data) — max 65,535 |
| Identification/Flags/Fragment offset | 32 | Fragmentation machinery (exists; discouraged; MTU/MSS handle sizes in practice — L18) |
| TTL | 8 | Decremented per hop; 0 → drop + ICMP Time Exceeded (traceroute's engine, L16) |
| Protocol | 8 | Demux: 6=TCP, 17=UDP, 1=ICMP (L02's demux chain, now concrete) |
| Header Checksum | 16 | Header-only integrity (IPv6 drops it — L15 explains why) |
| Source/Destination | 32+32 | Interface addresses end-to-end (NAT will rewrite them at L14) |

- Emphasize the **three fields students will use weekly**: TTL, Protocol, addresses.
- Fragmentation: teach the *existence and cost* (CPU, loss amplification, firewall
  weirdness); modern practice avoids via MSS/path MTU discovery — details L18.

### 3.3 ARP (15 min, the translator)
- The problem: IP says "deliver to 192.168.10.23"; Ethernet says "give me a 48-bit MAC".
- **The flow (simplified RFC 826):** sender checks its ARP cache → miss → **broadcast**
  ARP Request (L07's ff:ff:ff:ff:ff:ff!) "who has 192.168.10.23?" → target replies
  **unicast** "I do, MAC is …" → requester caches (typically minutes); *all* hosts may
  opportunistically cache the requester's mapping too.
- **Gratuitous ARP:** unsolicited announcement ("this is my new MAC") — used on failover;
  also an attack primitive (spoofed announcements — §3.5).
- Proxy ARP (enr, one line): a router answers on behalf of another subnet — historical.
- **Why both address systems exist:** IP addresses are *topological* (where you are —
  routable), MAC addresses are *identity-of-NIC* (who the NIC is — flat, not routable).
  The layering cost/benefit discussion from L02 gets its best concrete example here.

### 3.4 Addressing notation primer (13 min — L13's runway)
- Dotted decimal ↔ binary: 192.168.10.23 = 11000000.10101000.00001010.00010111 (do two
  octets live, students do two).
- Prefix notation preview: 192.168.10.0/24 — "first 24 bits are the network" (L13
  makes it computational).
- Special addresses table (memorize): 127/8 loopback; 10/8, 172.16/12, 192.168/16
  private (RFC 1918); 169.254/16 link-local (DHCP failure signature!); 255.255.255.255
  broadcast.

### 3.5 ARP security preview (13 min)
- The flaw: **no authentication** — any host may *answer* any request or send
  gratuitous ARP. Attacker announces "gateway's IP is *my* MAC" → victims send traffic
  to attacker (MITM); symptoms: intermittent "session drops" (traffic forwarded with
  delay/inspection), duplicated responses.
- Defenses (named, concept level): Dynamic ARP Inspection (switch validates ARP against
  a trusted binding table), static ARP entries (small nets), 802.1X admission (L11).
- Ethics restate: we study this in the VM lab only (GA-26).

### Reference diagram — ARP exchange

```text
A (10.0.0.5) asks for 10.0.0.9's MAC:
 A ──→ ff:ff:ff:ff:ff:ff   "Who has 10.0.0.9?"   (broadcast frame)
 B ──→ A                  "10.0.0.9 is at <MAC_B>" (unicast reply)
 A caches the mapping; B also caches A's (it saw the request)
```

## 4. Important definitions
Best-effort delivery · Connectionless · Hop-by-hop forwarding · TTL · Protocol field ·
IHL · Fragmentation (existence) · ARP · ARP cache · ARP Request (broadcast) / Reply
(unicast) · Gratuitous ARP · Proxy ARP (enr) · Link-local address · Private addresses
(RFC 1918) · Loopback.

## 5. Real-world examples
- **169.254.x.x on a laptop** = DHCP failed: the address *tells a story* — teach
  students to read addresses diagnostically from day one of Module 3.
- **TTL in the wild:** `ping` output's TTL reveals hop count (255−observed on many
  stacks, 64/128 initial values) — a party trick that reinforces TTL's job.
- **"New router, everything works instantly"** is ARP + gratuitous ARP + DHCP renewals
  doing a choreographed handover.

## 6. Mathematical/technical example
Header size arithmetic: IHL=5 → 5×4=20 B; with 8 B options (IHL=7) → 28 B. Total Length
1,500 → payload = 1,500−20−20(TCP) = 1,460 B. Efficiency: 1,460/1,540 (with Ethernet)
≈ 94.8% — consistent with L04's iperf observations. Students compute one full overhead
chain themselves (app→frame) as a bridge from L02.

## 7. GA-12: ARP resolution walk (20 min)
Provided trace excerpt (ARP request broadcast → reply unicast → ICMP echo):
students fill: requester/target IPs & MACs, which frame was broadcast, cache effects,
and "what would change if the target were on another subnet?" (answer: it never
happens — ARP is link-local; the packet goes to the *gateway's* MAC — the fundamental
"ARP for the next hop, not the destination" insight).
Answer key: instructor copy only (per template rule).

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "ARP finds the MAC of any destination IP anywhere" | ARP is link-local; remote destinations resolve to the *gateway's* MAC |
| "IP guarantees delivery" | Best effort by design; TCP adds reliability (L18) |
| "The MAC address travels end-to-end like the IP address" | MACs are rewritten every hop; IPs stay (pre-NAT) |
| "A host's IP identifies the machine" | It identifies an interface; routers/phones have several |
| "Checksum protects the payload" | IPv4 header checksum covers the header only |
| "Private addresses are unreachable because they're secret" | They're *routable locally*; unreachable globally by allocation (RFC 1918) |

## 9. Suggested practical demonstration
Live on VM: `ping` a neighbor → `ip neigh show` (ARP cache populated) → Wireshark filter
`arp` shows the request/reply pair; then clear the cache (`sudo ip neigh flush all`)
and repeat — the protocol made visible twice. ⚠ Pre-verify neighbor-discovery commands
and capture on the image.

## 10. Classroom activities
- **Header field lottery:** one student per field, holds a card, physically assembles
  the 20-byte header in the right order — kinesthetic and fast.
- **"Who answers?" drill:** 6 rapid scenarios (same subnet? different subnet? gateway
  down?) — students shout the ARP outcome. Builds the next-hop reflex.

## 11. Problem-solving questions
1. Sender 192.168.10.23/24 wants to reach 8.8.8.8. Whose MAC does ARP resolve? Why?
2. TTL arrives at you as 53. Minimum hops traversed? (with initial 64: ≥11)
3. Why does IPv6 delete the header checksum? (preview question — collect guesses for L15)
4. A host shows 169.254.3.77. What happened? What would you check next?
5. Attacker sends gratuitous ARP claiming the gateway's IP. What do victim caches now
   contain, and what symptom appears?

## 12. Formative assessment (with answers)
- MCQ: Protocol field 17 means → **UDP**.
- MCQ: ARP Request is sent to → **ff:ff:ff:ff:ff:ff (broadcast)**.
- MCQ: TTL is decremented → **by each router**.
- Short: why doesn't IP use MAC addresses for routing? → MACs are flat identity, not
  topological; routing needs location-structured addresses.

## 13. Exit ticket
1. The three header fields you'll check first when diagnosing: ________
2. ARP resolves the MAC of the ________ (next hop / final destination).
3. 192.168.10.23 in binary (first two octets): ________

## 14. Anticipated difficulties
- The next-hop ARP insight (GA-12 Q5) is the module's biggest conceptual hurdle; give
  it board time and a second example before moving on.
- Binary conversion speed varies wildly; assign the 10-address drill as prep (README).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify ARP capture demo on image (`ip neigh flush`, ping, filter `arp`)
- [ ] Prepare field-lottery cards (header fields, one per card)
- [ ] Print GA-12 trace excerpt; keep instructor answer key separate
- [ ] Board pre-write: header table skeleton; special-addresses table

## 16. Timing fallbacks
Drop proxy ARP and the lottery activity; the ARP walk (GA-12) and header walkthrough are
protected — both feed quizzes and the midterm.

## 17. References
- KR §4.3.1–4.3.2; RFC 791 (IPv4); RFC 826 (ARP); RFC 1918 (private addresses).
- Wireshark wiki sample captures (ARP example) for GA-12 source material.
- ⚠ VERIFY editions/sections this semester.
