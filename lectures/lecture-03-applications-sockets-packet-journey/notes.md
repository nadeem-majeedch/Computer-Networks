# Lecture 03 — Instructor Teaching Notes
## Applications, Sockets & the First Packet Hunt (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO1 primary; CLO4 introduced |
| Textbook anchor | KR §2.1; PD §9.1 |

---

## 1. Objectives hook
Board: **"An app can't touch the network directly. Something must lend it a door. What is
that door — and what's on the other side?"**

Hook (2 min): two-line Python that fetches a web page. "By the end of today you can predict
every packet that code produces."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–7 | Recap + hook | L01/L02 recall (2 items); hook demo teaser |
| 7–25 | Concept 1 | App architectures: client/server, P2P, hybrids; ports & transport choice |
| 25–45 | Concept 2 | Sockets: IP+port, the socket API, client vs server side |
| 45–60 | Concept 3 | Journey of one HTTP request (DNS → TCP → TLS → HTTP) end to end |
| 55–60 | Break | (concept 3 continues after break as activity prep) |
| 60–63 | Recap | 2 rapid items |
| 63–80 | GA-03a | Python socket demo + students run it on the VM |
| 80–100 | GA-03b | Journey mapping activity, pairs, then reveal |
| 100–112 | Worked example + Q&A | Packet counts; overhead; "why 3 packets before the URL?" |
| 112–118 | Summary + exit ticket | — |
| 118–120 | Preview | LAB-01 tomorrow: bring the VM |

## 3. Concept walkthrough

### 3.1 Application architecture (20 min)
- **Client/server:** always-on server with a well-known address; clients initiate. Scales by
  adding server capacity; the bottleneck/owner is centralized (Web, email, DNS at scale).
- **P2P:** peers are intermittent, each both client and server; self-scalable (each new peer
  adds capacity) but hard to manage/secure. File distribution, some voice apps.
- **Hybrid reality:** most "P2P" systems still use servers for discovery (BitTorrent
  trackers/DHT hybrids; Skype-classic used directory servers). Teach the spectrum, not a
  binary.
- **Addressing model for apps (the part students miss):** to reach a service you need
  ① IP address ② transport protocol ③ **port number** identifying the *process*. Well-known
  ports (IANA registry): 80/443 web, 25/587 SMTP, 53 DNS, 22 SSH.
- **Transport choice made *by the app*:** TCP (reliable, ordered bytes) vs UDP (fast,
  datagram) — one slide, full treatment at L17–L20.

### 3.2 Sockets (20 min)
- **Socket = (IP address, port) pair** on a host, as seen by a process: the API door between
  app and transport. Not a cable, not a file descriptor that "is" the network — a software
  endpoint.
- Client side: `socket()` → `connect(server_ip, port)` → `send()`/`recv()` → `close()`.
  Server side: `socket()` → `bind(ip, port)` → `listen()` → `accept()` → per-client `recv`/`send`.
  (Show on one slide; students run it in GA-03a.)
- **Process-to-process vs host-to-host:** IP delivers host-to-host (L12); ports make it
  process-to-process. A web server and a game server on one machine coexist because of ports.
- Simplified teaching model note: a TCP "connection" is *state* at both ends (seq numbers,
  buffers, timer values) — no dedicated wire, no per-connection bandwidth reservation.
  Realization details (buffers, congestion window) at L18–L19.

### 3.3 Journey of one HTTP request (20 min, the lecture's spine)
Before any page content: three pre-flights.
1. **DNS:** browser asks resolver "what is example.com?" — UDP/53 round trip (or DoH — one
   sentence, L21 full). Without cache, root→TLD→authoritative walk (L21).
2. **TCP handshake:** SYN → SYN-ACK → ACK (why: sequence-number sync; L18).
3. **TLS handshake (for https):** 1–2 RTTs version-dependent; certificates (L24).
Then the **HTTP request** (`GET / HTTP/1.1`, `Host:` header) and **response** (status line,
headers, body). Each step is a row in our journey table — students rebuild it in GA-03b.
- Packet-count estimate for one small page over HTTPS ≈ 10–20 packets before *content*:
  DNS q/r (2) + TCP 3 + TLS 2–4+ + HTTP req/resp + ACKs. Predict-observe-explain pairs
  beautifully with the L01 Wireshark demo.

### Reference diagram — Encapsulation walk (the packet journey)

```text
┌─────────────┬──────────────┬───────────────┬─────────────┐
│ application │   transport  │   internetwork│  link       │
│ "GET /…"    │ +ports, seq  │ +IP addrs,TTL │ +MACs, FCS  │
│   message   │   segment    │   packet      │   frame     │
└─────────────┴──────────────┴───────────────┴─────────────┘
        sender adds each header → receiver strips in reverse
```

## 4. Important definitions
Client/server · Peer-to-peer · Socket · Port · Well-known ports · DNS · TCP · UDP ·
Handshake · Request/response · Latency budget (page load = Σ RTTs × steps).

