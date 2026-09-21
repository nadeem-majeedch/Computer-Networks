# LAB-04 — Subnetting Drills & Address-Plan Design

| Field | Value |
|---|---|
| Anchor lectures | L13 (subnetting/VLSM), L14/L15/L16 (applied: DHCP, IPv6, routing) |
| CLOs | CLO3 (addressing design) |
| Assessment | **The 5% subnetting problem set** (assessment-strategy §3.3); individual |
| Mode / duration | Individual; start in session, due L16 (per schedule) |
| Environment | Paper first; then VM/lab box with Python 3 (`ipaddress` module) to verify |

## Learning outcomes
1. Subnet by hand: given an address block and requirements, produce network/broadcast/
   usable ranges with correct VLSM ordering (largest-first).
2. Choose an addressing plan under constraints (headroom rule, summarization, growth).
3. Verify hand arithmetic with Python's `ipaddress` module — and explain any mismatch
   (the verifier is the tool, the reasoning is yours).
4. Apply the plan discipline from L31's method in miniature (state your headroom rule).

## Pre-lab
1. Compute by hand: 192.168.100.0/24 split into four equal /26s — write each network,
   broadcast, usable count. (Bring the answer; T1 verifies it.)
2. How many usable hosts in a /29? In a /30? When is a /30 preferable to a /29?
3. What is the mask of 10.20.4.96/27, and which range does it cover?

## Tasks

### T1 — Drill set (do by hand, then verify) (45 min)
Hand-solve all five; then verify each with Python:
```python
import ipaddress
n = ipaddress.ip_network("192.0.2.0/27")
print(n.network_address, n.broadcast_address, n.num_addresses)
print(list(ipaddress.ip_network("192.168.100.0/26").hosts())[:3])
a = ipaddress.ip_interface("10.20.4.96/27")
print(a.network, a.netmask, a.ip in ipaddress.ip_network("10.20.4.64/27"))
```
1. 192.0.2.0/24 → four equal /26s: ranges, broadcast, usable per subnet.
2. 172.16.9.0/24 → subnets for 60, 30, 12, 2 hosts (VLSM, largest first, no waste):
   give each network + mask.
3. 10.20.4.96/27: network, broadcast, first/last usable. Is 10.20.4.110 inside it?
4. Your host is 192.0.2.137/26. Which subnet are you on, and what is the gateway range
   convention you would adopt (state it)?
5. CIDR sum: which single prefix summarizes 192.0.2.0/26 and 192.0.2.64/26?

**Expected observation:** the Python output matches your hand work *if* your bit
arithmetic is right; every mismatch is a learning event — record what you got wrong.

### T2 — Design exercise (Meridian guest + staff block) (35 min)
Given 10.20.0.0/16 (Meridian campus block, from the case study): plan Building A's
address space for **180 staff devices**, **40 guests**, **12 printers**, **6 server
VLANs (/26 each)**, a **/30-style point-to-point habit** for future router links.
State: your headroom rule (e.g., double each requirement), your VLSM order, the final
table, and which single summary route could announce the whole building to the core
(L16 preview).

### T3 — Verify the plan (10 min)
Write a 10-line Python snippet that takes your T2 table and asserts non-overlap plus
summary correctness (`ipaddress.summarize_address_range` or `.supernet()`).
Include the snippet + its output in the report.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Python says your subnet is invalid | host bits set (e.g., .96/27 given as .100/27) | `ipaddress.ip_network("...", strict=False)` to see the canonical network, then re-derive |
| Off-by-one in usable range | counting network/broadcast as usable | remember: usable = total − 2 (except /31,/32 special cases — beyond this course) |
| VLSM overlaps | wrong ordering (did small first) | redo largest-first; assertion in T3 catches it |

## Post-lab questions
1. Why does VLSM require largest-first ordering? Show the failure with drill 2 done
   smallest-first.
2. Your headroom rule doubled everything: what price does the campus pay at the core,
   and why does summarization (drill 5) matter there?
3. When would a /30 point-to-point habit fail you? (Name the modern alternative and its
   trade-off — L16/L15 hint.)

## Challenge (ungraded)
IPv6 plan: convert your T2 table to a /64-per-VLAN IPv6 scheme under 2001:db8:acad::/48,
stating nibble-aligned boundaries. (RFC 8374 reserves 2001:db8::/32 for documentation —
acceptable for coursework; cite it.)

## Accessibility / low-resource alternatives
- Entirely doable on paper; the Python verification can run on any machine with Python 3
  (no network, no root). Screen-reader friendly: `ipaddress` output is plain text.
- A calculator-only route: verify with `ipcalc` if Python is unavailable.

## Safety notes
No network access involved; `TEST-NET` and documentation ranges only (RFC 5737, RFC 8126)
— per syllabus-safety §3.4 (synthetic data only).
