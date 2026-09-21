# PB-005 — Sixty Seconds of Frustration (L03, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L03 — Applications, Sockets & the Packet's Journey |
| CLOs | CLO1, CLO2 (trace a request through the stack) |
| In-class slot | Opening hook; 10 min, pairs |
| Case type | Conceptual (symptom decomposition) · Topic: Network fundamentals |
| Evidence policy | Synthetic symptoms, labeled; decomposition consistent with L03's stage model |

---

## Student version

### Scenario
An analyst clicks "Open dashboard" and watches a spinner for 60 seconds before a
timeout. The dashboard's web server is known-good (other users are fine right now). Her
teammate opens the same URL successfully on the same desk.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
E1  Another app on her machine reaches the internet normally.
E2  `ping dashboard.meridian.local` → "could not resolve host"  (her machine)
E3  Same command, teammate's machine → replies in 2 ms.
E4  She can ping the dashboard server by IP: 10.20.5.30.
```

### Problem statement
Decompose the 60-second failure into **stages of the packet's journey** (application →
naming → transport → network → link), state which stage is failing, and propose the
single most likely broken component.

### Evidence pack
The four labeled synthetic observations. Everything else is assumption until checked.

### Constraints
- Name a stage per evidence item; no fixes yet, only localization.
- Use evidence E1–E4; you may not invent extra test results.

### Student questions
1. Which journey stage does E2 point to?
2. Using E3 + E4 together, what can you already rule out? Be precise.
3. Give the most likely single component that is broken, and one cheap test to confirm.
4. Why did the failure take ~60 s rather than failing instantly? Relate to what the
   application was waiting on.

### Expected learning outcomes
- Map symptoms to stages of an end-to-end packet journey.
- Combine positive and negative evidence to rule out layers.
- Connect timeout duration to the stage that stalled (name resolution wait).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "E1 says her machine's networking is broadly fine — so the failure is specific. To
   what?"
2. "E4 is a packet that *did* make the whole round trip. What does that prove about
   path, and not prove about names?"

### Solution
1. E2 → the **naming** stage (DNS/name resolution) fails on her machine.
2. E4 proves the L2–L4 path from her machine to 10.20.5.30 works (an ICMP round trip).
   It does **not** prove name resolution works, nor that TCP/HTTP to the service works.
   E3 shows name resolution works for *other* hosts/users — so the fault is local to her
   resolver configuration, not the DNS server.
3. Most likely: her machine's resolver configuration (e.g., wrong or stale DNS suffix /
   static DNS entry for `.local`). Cheap test: compare `resolv.conf`/adapter DNS settings
   with the teammate's, or resolve by explicit server (`nslookup dashboard.meridian.local
   <dns-server-ip>`).
4. A resolver that cannot answer often waits through retries/timeouts (applications
   serialize on "get name → then connect"); 60 s is consistent with a name-lookup timeout
   pattern, whereas a refused TCP connection typically fails in milliseconds.

### Reasoning process
Facts: E1 (host generally healthy), E2 (name fails locally), E3 (naming works elsewhere),
E4 (path works by IP). Hypothesis: local resolver config. Test: replicate resolution
against a known server. Distinguish: path (proven OK) vs naming (failing).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Ping works so DNS is fine" | E4 pinged **by IP** — naming was never exercised |
| Blaming the dashboard server | Other users and E1–E3 contradict it |
| Reboot-first debugging | Localization before action; otherwise no learning |
| "The network is down" | The network carried an ICMP reply; one stage failed |

### Extension question
The analyst is also a data-science student who schedules a nightly `pandas.read_csv` from
the same dashboard host by **IP**. Why does her scheduled job succeed while the browser
fails? What design lesson about relying on names vs addresses does this contrast teach?
(Expected: IP-based jobs bypass the broken resolver; names provide indirection/mobility —
pinning addresses trades resilience for fragility.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Correct stage localization; rules out path via E4 precisely; timeout explained via resolver wait |
| 3 Proficient | Correct stage and component; misses the E4 nuance (what ping-by-IP doesn't prove) |
| 2 Developing | Uses single evidence item; overclaims from ping |
| 1 Beginning | Restarts or blames the server without decomposition |

### References
- PD §2.5 (DNS naming), §2.1 (socket API and the journey)
- Kurose & Ross §2.4 (DNS), §2.7.1 (socket programming stages)
