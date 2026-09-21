# Question Bank — Routing & Troubleshooting

| Field | Value |
|---|---|
| Scope | Forwarding logic, route selection, failure diagnosis, multi-layer reasoning |
| Tagging | `[Difficulty|CLO|Source]`; synthetic topologies are labeled and internally consistent |
| Key | fenced at end — do not distribute |

## Questions

**RT-01 [I|CLO4|L16]** FIB on R4: `0.0.0.0/0 → R9` · `10.0.0.0/8 → R1` · `10.8.0.0/16 → R2` ·
`10.8.7.0/24 → local`. Where do packets for 10.8.7.5, 10.8.9.9, and 10.9.1.1 go?

**RT-02 [I|CLO4|L16]** Two OSPF routes to 10.5.0.0/16: path A cost 30, path B cost 50.
The admin adds a static route to 10.5.0.0/16. What forwards now, why, and what one
command-style check confirms the winner? (Concept-level: name the table.)

**RT-03 [A|CLO6|L16]** Site uses 10.20.0.0/22. A new router advertises 10.20.2.0/24
toward a lab that "went dark" for the rest of campus. Explain the mechanism, and the
two-step verification (where to look first, what proves it).

**RT-04 [I|CLO6|L14]** Staff PC: IP 192.168.8.44/24 correct, gateway 192.168.8.1
correct, gateway ping works, internet ping fails. Order your hypotheses and one test
each (NAT rule, DNS, ISP uplink).

**RT-05 [I|CLO6|L13/L14]** After a scope change, a lab VLAN hands out addresses from
the *server room's* subnet instead of the lab's. Give the two misconfigurations that
produce exactly this, and which one the relay's giaddr exposes.

**RT-06 [I|CLO6|L09/L16]** Same-switch, same-VLAN host A reaches server S; host B does
not; B's link lights are green. Give a two-test plan separating L2 from L3 causes.

**RT-07 [A|CLO6|L16/L29]** A `traceroute` to a working server shows hop 4 stars, hop 5
replies, then success. Distinguish reply-suppression from real loss using (i) what
"success at the end" already proves, and (ii) one additional probe (`ping` to hop 5).

**RT-08 [I|CLO6|L18/L19]** One client's file transfers crawl; others are fine. Same
switch, same VLAN. You see 3 duplicate ACKs streams and retransmissions in its capture.
Name the layer and give two causes with one distinguishing observation each.

**RT-09 [I|CLO6|L19]** Transfers cap at 3 Mb/s on a 100 Mb/s, 30 ms path that `ping`s
clean. Compute the window the rate implies, then state which mechanism to inspect
first.

**RT-10 [A|CLO6|L15/L16]** A dual-stack host reaches IPv4 sites but not IPv6 sites.
Give the ordered checks (link-local present? RA received? default route? DNS AAAA?) and
what each result eliminates.

**RT-11 [I|CLO6|L21/L29]** After a server move, half the offices still reach the old
address for hours. Identify the mechanism (DNS TTL + caches) and the two artifacts to
check (record TTL, resolver cache age).

**RT-12 [A|CLO6|L25/L29]** A firewall change at 14:00 coincides with "app slow." The
app team says network; the network team says app. Design the evidence that decides it
in 30 minutes (two measurements and the decision rule).

**RT-13 [E|CLO6|L08/L16/L29]** Campus-wide: intermittent "destination unreachable" for
one building's subnet, worse at class-change times. Your monitoring shows 92% uplink
utilization spikes. Give the failure hypothesis chain (broadcast/queueing/link) and the
one capture that discriminates between the top two links in the chain.

**RT-14 [I|CLO6|L27]** Containerized app: `curl` between pods works; external calls
stall on large payloads. State the two-layer hypothesis (MTU/NAT) and the single
setting comparison that tests it first.

**RT-15 [I|CLO6|L12/L22]** A client shows 169.254.x.x and cannot reach anything. State
why the address *itself* tells you the failure stage, and the two physical/logical
checks before blaming DHCP.

