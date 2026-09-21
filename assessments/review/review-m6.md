# Module 6 Review Questions (L24–L26)

| Field | Value |
|---|---|
| Coverage | L24 security principles & crypto building blocks · L25 firewalls, segmentation & VPNs · L26 attack & defense case workshop |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · LAB-13 · GA-24 · Cases PB-047…PB-052 |

## Questions

### L24 — Security principles & cryptographic building blocks
1. [B|CLO7] Match: (i) tamper-evident ledger, (ii) sealed envelope, (iii) notarized
   signature — to hash, encryption, or digital signature.
2. [I|CLO7] Symmetric vs asymmetric: which protects bulk data and which bootstraps
   trust, and why the split?
3. [I|CLO7] What does a TLS certificate actually bind, and who vouches for the binding?
4. [I|CLO7] Name the two properties a password-hashing scheme needs beyond a plain
   hash (salt, work factor) and what each defeats.

### L25 — Firewalls, segmentation & VPNs
5. [I|CLO7] Default-deny vs default-allow: which is the defensible baseline and why,
   in one sentence?
6. [I|CLO7] Zone-based segmentation: staff, servers, guests, IoT. State the minimum
   permit set for guests and the default for IoT→any.
7. [I|CLO7] Site-to-site VPN: what exactly is encrypted, and what do observers still
   learn?
8. [I|CLO7] NAT vs firewall: which alters addressing, which alters reachability, and
   where they overlap in home routers.

### L26 — Attack & defense case workshop
9. [I|CLO7] Classify: (i) ARP poisoning, (ii) DNS spoofing on-path, (iii) credential
   phishing — by required attacker position (off-path/on-path/local).
10. [I|CLO6] For the on-path DNS attack: name the control that most directly raises
    the attacker's bar and why.
11. [I|CLO7] Defense-in-depth: give one control per layer (human, L2, L3, transport,
    application) against unauthorized access to a server.
12. [I|CLO6] During the workshop your detection rule flags 200 events/hour with 2 true
    positives. Name the tuning problem and one principled fix.

---

## SELF-CHECK KEY — attempt first, then verify

1. (i) hash (tamper-evident digest), (ii) encryption (confidentiality envelope),
   (iii) digital signature (notarized authenticity/integrity).
2. Symmetric: bulk data (fast per byte). Asymmetric: bootstraps trust/keys without a
   pre-shared secret; too slow for bulk, so it protects only the handshake.
3. A name ↔ public key binding; a CA vouches by signing the certificate (trust
   anchored in the client's trust store).
4. Salt: defeats precomputed/rainbow-table attacks (per-user unique input). Work
   factor: makes brute force cost-prohibitive per guess (slow hashing per attempt).
5. Default-deny: every flow must be justified by an explicit rule, so unanticipated
   services stay unreachable — the safe failure mode.
6. Guests: permit DNS/DHCP + internet egress only (HTTP/HTTPS); default IoT→any: deny
   (IoT gets narrow, explicit exceptions if any).
7. Inner IP packets are encrypted/authenticated between sites; observers learn outer
   headers — the two public endpoints communicate, timing/volume, nothing inner.
8. NAT alters addressing (rewrites IP/port); firewall alters reachability (permits/
   denies flows). Home routers overlap by doing both on one box — translation plus
   implicit inbound filtering.
9. (i) ARP poisoning: local/on-link attacker. (ii) DNS spoofing on-path: attacker who
   can see/inject along the path. (iii) Phishing: off-path — no network position
   needed, only user deception.
10. DNSSEC (signed records): forged responses fail validation — raises the bar from
    "inject a packet" to "forge a signature chain."
11. Human: training/least-privilege accounts; L2: port security/802.1X; L3: ACLs/
    segmentation; transport: stateful firewall on 22/3389 etc.; application:
    authentication + patching. One per layer suffices.
12. False-positive-dominated alerting (low precision): raise the evidence threshold,
    correlate with a second signal, or scope the rule (asset/time) — any principled
    tuning accepted.
