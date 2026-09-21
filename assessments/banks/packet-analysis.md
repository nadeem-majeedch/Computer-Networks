# Question Bank — Packet Analysis

| Field | Value |
|---|---|
| Scope | Reading frames/segments: header dissection, handshake state, anomaly reading |
| Evidence policy | Every excerpt below is **synthetic, written for teaching, internally consistent** — none is a real capture. State this to students before use (course evidence-labeling rule) |
| Tagging | `[Difficulty|CLO|Source]` |
| Key | fenced at end — do not distribute |

## Excerpts (all synthetic — labeled on worksheets too)

**Excerpt A — Ethernet frame (hex field view, synthetic)**

```text
dst MAC  = 3c:2a:f4:11:22:33
src MAC  = 9c:b6:d0:aa:bb:01
type     = 0x0800
IP src   = 10.40.1.25   IP dst = 10.40.9.7   ttl = 63  proto = 6 (TCP)
TCP src  = 49221       TCP dst = 443
flags    = [SYN] seq=0 win=64240 len=0
FCS      = ok
```

**PA-01 [B|CLO4|L07/L12]** Which machine sent this frame, and what does `ttl = 63`
imply about how many routers it crossed?
**PA-02 [I|CLO4|L12]** The IPs are off-link from each other. Which MAC should have
carried this frame if it were captured at 10.40.1.25's own interface, and why does
that differ from the IP destination?
**PA-03 [I|CLO4|L23]** Why is `TCP dst = 443` not proof of HTTPS? What would confirm
the application?

**Excerpt B — TCP handshake (synthetic)**

```text
t=0.000  10.1.1.5:51000 → 198.51.100.9:443  [SYN] seq=1000
t=0.040  198.51.100.9:443 → 10.1.1.5:51000  [SYN,ACK] seq=7000 ack=1001
t=0.041  10.1.1.5:51000 → 198.51.100.9:443  [ACK] seq=1001 ack=7001 win=65535
t=0.042  10.1.1.5:51000 → 198.51.100.9:443  [PSH,ACK] seq=1001 len=517
t=0.200  (no further packets from server in excerpt)
```

**PA-04 [I|CLO4|L18]** Compute the RTT from the handshake, showing which pair you used.
**PA-05 [I|CLO6|L18]** After t=0.200 the capture ends. What single follow-up packet
would you *expect* and what does its absence suggest (name two hypotheses)?
**PA-06 [A|CLO6|L18]** Suppose the next visible packet is a client **retransmission**
of seq=1001 at t=0.500. Which failure hypothesis from PA-05 does this support, and
what one extra capture point settles it?

**Excerpt C — DNS exchange (synthetic)**

```text
t=0.000  10.2.3.4:53411 → 10.2.3.1:53  Q: portal.internal.corp A
t=0.002  10.2.3.1:53   → 10.2.3.4:53411  A: portal.internal.corp CNAME web.front.corp
t=0.003  10.2.3.1:53   → 10.2.3.4:53411  A: web.front.corp A 10.9.0.80 ttl=300
```

**PA-07 [I|CLO4|L21]** How many records does the answer carry, and which one actually
gives the address?
**PA-08 [I|CLO6|L21]** Users later report `portal.internal.corp` failing *only* in one
building whose resolver caches aggressively. Given the CNAME chain and ttl=300, state
the likely stale-object and the fix window.

**Excerpt D — ARP frames (synthetic)**

```text
t=0.000  broadcast  who-has 10.50.7.9?  tell 10.50.7.20
t=0.001  10.50.7.9 at aa:bb:cc:07:00:09 → 10.50.7.20
t=0.030  broadcast  who-has 10.50.7.9?  tell 10.50.7.21
t=0.031  10.50.7.9 at aa:bb:cc:07:00:09 → 10.50.7.21
t=0.100  broadcast  who-has 10.50.7.9?  tell 10.50.7.20   (repeat)
```

**PA-09 [I|CLO4|L12]** What is normal in this excerpt, and what is *not*?
**PA-10 [I|CLO6|L12/L26]** Name two benign explanations for the repeated `who-has`,
and one malicious one with its L2 defense.

**Excerpt E — ICMP pair (synthetic)**

```text
t=0.000  10.1.1.5 → 203.0.113.7  ICMP echo request  id=7 seq=1
t=0.045  203.0.113.7 → 10.1.1.5  ICMP echo reply    id=7 seq=1
t=1.000  10.1.1.5 → 203.0.113.7  ICMP echo request  id=7 seq=2
t=1.050  203.0.113.7 → 10.1.1.5  ICMP echo reply    id=7 seq=2
```

**PA-11 [B|CLO4|L16]** What does this excerpt measure, and why must id and seq match
across the pair?
**PA-12 [I|CLO6|L16]** A different host on the same path gets **no** replies at all,
yet this host's pings succeed. Give one cause on the *path* and one on the *other
host*, each consistent with this asymmetry.

