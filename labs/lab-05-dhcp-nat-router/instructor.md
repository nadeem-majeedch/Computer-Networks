# LAB-05 — Instructor Guide

## Setup (before session)
- ⚠ **Image caveat:** `udhcpc` comes from busybox; `dhclient` from isc-dhcp-client — the
  teaching image may have neither. Test T1 the week before; ship the `dhcp-request.py`
  Python scaffold (socket broadcast to 255.255.255.255:67, parse option 53) as the
  guaranteed path. The DHCP *server* side is the graded skill.
- Pre-build both captures for the offline route from your own working run.

## Solutions / expected values
- **Pre-lab 1:** Discover(client, bcast) → Offer(server) → Request(client, bcast) → Ack(server).
- **Pre-lab 2:** src IP (to its outside address), src port; remembers the 5-tuple to
  reverse-map replies.
- **Pre-lab 3:** client has no IP yet — broadcast MAC/IP is the only deliverable channel.
- **T2:** Discover/Request: src 0.0.0.0, MAC = client. Offer/Ack: src 192.0.2.1, option 53
  values 2 and 5 respectively.
- **T3:** ICMP *identifier* and sequence stay constant; only source IP changes (ICMP has no
  ports — the id is how NAT distinguishes flows; stateful tracking is in the conntrack table,
  visible with `nft list ruleset` + counters if you add them).
- **Post-lab 4 (L22):** at T1 (50%) the client unicasts a renewal; server down → keeps using
  the lease; at T2 (87.5%) rebinds by broadcast; expiry → restarts discovery.

## Common failure modes
1. dnsmasq started without `--no-daemon &` pattern and students think it died. Show
   `pgrep dnsmasq`.
2. Missing default route on client → ping fails after NAT is configured; students blame
   NAT. Diagnose with `ip netns exec client ip route`.
3. Capturing only after the ping finished → empty files; remind: start captures first.
4. Two pairs using the same netns names → "weird cross-pings". Teardown helper between pairs.

## Grading notes
- Correct results (40): DORA annotation table (option 53 per message) + the two-capture
  translation pair (inside/outside files submitted).
- Analysis (30): post-lab 1 must name both changed fields; post-lab 3 must address the
  reply-path problem (state).
- Reproducibility (20): dnsmasq config + nft ruleset pasted verbatim.
- The Python-scaffold DHCP client is fully acceptable; there is no bonus for udhcpc.
