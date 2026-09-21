# PB-036 — Handshake Fine, Transfer Frozen (L18, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L18 — TCP Essentials: Connections & Reliable Delivery |
| CLOs | CLO2 (segment/MTU interactions), CLO6 (multi-evidence diagnosis) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: Multi-layer troubleshooting (L2/L3/L4) |
| Evidence policy | Synthetic evidence, labeled; PMTUD semantics per RFC 1191/1981 framing; values internally consistent |

---

## Student version

### Scenario
After the new VPN concentrator was inserted between HQ and the analytics cluster,
"small things work, big things freeze": SSH sessions connect, tiny commands succeed,
but file copies hang at exactly 1,448 bytes of progress, then resume in dribbles.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Path: client — HQ router — VPN concentrator (encapsulates, adds overhead) — cluster
Symptoms:
  TCP handshake:          OK (SYN, SYN-ACK, ACK small)
  Interactive SSH:        OK (keystroke-sized segments)
  Bulk copy (1500 B MSS): stalls; bytes delivered per burst ≈ 1,448 then pause
  ping -s 1472 -M do → 10.20.40.25 (via VPN): no reply
  ping -s 1372 -M do → 10.20.40.25 (via VPN): replies
Client TCP:             MSS advertised 1460; PMTUD enabled; DF set on data segments
ICMP on VPN path:       "ICMP unreachable/fragmentation-needed not observed" in the
                        capture (students checked)
```

### Problem statement
Explain why the handshake survives while bulk transfer dies, compute the effective
path MTU from the ping evidence, and connect the missing ICMP message to the stall
mechanism. Give the two standard fixes and their trade-offs.

### Evidence pack
The labeled synthetic evidence. Facts: DF set; 1472+28=1500 fails, 1372+28=1400
passes; no ICMP frag-needed observed; stall quantum ≈1,448 B. Tunnel adds header
overhead (state it: typical IPsec adds tens of bytes ⚠ mode/cipher-dependent).

### Constraints
- The stall quantum 1,448 must be explained (what fits in the tunnel).
- Fixes: MSS clamping vs raising/clearing DF — one trade-off each; no "disable
  PMTUD" hand-waving.

### Student questions
1. Why does the handshake succeed while full-MSS segments die? (What differs about the
   packets?)
2. From the ping evidence, compute the effective path MTU on the tunnel path. Show
   the +28 arithmetic.
3. With PMTUD enabled but ICMP frag-needed filtered, what does the TCP sender
   *experience* when a full-MSS segment vanishes? Name the retransmission behavior
   and why the 1,448 quantum appears.
4. Fixes: (a) clamp MSS to fit the tunnel, (b) allow ICMP frag-needed end-to-end.
   One trade-off each, and state which you'd deploy first and why.

### Expected learning outcomes
- Explain MTU/PMTUD mechanics across an encapsulating hop.
- Diagnose a black-hole PMTUD path from ping/DF evidence.
- Choose between MSS clamping and ICMP repair knowingly.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "SYN packets are tiny. Bulk segments try to fill 1500 bytes. What does the tunnel
   do to the size budget?"
2. "The sender's segments carry DF. The router that can't forward them must *tell*
   someone. Did anyone get told?"

### Solution
1. Handshake/control packets are header-sized (≤ ~100 B) — far below the tunnel's
   effective MTU, so they pass. Full-MSS data segments (1500 B on the wire) become
   1500+tunnel-overhead inside the tunnel — exceeding the *underlying* link's MTU;
   with DF set, the concentrator cannot fragment, so the segment is dropped. ACKs
   (small) still flow — hence "connects, small commands work".
2. ping -s X -M do builds an IP packet of X+28 bytes (X ICMP payload + 20 IP + 8
   ICMP). 1372+28 = **1400 B passes; 1472+28 = 1500 B fails** → effective path MTU =
   1400 B (bisectable further to find the exact value; 1400 is consistent with a
   1500-B underlay minus ~100 B tunnel overhead ⚠ typical IPsec+ESP overhead range).
3. The sender retransmits the full-MSS segment repeatedly (same size, same DF) —
   each retransmission dies identically. No frag-needed ICMP arrives (filtered), so
   PMTUD never learns; TCP is stuck retransmitting into the void. The ~1,448 quantum:
   either an intermediate MSS clamp is active at ~1,448 (1500−52) for some flows, or
   the application's writes split at ~1.4 KiB and only the first (sub-MSS) chunk
   crosses before the next full-MSS segment hangs — flag the ambiguity ⚠; both are
   consistent with a black hole. The *discriminator* is the ping-DF evidence: path
   MTU ≈1400.
4. (a) MSS clamping to ~1360 (1400 − 40 TCP/IP) on the VPN/router: immediate, robust,
   but slightly reduces max throughput per segment and must be re-tuned when the
   underlay changes. (b) Permit ICMP frag-needed (type 3 code 4) through the VPN
   firewall both ways: restores correct PMTUD for *all* protocols, but security teams
   often filter ICMP wholesale; partial-ICMP policies are the root cause here.
   Deploy (a) first (unblocks now), then fix (b) and relax the clamp — clamping is a
   band-aid that shouldn't be permanent.

### Reasoning process
Facts: small packets pass, 1500-with-DF dies, MTU ≈1400 by DF ping, no frag-needed
ICMP. Model: encapsulation shrinks effective MTU; DF prevents fragmentation; filtered
ICMP blinds PMTUD; TCP retransmits identical doomed segments (black hole). Fixes act
on packet size (clamp) or on feedback (ICMP).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The VPN is dropping everything" | Handshake and small flows traverse fine |
| "TCP is broken" | TCP behaves exactly as specified when *feedback* is filtered; the fault is the ICMP policy |
| "Disable DF / enable fragmentation" | Masks the black hole; fragmentation at routers is slow, fragile, and security teams rightly object — plus DF-clearing doesn't fix the sender's own MSS choice |
| Clamp to 1300 "to be safe" | Works but wastefully small; compute the actual budget (1400−40) instead |

### Extension question
An IPv6 twin of this fault appears (no fragmentation exists in IPv6 routers at all).
What changes in the failure mode and the required ICMP policy? (In IPv6, *only* the
source fragments; routers drop oversize and must send ICMPv6 Packet Too Big —
filtering ICMPv6 type 2 breaks PMTUD *by design*; "permit essential ICMPv6" is
mandatory, not optional.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Size-budget mechanism; MTU computed with +28 arithmetic; black-hole retransmission loop; both fixes with trade-offs + deployment order |
| 3 Proficient | Correct diagnosis and MTU; fixes lack trade-offs |
| 2 Developing | "MTU mismatch" named; ICMP-blinding mechanism absent |
| 1 Beginning | "Restart the VPN" |

### References
- RFC 1191 (IPv4 PMTUD), RFC 1981 (IPv6 PMTUD) — behavior framing
- PD §5.3 context (segment size, MSS) ⚠ verify section mapping
