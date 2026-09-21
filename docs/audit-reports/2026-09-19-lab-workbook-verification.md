# Laboratory Workbook Verification Report — 2026-09-19

| Field | Value |
|---|---|
| Phase | Lab workbook build: `labs/` (16 labs, 51 files incl. syllabus, setup guide, index) |
| Auditor / verifiers | `tools/scripts/audit_labs.py` (9 checks) · `tools/scripts/check_lab_syntax.py` (fenced-command syntax) · `tools/scripts/check_lab_env.py` (host tool inventory) |
| Result | **Lab audit: 9 PASS / 0 WARN / 0 FAIL · Syntax: 36 PASS / 0 FAIL / 0 SKIP** |
| Regression | Lectures 13 PASS + 1 WARN (slides pending) · Foundation 15 PASS — no regressions |
| Scope of change | `labs/**` (51 files), `tools/scripts/audit_labs.py`, `tools/scripts/check_lab_syntax.py` (new), `tools/scripts/check_lab_env.py` (new) |
| Status | Draft v0.1 — awaiting instructor review |

---

## 1. Executive summary

The workbook contains 16 lab triads (student README, instructor guide, worksheet) plus a
syllabus/safety document, environment setup guide, and index. Structural checks, lab↔lecture
alignment, graded-set consistency with the assessment strategy, safety wiring, and
command-syntax verification all pass.

**What this report does NOT claim:** no lab has been *executed*. Every "expected
observation" in the workbook is derived from tool semantics and standards (named as such in
each lab) — not from captured transcripts. The authoring host is a Windows machine without
a Linux lab environment; executing the labs is an instructor run-through task before first
delivery (§5).

## 2. Verification performed (actual results)

### 2.1 Structure and alignment — `audit_labs.py` (9/9 PASS)

| Check | Result | Evidence |
|---|---|---|
| 16 complete triads, none empty | PASS | 48 files across `lab-01…lab-16` |
| Required elements | PASS | outcomes, pre-lab, tasks, expected observations, troubleshooting, post-lab, challenge, accessibility, safety; instructor solutions + failure modes + grading notes; worksheet pre/post sections |
| Element substance | PASS | ≥3 tasks, ≥2 pre-lab + ≥3 post-lab questions per lab; non-trivial worksheets |
| Lab↔lecture alignment | PASS | all anchor lectures exist in `schedule-32-lectures.md`; every graded/project lab referenced by ≥1 lecture README |
| CLO references | PASS | all 16 labs cite CLO1–8 only |
| Graded-set consistency | PASS | 12 graded-pool rows + LAB-10/11 project (10%) + LAB-15/16 optional; matches `assessment-strategy.md` §3 (13 deliverables, drop lowest) |
| Safety/ethics wiring | PASS | all 16 labs cross-reference `syllabus-safety.md` §3; isolation, no-external-probing, and acknowledgment-gate rules present |
| No fabricated output | PASS | expected observations phrased as expectations/tool semantics (machine-checked phrasing; human re-read still advised) |
| Labs index links | PASS | 16 links resolve; 16-row inventory |

### 2.2 Command syntax — `check_lab_syntax.py` (36/36 PASS)

Every fenced `bash` (33) and `python` (3) block in `labs/**/*.md` parsed with
`bash -n` / `ast.parse` on this host.

**Real defects this check caught and fixed** (the reason the pass exists):

1. **2 hard syntax errors** — unquoted `<placeholder>` tokens in runnable-looking blocks
   parsed as file redirections (`ping -c 20 <gateway-ip>` → input-redirect from a file
   named `gateway-ip`, then a dangling `>`). Files: `lab-01…/README.md:31`,
   `lab-06…/README.md:55`.
2. **8 silent traps of the same class** (`iperf3 -c <peer>`, `tcpdump -i <link>`,
   `iw dev <wifi-iface>`, OpenVPN `--remote <peer-wan-ip>`, …) that *parse* but would
   misbehave at runtime. All 10 fixed by quoting (`'<gateway-ip>'`), the standard
   lab-manual convention: substitute or fail loudly with a name-resolution error.
