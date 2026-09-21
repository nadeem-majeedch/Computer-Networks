# PB-053 — "I Opened the Port!" (L27, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L27 — Cloud & Virtual Networking |
| CLOs | CLO2 (layered policy), CLO6 (diagnose multi-gate paths) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: Cloud and data center networking |
| Evidence policy | Synthetic console/config evidence, labeled; every symptom maps to one named gate |

---

## Student version

### Scenario
A student provisions a Jupyter server in a cloud VPC and opens port 8888 in the
cloud console. The server is reachable by SSH (22) but the notebook port times out
— from their laptop *and* from a co-located VM in the same VPC.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Cloud security group (inbound):  allow tcp/22 from 0.0.0.0/0
                                 allow tcp/8888 from 0.0.0.0/0   ← added at 10:02
Host (Ubuntu VM):
  ufw status:  active
               allow OpenSSH
               (no 8888 rule)
jupyter:       listening on 0.0.0.0:8888 (ss -tlnp confirms)
Same-VPC test VM → 8888: timeout
Internet laptop → 8888:  timeout
SSH from both:           works
```

### Problem statement
Name every gate a SYN to port 8888 must pass, identify the failing one from the
evidence, and explain the security-group-vs-host-firewall division of labor (what
each layer is *for*).

### Evidence pack
The labeled synthetic console/config evidence. Facts: cloud layer allows 8888; the
host's ufw allows only SSH; Jupyter listens on all interfaces. Everything else
follows.

### Constraints
- Trace the SYN gate-by-gate; the failing gate must be named with its evidence.
- The "division of labor" answer must say why *both* layers exist (defense-in-depth),
  not which to delete.

### Student questions
1. List the gates, in order, for an inbound SYN to 8888 (cloud layer, instance
   layer, service layer).
2. Which gate fails, and what specific line proves it?
3. Why does SSH work while 8888 fails, when both are "allowed in the cloud"?
4. Fix + the design question: after it works, *should* 8888 be open to 0.0.0.0/0?
   What's the better cloud-layer shape?

### Expected learning outcomes
- Enumerate the policy layers on a cloud VM's inbound path.
- Diagnose which layer fails from layered evidence.
- Argue the defense-in-depth division of labor between cloud and host firewalls.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The packet passes two policy checkpoints before Jupyter ever sees it. You've
   verified the first one. Who verifies the second?"
2. "SSH works because *both* layers allow it. Port 8888 is allowed by exactly one."

### Solution
1. Gates: (1) cloud security group / VPC firewall (stateful, instance-attached);
   (2) host firewall (ufw/iptables on the VM); (3) the service itself — listening
   socket bound to the right address (`0.0.0.0:8888` ✓, verified via `ss`). Plus
   (0) routing/subnet reachability — same-VPC timeout rules out route issues shared
   with SSH.
2. Gate 2 — the host firewall: `ufw status` shows only OpenSSH allowed; 8888 has no
   host-level rule. The cloud layer's 10:02 allow is necessary but insufficient.
3. SSH passes both gates (cloud ✓ + ufw's OpenSSH rule ✓); 8888 passes the cloud
   gate and dies at ufw's default-deny. "Opened the port" happened at one layer of
   two.
4. Fix: `ufw allow 8888/tcp` (or bind Jupyter to localhost + tunnel via SSH — the
   security-preferable variant; note it changes the workflow). Design question: no —
   notebook endpoints on 0.0.0.0/0 are a standing risk (auth tokens leak in logs,
   brute-force surface); better: cloud-layer allow scoped to the campus/VPN CIDR
   (or SSH-tunnel-only, cloud port closed entirely). Division of labor: cloud SG =
   fleet-level coarse boundary (fast, centralized, stateful); host firewall =
   per-instance fine policy that survives SG mistakes and protects lateral moves —
   defense-in-depth, both maintained.

### Reasoning process
Facts: SG allows 8888; ufw denies it; listener healthy; SSH (double-allowed) works.
Model: inbound path = ordered gates; a flow needs *all* gates to pass. Evidence
localizes the failing gate. Fix at the failing gate; harden the design question at
the scope level.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Recreate the VM" | Same two gates, same outcome; nothing about the instance is broken |
| "Disable ufw permanently" | Restores 8888 by deleting a layer — the anti-pattern this case teaches against |
| "Open 8888 in the *host* to 0.0.0.0/0 too" | Works, but compounds the exposure; scope both layers instead |
| "It's the security group" | The evidence shows the SG *was* updated at 10:02 and SSH (same SG) works — wrong gate |

### Extension question
A teammate says "host firewalls are redundant in the cloud — the SG is enough."
Give one concrete incident class the host firewall catches that the SG cannot, and
one the SG catches that the host cannot. (Host catches: lateral movement *between*
instances where the SG was scoped by tag/VPC but the *instance* is compromised, or
config drift when someone widens the SG fleet-wide — ufw still refuses. SG catches:
traffic the host firewall trusts by source IP but that arrives *spoofed/forwarded*
from inside the VPC? — careful, both can fail; the clean SG-only win: SGs apply
even when the OS firewall is off/flooded/misconfigured during boot, and they
protect the host *before* ufw loads.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Gates enumerated in order; failing gate named with the proving line; division-of-labor argued both directions; hardened scope suggestion |
| 3 Proficient | Correct failing gate; division-of-labor one-sided |
| 2 Developing | Blames the cloud layer despite SSH evidence |
| 1 Beginning | Reboots the VM |

### References
- PD §8.4 (firewalls: stateful inspection concept) ⚠ verify section mapping
- Kurose & Ross §8.9 (firewalls); cloud provider SG/NSG docs are vendor-specific ⚠
