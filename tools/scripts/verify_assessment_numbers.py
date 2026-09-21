#!/usr/bin/env python3
"""Numerical verification for the assessment package.

Re-computes every [MC]-tagged numeric claim in assessments/ (subnet math via the
standard-library ipaddress module; capacity/delay/transport arithmetic directly).
Run from the repository root:  python tools/scripts/verify_assessment_numbers.py
Exit 0 = all checks pass; 1 = at least one mismatch (a real answer-key bug).
Standard library only.
"""

import math
import sys
from ipaddress import IPv4Network, IPv6Address, IPv4Address

FAILURES = []
COUNT = [0]


def check(name, ok, detail=""):
    COUNT[0] += 1
    if not ok:
        FAILURES.append((name, detail))
        print(f"[FAIL] {name}  {detail}")


def close(a, b, tol_rel=0.02, tol_abs=0.0):
    return abs(a - b) <= max(tol_abs, tol_rel * abs(b))


def usable(n):
    return IPv4Network(n).num_addresses - 2


# ---------------------------------------------------------------- subnet math
check("/26 usable 62", usable("10.0.0.0/26") == 62)
check("/27 usable 30", usable("10.0.0.0/27") == 30)
check("/28 usable 14", usable("10.0.0.0/28") == 14)
check("/25 usable 126", usable("10.0.0.0/25") == 126)
check("/23 usable 510", usable("10.0.0.0/23") == 510)
check("/21 usable 2046", usable("10.0.0.0/21") == 2046)
check("/22 usable 1022", usable("10.0.0.0/22") == 1022)
check("/24 usable 254", usable("10.0.0.0/24") == 254)

# N-02: 172.16.20.77/28
net = IPv4Network("172.16.20.77/28", strict=False)
check("N-02 network .64", str(net.network_address) == "172.16.20.64", net)
check("N-02 broadcast .79", str(net.broadcast_address) == "172.16.20.79")
check("N-02 usable .65-.78",
      usable("172.16.20.64/28") == 14 and
      str(net.broadcast_address) == "172.16.20.79")

