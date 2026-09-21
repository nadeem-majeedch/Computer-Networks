# Module 3 Review Questions (L12–L16)

| Field | Value |
|---|---|
| Coverage | L12 IP & ARP · L13 subnetting/VLSM · L14 DHCP & NAT · L15 IPv6 · L16 routing & ICMP |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · LAB-04…LAB-07 · Cases PB-023…PB-032 |

## Questions

### L12 — IP fundamentals & ARP
1. [B|CLO3] What two jobs does an IP address do (identity roles), and which header
   field do routers actually *decrement*?
2. [I|CLO4] Host 172.16.9.20/24 sends to 172.16.9.200 and to 8.8.8.8. For each, state
   the ARP target and why.
3. [I|CLO3] Why do subnets need a network and a broadcast address (why can't hosts use
   them)? One reason each.

### L13 — Subnetting & VLSM
4. [I|CLO3] You need six subnets from 192.168.10.0/24 with sizes: 100, 50, 30, 10,
   6, and 2 hosts. Give each prefix and range (exact fit or next size up), state your
   ordering rule, and name the leftover block.
5. [I|CLO3] Why does VLSM beat fixed-length subnetting on address waste? One concrete
   example from your answer to Q4.
6. [I|CLO3] What is route aggregation, and why does the /16 summary of 10.40.0.0/24…
   10.40.255.0/24 work?

### L14 — DHCP & NAT
7. [B|CLO4] Name the four DHCP configuration fields every client typically learns.
8. [I|CLO4] A DHCP relay exists because Discover is broadcast. What does the relay do
   to the request, and what must the server have to answer correctly?
9. [I|CLO4] NAT: two LAN hosts open connections from the same source port 51300 to two
   different web servers. Can both translate? Why?

### L15 — IPv6
10. [B|CLO3] Give the IPv6 address-type for: fe80::/10, 2001:db8::/32, ff02::1.
11. [I|CLO3] SLAAC vs stateful DHCPv6: who assigns the address in each, and what does
    the host still verify either way?
12. [I|CLO3] Why does IPv6 remove NAT as a requirement for "many hosts, few public
    addresses," yet NAT (NPTv6-class) still appears in practice?

### L16 — Routing fundamentals & ICMP
13. [B|CLO4] Write the router's forwarding rule in one sentence (two tables max).
14. [I|CLO4] Two routes reach 10.1.0.0/16: static (AD 1, metric 10) and OSPF-learned
    (AD 110, metric 3). Which installs in the FIB, and what single criterion decided?
15. [I|CLO4] ICMP redirect exists to fix one specific inefficiency. Name it.
16. [I|CLO6] Your `traceroute` shows three hops of `* * *` then success. Give two
    benign causes and what distinguishes them from a real drop.

---

## SELF-CHECK KEY — attempt first, then verify

1. Identity: interface locator (where it is) and interface identifier (who it is);
   routers decrement **TTL/hop-limit**.
2. To 172.16.9.200: on-subnet → ARP for 172.16.9.200 itself. To 8.8.8.8: off-subnet →
   ARP for the default gateway 172.16.9.1 (frame goes to gateway; IP dst stays 8.8.8.8).
3. Network address = the subnet's own identifier, used by routing/summary logic, so it
   cannot name a host; broadcast = "all hosts here" selector for one-to-many local
   delivery, so a unicast host using it would hijack delivery semantics.
4. Largest-first: **/25** .0–.127 (126 ≥ 100) · **/26** .128–.191 (62 ≥ 50) ·
   **/27** .192–.223 (30 = 30) · **/28** .224–.239 (14 ≥ 10) · **/29** .240–.247
   (6 = 6) · **/30** .248–.251 (2 = 2). Leftover: **.252–.255** (a spare /30).
   Sum check: 128+64+32+16+8+4 = 252 ≤ 256 [MC]. (Instructor note: with sizes
   100/50/30/10/10/2 the demand totals 260 > 256 and does **not** fit — a valid
   variant answer is to prove overflow, if you edit the sizes back.)
5. Fixed-length would carve /24 into e.g. all-/26 (62-host) chunks: the 2-host link
   would still burn 62 addresses. VLSM gives the /30 its own 4-address block — waste 2,
   not 60.
6. Advertising one prefix (10.40.0.0/16) for many constituent routes shrinks table size;
   it works because all covered routes share the /16's leading bits — longest-prefix
   still resolves if exceptions exist.
7. IP address, subnet mask (prefix), default gateway/router, DNS server(s).
8. Relay re-broadcasts/forwards Discover *unicast* to the configured server, inserting
   its interface address (giaddr) so the server knows which scope to allocate from.
9. Yes. NAT creates two distinct mappings — (publicIP, 51300→hostA,51300→srv1) and
   (publicIP, *different* public port or distinct 5-tuple →hostB,51300→srv2). Port
   collisions are resolved by re-mapping one side's translated port.
10. fe80::/10 link-local · 2001:db8::/32 documentation prefix · ff02::1 all-nodes
    multicast (link scope).
11. SLAAC: the host builds its address from router-advertised prefix + its interface
    identifier. Stateful DHCPv6: a server assigns. Either way the host runs duplicate
    address detection (DAD) before use.
12. IPv6's address space makes every host globally addressable, so port-translation
    scarcity disappears; NAT still appears for topology privacy/policy or renumbering
    convenience — stated as course-level rationale.
13. Longest-prefix match wins: pick the route whose prefix matches most bits; among
    equal prefixes, lowest administrative distance, then lowest metric.
14. The **static** route installs — administrative distance (trustworthiness of source)
    is compared *before* metrics; 1 < 110.
15. A host sending via a non-optimal gateway: the better-connected router tells the
    host to use a different next hop on the same link, trimming a redundant hop.
16. (i) Router drops/deprioritizes ICMP TTL-expired replies under load but forwards
    fine; (ii) firewall suppresses TTL-expired while allowing end-to-end traffic.
    Distinguisher: end-to-end success plus consistent hop identity via other probes —
    the *destination* is reachable, so the stars are per-hop reply suppression, not a
    path break.
