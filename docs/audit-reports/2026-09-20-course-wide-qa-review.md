# Course-Wide QA Review — Computer Networks (2026-09-20)

| Field | Value |
|---|---|
| Reviewer | QA pass over all generated material (foundation → site phases) |
| Method | Full re-run of all 9 validation tools + targeted manual inspection of protocol passages, teaching quality, labs, cases, references |
| **Overall status** | **PASS WITH WARNINGS** |
| Content not committed/pushed | Confirmed — per project rules |

## 1. Validation commands executed (actual results)

| Command | Result |
|---|---|
| `python tools/scripts/audit_foundation.py` | **15/15 PASS** (link integrity, placeholders, schedule↔folders, nav) |
| `python tools/scripts/audit_lectures.py` | **14/14 PASS** (32 packages, required sections, CLO tags, slides=notes) |
| `python tools/scripts/audit_labs.py` | **9/9 PASS** (16 labs, safety, deliverables, lecture mapping) |
| `python tools/scripts/check_lab_syntax.py` | **Syntax PASS: 36 / FAIL: 0** (all fenced bash parses; `bash -n`) |
| `python tools/scripts/audit_casebank.py` | **10 PASS / 0 FAIL** (65 cases, difficulty ramp, evidence labels, lecture coverage) |
| `python tools/scripts/audit_assessment.py` | **12 PASS / 0 FAIL** (112 items, zero duplicate stems, exam mark-sums, tags) |
| `python tools/scripts/verify_assessment_numbers.py` | **All [MC] claims verified (99/99)** — subnet math via `ipaddress`, capacity/transport arithmetic recomputed |
| `python tools/scripts/calendar_lib.py --validate` | **21/21 PASS** (placement, holiday-shift invariant, milestones) |
| `python tools/scripts/build_site_docs.py` + `mkdocs build --strict` | **Clean build, 0 warnings** (301-file tree) |
| `python tools/scripts/validate_site.py` | **26/26 PASS** (config, subpath URLs, inventory, instructor-leak scan, nav↔files, HTML paths, workflow semantics) |

## 2. Findings

### Critical

**C-1 · Incorrect CRC worked examples in Lecture 06 (both files).**
`lectures/lecture-06-data-link-framing-errors/slides.md` (exit-question notes) claimed
message `111000`, generator `1011` → remainder **111**, codeword `111000111`; the notes'
board example claimed `101101`/`1101` → **100**, codeword `101101100`. Both are wrong and
the deck asserted "desk-checked … re-division yields 000," which is false. Verified by
polynomial division and an independent register model: true answers are **110**
(codeword `111000110`) and **010** (codeword `101101010`); only the corrected codewords
re-divide to remainder 0. **Fixed during this review** (values corrected, verification
note added, stale "desk-checked" claim replaced); worksheet's unanswered M=110101/G=1011
problem has true answer `111` → codeword `110101111` — key deliberately remains in
`notes.md` only, per template.
*Residual risk:* neighboring error-detection passages should get one instructor
re-derivation before first delivery (the earlier "desk-checked" language shows
manual verification claims cannot be trusted here).

### High

**H-1 · Demo/quality gates depend on a VM image that does not exist yet.**
`docs/lecture-template.md` gate: "Demo verified on the current VM image (date recorded)";
`docs/lab-strategy.md` requires SHA-256 publication; no `vm/` or image directory exists
in the repository. Consequence: first-semester delivery risk for demos and lab pacing.

**H-2 · Graded case bundles CS-01…CS-04 are referenced but not built.**
`docs/case-study-strategy.md` defines the longitudinal Meridian thread (CS-01 kickoff
L03; CS-02 due L16; CS-03 stages L23/L26/L29; CS-04 capstone L32), the assessment
strategy assigns them 10% + 15% (capstone), and several decks announce the kickoffs —
but no CS bundle files exist (only the 65-case PB practice bank). This is the largest
missing deliverable.

**H-3 · No real packet-capture assets in the repository (0 `.pcap`/`.pcapng` files).**
11 lecture decks reference "pre-captured"/"provided" traces; CS-01's vignette promises "a
small provided capture." All teaching transcripts are clearly labeled synthetic (the
case-bank audit enforces labeling; L21 DNS notes label its edited `dig` transcript), so
no fabrication is presented as real — but the instructor must create/capture these
assets before lectures that depend on them.

### Medium

**M-1 · Quiz-window discrepancy inside foundation docs** — `assessment-strategy.md` §2
says W4/W7/W10/W13; syllabus + schedule calendar say W4/W12. Carried through with an
explicit reconciliation note (calendar page, assessment README) rather than silently
resolved. Resolution is one instructor decision, then ~4 file edits.

**M-2 · Data-science contextualization is thin outside the case bank.** Explicit
DS framing exists in the 65-case bank (19 tagged cases incl. cluster/training-job
transfers) and L31's dedicated "data-science connection" segment — but most lecture
notes never mention DS contexts. Module 4 (transport) and L27/L29 would absorb DS
examples (e.g., AllReduce traffic, dataset sync) without changing the outline.

**M-3 · Textbook edition risk flagged, not resolved.** `docs/textbooks-references.md`
marks Kurose & Ross with "⚠ VERIFY: newer edition than 8th (2021)" — correct caution:
a 9th edition exists per the publisher as of drafting. Every edition-sensitive reading
in lecture decks carries the same ⚠ flag.

**M-4 · In-class worksheets lack per-item points/rubrics.** Lecture worksheets carry
CLO tags and exit tickets, but GA scoring guidance lives mostly in the assessment
package rubrics rather than per worksheet. Acceptable under the strategy (GA credit is
completion-based), but new TAs will ask.