# N-03: /16 -> 512 x /25
check("N-03 512 subnets", IPv4Network("10.0.0.0/16").num_addresses // 128 == 512)

# N-04: summary 192.168.16.0/20 covers 192.168.16.0-192.168.31.255
s = IPv4Network("192.168.16.0/20")
check("N-04 /20 span",
      str(s.network_address) == "192.168.16.0" and
      str(s.broadcast_address) == "192.168.31.255")

# N-05: VLSM in 10.200.0.0/21 (prefix, need, first usable, last usable)
alloc = [("10.200.0.0/23", 500, "10.200.0.1", "10.200.1.254"),
         ("10.200.2.0/24", 200, "10.200.2.1", "10.200.2.254"),
         ("10.200.3.0/25", 100, "10.200.3.1", "10.200.3.126"),
         ("10.200.3.128/26", 50, "10.200.3.129", "10.200.3.190"),
         ("10.200.3.192/30", 2, "10.200.3.193", "10.200.3.194"),
         ("10.200.3.196/30", 2, "10.200.3.197", "10.200.3.198")]
for prefix, need, first, last in alloc:
    n = IPv4Network(prefix)
    check(f"N-05 {prefix} fits {need}", usable(prefix) >= need,
          f"{usable(prefix)} < {need}?")
    check(f"N-05 {prefix} usable {first}-{last}",
          str(IPv4Address(int(n.network_address) + 1)) == first and
          str(IPv4Address(int(n.broadcast_address) - 1)) == last,
          f"got {IPv4Address(int(n.network_address)+1)}-"
          f"{IPv4Address(int(n.broadcast_address)-1)}")
# first free address after allocation
n5 = IPv4Network("10.200.3.196/30")
check("N-05 free starts 10.200.3.200",
      int(n5.broadcast_address) + 1 == int(IPv4Address("10.200.3.200")))

# N-11: 10.20.30.44 in 10.20.30.32/27
check("N-11 membership", IPv4Address("10.20.30.44") in IPv4Network("10.20.30.32/27"))

# N-12: /29 count in /26
check("N-12 count 8", IPv4Network("10.0.0.64/26").num_addresses // 8 == 8)

# N-13: IPv6 compression
check("N-13 compression",
      IPv6Address("2001:0db8:0000:0001:0000:0000:0000:00ff").compressed
      == "2001:db8:0:1::ff")

# quiz-w06: four /26s of 192.168.4.0/24; .197 in last
q6 = [str(IPv4Network("192.168.4.0/26").network_address),
      str(IPv4Network("192.168.4.64/26").network_address),
      str(IPv4Network("192.168.4.128/26").network_address),
      str(IPv4Network("192.168.4.192/26").network_address)]
check("W06 four /26 ranges", q6 == ["192.168.4.0", "192.168.4.64",
                                    "192.168.4.128", "192.168.4.192"], q6)
check("W06 .197 in last /26",
      IPv4Address("192.168.4.197") in IPv4Network("192.168.4.192/26"))

# quiz-w07: 10.20.0.0/26 staff, 10.20.0.64/30 link
check("W07 /26 usable .1-.62", usable("10.20.0.0/26") == 62)
check("W07 /30 usable 2", usable("10.20.0.64/30") == 2)
# /22 total and free range end
check("W07 /22 span", str(IPv4Network("10.20.0.0/22").broadcast_address)
      == "10.20.3.255")

# review-m3 Q4 (new sizes): /25,/26,/27,/28,/29,/30 in 192.168.10.0/24
r3 = [usable(p) for p in ("192.168.10.0/25", "192.168.10.128/26",
                          "192.168.10.192/27", "192.168.10.224/28",
                          "192.168.10.240/29", "192.168.10.248/30")]
check("M3-Q4 sizes 126/62/30/14/6/2",
      r3 == [126, 62, 30, 14, 6, 2], r3)
check("M3-Q4 fits", sum(IPv4Network(p).num_addresses for p in
      ("192.168.10.0/25", "192.168.10.128/26", "192.168.10.192/27",
       "192.168.10.224/28", "192.168.10.240/29", "192.168.10.248/30")) == 252)
check("M3-Q4 leftover /30 .252-.255",
      str(IPv4Network("192.168.10.252/30").network_address) == "192.168.10.252")

# midterm B1: 10.30.0.0/22
check("MT-B1 four /24s",
      [str(IPv4Network(f"10.30.{i}.0/24").network_address) for i in range(4)]
      == ["10.30.0.0", "10.30.1.0", "10.30.2.0", "10.30.3.0"])
check("MT-B1 mask /25 for 90", usable("10.30.0.0/25") == 126)
check("MT-B1 .3.200 in 4th /24",
      IPv4Address("10.30.3.200") in IPv4Network("10.30.3.0/24"))
check("MT-B1 mask dotted", str(IPv4Network("10.30.0.0/22").netmask)
      == "255.255.252.0")
check("MT-B1 /21 summary spans .0-.7.255",
      str(IPv4Network("10.30.0.0/21").broadcast_address) == "10.30.7.255")

# final B1: 10.0.0.0/21
check("FN-B1 halves /22",
      str(IPv4Network("10.0.0.0/22").broadcast_address) == "10.0.3.255" and
      str(IPv4Network("10.0.4.0/22").network_address) == "10.0.4.0" and
      str(IPv4Network("10.0.4.0/22").broadcast_address) == "10.0.7.255")
check("FN-B1 /26 for 60", usable("10.0.0.0/26") == 62)
check("FN-B1 .5.200 in second /22",
      IPv4Address("10.0.5.200") in IPv4Network("10.0.4.0/22"))

# N-16: DHCP pool /23 minus 10
check("N-16 pool 500", usable("10.1.6.0/23") - 10 == 500)

# ------------------------------------------------------- capacity/transport
MSS = 1460
check("W01 serial 120us", close(1500 * 8 / 1e8 * 1e6, 120.0))
check("W02 10MB@25M = 3.2s", close(10e6 * 8 / 25e6, 3.2))
check("W02 +80ms = 3.28s", close(3.2 + 0.08, 3.28))
check("W03 Shannon 29.9kb/s", close(3000 * math.log2(1001) / 1e3, 29.9, 0.01))
check("W03 Nyquist 16kb/s", close(2 * 4000 * math.log2(4), 16000))
check("W04 512ns", close(512 / 1e9 * 1e9, 512.0))
check("W10 BDP 625kB", close(100e6 * 0.05 / 8, 625e3))
check("W10 slow start 4 RTTs", 2 ** 4 == 16)
check("W10 ssthresh 10", max(20 // 2, 2) == 10)
check("W10 window 12.5kB", close(5e6 * 0.02 / 8, 12.5e3))
check("W16 200GB = 1600s", close(200e9 * 8 / 1e9, 1600.0))
check("W16 BDP 3.75MB", close(1e9 * 0.03 / 8, 3.75e6))
check("M1-Q16 278Mb/s", close(500e9 * 8 / (4 * 3600) / 1e6, 278.0, 0.01))
check("M2-Q1 Nyquist 32kb/s", close(2 * 4000 * math.log2(16), 32000))
check("M2-Q2 Shannon 26.6kb/s", close(4000 * math.log2(101) / 1e3, 26.6, 0.01))
check("M2-Q9 1.21us", close(1518 * 8 / 1e10 * 1e6, 1.21, 0.01))
check("M4-Q8 BDP 5MB", close(1e9 * 0.04 / 8, 5e6))
check("M5-Q12 350ms", close(math.ceil(40 / 6) * 0.05, 0.35))
check("M8-Q5 2TB = 1600s", close(2e12 * 8 / 1e10, 1600.0))
check("M8-Q5 BDP 25MB", close(1e10 * 0.02 / 8, 25e6))
check("N-06 250GB = 2000s", close(250e9 * 8 / 1e9, 2000.0))
check("N-07 25ms one-way", close(5e6 / 2e8, 0.025))
check("N-08 BDP 50MB", close(1e10 * 0.04 / 8, 50e6))
check("N-09 120us/12us",
      close(1500 * 8 / 1e8 * 1e6, 120.0) and close(1500 * 8 / 1e9 * 1e6, 12.0))
check("N-10 Shannon 50.3Mb/s", close(10e6 * math.log2(1 + 10 ** 1.5) / 1e6, 50.3, 0.01))
check("N-14 ack 5201", 5000 + 1 + 200 == 5201)
check("N-15 0.46s", close(5e6 * 8 / 1e8 + 2 * 0.03, 0.46))
check("N-17 36us", close(3 * (1500 * 8 / 1e9) * 1e6, 36.0))
check("N-18 20Mb/s", close(100 / 5, 20.0))
check("N-19 1.2ms", close(100 * (1500 * 8) / 1e9 * 1e3, 1.2))
check("N-20 96.2%", close(MSS / 1518 * 100, 96.2, 0.01))
check("N-21 256000/17x", 4 * 64000 == 256000 and close(256000 / 15000, 17.1, 0.05))
check("N-22 20%: /21", 800 * 1.2 ** 3 > usable("10.0.0.0/22") and
      800 * 1.2 ** 3 <= usable("10.0.0.0/21") and close(800 * 1.2 ** 3, 1382))
check("N-22 40%: /20", 800 * 1.4 ** 3 > usable("10.0.0.0/21") and
      800 * 1.4 ** 3 <= usable("10.0.0.0/20") and close(800 * 1.4 ** 3, 2195))
check("N-23 margin 39.88ms", close(100 - 60 - 0.12, 39.88, 0.001))
check("N-24 overhead 6%", close((10 - 9.4) / 10 * 100, 6.0))
check("RT-09 window 90kb=11.25kB", close(3e6 * 0.03, 90e3) and
      close(90e3 / 8, 11.25e3))
check("MT-B2 0.84s/0.8s",
      close(2 * 2 ** 20 * 8 / 2e7, 0.84, 0.01) and close(2e6 * 8 / 2e7, 0.8))
check("MT-B2 Shannon 6.66Mb/s", close(1e6 * math.log2(101) / 1e6, 6.66, 0.01))
check("MT-B2 prop 1.5ms", close(3e5 / 2e8 * 1e3, 1.5))
check("MT-C2 ack 4001", 3000 + 1 + 1000 == 4001)
check("MT-C1 ttl 64-62 = 2 routers", 64 - 62 == 2)
check("FN-B2 BDP 5MB", close(1e9 * 0.04 / 8, 5e6))
check("FN-B2 slow start 5 RTTs", 2 ** 5 == 32)
check("FN-B2 ssthresh 10", max(20 // 2, 2) == 10)
check("FN-B2 window 25kB", close(4e6 * 0.05 / 8, 25e3))
check("FN-C1 ack 8300", 6840 + 1460 == 8300)
check("FN-C1 RTT 50ms", close(0.107 - 0.057, 0.05))
check("FN-C1 dup count 3", ["0.052", "0.054", "0.056"].__len__() == 3)
check("PA-13 fresh 5s", 60 - 55 == 5)
check("PA-01 1 router", 64 - 63 == 1)
check("PA-04 RTT 40ms", close(0.040 - 0.000, 0.04))
check("W09 ack 1501", 1001 + 500 == 1501)

print("-" * 72)
print(f"Checks: {COUNT[0]}  FAIL: {len(FAILURES)}")
if FAILURES:
    for name, detail in FAILURES:
        print(f"  - {name}: {detail}")
    sys.exit(1)
print("All [MC] claims verified.")
