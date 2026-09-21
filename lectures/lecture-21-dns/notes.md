# Lecture 21 — Instructor Teaching Notes
## DNS: The Internet's Directory (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4 primary; CLO7 supporting |
| Textbook anchor | KR §2.4; RFC 1034/1035 |

---

## 1. Objectives hook
Board: **"8.8.8.8 answers billions of questions per second, most of them 'where is
X?'. No central list exists. How does ANY query find its answer?"**

Hook (2 min): `dig +short example.com` on the projector — 12 letters of command,
hundreds of milliseconds, possibly three servers consulted. "By the end you can name
every hop."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L20 project check-in (1 min); dig teaser |
| 6–26 | Concept 1 | Namespace, hierarchy, zones, delegation |
| 26–48 | Concept 2 | Resolution: recursive vs iterative; caching & TTL |
| 48–60 | Concept 3 | Record types; `dig` anatomy (live) |
| 60–63 | Break | — |
| 63–85 | GA-21 | dig drills + resolution capture, pairs |
| 85–100 | Concept 4 | Failure modes: NXDOMAIN, negative caching, split brain |
| 100–112 | Security preview | Spoofing/hijacking; DoH/DoT; DNSSEC concept |
| 112–118 | Summary + exit ticket | — |
| 118–120 | Preview | DHCP deep-dive (the "other" directory) |

## 3. Concept walkthrough

### 3.1 Namespace & delegation (20 min)
- **Tree:** root (`.`) → TLDs (com/org/pk/…) → domains → subdomains. Case-insensitive,
  dots separate labels; max 255 B names, 63 B labels.
- **Zones = delegation units:** a zone is the part of the tree a server is
  authoritative for; NS records *delegate*: "ask the com servers", "ask
  example.com's nameservers". Delegation is what makes the system *distributed
  without a central list* — the answer to the hook question.