**Excerpt F — HTTP response headers (synthetic)**

```text
HTTP/1.1 200 OK
server: front-door
content-type: text/html
cache-control: public, max-age=60
age: 55
x-cache: HIT
```

**PA-13 [I|CLO4|L23]** Compute how long this cached object remains fresh *to the
client*, given `age`.
**PA-14 [I|CLO4|L23]** What does `x-cache: HIT` prove about the path between client
and origin, and what does it *not* prove?

**Excerpt G — request with a long pause (synthetic)**

```text
t=0.000  C→S [SYN] seq=100
t=0.040  S→C [SYN,ACK] seq=900 ack=101
t=0.041  C→S [ACK] ack=901
t=0.050  C→S [PSH,ACK] seq=101 len=412      (GET /report)
t=0.090  S→C [ACK] ack=513
t=8.090  S→C [PSH,ACK] seq=901 len=280      (HTTP/1.1 502 Bad Gateway)
```

**PA-15 [E|CLO6|L18/L23/L29]** Where does the ~8 s latency live? Name the layer and
the evidence in the excerpt, and name two server-side measurements that would
confirm your attribution.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**PA-01.** Sender: 9c:b6:d0:aa:bb:01 (source MAC). TTL 63 = started at 64 → **1 router**
crossed. **PA-02.** Captured at the sender's interface, dst MAC should be the *default
gateway's* MAC (off-link destination). The excerpt's dst MAC (3c:2a:f4:...) is the
first-hop router — the IP dst (10.40.9.7) and MAC dst legitimately differ; that
asymmetry is normal at every routed hop. **PA-03.** Port 443 only says "the TLS well-
known port was chosen." Proof of HTTPS is a TLS record (ClientHello) inside; anything
can listen on 443. **PA-04.** SYN t=0.000 → SYN,ACK t=0.040 → **RTT ≈ 40 ms** (accept
41 ms if the client ACK timestamp is used for the return leg's confirmation — both
defensible; state which pair). **PA-05.** Expect the server's response to the 517 B
payload (ACK + app reply, e.g., TLS ServerHello). Absence suggests: (i) server-side
stall (app listening but not answering / overloaded), (ii) return-path filtering of
server→client packets (asymmetric route/firewall). **PA-06.** Client retransmission
supports *return-path or server loss* rather than client-path loss (the handshake
succeeded both directions, so the path worked seconds earlier): the retransmit firing
at 0.5 s implies no ACK for the data segment. Settling capture: on the **server side**
— if the data segment arrives there, the return path drops; if it never arrives, the
forward path changed. **PA-07.** Two records: one CNAME + one A; the **A record for
web.front.corp** carries 10.9.0.80. **PA-08.** Stale object: either the CNAME or (more
likely) the cached A record for web.front.corp in that building's resolver, older than
its ttl (300 s). Fix window: records refresh within ~5 min of TTL expiry (or flush the
resolver). **PA-09.** Normal: one who-has → one reply per requester. Not normal: the
*same requester* (10.50.7.20) asks again 100 ms later despite having received a reply
— either its cache write failed or something is wrong. **PA-10.** Benign: requester's
own ARP entry churn (e.g., interface restart/flushed cache) or reply lost on its way
back (wireless/lossy link). Malicious: ARP poisoning in progress — a spoofer answers
each probe with *its* MAC (would show conflicting pairs); defense: dynamic ARP
inspection / port security. **PA-11.** It measures RTT between the pair (~45 ms, ~50
ms here); id identifies the ping *session*, seq the *probe*, so replies pair with
requests unambiguously. **PA-12.** Path: intermediate router rate-limits ICMP (echoes
deprioritized) per source/scope. Other host: its firewall drops inbound/outbound ICMP
echo while normal traffic flows — echo replies are policy, not reachability. **PA-13.**
Fresh = max-age − age = 60 − 55 = **5 s** to the client (response arrived already
55 s into its cache life). **PA-14.** Proves: some intermediary cache (CDN edge/proxy)
served it, so origin was not touched for this fetch. Does not prove: origin health —
an origin outage can hide behind a HIT until freshness expires.
**PA-15.** The delay is **application/backend**, not transport: handshake RTT ≈ 40 ms
and the request was ACKed at t=0.090 with zero retransmissions and zero window stalls
— the network did its job in under 100 ms. The ~8 s gap sits between the server's
ACK and its response; the **502 Bad Gateway** is the classic signature of a proxy
waiting on (and timing out against) its upstream — accept any backend-stall
attribution with that reasoning. Confirm on the server with: (i) application response-
time percentiles for /report (expect the same ~8 s shape), and (ii) the proxy's
upstream connect/timeout log for that timestamp.
