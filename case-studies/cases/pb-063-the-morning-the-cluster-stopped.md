# PB-063 — The Morning the Cluster Stopped (L32, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L32 — Capstone Workshop, Presentations & Course Synthesis |
| CLOs | CLO6 (systematic multi-layer diagnosis), CLO5 (cross-layer reasoning) |
| In-class slot | Capstone clinic; 30 min, teams of 3 |
| Case type | Multi-layer synthesis · Topic: Multi-layer troubleshooting (whole-course) |
| Evidence policy | Synthetic evidence bundle, labeled; deliberately spans 4+ layers; one red-herring fact included |

---

## Student version

### Scenario (capstone synthesis exercise)
At 07:40, the analytics cluster's jobs queue but never start. You hold an evidence
bundle collected by two different people (their notes, verbatim). No single fact
explains the outage — your team must build the diagnostic *plan* and name the
two cooperating root causes.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
E1  (NetOps note) "Uplink switch Gi1/0/24 got a new 'temporary' cable patch at
    07:25 — labeled 'to printer VLAN test'. Port is up."
E2  (NetOps note) "MAC flapping alarm for 10.20.40.25's MAC at 07:26 — alternate
    Gi1/0/3 ↔ Gi1/0/24, 40 moves/min."
E3  (DS note) "Training jobs pull the dataset from file server 10.20.40.25 via
    NFS. Jobs fail with 'server unreachable' after ~30 s."
E4  (DS note) "Pings to 10.20.40.25 from the cluster work fine (~0.3 ms)."
E5  (DS note) "Cluster's ARP cache shows 10.20.40.25 → switch MAC (not the
    server's MAC) during the incident."   ← captured mid-incident
E6  (NetOps note) "Spanning-tree 'topology change' counter incremented 4× at 07:26."
E7  (App note) "The DNS server (10.20.5.53) reports high query rates for
    file01.hq-b.meridian.internal — from the cluster."   ← red herring candidate
E8  (DS note) "After 08:10 (unplugging Gi1/0/24), jobs start. A second run at
    09:00 stalls again for ~90 s, then completes."
