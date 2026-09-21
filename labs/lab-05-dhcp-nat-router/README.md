# LAB-05 — DHCP & NAT on a Linux Router

| Field | Value |
|---|---|
| Anchor lectures | L14 (DHCP DORA, NAT), L22 (lease lifecycle preview) |
| CLOs | CLO3 (addressing), CLO5 (build/measure) |
| Assessment | Graded lab deliverable (pairs; 15% pool) |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | Linux namespaces (route C) or two VMs + router VM; tools: `dnsmasq`, `nftables`, `tcpdump` |

## Learning outcomes
1. Configure a DHCP server (dnsmasq) on an isolated link and observe the full DORA
   exchange in a capture.
2. Configure NAT (nftables masquerade) on the router and demonstrate translation by
   comparing captures inside vs outside the NAT.
3. Explain which header fields NAT rewrites and why the "inside" address never appears
   on the outside wire.
4. Read a DHCP lease table and relate it to the DORA capture.

## Pre-lab
1. Write the DORA message order and who broadcasts each (L14/L22).
2. NAT rewrites which fields for a simple outbound ping? What does the router remember?
3. Why does DHCP *need* broadcast at discovery time?

## Topology (T0)

```
 [client ns] ──veth── [router ns: DHCP server + NAT] ──veth── [wan ns = fake internet]
   (DHCP client)        inside 192.0.2.0/24              outside 198.51.100.0/24
```

## Tasks

### T0 — Build (20 min)
```bash
sudo ip netns add client; sudo ip netns add router; sudo ip netns add wan
sudo ip link add c-r type veth peer name r-c
sudo ip link add r-w type veth peer name w-r
sudo ip link set c-r netns client; sudo ip link set r-c netns router
sudo ip link set r-w netns router; sudo ip link set w-r netns wan
sudo ip netns exec router ip addr add 192.0.2.1/24 dev r-c
sudo ip netns exec router ip addr add 198.51.100.1/24 dev r-w
sudo ip netns exec wan    ip addr add 198.51.100.10/24 dev w-r
for i in c-r r-c r-w w-r; do sudo ip link set $i up; done
sudo ip netns exec client ip link set lo up; sudo ip netns exec wan ip link set lo up
sudo ip netns exec router sysctl -w net.ipv4.ip_forward=1
```

### T1 — DHCP server (20 min)
Create `dnsmasq-lab.conf`:
```ini
interface=r-c
bind-dynamic
dhcp-range=192.0.2.100,192.0.2.150,12h
dhcp-leasefile=/tmp/dnsmasq-lab.leases
log-dhcp
no-resolv
port=0
```
Start it and a client DHCP request (client side, no static address):
```bash
sudo ip netns exec router dnsmasq -C dnsmasq-lab.conf --no-daemon &   # note the PID
sudo ip netns exec client ip link set c-r up
sudo ip netns exec client udhcpc -i c-r -n -q 2>/dev/null || \
  sudo ip netns exec client dhclient -v c-r 2>/dev/null || \
  echo "use the busybox-static route below"
```
If neither client exists (image-dependent), use Python (§LAB-08 skills) or the provided
`dhcp-request.py` scaffold — the server side is what this lab grades.
**Expected observation:** lease file gains a line (client MAC → 192.0.2.10x); capture
shows Discover(bcast) → Offer → Request(bcast) → Ack.

### T2 — Capture DORA (20 min)
```bash
sudo tcpdump -i r-c -nn -e -c 12 -w lab05-dora.pcapng 'udp port 67 or udp port 68' &
# trigger the client (re-run the T1 client command)
```
Annotate each of the four messages: who, src/dst MAC + IP, message type option (53).
**Expected observation:** server MAC/IP on Offer/Ack; broadcast MAC ff:ff:ff:ff:ff:ff on
Discover/Request (client has no address yet for unicast IP delivery).

### T3 — NAT (25 min)
```bash
sudo ip netns exec router nft add table ip lab05
sudo ip netns exec router nft add chain ip lab05 postrouting { type nat hook postrouting priority 100 \; }
sudo ip netns exec router nft add rule ip lab05 postrouting oifname "r-w" masquerade
# a ping across, captured on both sides simultaneously:
sudo tcpdump -i r-c -nn -c 4 'icmp' &
sudo tcpdump -i r-w -nn -c 4 'icmp' &
sudo ip netns exec client ping -c 3 198.51.100.10     # needs a default route first:
sudo ip netns exec client ip route add default via 192.0.2.1
```
**Expected observation:** inside capture shows source 192.0.2.10x; outside capture shows
the same ICMP id but source 198.51.100.1 (the router's outside address). Find the same
ICMP echo id in both files — that pair *is* the translation, made visible.

### T4 — Lease table (10 min)
`cat /tmp/dnsmasq-lab.leases`: relate expiry time, MAC, IP, hostname to your capture.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| dnsmasq "port 53 in use" | forgot `port=0` (DNS off) | add it — this lab needs DHCP only |
| Client never gets a lease | `bind-dynamic` missing / wrong interface | check `interface=r-c`; watch `log-dhcp` output |
| Ping crosses but outside capture shows 192.0.2.x | NAT rule wrong interface | `nft list ruleset` — rule must be `oifname "r-w"` |
| Inside capture shows 198.51.100.1 too | you captured on r-w by mistake | `-i r-c` is the inside link |

## Post-lab questions
1. Which two header fields changed between your inside and outside captures, and which
   stayed identical (proving it's the same packet)?
2. Why did the Ack use broadcast here, and when would a renewal be unicast (L22)?
3. What breaks on the internet if NAT did **not** track state (reply address problem)?
4. Lease time 12h: what happens at 50% (T1) if the server is down? (L22 answer.)

## Challenge (ungraded)
Add a second client ns; confirm both get distinct addresses and that the outside capture
during *both* pings shows how NAT distinguishes the flows (ICMP id / ports discussion).

## Accessibility / low-resource alternatives
- Offline route: instructor captures `lab05-dora.pcapng` + inside/outside ping pair;
  T2–T4 become analysis; T1 answers from the provided config + lease file snapshot.
- Screen-reader note: tcpdump `-nn` output is plain text; no GUI needed anywhere.

## Safety notes
All inside namespaces. NAT policy lives only on the lab link; never attach this topology
to a real network (syllabus-safety §3.1).
