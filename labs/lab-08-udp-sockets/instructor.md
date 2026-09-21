# LAB-08 — Instructor Guide

## Setup (before session)
- Ship `lab08-skeleton.py` + this README's server/client as runnable starting points.
- Pre-test T4 on the teaching kernel: ICMP-driven socket errors are platform-dependent —
  on Linux, an ICMP port-unreachable typically surfaces as `ConnectionRefusedError` on the
  *next* send/recv for connected sockets; unconnected `recvfrom` may just time out.
  ⚠ Record your kernel's actual behavior once and use it as the reference answer.

## Solutions / expected values
- **Pre-lab 1:** any datagram with dst port 5000; demux key (src IP, src port, dst IP,
  dst port).
- **Pre-lab 2:** 8 bytes — src port, dst port, length, checksum.
- **Pre-lab 3:** any of ACK/retransmit/ordering/dedup; e.g. gaming/VoIP/DNS favor UDP.
- **T1:** first captured packet is a data-bearing UDP datagram; no handshake.
- **T2/T3:** after `seq|ack` + timeout retransmit ×3, forced server-death yields exactly
  3 attempts then a clean failure — students must show the count in their log.
- **Post-lab 1:** key = (192.0.2.x, ephemeral, 192.0.2.22, 5000); the reply works because
  the server reads the *sender's* address from `recvfrom` and sends back to it — no client
  bind needed (the OS picked the client's ephemeral port at first sendto).
- **Post-lab 2:** added: per-datagram ACK + timeout retransmit; still missing: ordering,
  dedup, flow/congestion control (any two named precisely = full credit).
- **Post-lab 4:** no — it's a *signal* that nobody was listening at that instant; the
  datagram is still not acknowledged, delivered-once, or ordered.

## Common failure modes
1. Pairs splitting server/client on one machine with 127.0.0.1 and capturing the wrong
   interface (capture on `lo` in single-machine mode).
2. Payload format drift ("ack: " prefix vs `ack|seq`) breaking T3 parsing — enforce one
   format per pair before the demo.
3. Students "fix" T3 by catching the timeout and looping forever — the 3-attempt cap is
   the graded behavior.

## Grading notes
- Demo (in session): live run of T2+T3 with capture visible; 60 s per pair.
- Correct results (40): seq/ack format + 3-attempt log + T4 ICMP record.
- Analysis (30): post-lab 1–2 with ladder vocabulary from L17.
- Reproducibility (20): both .py files + capture file submitted (`LAB08-task1-evidence.pcapng`).
- Challenge (window of 3) is a natural LAB-10/11 on-ramp — mention it in session.
