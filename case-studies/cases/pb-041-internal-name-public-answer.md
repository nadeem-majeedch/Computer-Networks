# PB-041 — Everyone Can Reach It Except Us (L21, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L21 — DNS: the Internet's Directory |
| CLOs | CLO2 (resolution path), CLO6 (localize with resolver tests) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: DNS/DHCP |
| Evidence policy | Synthetic resolver outputs, labeled; recursion/caching semantics per DNS standard behavior |

---

## Student version

### Scenario
The new analytics portal works from home, from phones, from the customer's office —
but not from inside Meridian's HQ LAN. Browsers there time out on the portal name
only. Everything else loads.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
From an HQ workstation:
  nslookup portal.meridian.example → 203.0.113.77      (the PUBLIC IP)
  nslookup portal.meridian.example 10.20.5.53 →
      ** server can't find portal.meridian.example: NXDOMAIN
From a home machine:
  portal.meridian.example → 203.0.113.77 → works (200 OK)
Edge router: port-forward 203.0.113.77:443 → 10.20.40.25 (portal); no hairpin/NAT
             reflection enabled (verified)
Internal DNS server 10.20.5.53: hosts internal zones (meridian.internal); the
             portal zone lives only on the public DNS provider
```

### Problem statement
Explain the two failure layers visible in the evidence (what the workstation's default
resolver says vs what the internal server says), then connect them to the timeout via
the NAT hairpin fact. Propose the standard fix and one quick client-side workaround.

### Evidence pack
The labeled synthetic outputs. Facts: default resolver returns the public IP; the
internal DNS says NXDOMAIN; hairpin NAT is off. All else is reasoning.

### Constraints
- Name the resolution path for each test (who was asked, what was cached where).
- The fix must serve *every* internal client, not one workstation.

### Student questions
1. Which resolver answered each nslookup, and what does each answer tell you about
   the zones?
2. With the public IP in hand, why does the connection still time out *from inside*?
   Trace the SYN's fate.
3. Why do home/phone users work? (What's different about their path?)
4. Fix + workaround: the infrastructure fix, and the 60-second client workaround for
   one testing machine.

### Expected learning outcomes
- Distinguish recursive-resolver answers from authoritative zone data.
- Explain NAT hairpin failure as the second layer of the fault.
- Choose a split-horizon DNS fix over per-host workarounds.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Two different servers answered. One reads a zone that exists; the other reports a
   zone that doesn't. Which is which?"
2. "The workstation *has* an address. Getting a SYN *to* the server is a separate
   journey — look at the hairpin note."

### Solution
1. Default resolver (likely the ISP/forwarder via DHCP) returned 203.0.113.77 — the
   public A record from the *public* zone. The internal server 10.20.5.53 returned
   NXDOMAIN because the portal name exists only in the public provider's zone — the
   internal server neither hosts nor forwards it (as configured).
2. Workstation → SYN to 203.0.113.77:443. Routed to the edge router, whose
   port-forward translates *inbound-from-outside* flows; a flow arriving from the
   *inside* interface destined to its own public IP requires hairpin NAT (translate
   and loop back) — disabled ⇒ the router drops/refuses the flow (vendor behavior
   varies ⚠) ⇒ client timeout. Two independent layers had to align: name→IP (worked,
   surprisingly) and IP→server (failed).
3. Home/phone clients are *outside*; their SYNs arrive at the public interface — the
   port-forward path works as designed. Their resolution also hits the public zone
   naturally.
4. Fix: split-horizon DNS — add the portal name to the internal DNS (a zone or
   override) answering 10.20.40.25 for internal clients; traffic then stays inside,
   no NAT involved. (Alternative: enable hairpin NAT ⚠ router support — but that
   routes internal traffic out-and-back through the edge, wasteful and often
   asymmetric.) Workaround: add a hosts-file entry `portal.meridian.example
   10.20.40.25` on the test machine — per-host, unmaintainable at scale; state that
   explicitly.

### Reasoning process
Facts: two resolver answers, hairpin disabled, external path works. Model: DNS
resolution and packet forwarding are separate layers; each must be diagnosed alone.
Fix at the layer that's wrong for the *fleet* (DNS view), not the layer that's
expensive to change (NAT).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "DNS is broken" | Resolution *worked* (public IP returned); the connection failed — two layers |
| "Open the firewall" | The SYN never completed translation; no port-forward change helps an inside-originated flow without hairpin |
| "Use the IP directly everywhere" | Breaks TLS name validation and mobility; a workaround masquerading as a fix |
| "Put the portal in the public zone only" | Status quo — that's the bug's shape |

### Extension question
The team instead publishes `portal.meridian.internal` internally AND
`portal.meridian.example` publicly (different names, same server). What operational
cost does this dual-name design create (TLS certificates, documentation, bookmarks)?
When is split-horizon *same-name* still the better choice? (Dual names: two certs/
SANs, two docs sets, split-brain confusion; same-name split-horizon keeps one
identity — preferable when the server serves both audiences.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both layers traced separately; hairpin fate of the SYN precise; fix at DNS layer with rationale; workaround labeled as such |
| 3 Proficient | Correct diagnosis; fix is hairpin-only without trade-off |
| 2 Developing | Conflates the two layers ("DNS and network are both broken") without separation |
| 1 Beginning | "Restart DNS" |

### References
- PD §2.5 (DNS: zones, recursion) ⚠ verify section mapping
- Kurose & Ross §2.4 (DNS); RFC 1034/1035 context
