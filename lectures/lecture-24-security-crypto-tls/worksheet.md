# Lecture 24 — Worksheet (GA-24) & Exit Ticket

Name: ________________  Date: ______

## Part A — Certificate chain (pairs, 10 min)
From the provided chain (course VM):
1. Leaf subject + SAN entries: ________
2. Intermediate issuer: ________ 3. The trust anchor is: ________
4. What exactly did the intermediate sign? ________
5. One sentence: why does swapping a byte in the leaf break verification? ________

## Part B — TLS 1.3 dissection (pairs, 12 min)
From the provided capture:
6. ClientHello's key_share = ________ (which pattern from class?) ________
7. The encryption boundary starts after ________.
8. CertificateVerify appears in flight ________.
9. How many round trips to first application data? ________
10. SNI value (and its privacy caveat): ________

## Exit ticket (3 items)
1. MAC provides ________ + ________; a signature provides ________ + ________.
2. The four-step secure-protocol template: ________
3. Forward secrecy means: ________