## 5. Real-world examples
- **Port 443 on a phone:** dozens of processes share one Wi-Fi card — demux by 4-tuple
  (srcIP, srcPort, dstIP, dstPort) — preview of L17's demux discussion.
- **Game servers** publish IP:port pairs you can read in their UI — sockets made visible.
- **"Why is the first load slow, reload fast?"** DNS/TLS cache warm; perfect example of the
  journey steps being *cached state*, reinforcing that they are protocol interactions.

## 6. Mathematical/technical example
Page load with RTT = 40 ms, uncached: DNS (1 RTT) + TCP (1 RTT) + TLS 1.3 (1 RTT) + HTTP
request/response (1 RTT) ≈ 4×40 = 160 ms before the first pixel can render (plus server
time). With cached DNS + reused connection: ≈ 1 RTT. Students compute both; discuss why CDNs
(L01) and HTTP/2 multiplexing (L23) exist. Extension: at 150 ms RTT the same page adds
600 ms — the mobile-network pain point.

## 7. GA-03a: Python socket demo (17 min)
Course VM, Python 3.10+:

```bash
python3 - <<'EOF'
import socket
# Minimal HTTP fetch with raw sockets (teaching: see every step)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(("example.com", 80))
s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
buf = b""
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    buf += chunk
print(buf[:400].decode(errors="replace"))
s.close()
EOF
```

Debrief questions (orally): what did `connect()` do on the wire (SYN)? Why did we send
`Host:`? What arrived first — headers or body? ⚠ Verify the demo has outbound port 80 from
the teaching network, or pre-record it.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "A socket is a physical connection/wire" | Software endpoint + state; TCP connection = shared state, not a circuit |
| "The browser knows IPs; URLs are enough" | DNS always precedes; cache only hides it |
| "Servers 'listen' on the network" (magic) | bind() to an IP:port; kernel demuxes by 4-tuple |
| "HTTPS is a different protocol than HTTP" | Same semantics over TLS; TLS is a layer under HTTP (L23/L24) |
| "P2P means no servers at all" | Discovery/bootstrap servers; hybrid spectrum |

## 9. Suggested practical demonstration
GA-03a live; plus Wireshark capture *during* the demo to show the DNS→TCP→HTTP packet order
matching the journey table. ⚠ Verify network egress or use recorded fallback.

## 10. Classroom activities
- **Journey ordering game (GA-03b):** 8 shuffled cards (DNS query, SYN, SYN-ACK, TLS
  ClientHello, HTTP GET, HTTP 200, ACK, FIN) — pairs order them for a first-visit https page
  load; reveal with trace.
- **Port hunt:** show `ss -tunlp` output on the VM projector; students name the service on 3
  ports. (Bridges to LAB-01 tooling.)

## 11. Problem-solving questions
1. Order the events for a first-visit `https://example.com` page load.
2. Two servers on one host, ports 80 and 8080 — can both receive packets to the same IP?
   Why does the kernel not confuse them?
3. RTT 60 ms: compute minimum first-visit load time with uncached DNS and TLS 1.2-style
   2-RTT handshake. (Answer: DNS+TCP+TLS+HTTP = 5 RTT ≈ 300 ms.)
4. An app needs lowest possible delay, can tolerate loss — TCP or UDP, and why?
5. Where in the journey could two different users get *different* IPs for the same name?
   (CDN/geodns teaser → L21.)

## 12. Formative assessment (with answers)
- MCQ: The pair (IP, port) identifies a → **socket**.
- MCQ: First packet of a TCP connection → **SYN**.
- MCQ: DNS mostly runs over → **UDP port 53**.
- Short: why does a TCP connection not reserve bandwidth? → no reservation; state +
  congestion window adapt to load (teaser L19).

## 13. Exit ticket
1. The three pre-flight steps before HTTP content, in order: ________
2. Socket = ________ + ________.
3. Which protocol turns a name into an IP? ________

## 14. Anticipated difficulties
- Students conflate `connect()` success with "server agreed" — clarify SYN-ACK semantics
  (full handshake semantics at L18).
- Python indentation errors eat time in GA-03a: provide the heredoc form above and a
  pre-written file on the VM.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify outbound port 80 from teaching room; else use recorded run
- [ ] Pre-place GA-03a script on VMs; test on one fresh VM
- [ ] Print/shuffle journey cards; test `ss -tunlp` output non-empty
- [ ] Prepare journey table reveal slide

## 16. Timing fallbacks
Drop the port-hunt activity; compress §3.1 to 12 min by pushing P2P hybrid examples to
reading; keep GA-03a and journey mapping (both assessed).

## 17. References
- KR §2.1 (application principles), §2.7 (socket programming overview); PD §9.1.
- IANA Service Name and Transport Protocol Port Number Registry.
- Python `socket` howto (docs.python.org).
- RFC 9110 (HTTP semantics) — for the GET/Host framing shown.
- ⚠ VERIFY editions/sections and network egress before class.