**M-5 · Website accessibility is theme-default.** MkDocs Material provides structure,
keyboard nav, and reasonable contrast out of the box, and headings/landmarks are
generated correctly — but no manual screen-reader pass or contrast audit has been
performed (not possible in this environment). Recorded as untested, not as failing.

### Low

**L-1 · Two directory-style links in `lectures/README.md` (L30/L31 rows)** build with an
INFO note (MkDocs does not validate them; they resolve correctly in browsers).
Normalization to `.md` targets would silence the INFO.

**L-2 · `mkdocs serve` (dev server) returned 404s for subpages in this environment**
while the built output is complete and correct under static serving (the mode GitHub
Pages uses). Instructor should sanity-check `mkdocs serve` locally; the deployed site
is unaffected.

**L-3 · `site-src/calendar.md` sample config block** shows a hypothetical holiday date
(`2026-11-09`) as an example only — clearly commented as an example, no risk, but worth
remembering when copying the block verbatim.

**L-4 · `classful addressing` appears in the master schedule's L12 topic string**
("classes→CIDR history") while the L12 package teaches prefix notation without the
classful detour. Harmless (history framing), but the schedule wording could match the
taught content.

## 3. Areas verified clean (manual inspection)

- **Terminology consistency**: PDU names, DORA, CSMA/CD vs CA, recursive vs iterative
  DNS, SLAAC/fe80::/10, /64 convention, NAT port rewrite + table semantics, stateful
  firewall semantics, TIME_WAIT framing, QUIC-over-UDP — spot-checked across decks and
  notes; no contradictions found.
- **TCP handshake numbers** (L18): SYN seq=1000 → SYN,ACK seq=5000 ack=1001 → ACK
  seq=1001 ack=5001; SYN-consumes-one-byte explained — correct.
- **Shannon/Nyquist forms** (L05, assessment bank): C=2B·log₂M and C=B·log₂(1+SNR)
  stated correctly; all bank numbers machine-verified.
- **Labs**: DOCIX documentation ranges (192.0.2.x etc.) used in lab-02; netns commands
  well-formed (36/36 bash parse); `sudo` scoped; no attack tooling (nmap/aircrack/
  hping/masscan) anywhere in labs; L26 attack content framed as walkthrough + defense.
- **Case bank**: 65/65 labeled synthetic evidence; difficulty ramp enforced by audit;
  instructor sections present in every case file.
- **References**: RFCs cited are real and current-generation (9293 TCP, 8200 IPv6,
  8446 TLS 1.3, 9110/9112/9113/9114 HTTP suite, 9000 QUIC, 2131 DHCP, 3022 NAT, 826
  ARP, 1034/1035 DNS); the ICMPv6/4443 footnote correctly self-corrects an older
  row; standards bodies (IEEE 802.3/802.1Q/802.11/802.1X, IANA, ICANN) correct.
- **Website**: strict build, 26/26 checks, no instructor leakage on the student tree,
  canonical subpath URL, current action versions (checkout@v4, setup-python@v5,
  configure-pages@v5, upload-pages-artifact@v3, deploy-pages@v4), deployment docs
  present (`docs-meta/github-pages-deployment-report.md`).

## 4. Not run (environment limitations)

| Item | Reason | Suggested manual verification |
|---|---|---|
| Browser rendering / layout pass of the site | No GUI in this environment | Open the deployed site; eyeball nav, tables, Mermaid diagrams on desktop + mobile |
| Mermaid diagram render check | No renderer available (syntax-audited only) | Load any lecture deck page; confirm diagrams draw |
| Screen-reader / contrast audit | No assistive tech | Run axe/Lighthouse once on the deployed URL |
| Lab commands executed on a live VM | No lab hypervisor; VM image unbuilt (H-1) | Instructor run-through per the lab-strategy checklist |
| External-link liveness (RFC/IEEE URLs) | Network fetches out of scope for this pass | `linkchecker` or manual spot-open |
| Deployment itself | Explicitly out of scope; requires user's push + Pages settings | Follow `docs-meta/github-pages-deployment-report.md` §7 |

## 5. Files affected during this review

| File | Change |
|---|---|
| `lectures/lecture-06-data-link-framing-errors/slides.md` | CRC exit-question answer corrected (110 / `111000110`); false verification claim replaced |
| `lectures/lecture-06-data-link-framing-errors/notes.md` | Board-example remainder/codeword corrected (010 / `101101010`); QA note added; post-fix re-division verified |

All nine validation tools re-run **after** these edits: green (table §1).

## 6. Recommended correction order

1. **Decide the quiz-window question (M-1)** and propagate to ~4 files — one-time.
2. **Build the CS-01…CS-04 graded bundles (H-2)** — the only content gap that affects
   the published assessment plan.
3. **Build/capture the teaching-asset set (H-1, H-3)**: VM image + the handful of real
   traces the decks and CS-01 promise; record SHA-256 per lab-strategy.
4. One instructor re-derivation pass over error-detection math near L06 (C-1 residual).
5. Optional polish: DS examples in Module 4/L27 (M-2), edition verification (M-3),
   per-worksheet point hints (M-4), link normalization (L-1/L-4).

**Bottom line:** the corpus is internally consistent, audit-clean, and pedagogically
coherent; the CRC errors were the only substantive correctness defect found and are now
fixed with machine-verified values. The pass-with-warnings verdict rests on missing
*assets* (VM image, real captures, graded CS bundles) rather than on the accuracy of
what exists.