```

### Problem statement
Sequence the causal chain from E1 to E8 (which fact causes which), identify the two
cooperating mechanisms, classify E7 as relevant or red herring *with reasoning*, and
produce the diagnostic plan a junior could follow (check order + what each check
discriminates).

### Evidence pack
The labeled bundle. Facts as listed; timestamps matter. You may assume the network
is otherwise standard (PB-016-style loop semantics; NFS over TCP).

### Constraints
- E4 "pings work" must be reconciled, not dismissed (why does ICMP succeed while
  NFS fails? — what differs at the path level).
- E8's second stall at 09:00 must fit your causal chain — a plan that explains
  07:40 but not 09:00 is incomplete.
- The plan must order checks by *information per minute* (cheap, discriminating
  checks first).

### Student questions
1. Causal chain: order E1→E8 (skip E7 for now) with one clause per link ("E2
   because E1 because…").
2. Reconcile E4 + E5 + E3: how can ping succeed while NFS fails — name the
   path-level difference (what does E5 say traffic *to* the server is hitting?).
3. E7: red herring or clue? Give the discriminating check either way.
4. Two cooperating mechanisms: name them and show how each alone would NOT have
   produced the full outage pattern.
5. Diagnostic plan: the ordered check list (what to run, what each result rules
   in/out), ending with the permanent fix + the monitoring that catches recurrence.

### Expected learning outcomes
- Build causal chains across L1/L2/L3/L7 evidence.
- Reconcile apparently contradictory observations (ping OK / app fails).
- Design ordered, discriminating diagnostic plans with permanent fixes.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "E1 is a cable. E2 is a MAC moving between ports. Ask what physically connects
   Gi1/0/24's far end to the rest of the network — PB-016's shape."
2. "E5 is the key: during the incident, 'the server's MAC' was the *switch's* MAC
   from the cluster's view. Where does a frame go when its destination MAC belongs
   to a switch?"

### Solution
1. Chain: E1 (patch creates a physical loop: the "printer VLAN test" cable's far
   end joins the same VLAN) → E2 (loop causes MAC flapping for the server's MAC
   — the server's frames circulate and arrive on both ports; PB-016 mechanism) →
   E6 (STP topology changes — either STP reconverging as the loop oscillates, or
   BPDU guard flapping the port; 4× consistent with intermittent loop) → E5
   (during flap windows, the cluster's ARP cache records the *switch's* MAC —
   proxy/redirect artifacts or the server's frames being answered by an
   intermediate device; most consistent: the loop briefly lets another path answer
   ARP, or the cache entry was overwritten by a spoofed-looking reply from the
   loop path) → E3 (NFS, long-lived TCP connections, break during the storm —
   retransmissions exhaust; jobs abort at 30 s) → E1 unplugged (08:10) → recovery;
   E8 second stall: the patch was *re-plugged* (or a second cable from the same
   bench) — flapping recurs ~90 s until STP stabilizes/blocks the loop port; the
   stall-then-complete pattern = transient loop again.
2. ICMP (single small packets, retried by ping) gets through in the gaps between
   flap windows; NFS/TCP *connections* (long-lived, sequence-continuous) die when
   the storm hits mid-connection — and E5 shows some traffic was being delivered
   to a switch MAC (never reaching the server). Resolution: partial reachability —
   "up" and "usable" are different properties during an L2 storm.
3. E7: **red herring** for the root cause (high DNS queries are a *consequence* —
   cluster jobs retry name resolution while NFS is down; DNS is healthy). The
   discriminating check: resolve file01 from a healthy host during the incident
   (works ⇒ DNS fine); or check DNS server CPU/logs (queries answered correctly
   ⇒ symptom, not cause). But note the *second-order* value: E7's query-rate spike
   timestamps the outage window precisely — red herrings still carry data.
4. Mechanism 1: the physical loop (E1/E2) — alone it causes broadcast storms and
   MAC flap alarms, but with STP *working correctly* it would be blocked in ≤ a
   few seconds, and long-lived NFS *might* survive a brief blip. Mechanism 2:
   whatever kept the loop oscillating instead of being stably blocked — e.g.,
   STP-mode mismatch on the patched port (portfast/BPDU-filter edge settings on
   an access port plugged into another switch ⚠ the classic misconfig), which
   delays blocking and lets the loop breathe for ~90 s windows. Alone (no loop)
   the misconfig is harmless. Together: recurring storm windows that kill
   long-lived connections while short pings survive. (Accept alternative
   mechanism-2 candidates with mechanisms: e.g., flap-prone link partner.)
5. Plan (cheap/discriminating first): (1) read port Gi1/0/24 config + far-end
   (what's plugged in? — 1 min, answers E1); (2) check CAM table for the server
   MAC flapping *now* (E2 live vs historical); (3) capture ARP on the cluster:
   who answers for 10.20.40.25, and does the answer MAC match the server's NIC?
   (discriminates E5 artifact vs real conflict); (4) STP state for the VLAN
   (root, blocked ports, topology-change rate) + the patched port's STP mode
   (mechanism 2); (5) only then: packet capture on the server's span port during
   a reproduction. Permanent fix: unpatch the loop + correct the edge-port STP
   config (BPDU guard on student/access ports); monitoring: MAC-flap alarm
   thresholds with paging (E2 was logged but nobody was paged), and a synthetic
   NFS connectivity probe from the cluster subnet (PB-056's presence-based
   pattern — the outage was invisible to value-based dashboards).

### Reasoning process
Method: facts → physical-layer hypothesis (cable) → L2 mechanics (loop/flap/STP) →
L3 artifacts (ARP confusion) → L7 symptoms (NFS/DNS); reconcile contradictions via
path-level differences (connection longevity, timing windows); red-herring
classification by mechanism test; plan ordered by information density; permanent
fix + monitoring for recurrence. The capstone's synthesis: every layer's tools from
L05–L29 appear once.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "DNS is the problem" (chasing E7 first) | Healthy-name answers + query spikes as consequence; also fails to explain E2's flapping |
| "The server is overloaded" | E1/E2/E6 are upstream of the server; load doesn't move MACs between ports |
| "Just ping more to prove the network is fine" | Ping's success is a *clue* (gap-timing), not a verdict; connection longevity is the discriminating property |
| Fix E8 by waiting | The 09:00 recurrence proves the cause is *configuration/physical*, not transient load |

### Extension question
Write the one-paragraph incident report a junior could send to management: what
happened, customer impact, root cause (two mechanisms), permanent fix, and the
monitoring gap that let it recur at 09:00. (Practices E8's "communicate findings"
objective: impact = analytics jobs delayed ~30 min across two windows; causes =
unauthorized patch creating an L2 loop + edge-port STP misconfig delaying
convergence; fix = patch removal + BPDU guard; gap = flap alarms unpaged, no
NFS-synthetic probe.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Causal chain complete incl. E8; E4 contradiction resolved via path properties; E7 classified with mechanism; ordered plan with discriminating checks + monitoring |
| 3 Proficient | Chain and plan right; E8 or E4 reconciliation thin |
| 2 Developing | Single-mechanism story; chases E7 |
| 1 Beginning | Reboots everything |

### References
- Course case bank: PB-016 (loop/flap), PB-024 (ARP semantics), PB-029/030
  (reachability nuance), PB-056 (monitoring gap), PB-057 (events vs polls)
- PD chapters 4–6 (L2/L3 mechanics) ⚠ verify section mapping
