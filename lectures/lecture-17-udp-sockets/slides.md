# Lecture 17 — UDP & Sockets — Slide Deck

| Field | Value |
|---|---|
| Slides | 17 (120 min: 10 open · 50 teach · 5 break · 50 LAB-08 · 10 wrap) |
| Companions | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) · [LAB-08](../../labs/lab-08-udp-sockets/README.md) |
| Style | [Course deck conventions](../../lectures/README.md#deck-conventions) |

## Deck outline

| # | Slide | # | Slide |
|---|---|---|---|
| 1 | Title | 10 | Who chooses UDP |
| 2 | Hook: no envelope, no receipt | 11 | Worked example: seq/ack-free reading |
| 3 | The UDP header | 12 | LAB-08 brief |
| 4 | Connectionless: what that means | 13 | Classroom questions |
| 5 | Ports & demux redux | 14 | Common misconceptions |
| 6 | The socket API: UDP flavor | 15 | Summary |
| 7 | Worked example: two apps, one port | 16 | Exit question |
| 8 | Checksum's job | 17 | App-choice table |
| 9 | Loss, reorder: the UDP contract | | |

## Slides

### Slide 1 — Title
**Computer Networks — Lecture 17**
UDP & sockets (LAB-08 today)

> Notes — Module 4: the transport layer. Start with the *simpler* transport — and why simpler is sometimes right.

### Slide 2 — Hook: no envelope, no receipt
- UDP = postal drop-box: no handshake, no delivery receipt
- Faster, simpler — and *your problem* if it matters
- When is "your problem" the right trade?

> Notes — 2 min. Collect candidates (DNS, video, games). The lecture's question is exactly this trade.

### Slide 3 — The UDP header

```text
| Src port | Dst port | Length | Checksum |
|   2 B    |   2 B    |  2 B   |   2 B    |
```

- 8 bytes total — TCP's is 20+ before options

> Notes — Four fields, one slide. The *absence* list (no seq, no ack, no flags) is the teaching content — each absence means "app's job."

### Slide 4 — Connectionless: what that means
- No setup, no teardown, no per-connection state
- Every datagram independent: address it, send it
- The app owns ordering, reliability, pacing

> Notes — "Independent datagrams" is the contract (review-M4 Q1 family). Preview L20: *you* will rebuild what TCP does.

### Slide 5 — Ports & demux redux
- L3 promised: Proto = 17 → this is UDP's
- Port pair (src, dst) → the receiving process
- One server port, thousands of client ephemeral ports

> Notes — L03's apartment metaphor finishes the story: protocol separates TCP-mail from UDP-mail at the same door number.

### Slide 6 — The socket API: UDP flavor

```python
s = socket(AF_INET, SOCK_DGRAM)
s.sendto(data, (ip, port))
data, addr = s.recvfrom(65535)
```

- No connect, no accept — just send/receive with addresses

> Notes — Compare to LAB-08's TCP flavor at L20: four fewer syscalls, zero state. The API *is* the concept.

### Slide 7 — Worked example: two apps, one port
- Server binds :7005; two clients send from :40001 and :40002
- Replies addressed back per client's source port
- What if both used :7005 as *source*? → server can't reply correctly

> Notes — The demux discipline in miniature (quiz W09-adjacent, bank practical PR-06 grades exactly this capture).

### Slide 8 — Checksum's job
- 2-byte sum over header+data: catches corruption in transit
- Optional in IPv4 UDP; computed anyway by real stacks
- Catches, does not repair — corrupted datagrams are dropped

> Notes — Review-M3 SA-01-adjacent. "Catches ≠ repairs" distinguishes from L06's ARQ cleanly.

### Slide 9 — Loss, reorder: the UDP contract
- Datagrams may vanish, arrive twice, arrive shuffled
- No signal — unless the app checks (sequence numbers)
- Telemetry apps: usually *don't care*; files: *must* care

> Notes — The contract's fine print. quiz W09 Q4 asks the two TCP behaviors UDP avoids + the cost — this slide is the setup.

### Slide 10 — Who chooses UDP

| App | Why UDP |
|---|---|
| DNS | one query, one reply — setup would double the cost |
| Live voice/video | late = useless; skip retransmit |
| Games | newest state beats complete history |
| QUIC | rebuilds reliability *its own way* (L23) |

> Notes — DNS is the canonical one (quiz-level). QUIC as the punchline: "UDP + done-right reliability = HTTP/3."

### Slide 11 — Worked example: seq/ack-free reading
- Capture excerpt (synthetic): 5 UDP datagrams, one lost
- Client's app-level counter jumps 3→5 — no transport complaint
- Where should retransmit live, if needed? (app)

> Notes — Contrasts with L18's slide-1 capture: TCP *would* have retransmitted. Same loss, two philosophies.

### Slide 12 — LAB-08 brief
- Pairs: echo server/client (LAB-08 spec), then a 10-line datagram logger
- Capture the datagrams; annotate the 4-tuples both ways
- Deliverable: working echo + annotated capture + port questions

> Notes — 50 min. The lab deliberately builds the *sending* half of L20's project — students will reuse this code.

### Slide 13 — Classroom questions
1. UDP has no handshake — what does the *first* datagram carry that TCP's SYN does?
2. Two clients use the same ephemeral port on different hosts — fine? Same host?
3. Where would you add sequence numbers — header or payload?

> Notes — Q2: fine across hosts (IP differs); same host = port collision at bind. Q3: payload — UDP header is fixed; L20 does exactly this.

### Slide 14 — Common misconceptions
- "UDP = unreliable, TCP = reliable" → *unordered, unacknowledged*; apps add what they need
- "UDP can't be fast AND correct" → QUIC/fEC prove otherwise (enrichment)
- "Ports make UDP secure" → ports are addressing, not access control (L25)

> Notes — The first misconception's correction ("no *built-in* reliability") is quiz-worded; drill the phrasing.

### Slide 15 — Summary
- 8-byte header; datagrams independent; app owns the rest
- Ports demux; the API is four syscalls
- Choose UDP when late beats lost — or when you'll rebuild reliability (L20)
- Next: the protocol that kept *its* promises since 1981 (L18)

> Notes — Recap by the absence list; students name what TCP adds (seq/ack/flags) — perfect L18 cold-open.

### Slide 16 — Exit question
Name the four UDP header fields, and one thing an app must add for ordered delivery.
*(LAB-08 due next session.)*

> Notes — Answer: ports, length, checksum; app adds seq numbers + reorder buffer. Exit slips feed W09 pool.

### Slide 17 — App-choice table (backup)
- DNS vs video vs file-sync on UDP: one line each with the deciding property
- Deploy during slide 10's plenary if the class splits on "why not TCP for DNS?"

> Notes — Backup for the recurring "DNS over TCP exists too" question — it does (truncation fallback); course-level note.

### Demonstration instructions (instructor)
- LAB-08: namespace pairs; `nc -u` fallback if Python stalls; capture on either side
- ITI: pre-test the lab's logger script on the teaching image; note any firewall-on-lab-router gotchas
- Capture beat: one lost datagram via a deliberately full queue (or narrate excerpt 11's synthetic loss — labeled)

### References for the deck
- RFC 768 (UDP)
- PD §5.1 (UDP), KR §3.3 (connectionless transport)
- LAB-08 package: [`../../labs/lab-08-udp-sockets/README.md`](../../labs/lab-08-udp-sockets/README.md)
