# PB-027 — Two Servers Answer the Door (L14, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L14 — IP Addressing at Scale: DHCP & NAT |
| CLOs | CLO2 (DORA exchange), CLO6 (read a capture summary) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual (packet level) · Topic: DNS/DHCP |
| Evidence policy | Synthetic capture summary, labeled; message semantics per DHCP (RFC 2131) |

---

## Student version

### Scenario
After a lab reshuffle, new laptops in the analytics VLAN get *valid* addresses but the
wrong default gateway (192.168.1.1 — an old firewall) and can't reach the intranet.
An old lab firewall was never decommissioned. A student captures the handshake:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (capture summary, illustrative values):**

```
Capture (analytics VLAN, UDP 67/68):
  DISCOVER (0.0.0.0 → 255.255.255.255)            broadcast
  OFFER     from 10.20.30.5 (new DHCP server):    yiaddr 10.20.30.87,
            option 3 (gateway) 10.20.30.1, option 6 (DNS) 10.20.30.5
  OFFER     from 192.168.1.1 (old firewall):      yiaddr 10.20.30.99,
            option 3 (gateway) 192.168.1.1, option 6 (DNS) 192.168.1.1
  REQUEST   → 255.255.255.255, server-id 192.168.1.1    ← the laptop's choice
  ACK       from 192.168.1.1: yiaddr 10.20.30.99, gw 192.168.1.1
```

### Problem statement
Walk through the DORA exchange as captured, explain how the laptop ended up with the
wrong gateway despite an authoritative server offering the right one, and give the
infrastructure fix.

### Evidence pack
The labeled synthetic capture summary. Fact: the laptop's REQUEST names the server it
accepts (server-id option). Everything else follows from DHCP semantics.

### Constraints
- One mechanism for the wrong choice (no "the laptop is broken").
- The fix must stop recurrence, not just repair one laptop.

### Student questions
1. Name each DORA message's role and who broadcasts vs unicasts it here.
2. Which single field in REQUEST records the laptop's decision, and what did this
   laptop choose?
3. Explain why the *presence* of a good OFFER didn't help. What does the client
   optimize for in multi-OFFER cases (per the standard)?
4. Give the fix (and the quick test that proves it worked).

### Expected learning outcomes
- Narrate the DORA exchange at packet level.
- Explain multi-server DHCP selection (first acceptable offer wins; no authority).
- Convert a rogue-server incident into an infrastructure control.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "DISCOVER asks everyone. Two servers answered. Who *decides* between OFFERs?"
2. "The REQUEST carries a server-id. Whose? The laptop doesn't know which server is
   'right' — it isn't told."

### Solution
1. DISCOVER: client broadcast (no address yet, 0.0.0.0→255.255.255.255). OFFERs: each
   server unicasts (or broadcasts ⚠ per implementation) an offer. REQUEST: client
   broadcast (so the *losing* server also hears it withdraws). ACK: chosen server
   confirms the lease.
2. The **server identifier (option 54)** in REQUEST: here 192.168.1.1 — the old
   firewall.
3. DHCP has no "authoritative vs rogue" concept on the wire: the client accepts the
   first *acceptable* OFFER (per RFC 2131's "collects... chooses one"). Both offers
   were syntactically fine; the laptop had no way to prefer 10.20.30.5. Its ACK
   delivered yiaddr 10.20.30.99 with gw 192.168.1.1 — valid address, dead path to the
   intranet.
4. Fixes: decommission the old firewall's DHCP scope (root cause); make recurrence
   impossible/loud — DHCP snooping on switches (only 10.20.30.5 trusted on port X ⚠
   switch feature) or at minimum an alert on OFFERs from non-authorized IPs. Test:
   release/renew on a fresh laptop → capture shows one OFFER, gw 10.20.30.1; intranet
   reachable.

### Reasoning process
Facts: two OFFERs, REQUEST server-id = rogue, ACK from rogue. Model: client-side
selection among acceptable offers; no trust ranking on the wire. Root cause: rogue
server present; durable fix: remove + snooping/policy.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Set the gateway statically on laptops" | Per-host workaround; every new laptop reinherits the rogue ACK |
| "Make the good server authoritative" | DHCPv4 has no authority flag (that's a DHCPv6 concept ⚠); the wire decides nothing |
| "Block MAC of the laptop" | The laptop is a victim, not a cause |
| Renew and hope | The rogue still answers first sometimes; nondeterministic |

### Extension question
The rogue firewall is removed, but a *second* authorized DHCP server is intentionally
added for redundancy. What must be true about the two servers' scopes for this to work
safely (and what failure mode appears if operators ignore it)? (Disjoint scopes or
split-scope/MAC-based partitioning; if both serve the same pool independently, lease
conflicts/duplicate offers for the same addresses — duplicate-address churn.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Full DORA narration; server-id role precise; no-authority insight; infrastructure-grade fix |
| 3 Proficient | Correct flow and cause; fix is per-host only |
| 2 Developing | "Wrong server answered" without selection mechanics |
| 1 Beginning | Reimages the laptop |

### References
- RFC 2131 (DHCP: client selection among offers, message roles)
- PD §5.4 (DHCP) ⚠ verify section mapping; Kurose & Ross §4.4.1 (DHCP)
