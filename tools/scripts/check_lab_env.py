#!/usr/bin/env python3
"""Lab environment verifier for the Computer Networks course workbook.

Run from the repository root (or anywhere):  python3 tools/scripts/check_lab_env.py
Prints a PASS/WARN/MISSING table for every tool the labs use, plus the labs
that need it. Paste the table into your lab report's environment section.
Standard library only; needs no root. Exit 0 always (it is a report, not a gate).
"""

import shutil
import subprocess
import sys

TOOLS = [
    # (name, command, version flag, minimum note, labs needing it)
    ("wireshark", "wireshark", "--version", "GUI captures (host labs)",
     "LAB-01 (optional), LAB-03"),
    ("tshark", "tshark", "-v", "CLI capture analysis (all offline routes)",
     "LAB-02, 03, 06, 08, 12, 14, 15"),
    ("tcpdump", "tcpdump", "--version", "live captures in namespaces",
     "LAB-01, 02, 05, 06, 07, 08, 09, 13"),
    ("ip (iproute2)", "ip", "-V", "links, addresses, routes, netns, bridges",
     "LAB-02, 05, 06, 07, 09, 13, 14, 16"),
    ("bridge", "bridge", "-v", "VLAN filtering (LAB-02)",
     "LAB-02"),
    ("tc (netem)", "tc", "-V", "impairments",
     "LAB-09, 11, 14, 16"),
    ("nft", "nft", "--version", "firewall policy + NAT",
     "LAB-05, 13, 14"),
    ("dnsmasq", "dnsmasq", "--version", "DHCP server",
     "LAB-05"),
    ("iperf3", "iperf3", "--version", "throughput + UDP load",
     "LAB-01, 09, 11, 13, 14"),
    ("dig", "dig", "-v", "DNS drills",
     "LAB-12 (GA-21 practice)"),
    ("traceroute", "traceroute", "--version", "path measurement",
     "LAB-01, 07"),
    ("ss", "ss", "-V", "TCP state (cwnd, retransmits)",
     "LAB-01, 09"),
    ("curl", "curl", "--version", "HTTP protocol work",
     "LAB-12"),
    ("nc", "nc", "-h", "ad-hoc TCP/UDP tests",
     "LAB-08 (fallback), 14"),
    ("openvpn", "openvpn", "--version", "site-to-site tunnel",
     "LAB-13"),
    ("python3", "python3", "--version", "sockets, verifiers, pollers (need >= 3.10)",
     "LAB-04, 08, 10, 11, 14, 15, 16"),
    ("openssl", "openssl", "version", "certificate inspection",
     "LAB-12"),
]


def classify(name, cmd, flag, note, labs):
    path = shutil.which(cmd)
    if path is None:
        return "MISSING", "-", note, labs
    try:
        out = subprocess.run([cmd, flag], capture_output=True, text=True, timeout=10)
        ver = (out.stdout or out.stderr).strip().splitlines()
        version = ver[0][:60] if ver else "?"
        if name == "python3":
            minor = version.split()[-1] if version else ""
            if minor and tuple(int(x) for x in minor.split(".")[:2]) < (3, 10):
                return "WARN", version, "python < 3.10 — socket lab snippets assume 3.10+", labs
        return "PASS", version, note, labs
    except Exception as exc:  # timeout, permission, garbled output
        return "WARN", "-", f"present but errored on --version: {exc}", labs


def main():
    rows = [classify(*t) for t in TOOLS]
    width = max(len(t[0]) for t in TOOLS) + 2
    print("Lab environment check — paste this table into your report")
    print("=" * 78)
    print(f"{'tool':<{width}}{'status':<9}{'version/notes'}")
    print("-" * 78)
    for (name, _c, _f, note, labs), (status, ver, _n2, _l) in zip(TOOLS, rows):
        line = f"{name:<{width}}{status:<9}{ver if ver != '-' else note}"
        print(line[:110])
    missing = [t[0] for t, r in zip(TOOLS, rows) if r[0] == "MISSING"]
    warned = [t[0] for t, r in zip(TOOLS, rows) if r[0] == "WARN"]
    print("-" * 78)
    print(f"PASS: {len(rows) - len(missing) - len(warned)}  WARN: {len(warned)}  "
          f"MISSING: {len(missing)}")
    if warned:
        print("WARN tools:", ", ".join(warned))
    if missing:
        print("MISSING tools:", ", ".join(missing))
        print("Install guidance: labs/setup-environment.md §3 (Ubuntu apt line) — "
              "or use the offline-bundle route for capture-only labs.")
    print("\nPer-lab requirements (which labs need which tool):")
    for (name, _c, _f, _note, labs) in TOOLS:
        print(f"  {name:<{width}} {labs}")
    print("\nThis is a report, not a gate — a MISSING tool means either install it "
          "(setup guide) or use that lab's accessibility/low-resource alternative.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
