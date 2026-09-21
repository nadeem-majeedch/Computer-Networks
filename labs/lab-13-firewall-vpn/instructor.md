# LAB-13 — Instructor Guide

## Setup (before session)
- Ship `lab13-build.sh` (topology) so pairs spend time on policy, not plumbing; test the
  OpenVPN static-key flow on the teaching image (its `--cipher` default era matters ⚠ —
  pin AES-256-GCM as in the README to avoid cipher-negotiation surprises).
- Pre-capture `lab13-before.pcapng` / `lab13-vpn.pcapng` for the offline route.

## Solutions / expected values
- **Pre-lab 1:** stateful — it consults the connection table for replies.
- **Pre-lab 2:** adds confidentiality/integrity on the path; does not fix endpoint
  compromise or bad internal policy.
- **T2:** hostB→hostA fails (no new-flow rule); its *replies* to hostA's flows pass via
  established. Counter output = blocked evidence.
- **T3:** without the established rule the reply is a "new" flow in the wrong direction —
  dropped by policy; `ct state established` checks the conntrack entry (direction, state,
  addresses/ports of an existing flow).
- **T4:** WAN shows UDP ciphertext between firewall WAN IPs; inner headers invisible —
  only size/timing leak. Post-lab 3 answers must cite their own capture pair.
- **Post-lab 4:** advantage: no PKI/setup simplicity; weakness: static shared key, no
  per-node identity/revocation — production uses TLS-based modes with proper key mgmt.

## Common failure modes
1. Students firewall the WAN link only and forget the inside hook — pings die for the
   wrong reason; make them *predict the drop point* before testing.
2. OpenVPN `--daemon` hides errors — first launch runs foreground until it works.
3. Route misses put traffic outside the tunnel (T4 symptom table covers the diagnosis).

## Grading notes
- Correct results (40): T2 pass/drop matrix + T4 capture pair.
- Analysis (30): policy table quality (rule/attack/cost columns) + post-lab 3 (what stays
  visible over VPN).
- Reproducibility (20): `nft list ruleset` verbatim + key-generation command (not the key).
- Clarity (10): asymmetry explanation (T2) is the canary for real understanding.