**RT-16 [B|CLO4|L16]** A host's request reaches its default gateway, but the reply
never comes back. Name the three return-path items to check first.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**RT-01.** 10.8.7.5 → local; 10.8.9.9 → R2 (/16 beats /8); 10.9.1.1 → R1 (/8 beats /0).
**RT-02.** The static route forwards: administrative distance (static 1 < OSPF 110)
decides *before* metrics — cost 30 is irrelevant against a different AD source.
Confirm in the RIB/FIB (route table shows the installed source). **RT-03.** More-
specific advertisement: 10.20.2.0/24 (longest prefix) diverts the campus /22's traffic
for that subnet into the lab path. Verify: (1) look at campus routers' tables for the
/24 next hop; (2) prove with traceroute from an affected client — the path bends
toward the lab. **RT-04.** Order: (1) NAT translation present for a test flow
(router's NAT table) — tests egress translation; (2) DNS resolves externally
(`nslookup` a public name) — separates name vs path; (3) ISP uplink state (interface
counters/wan ping) — distinguishes router↔ISP failure. Any sound order with matching
tests earns credit. **RT-05.** (i) Relay not configured (or pointing at wrong scope):
server saw the request without giaddr → used the server-local pool; (ii) server scope
subnet/gateway mis-set. giaddr exposes (i): the relay inserts its interface address,
so a missing/wrong giaddr maps to (i); correct giaddr + wrong pool = (ii). **RT-06.**
L2 test: does B's ARP for anyone resolve (or do A↔B frames appear on B's port)?
L3 test: B pings its gateway — succeeds → L2 fine, fault above (wrong mask/duplicate
IP); fails → L2/port/VLAN issue. Two tests, decision rule stated. **RT-07.** (i)
End-to-end success proves the *path through hop 5* forwards data — the star cannot be
a path break; (ii) `ping hop5` from the source: replies → hop 5 only suppresses TTL-
expired; no replies but other traffic passes → filtering/rate-limit at hop 5. **RT-08.**
Layer: transport (TCP). Causes: (1) loss on its access path (duplex/cable) —
distinguisher: interface error counters rise only on its port; (2) windowing/app
pattern — distinguisher: RTT clean, retransmits absent, but small `win=` advertised.
**RT-09.** window = 3×10⁶ b/s × 0.03 s = 90 000 bits ≈ **11 kB** — far below the
path's BDP (3.75 MB); inspect the *receive window/app socket* first (rwnd), not the
link. **RT-10.** (1) fe80:: link-local present? absent → interface/v6 stack; (2) RA
received (prefix learned)? absent → router advertisement/VLAN; (3) default route
(::/0) present? absent → RA flags/gateway; (4) AAAA resolves? fails → DNS path (AAAA
filtering). Each check eliminates everything *below* it. **RT-11.** Mechanism:
resolvers keep the old A record until TTL expiry after the change — clients in
offices with long-cached answers keep hitting the old server. Artifacts: the record's
TTL (was it lowered *before* the move?) and the resolver cache entry age (proves
staleness window). **RT-12.** Measurements: (1) network RTT/loss client→app before/
after 14:00 (path evidence); (2) app server response time percentiles (server
evidence). Decision rule: network metric degraded *and* correlates with the change
window → network; network clean + server latency spiked → app. Both clean → look
between (proxy/DB). **RT-13.** Chain: class-change burst → broadcast/ARP storm on the
flat segment → uplink queueing (92%) → queue overflow drops → unreachable.
Discriminating capture: span the uplink at spike time — if drops are broadcast-heavy
with FDB flapping → L2 storm; if drops are unicast queue overflows → capacity/link.
**RT-14.** Hypothesis: overlay/egress MTU shrinks effective path MTU while NAT hides
return paths. Test first: compare pod interface MTU (+ overlay overhead) with the
underlay's minimum MTU — mismatch confirms MTU without touching NAT. **RT-15.**
169.254.x.x is APIPA — self-assigned only after DHCP *discovery fails*, so the failure
stage is "no offer received," not "bad lease data." Check: (1) link/cable/port state,
(2) VLAN/relay reachability to the server — blame DHCP scope data only after an offer
is proven to arrive.
**RT-16.** (1) The gateway's route back to the host's subnet (asymmetry check);
(2) NAT translation state, if the path translates — no mapping, no return;
(3) stateful firewall on the return leg allowing the reply direction.
