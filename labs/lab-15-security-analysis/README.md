# LAB-15 — Security Analysis, Safely (optional, recognition-only)

| Field | Value |
|---|---|
| Anchor lectures | L24 (crypto/TLS), L25 (defenses), L26 (attack & defense workshop) |
| CLOs | CLO7 (threats/defenses) |
| Assessment | **Optional — recognition only, zero course weight** (see [`../syllabus-safety.md`](../syllabus-safety.md) §2) |
| Mode / duration | Pairs; 2-h session |
| Environment | Course namespaces only (every technique against course-owned targets you and your pair created); offline captures provided |

## Ethics gate (this lab enforces it)
Everything here runs **inside your own pair's namespaces**. No campus network, no other
pair's lab net, no external systems — the techniques are the same shapes as real attacks,
which is exactly why the boundary is absolute (syllabus-safety §3.2). Violations are a
conduct matter, not a lab mistake.

## Learning outcomes
1. Emulate a benign port-scan *pattern* against your own target namespace and read its
   footprint on the wire (SYN packets, no payload) — then detect it from the defender's side.
2. Demonstrate ARP spoofing in a contained 3-namespace topology you own, observe the
   man-in-the-middle effect on *unencrypted* traffic, and implement the defense (static
   neighbor entries / DAI-style validation) — then articulate why HTTPS limits the damage.
3. Analyze provided offline captures for scan/recon patterns (no attack execution at all)
   and write detection rules (thresholds) that would catch them.
4. Explain the defender's economics: which defense stops which technique, at what cost.

## Pre-lab
1. What does a TCP SYN scan send, and what does a closed vs open port answer?
2. ARP spoofing: which packet lies, and what entry does the victim cache?
3. Why does TLS turn a MITM from "total compromise" into "metadata observation"?

## Tasks

### T1 — The attacker's view, contained (20 min)
Your pair builds: `attacker ns` + `victim ns` + `switch ns` (a plain bridge). A tiny HTTP
server on the victim (two ports open, two closed — scaffold provided).
Scan it with a *course Python scanner* (scaffold: connect-ex pattern, sequential, slow) —
**not** external tooling, to keep the shape visible.
**Expected observation (attacker side):** open ports complete the handshake (SYN/ACK),
closed answer RST, filtered time out. Record the three patterns.

### T2 — The defender's view (20 min)
On the "switch", capture during the scan: identify the scan's footprint (many SYNs to
sequential ports from one MAC, no payload). Write a detection rule in words + a threshold
(e.g., > N distinct dst ports in T seconds from one source) and test it: does it fire?
What false-positive could it have? (Hint: a busy NAT gateway.)

### T3 — ARP spoofing, contained (25 min)
Same topology + a `gateway ns`. The "spoofer" ns sends gratuitous ARP replies claiming the
gateway's IP with its own MAC (course scaffold — 4 lines of Python). From the victim,
fetch the attacker-controlled plain-HTTP page served by the spoofer; observe the MITM.
Then: enable the defense (static `ip neigh` entries or bridge `vlan`/arp validation in the
switch ns) and show the spoof fail.
**Expected observation:** before defense, victim's `ip neigh` maps gateway IP → spoofer
MAC; traffic flows through the spoofer. After defense: unchanged MAC, no MITM.

### T4 — Why HTTPS changes the story (15 min)
From your T3 capture: with plain HTTP the spoofer sees everything; with the course-provided
TLS capture of the same fetch (`lab15-tls-mitm.pcapng`, offline), the spoofer sees only
SNI/IPs/sizes and the certificate validation *fails* for a fake cert. Two paragraphs:
what TLS protects, what it cannot (metadata, endpoint compromise).

### T5 — Detection engineering, offline (15 min)
`lab15-scan.pcapng` (a real capture of the scaffold's scan): write two detection rules
(threshold-based) and evaluate them against the capture + a normal-traffic capture
(`lab15-normal.pcapng`): true positives, false positives. Defender's economics table.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Scan finds nothing | victim server not running / wrong IP | verify with a normal request first |
| ARP spoof "doesn't work" | victim's static entry already set (defense on!) | that *is* the defense working — remove it to see the attack, then re-enable |
| Detection never fires | threshold too high for the scaffold's slow scan | lower N/T; compute from the capture's actual rate |
| Pair next door "sees" your scan | shared bridge you didn't create | teardown + rebuild your pair's namespaces; report it |

## Post-lab questions
1. Which of your two detection rules has the worse false-positive profile, and why?
2. The MITM defense you enabled: what does it *not* stop (name a technique beyond this lab)?
3. In T4's TLS capture: exactly what data did the "attacker" still collect, and why is that
   unavoidable at L3/L4?
4. Defender's economics: your cheapest effective defense across the lab, with its cost.

## Challenge (ungraded)
IPv6 neighbor-discovery spoofing: repeat T3's shape with NS/NA (`ip -6 neigh`), and state
which defense transfers and which must be relearned.

## Accessibility / low-resource alternatives
- Fully offline route: all captures provided (`lab15-scan.pcapng`, `lab15-normal.pcapng`,
  `lab15-tls-mitm.pcapng`) + transcript of the contained demos; T1–T4 become analysis;
  T5 unchanged. Same recognition.
- Screen-reader friendly: all text tools.

## Safety notes
This lab is the syllabus-safety §3.2 case study: every technique is bounded by the
topology you built, and nothing leaves it. The instructor verifies topologies before T3.