- **Authoritative vs recursive:** authoritative servers *own* answers for their
  zones; recursive resolvers (8.8.8.8, your ISP's, 1.1.1.1) do the legwork on your
  behalf and cache.
- Simplified-model flag: root server "a-m" are not 13 boxes but anycast *farms*;
  nameservers have IPs known out-of-band (the "root hints" bootstrap problem —
  resolved by shipped hint files, a lovely chicken-and-egg aside).

### 3.2 Resolution & caching (22 min, the spine)
- **Recursive vs iterative (define precisely):** the *stub* (your OS) asks the
  *recursive resolver* (recursive mode: "get me the answer"); the resolver's walk
  *down the tree* is iterative (each server says "try this referral").
- **The walk (board trace for `www.example.com`):** stub → resolver (cache?) →
  root (referral: com NS) → TLD (referral: example.com NS) → authoritative
  (answer: A record) → cached → answer. Each hop costs an RTT (L03's journey
  math returns!).
- **Caching:** every hop caches per **TTL**; TTL = the publisher's *speed-vs-load*
  dial (300 s common; 60 s for failover-heavy records; 86400 for static). Long TTL
  = fast+cheap but slow to change; short TTL = chatty but agile — a real
  engineering trade-off students can argue.
- **Negative caching:** NXDOMAIN answers are cached too (RFC 2308) — a typo'd domain
  can stay "missing" for a while *after* it's fixed; classic support-desk mystery.

### 3.3 Records & dig (12 min)
| Type | Meaning | Example |
|---|---|---|
| A / AAAA | v4 / v6 address | example.com A 93.184.216.34 |
| CNAME | alias → another name | www → example.com |
| MX | mail exchanger (+priority) | 10 mail.example.com |
| NS | delegation | ns1.example.com |
| TXT | free text (SPF, verification, DoH metadata) | "v=spf1 …" |
| SOA | zone metadata (serial, refresh, TTLs) | — |
- `dig` anatomy live: QUESTION/ANSWER/AUTHORITY/ADDITIONAL sections; flags (aa, ra);
  TTL countdown; `dig +trace` performs the iterative walk *in front of the class*
  (the reveal moment).

### 3.4 Failure modes (15 min)
- **Split brain / split-horizon:** internal names resolve only internally — is it a
  bug or a feature? (Feature, until it breaks your VPN.)
- **Wrong NXDOMAIN handling by resolvers/ISPs** (search-domain pollution); captive
  portals hijacking NXDOMAIN — real-world weirdness students will meet.
- **Glue records** (delegation circularity: nameserver *inside* its own zone) —
  one-minute aside, satisfies the "how does that even work" student.

### 3.5 Security preview (12 min)
- The directory is *trusted infrastructure*: spoofing answers (off-path guessing
  port/TXID — historically feasible), cache poisoning (Kaminsky-style: flood fake
  referrals to cache a bogus record), registrar hijacking (social/credential — the
  record *ownership* attack).
- Defenses: randomization (source port + TXID — why the L17 demux aside matters),
  **DNSSEC** (signs records — chain of trust from root; concept only: validate the
  chain, don't encrypt), **DoH/DoT** (encrypt stub↔resolver — privacy/integrity on
  that hop; changes network management: DNS becomes invisible to local admins —
  honest trade-off discussion).
- Ethics gate restated: no spoofing demos against real resolvers; GA-26 does
  concept-level work in the VM lab only.

### Reference diagram — Recursive vs iterative DNS lookup

```text
stub ──recursive──→ resolver ──iterative──→ root        (.com NS)
                    resolver ──iterative──→ .com NS     (authoritative)
                    resolver ──answer + TTL──→ stub     (then cached)
```

## 4. Important definitions
Namespace · TLD · Zone · Delegation · NS record · Authoritative vs recursive
resolver · Iterative vs recursive query · Referral · TTL · Caching · Negative
caching · NXDOMAIN · Glue records · Anycast (named) · DoH/DoT (named) ·
DNSSEC (concept) · Cache poisoning (named).

## 5. Real-world examples
- **"It works on my phone but not my laptop"** = different resolvers + caches:
  `dig @1.1.1.1` vs `dig @<isp-dns>` — students can *see* split answers.
- **CDN geography:** same name, different A records per resolver location (L03's
  geodns teaser resolved) — DNS as traffic engineering.
- **The day a TLD broke** (registry outage headlines): every site under it
  vanishes *for cached users only after TTL* — TTL arithmetic made news.

## 6. Mathematical/technical example
Latency budget (L03 revisited, now precise): uncached resolution = up to 3 RTTs
(root, TLD, authoritative) + answer: at 40 ms each ≈ 120 ms *before* TCP can even
SYN. With a warm cache: ~0. Extension: TTL 300 s with 100 queries/s = 30,000
answer-queries upstream per TTL window... actually 1 upstream fetch per 300 s →
0.33 QPS upstream per cached name — cache math that explains resolver economics.

## 7. GA-21: drills + capture (22 min)
Worksheet: (a) `dig +short`, `dig +trace`, `dig -x` (reverse), `dig MX` on 4 domains;
(b) capture a first-contact resolution (flush local cache: `resolvectl flush-caches`
or restart dnsmasq on VM) and mark the referral chain in the trace; (c) answer the
"who cached what, for how long" questions. ⚠ Verify lab network permits outbound
UDP/53; else use the provided pcap + offline dig against a local dnsmasq.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "There's a central DNS database" | Delegation tree; no global list; root only knows TLDs |
| "Recursive resolver IS authoritative" | Legwork vs ownership; caching blurs but doesn't merge them |
| "CNAME chains resolve instantly" | Each alias = another lookup (cached, but real cost) |
| "TTL is how long *your* resolver keeps it" | Any hop may cache up to TTL; publishers can't force eviction |
| "DNSSEC encrypts DNS" | It signs (integrity/origin); DoH/DoT encrypt (privacy) — orthogonal |
| "DNS only runs on UDP 53" | UDP first; TCP for large/secure answers (DNSSEC, zone transfers) |

## 9. Suggested practical demonstration
`dig +trace www.wikipedia.org` projected (the walk made visible), then the same name
via `dig @1.1.1.1` (one RTT) — the caching story in two commands. ⚠ Verify outbound
53; pre-run to have output as backup.

## 10. Classroom activities
- **Referral relay:** 4 students (stub/resolver/root/TLD/auth) pass a "query" card
  with referral arrows — the walk, kinesthetic, 3 minutes.
- **TTL debate:** "Your site fails over between data centers — TTL 300 or 60?"
  Teams argue load vs staleness; instructor reveals the failover SLA math.

## 11. Problem-solving questions
1. Why can't the root server answer "where is www.example.com" directly?
2. TTL 60 vs 3600: name one cost and one benefit of each.
3. Your resolver returns NXDOMAIN for a domain that works for a friend. Three
   hypotheses + one test each.
4. Why did randomizing UDP source ports harden DNS? (connects L17's demux)
5. A user's DNS works but HTTPS fails. What did DNS *not* do for them? (resolved
   name ≠ service up — diagnostic boundary L29 formalizes)

## 12. Formative assessment (with answers)
- MCQ: An NS record's job → **delegate a zone**.
- MCQ: The resolver's walk down the tree is → **iterative**.
- MCQ: Negative caching caches → **NXDOMAIN answers**.
- Short: one thing DNSSEC gives and one it doesn't. → integrity/origin; not
  confidentiality.

## 13. Exit ticket
1. Order the walk: authoritative / stub / root / resolver / TLD: ________
2. A / AAAA / CNAME / MX mean: ________
3. DoH encrypts DNS between ________ and ________.

## 14. Anticipated difficulties
- Recursive-vs-iterative is a vocabulary trap (the *same* resolver acts
  recursively to stubs, iteratively upstream) — the relay activity fixes it;
  don't skip.
- `dig` output density overwhelms; teach the 4 sections as a map first.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify outbound UDP/53 or prepare offline pcap + local dnsmasq variant
- [ ] Pre-run `dig +trace` on 2 domains; capture screenshots
- [ ] Print GA-21 worksheets; prepare referral-relay cards
- [ ] Board pre-write: tree diagram; walk sequence; record-type table

## 16. Timing fallbacks
Drop glue records and split-horizon (§3.4) to reading; the walk + GA-21 are
protected; security preview can compress to DoH/DoT only (DNSSEC one sentence).

## 17. References
- KR §2.4; RFC 1034/1035 (DNS); RFC 2308 (negative caching); RFC 8484 (DoH),
  RFC 7858 (DoT); RFC 4033-4035 (DNSSEC family — concept citations).
- `dig` (BIND 9) documentation; dnsmasq docs (lab resolver).
- ⚠ VERIFY editions/sections this semester.