3. A **checker false-positive class**: on Windows, PATH-first `bash` is the WSL stub,
   whose launcher errors initially masqueraded as 33 content FAILs. The checker now
   probes for a working interpreter (also honoring a `CNLAB_BASH` override), treats an
   unusable bash as SKIP — never as content failure — and warns on any *remaining*
   unquoted placeholder pattern.

Final state: `Syntax PASS: 36 · syntax FAIL: 0 · SKIP: 0 · placeholder WARNs: 0`.

### 2.3 Host tool inventory — `check_lab_env.py`

Ran on the authoring host: 14 tools MISSING with pointers to `setup-environment.md` —
correct, honest behavior for a non-lab machine (it is a report, not a gate). On lab VMs it
should show the teaching image as ready; instructors should have students paste its table
into LAB-01's environment record.

## 3. Lab-to-lecture alignment (summary)

| Lab | Anchor lectures | Notes |
|---|---|---|
| LAB-01 | L04 | measurement foundations |
| LAB-02 | L08–L09 | switching, VLANs |
| LAB-03 | L10–L11 | Wi-Fi fundamentals, LAN security |
| LAB-04 | L13–L16 | subnetting → routing check (5% instrument) |
| LAB-05 | L14 | DHCP + NAT |
| LAB-06 | L15 | dual stack |
| LAB-07 | L16 | static routing, traceroute |
| LAB-08 | L17 | UDP sockets |
| LAB-09 | L19 | TCP under netem |
| LAB-10/11 | L20 (demo W12) | reliable transport project (10%) |
| LAB-12 | L23 | HTTP versions, TLS, SMTP/SSH |
| LAB-13 | L25 | firewall + VPN |
| LAB-14 | L29 | monitoring, fault injection |
| LAB-15 | L24–L26 | optional security analysis |
| LAB-16 | L31–L32 | optional design rehearsal |

The lecture-layer machine check (every graded lab referenced from ≥1 lecture README) passes;
conversely, `audit_lectures.py` verifies all LAB references in lectures fall in LAB-01…14.

## 4. Privilege / OS / hardware dependencies (task-required identification)

| Dependency | Affects | Alternative provided |
|---|---|---|
| Root (`sudo`) + Linux namespaces (`ip netns`, `tc`, bridges, `nftables`) | LAB-02, 05, 06, 07, 08, 09, 13, 14, 15 | lab VM image (setup guide, route C); offline pcap route for observation-only tasks |
| Physical Wi-Fi adapter + monitor-mode-adjacent tools (`iw`) | LAB-03 | campus/offline survey analysis; instructor demo capture |
| GNS3 (optional GUI simulator) | LAB-07 (optional) | pure-namespace topology is the default |
| Packet Tracer (optional, licensing) | LAB-02 visualization only | not required anywhere |
| Internet access | none required | all demos loopback/namespace-local; captures offline |

All attack-technique content (LAB-15) runs exclusively against course-owned namespaces or
offline captures; no external systems are probed (`syllabus-safety.md` §3, audit-checked).

## 5. Honest limitations / instructor to-do before delivery

1. **No lab has been executed end-to-end.** An instructor must run each lab once on the
   teaching image (especially LAB-02's `vlan_filtering` bridge stack, LAB-05's
   `dnsmasq`/`nftables` versions, and LAB-09's netem figures) and adjust version-specific
   details. The syntax pass verifies parsing, not runtime semantics.
2. **Numerics are desk-checked, not machine-verified** (e.g., LAB-09's RTT/throughput
   figures, LAB-04 subnet tables). One human spot-check each before first delivery.
3. Version drift risk: tool flags (`ss`, `tc`, `nft`) vary across distributions; the
   troubleshooting tables name the likely culprits but cannot anticipate every image.
4. The slide-deck WARN from the lecture phase applies to labs' companion briefings too.

## 6. Conclusion

Workbook structure, alignment, safety wiring, and command syntax: verified green. Runtime
behavior: deliberately *not* claimed — it is the documented pre-delivery instructor task.
Nothing in this report should be read as evidence any lab command was executed.
