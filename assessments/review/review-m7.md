# Module 7 Review Questions (L27–L29)

| Field | Value |
|---|---|
| Coverage | L27 cloud & virtual networking · L28 SDN & programmable networks · L29 monitoring & troubleshooting |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · LAB-14 · GA-27/28 · Cases PB-053…PB-058 |

## Questions

### L27 — Cloud & virtual networking
1. [B|CLO6] Name the three virtual components on a container host: namespace, veth,
   bridge — and each one's job in one line.
2. [I|CLO6] Overlay MTU: an underlay supports 1500; an overlay adds 50 B of headers.
   What inner MTU must tenants use, and what symptom appears if they don't?
3. [I|CLO6] Ingress rule "allow 443/tcp" vs egress "allow 443/tcp": why do both exist
   for a public web server's *return* traffic? (Stateful security groups explanation.)
4. [I|CLO6] VPC peering vs public-internet path between two cloud subnets: one security
   and one performance property each.

### L28 — SDN & programmable networks
5. [B|CLO6] Define the three planes and where they live in a traditional switch.
6. [I|CLO6] An SDN controller wants H1→H2 through switches S1→S2. Write the two
   match/action rules (words) and state who computes the path.
7. [I|CLO6] Why can an SDN outage freeze *changes* but not *existing* flows? What does
   that imply for the failure's blast radius?
8. [I|CLO6] Give one case where per-switch autonomous control (traditional) beats
   centralized control, and one where centralization wins. Justify each.

### L29 — Monitoring & troubleshooting
9. [B|CLO4] Name two continuous metrics and two *event* records a monitoring stack
   stores (log/sysflow/flow class).
10. [I|CLO6] Baseline deviation alerting: why does "90% CPU" need a baseline to be
    actionable, while "device unreachable for 3 min" mostly does not?
11. [I|CLO6] Troubleshooting drill: users can ping the server but the app times out.
    Give the ordered hypotheses you test (bottom-up or top-down) and one test each.
12. [I|CLO6] Your monitor polls every 60 s and you still missed a 30 s outage. Name
    the two measurement concepts (sampling, blind window) and one fix.

---

## SELF-CHECK KEY — attempt first, then verify

1. Namespace: isolates the container's network view (interfaces, routes, ports); veth:
   virtual cable pairing namespace to host; bridge: host-side L2 switch connecting
   pairs and the outside.
2. 1450 B inner. Symptom: large packets drop (or fragment) — small handshakes pass,
   big transfers stall.
3. Security groups are stateful: an *allow-in* 443 rule admits the request, and the
   connection's return traffic is auto-allowed — the egress rule governs only
   connection-*initiating* traffic, so both exist for different directions of intent.
4. Peering: private address space/path, no public exposure (security); stays inside
   the provider's backbone — lower latency/jitter than transit (performance).
5. Management: operator-facing config plane. Control: decides topology/forwarding
   (protocols, in the switch CPU). Data: forwards packets (ASIC/tables) — all three
   live *inside* each traditional device.
6. S1: match (in-port of H1, dst H2) → forward toward S2. S2: match (from S1, dst H2)
   → out-port to H2. The controller computes the path and installs both rules.
7. Switches keep forwarding by installed rules independently of the controller; only
   *new* decisions (new flows' path changes, failure re-routing) wait. Blast radius:
   frozen reachability for *changes*, not blackholing of existing paths (unless the
   failure itself changed the path).
8. Autonomous wins: fast local reaction to a link failure (sub-second, no controller
   round-trip). Centralized wins: global policy — consistent, conflict-free rules for
   segmentation/migration across the whole fabric (no per-box drift).
9. Continuous: utilization %, RTT, loss. Events: syslog entries, flow records
   (who-talker pairs), config-change logs, alert states. Any 2+2 with correct class.
10. 90% CPU may be the *normal* 03:00 backup shape — thresholds need context, so
    baselines separate normal-but-loud from abnormal. Unreachable is binary-state:
    absence is abnormal by definition.
11. Top-down fits (path proven up): (1) server process listening — `ss -tlnp`;
    (2) firewall on path — try the port from the client (`nc -vz srv 443`);
    (3) MTU/application-layer stall — capture the handshake (SYN/SYN-ACK vs
    connection success). Ordering + one test each earns credit.
12. Sampling at 60 s has a ≥30 s blind window per poll cycle (outage between polls
    invisible); fix: event-driven telemetry (syslog/SNMP trap on state change) or
    faster polling on critical assets.
