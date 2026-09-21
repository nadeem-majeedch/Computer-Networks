# Lab Environment Setup & Tool Guide

| Field | Value |
|---|---|
| Companion | [`syllabus-safety.md`](syllabus-safety.md) · [`../docs/lab-strategy.md`](../docs/lab-strategy.md) §2 |
| Status | Draft v0.1 — awaiting instructor review |
| Verify your install | `python3 tools/scripts/check_lab_env.py` (report PASS/WARN/MISSING per tool) |

## 1. Three supported routes

| Route | Hardware needed | Used for | Difficulty |
|---|---|---|---|
| **A. Course VM image** (recommended) | 2 CPU cores, 4 GB RAM free, ~25 GB disk | All labs | Low ⚠ image must be verified per semester |
| **B. Self-built Ubuntu VM** | same | All labs | Medium (you do the install below) |
| **C. Namespaces-only on a Linux box** | any Linux with root in a lab account | Labs 01, 04–08, 10–15 (not LAB-02/03 GUI-heavy parts) | Medium |

The **host** additionally needs Wireshark for the two host-side labs (LAB-01 route A host
part is optional; LAB-03 survey). Everything else happens inside VM/namespaces.

## 2. Route A — course VM image

1. Get `cnlab.ova` from the instructor. **Verify the hash before importing:**
   `sha256sum cnlab.ova` (Linux/macOS) or `certutil -hashfile cnlab.ova SHA256` (Windows)
   and compare against the value the instructor published this semester
   (⚠ instructor: build image, publish SHA-256 — checklist in lab-strategy §7).
2. Import into VirtualBox or VMware Workstation Player (⚠ verify the teaching room's
   hypervisor version against the image's export version).
3. VM network settings: **NAT** (for internet-dependent tasks) and a **host-only** adapter
   (`cnlab-lab` 192.0.2.0/24 range reserved for the course) for lab-internal tasks. Default
   in the image: enp0s3 = NAT, enp0s8 = host-only.
4. Log in as `lab` (password provided in session), open a terminal, run
   `python3 ~/check_lab_env.py` (copy from `tools/scripts/` on the course share) — all
   PASS expected.
5. Snapshot the clean VM now (`lab-clean`); restore it whenever a lab breaks the environment.

## 3. Route B — build it yourself (Ubuntu 22.04/24.04 LTS)

```bash
# system tools (needs sudo — lab accounts have it inside the VM)
sudo apt update
sudo apt install -y wireshark tcpdump iperf3 dnsmasq nftables \
     traceroute mtr-tiny curl dnsutils netcat-openbsd openvpn \
     network-manager bridge-utils python3 python3-pip
sudo usermod -aG wireshark "$USER"        # allow non-root captures; re-login after
# enable netem + namespaces (kernel modules ship with stock Ubuntu)
sudo modprobe ifb numifbs=1 2>/dev/null || true   # only needed for some netem ingress setups
ip netns list                              # sanity: runs without error
python3 --version                          # 3.10+ expected
```

Wireshark config used in the course: View → check "Show capture filter bar"; the course
profile (coloring rules only — no behavioral changes) is on the course share.

## 4. Route C — namespaces only (no VM)

Root on a Linux lab machine (or sudo group) is enough for most tasks:

```bash
sudo ip netns add blue        # every lab that says "VM-blue" can use `ip netns exec blue`
```

LAB-02 (switching/VLANs) and LAB-03 (Wi-Fi survey) need real/simulated GUI environments and
are the two labs this route cannot fully cover; the offline-capture alternative in each lab
README covers them.

## 5. Host Wireshark (LAB-01, LAB-03)

Install from <https://www.wireshark.org> (Windows/macOS: standard installer; Linux: distro
package). On Windows, install Npcap with default options. LAB-03's RF survey runs on the
host because VMs bridge Wi-Fi as Ethernet — see that lab's README.

## 6. Optional simulators

- **GNS3** (optional, LAB-07 and LAB-02 alternatives): instructor decision per semester;
  ⚠ verify image licensing/availability (lab-strategy §7). The labs are written to work
  without it.
- **Cisco Packet Tracer** (optional visualization only, where the institution licenses it):
  no deliverable depends on it; use it to *sketch* topologies from LAB-02/LAB-07 if helpful.

## 7. What the verification script checks

`tools/scripts/check_lab_env.py` (stdlib only, no root needed) classifies each tool as
PASS / WARN / MISSING and prints the lab(s) that need it: wireshark/tshark, tcpdump, ip,
br/bridge, tc (netem), nft, dnsmasq, iperf3, dig, traceroute, ss, python3 ≥3.10, curl,
nc, openvpn. Run it after setup and paste its table into every lab report's environment
section (submission format).

## 8. Known environment-dependent items (⚠ instructor checklist)

- [ ] ⚠ VM image hash published; boots on the room's hypervisor version
- [ ] ⚠ LAB-12 external HTTP/3 endpoints reachable from the room; local fallback server in image
- [ ] ⚠ LAB-03 Wi-Fi survey feasible in local RF (room/campus policy)
- [ ] ⚠ GNS3 images/licensing if the optional route is used
- [ ] ⚠ Lab accounts: `wireshark` group membership + netns permissions confirmed
