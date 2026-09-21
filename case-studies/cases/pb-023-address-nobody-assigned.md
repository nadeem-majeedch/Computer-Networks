# PB-023 — The Address Nobody Assigned (L12, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L12 — IP Fundamentals & ARP |
| CLOs | CLO2 (special addresses; L2 vs L3 reachability) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: IP addressing |
| Evidence policy | Synthetic outputs, labeled; APIPA behavior per RFC 3927 framing |

---

## Student version

### Scenario
A student's laptop joins the analytics Wi-Fi and "connects" — but only local things
work. Classmates on the same SSID are fine. The student runs two commands:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
ip config summary:
  IPv4 address:      169.254.137.44/16   (self-assigned)
  Default gateway:   (blank)
ping tests:
  ping 169.254.137.1 → replies                  (another laptop with same problem)
  ping 10.20.30.1    → "Destination host unreachable" from own address
```

### Problem statement
Explain what the 169.254 address means, why the laptop can reach one host but not the
gateway, and what single infrastructure component most likely failed.

### Evidence pack
The labeled synthetic outputs. Fact: the address block 169.254.0.0/16 is link-local
self-assigned (no DHCP). Everything else follows from the L2/L3 model.

### Constraints
- Explain why 169.254↔169.254 works while 169.254→10.20.30.1 cannot.
- One most-likely component; justify against the "classmates are fine" datapoint.

### Student questions
1. What is the 169.254.0.0/16 block for, and who assigned this address?
2. Why did ping 169.254.137.1 succeed? Which layer did all the work?
3. Why can the laptop not reach 10.20.30.1 — give the mechanical reason (hint: what
   does the host do with a packet for a foreign network?).
4. Name the most likely failed component and the one-line check that confirms it.

### Expected learning outcomes
- Recognize link-local self-assigned addressing and its implications.
- Distinguish on-link delivery (ARP + L2) from off-link delivery (gateway dependency).
- Localize an addressing failure to DHCP vs radio vs switch.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Nobody assigned that address — the OS picked it alone. What condition triggers
   that?"
2. "Off-link delivery needs a *router*. What does a blank gateway field mean for any
   packet leaving 169.254.0.0/16?"

### Solution
1. 169.254.0.0/16 is the IPv4 link-local block: when DHCP fails, the host self-assigns
   a random address from the block (per the link-local addressing rules, with
   duplicate detection). No DHCP server responded to this laptop.
2. The other laptop self-assigned in the same block; delivery stayed *on-link*: ARP for
   169.254.137.1, then a direct L2 exchange. The network (radio, switch) is fine at L2
   — the address plan just bypasses the router entirely.
3. 10.20.30.1 is outside 169.254.0.0/16, so the host must hand the packet to a default
   gateway — but the gateway field is blank. With no route, the IP layer discards the
   packet and reports "Destination host unreachable" locally; nothing ever leaves for
   the gateway. (The unreachable message comes from the *own host*, a key detail.)
4. Most likely: the DHCP service/lease process for this laptop failed (server up but
   out of leases, relay misconfig, or a per-client filter). Check: does the laptop get
   an offer at all? (`ipconfig /renew` or packet capture of UDP 67/68 — a capture
   showing DISCOVER with no OFFER vs OFFER-without-ACK splits the diagnosis cleanly.)
   "Classmates are fine" points to *this client's* DHCP interaction, not the server
   being wholly down.

### Reasoning process
Facts: self-assigned address, blank gateway, one on-link ping works, off-link fails.
Model: on-link = ARP+L2 (works); off-link = gateway-dependent (impossible without
route). Cause selection constrained by "classmates fine" → client-specific DHCP
interaction.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "169.254 means the network is down" | L2 demonstrably works (the other laptop replied) |
| "Ping the gateway harder" | There is no gateway configured — no amount of pinging helps |
| "Set a static IP and move on" | Masks the DHCP failure; acceptable as a workaround, but the diagnosis must state the root cause |
| Blaming the Wi-Fi | Association works; the failure is above L2 |

### Extension question
The student sets a static IP in 10.20.30.0/24 and everything works — until next week
when a *different* laptop shows the same 169.254 symptom. What does the recurrence
pattern tell you about your earlier hypothesis, and what evidence would distinguish
"out of leases" from "relay misconfig"? (Recurrence on a different client shifts
suspicion from client to server/relay. Evidence: lease-pool utilization on the server
vs DHCP DISCOVER arriving at the server (relay forwards?) — capture/relay logs split
it.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Link-local semantics + on-link/off-link split precise; unreachable-source detail noticed; component localized with a discriminating check |
| 3 Proficient | Correct block meaning and cause; mechanism of failure partly vague |
| 2 Developing | "Bad IP address" without block semantics |
| 1 Beginning | Reinstalls network drivers |

### References
- RFC 3927 (Dynamic Configuration of IPv4 Link-Local Addresses) — 169.254.0.0/16 semantics
- Kurose & Ross §4.4 (IPv4 addressing; DHCP subsection) ⚠ verify section number per edition
