# LAB-08 — UDP Client & Server (Python Sockets, Observed on the Wire)

| Field | Value |
|---|---|
| Anchor lectures | L17 (UDP & the transport layer's job), L03 (sockets API) |
| CLOs | CLO4 (packet analysis), CLO5 (build/measure) |
| Assessment | Graded lab deliverable (pairs; 15% pool) — working code + demo |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | VM/namespace; Python 3.10+ standard library only; `tcpdump` for observation |

## Learning outcomes
1. Build a UDP client and server with Python's socket API (`bind`, `sendto`, `recvfrom`)
   and run them across a namespace/VM link.
2. Observe your own protocol in a capture: ports, payload bytes, and the absence of any
   connection setup — then explain UDP's demultiplexing from *your* packets.
3. Extend the message format with sequence numbers and a minimal ACK — and articulate
   precisely which reliability rung (L17's ladder) you just built and why.
4. Predict and verify socket errors (port unreachable → ICMP) as a *feature* of UDP.

## Pre-lab
1. L17: what does a bound UDP socket on `*:5000` receive, and what key does the OS use
   to demultiplex?
2. UDP header is N bytes — name its four fields.
3. One reliability rung UDP omits — and one app where that's the right trade-off.

## Tasks

### T0 — Skeleton walkthrough (15 min)
Provided on the course share (`lab08-skeleton.py`); the graded work is the extensions:
```python
# server (lab08-server.py)
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 5000))
while True:
    data, addr = s.recvfrom(2048)
    print(f"from {addr}: {data!r}")
    s.sendto(b"ack: " + data, addr)
# client (lab08-client.py)
import socket
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.settimeout(2)
c.sendto(b"hello", ("192.0.2.22", 5000))
print(c.recvfrom(2048))
```
Run both in the lab net; confirm the round trip.

### T1 — See your own protocol (20 min)
```bash
sudo tcpdump -i '<link>' -nn -X -c 8 'udp port 5000'
```
**Expected observation:** your message's ASCII bytes in the hex dump; src/dst ports
(ephemeral client → 5000 server); *no* SYN/ACK-style setup packets anywhere — the first
packet is already data. Two-line note: what "connectionless" looks like in a capture.

### T2 — Sequence numbers (25 min)
Extend the payload to `seq|message` (client numbers each message; server echoes
`seq|ack`). Update and re-capture. Then answer: if packet 2 is lost, what does your
protocol *currently* do? (Nothing — UDP delivers no signal; that's the gap LAB-10/11
closes.) Record the answer before implementing more.

### T3 — Minimal ACK protocol (20 min)
Client sends `seq|msg`; server replies `ack|seq`. Client retransmits after a 1 s timeout
(`socket.timeout` from `settimeout`) up to 3 times. Kill the server mid-test to force a
timeout path; record observed behavior. **Expected observation:** exactly 3 client
attempts then a clean client-side failure message.

### T4 — The ICMP side effect (10 min)
Send to a port with no listener while capturing:
```bash
sudo tcpdump -i '<link>' -nn -c 4 'icmp or udp' &
sudo ip netns exec '<client>' python3 - <<'EOF'
import socket
c=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); c.settimeout(2)
c.sendto(b"x", ("192.0.2.22", 9999))
try: c.recvfrom(2048)
except Exception as e: print(type(e).__name__, e)
EOF
```
**Expected observation:** ICMP port-unreachable arrives; the next `recv`/timeout reflects
it (OS-dependent ⚠ record what *your* stack does — behavior differs by platform).

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Server binds, client times out | wrong IP/firewall between ns | ping first; check `ip addr` on both ends |
| `Address already in use` | old server instance | `pkill -f lab08-server.py` |
| Capture empty | wrong interface (`-i` inside vs outside the ns) | capture on the veth carrying the flow (T1 of LAB-02's lesson) |
| ACK echoes raw bytes in the client | payload format mismatch | print `repr()` of both sides; agree the `|` format |

## Post-lab questions
1. From *your* capture: the demux key that delivered your message to the server, and why
   the reply found the client without it being "bound" to 5000.
2. Your T2 loss gap: name the two rungs (L17's ladder) UDP lacks and you partially added
   in T3 — and the rung you *still* lack.
3. Why can the server reply to the client using only the address from `recvfrom`?
4. Your ICMP observation: is the port-unreachable a reliability guarantee? Why not?

## Challenge (ungraded)
Replace stop-and-wait with a sliding window of 3: send seq, seq+1, seq+2 before any ACK.
Measure simple throughput vs stop-and-wait over a `netem delay 50ms` link (`tc` from
LAB-09) — report the ratio.

## Accessibility / low-resource alternatives
- Skeleton runs on any Python 3 machine — single-machine mode works with `127.0.0.1`
  (capture on `lo`), so no VM/netns is strictly required.
- Screen-reader friendly throughout; capture analysis via `tshark -x` (hex+ASCII dump).

## Safety notes
Lab-internal addresses only. Chat content: synthetic text only (no personal data —
syllabus-safety §3.4).
