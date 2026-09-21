# LAB-12 Worksheet

Name: ________________  Date: ______  Environment table: ______
Data source used: ☐ live captures ☐ offline bundle (list files used): ______________

## Pre-lab
1. keep-alive: ______________________ multiplexing: ______________________
2. HTTP/3 transport: ______ ; what changed about connection setup: ______________
3. A certificate proves: ______________________ to whom: ______________________

## T1 — HTTP/1.1
| Event | Packet # | Note |
|---|---|---|
| DNS | | |
| TCP handshake | | |
| GET | | |
| Response | | |
Your GET readable in cleartext? ☐ yes ☐ no (security lesson: __________)

## T2 — HTTP/2
ALPN value seen: ______ ; frame types in first 20 http2 records: ______________

## T3 — HTTP/3 / QUIC
UDP 443 flow seen? ☐ yes ☐ bundle ; TCP handshake present for same request? ☐
QUIC packet type identified: ______________

## T4 — Chain record
Subject: ______________________ Issuer: ______________________
Not before / not after: __________ / __________ Chain order (-brief): ______________

## T5 — SMTP & SSH boundaries
SMTP: cleartext commands observed: ______________________
SSH: plaintext ends after: ______ ; auth payload visible? ☐

## Post-lab (full answers in report)
1. 3-object page: HTTP/1.1 vs HTTP/2 cost arithmetic
2. Two things QUIC re-implements + your evidence
3. Chain: who vouches for whom; expiry consequence
4. SMTP vs SSH: what encryption hides in each
