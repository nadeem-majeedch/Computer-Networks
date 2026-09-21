# LAB-12 — Application Protocols on the Wire: HTTP/1.1, HTTP/2, HTTP/3 + TLS/SSH

| Field | Value |
|---|---|
| Anchor lectures | L23 (application protocols), L24 (TLS preview) |
| CLOs | CLO4 (packet analysis), CLO7 (security awareness) |
| Assessment | Graded lab deliverable (individual; 15% pool) — worksheet + capture evidence |
| Mode / duration | Individual; 2-h session + 48-h window |
| Environment | VM with internet (NAT) or offline bundle; tools: `curl`, `tshark`, `openssl s_client` |

## Learning outcomes
1. Capture and compare HTTP/1.1, HTTP/2, and HTTP/3 transfers: transport used, connection
   reuse behavior, visible header differences.
2. Explain HTTP/3's transport change (QUIC over UDP) from *your capture* — no TCP
   handshake, no TCP retransmits; identify QUIC's UDP pattern.
3. Read a live TLS certificate chain with `openssl s_client` and name its components.
4. Dissect a course-provided SMTP/SSH exchange offline and mark where plaintext ends.

## Pre-lab
1. HTTP/1.1 keep-alive vs HTTP/2 multiplexing: one sentence each (L23).
2. Which transport does HTTP/3 use, and what does that change about "connection setup"?
3. In TLS (L24 preview): what does the certificate *prove*, and to whom?

## Tasks

### T1 — HTTP/1.1 on the wire (20 min)
```bash
sudo tcpdump -i any -nn -w lab12-http11.pcapng 'tcp port 80' &
curl -v http://neverssl.com/ -o /dev/null     # plain-HTTP teaching site
```
Annotate: DNS lookup, TCP handshake, GET, response, connection close (or reuse if you
fetch twice with the same `curl` session).
**Expected observation:** everything is plaintext — you can read your own GET in the
capture. (That is the security lesson too.)

### T2 — HTTP/2 vs HTTP/1.1 (20 min)
```bash
curl -sv --http2 https://cloudflare-quic.com/ -o /dev/null --trace-time
# capture TLS on 443 while it runs; compare frame types with tshark:
tshark -r lab12-h2.pcapng -Y "http2" -c 20
```
**Expected observation:** ciphertext everywhere (TLS), ALPN negotiation visible in the
handshake (`tshark -Y "tls.handshake.extensions_alpn"`), binary frames instead of
plaintext headers.

### T3 — HTTP/3 / QUIC pattern (20 min)
```bash
curl -sv --http3 https://cloudflare-quic.com/ -o /dev/null 2>&1 | grep -i "http/3" || \
  echo "curl lacks HTTP/3 on this image — use the offline bundle"
```
From the offline bundle (or your capture if the build supports it): identify UDP 443
flows, QUIC initial packets, absence of any TCP handshake for the same request.
**Expected observation:** one UDP flow carries connection setup + request streams.
⚠ External HTTP/3 endpoints change; the image's local fallback or the offline bundle is
the guaranteed path (setup-environment §8).

### T4 — TLS certificate chain (15 min)
```bash
openssl s_client -connect cloudflare-quic.com:443 -brief < /dev/null
openssl s_client -connect cloudflare-quic.com:443 < /dev/null 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates
```
Record: subject, issuer, validity window, and the chain order shown by `-brief`.

### T5 — SMTP & SSH, offline (15 min)
Course captures `lab12-smtp.pcapng` (a scripted local MTA exchange with synthetic
addresses) and `lab12-ssh.pcapng` (login to a lab VM, password redacted at capture).
Mark: SMTP commands visible in cleartext (`tshark -Y "smtp"`); SSH: where the banner ends
and binary packets begin; note that authentication payloads are invisible after KEX.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| No HTTP/3 curl support | distro build without QUIC | offline bundle route (by design) |
| Capture on `any` shows duplicated frames | multiple interfaces see the flow | acceptable for analysis; note it |
| `s_client` handshake fails in the lab | room intercepts TLS | use the provided `lab12-chain.txt` snapshot and say so |
| neverssl.com unreachable | outbound policy changed | use the image's local plain-HTTP server fallback ⚠ |

## Post-lab questions
1. From your captures: what does HTTP/1.1's connection handling cost on a 3-object page
   vs HTTP/2's single connection? (Arithmetic with RTT from LAB-01's habit.)
2. QUIC: name two things it must re-implement because it left TCP (and where you saw the
   evidence in your capture/bundle).
3. Your certificate: who vouches for whom, and what expires? What breaks on expiry?
4. SMTP vs SSH: what exactly does the encryption boundary hide in each?

## Challenge (ungraded)
Fetch the same page via HTTP/1.1 (cabled capture) and HTTP/3 (bundle) and compare
*connection-setup packet counts*. Explain the difference using L18's handshake + L24's
TLS handshakes layered on top.

## Accessibility / low-resource alternatives
- The offline bundle (`lab12-http11.pcapng`, `lab12-h2.pcapng`, `lab12-h3.pcapng`,
  `lab12-smtp.pcapng`, `lab12-ssh.pcapng`, `lab12-chain.txt`) makes the entire lab
  analysis-only; T1–T5 questions unchanged.
- tshark commands throughout; no GUI needed. Plain-text chain snapshot for T4.

## Safety notes
Fetches target public teaching sites with synthetic data only (syllabus-safety §3.4);
no credentials transmitted — synthetic logins in provided captures, password redacted
at capture time. No active probing of any external host (§3.2).
