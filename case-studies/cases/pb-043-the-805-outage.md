# PB-043 — Every Morning at 08:05 (L22, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L22 — DHCP Deep Dive, BOOTP & Address Management |
| CLOs | CLO2 (lease lifecycle: T1/T2), CLO6 (diagnose from timing pattern) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: DNS/DHCP |
| Evidence policy | Synthetic logs, labeled; renewal semantics per DHCP standard (T1 = 50%, T2 = 87.5%) |

---

## Student version

### Scenario
Half the analytics office loses connectivity for ~90 seconds every workday at about
08:05. Weekends are fine. The help desk has "solved" it three times by rebooting
switches; it returns the next morning.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
DHCP scope: lease time 2 hours; clients boot ~06:00 (sync job wakes the NICs)
DHCP server: nightly backup window 08:03–08:07 (service stopped, not just paused)
Client logs (one laptop):
  06:00:02  DHCP ACK (lease: 06:00 → 08:00, T1 renewal at 07:00)
  07:00:01  DHCPREQUEST (unicast renewal) → ACK; lease extended to 09:00
  08:05:xx  DHCPREQUEST (unicast renewal) → no reply (server down)
            → 08:05:xx +4 s: DHCPDISCOVER (broadcast) → no reply
            → fallback at 87.5% of lease: rebinding broadcast
  08:06:40  connectivity resumes (server back at 08:07? — logs show ACK at 08:06:58)
Symptom map: only machines whose renewal lands in the 4-min window drop; ~half the
             office renewed near 08:03–08:07 (they booted in a batch at 06:00)
```

### Problem statement
Explain the outage using the lease lifecycle (T1 renewal, T2 rebinding), reconcile the
~90-second symptom with the 4-minute window, and give the two infrastructure fixes
(either sufficient alone).

### Evidence pack
The labeled synthetic logs. Facts: 2-h leases, batch boot at 06:00, server stopped
08:03–08:07, T1 = 50% of lease. The 90-second reconciliation is the puzzle.

### Constraints
- Explain why *unicast* renewal fails to the stopped server, and what the client's
  fallback ladder is.
- Both fixes must be named; state what each does NOT fix.

### Student questions
1. Walk the lease lifecycle for this laptop: grant, T1 renewal, T2 rebinding — with
   this lease's actual times.
2. Why did the 08:05 renewal fail *silently* at first (unicast), and what did the
   client do next?
3. Reconcile: the server was down ~4 minutes, but users noticed ~90 seconds. What
   fills the gap? (Hint: when does the client *notice*, and what do the broadcast
   retries cost?)
4. Fixes: (a) server-side, (b) design-side. What does each not fix?

### Expected learning outcomes
- Recite and apply the lease lifecycle (grant → T1 → T2 → expiry).
- Trace client fallback behavior when renewal fails.
- Separate root causes (server maintenance vs lease design) and fix accordingly.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A 2-hour lease renews at its halfway point. When is 50% of 06:00→08:00?"
2. "Unicast renewal talks to *one* server. Broadcast rebinding asks *anyone*. Where
   does the client sit between those two attempts?"

### Solution
1. Grant 06:00→08:00; T1 renewal at 07:00 (50%) — succeeded, extending to 09:00;
   next T1 would be 08:00 (50% of the extended lease)... note the log shows renewal
   traffic at 08:05: consistent with an *earlier* boot cohort whose extended lease
   put T1 in the window — the exact per-machine timing varies; the teaching point is
   the ladder, not the minute (flag the cohort nuance).
2. Renewal is unicast to the *granting* server; stopped server = no reply, silently.
   The client keeps trying unicast, then at T2 (87.5% of lease) switches to broadcast
   DISCOVER/REQUEST — asking any server. Broadcast retries are rate-limited and
   randomized, adding seconds to minutes.
3. The 4-minute window is server downtime; user-visible outage = time from *failed
   renewal* to a successful broadcast response (or to when the client gives up on
   renewing and keeps the address until actual expiry — clients stay connected while
   the lease is valid!). The ~90 s gap = retry ladder + the subset of clients whose
   lease was *near* expiry (rebinding or freshly expired) rather than merely renewing.
   Clients far from expiry never noticed. So "half the office" = the renewal-cohort,
   and "~90 s" = the unlucky subset's retry interval — both follow from the ladder.
4. (a) Server-side: move the backup window, or (better) run DHCP as a redundant
   pair (failover peers share leases ⚠ protocol support varies) — maintenance no
   longer stops the service. Does not fix: a poorly-sized lease policy that batches
   renewals (sync-job boot cohorts) — the herd remains, just harmless. (b)
   Design-side: lengthen leases (e.g., 8 h+) and stagger reservations, so renewals
   spread out and tolerate a short maintenance window entirely. Does not fix: a
   genuinely dead DHCP server beyond the T2 horizon (clients eventually expire and
   drop — redundancy still needed for true outages).

### Reasoning process
Facts: lease 2 h, batch boots, 4-min maintenance, cohort-level symptom. Model:
renewal ladder (unicast T1 → broadcast T2 → expiry) + cohort timing. Diagnose the
*intersection* of maintenance window and renewal cohort; two complementary fixes at
different layers.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| Reboot switches (help desk's fix) | No L1/L2 involvement; the pattern returns by design the next morning |
| "Make leases 5 minutes so renewals are quick" | Multiplies renewal traffic and failure frequency; backwards |
| "Set static IPs everywhere" | Treats the symptom; loses central address management; next dynamic need re-breaks |
| "Just always run the backup at night" | Fine, but the design-side fix is still worth taking — the herd is one window-change away from recurrence |

### Extension question
One laptop shows a lease that *did* expire during a longer outage, and it kept its
address but stopped passing traffic. Explain that behavior (why "keep the address but
stop using it"?). (A client must stop using an expired lease — the address may be
reassigned to another host; keeping it risks conflict. Some stacks mark the address
deprecated/duplicate-detect before reuse ⚠ per implementation — the visible symptom
is "connected but dead", matching the log.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Ladder with real times; cohort reconciliation (4-min window → 90-s symptom); both fixes with honest non-coverage |
| 3 Proficient | Ladder correct; symptom reconciliation partial |
| 2 Developing | "DHCP was down" without lifecycle mechanics |
| 1 Beginning | Buys a new switch |

### References
- RFC 2131 (lease lifecycle: T1/T2 timers) ⚠ verify sections
- PD §5.4 (DHCP) ⚠ verify section mapping; Kurose & Ross §4.4.1 (DHCP)
