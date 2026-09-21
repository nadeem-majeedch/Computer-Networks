# Slide Deck Build — Audit Report (2026-09-20)

| Field | Value |
|---|---|
| Phase | Presentation-ready slide decks (`lectures/*/slides.md`, 32 files) |
| Auditor | Manual structure scan (counts + pattern greps) + `audit_lectures.py` regression |
| Result | **audit_lectures: 14 PASS / 0 WARN / 0 FAIL** — the slide-deck WARN is cleared |
| Scope of change | `lectures/*/slides.md` (32 new files), `lectures/README.md` (+Deck conventions section); nothing else modified |
| Commit status | Nothing committed or pushed (per workflow) |

## 1. What was built

Each of the 32 lecture packages now carries a `slides.md` deck (16–18 slides each;
548 slides total) containing, per the task's per-lecture list:

1. **Deck outline** — two-column slide-number/title table at the top of every deck.
2. **Slide-by-slide content** — one idea per slide, ≤6 bullets, tables where the
   content *is* a table (field maps, comparisons).
3. **Speaker notes** — a `> Notes —` blockquote under *every* slide (548/548 —
   mechanically verified), separated from student-facing content by format.
4. **Diagrams** — Mermaid (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`) or
   labeled ASCII for all 14 requested visual topics: encapsulation (L02), Ethernet
   frames (L07), switching/VLANs (L08/L09), subnetting (L13), IPv6 (L15), routing
   tables (L16), TCP handshake (L18), DNS resolution (L21), DHCP (L14/L22), NAT
   (L14/L27), firewalls (L25), cloud networking (L27), SDN architecture (L28),
   troubleshooting workflow (L29).
5. **Worked examples** — at least one per deck, numbers shared with the assessment
   package's verified values (e.g., 120 µs serialization, 3.2 s transfer, 625 kB
   BDP, 350 ms connection-round math — all machine-checked via
   `verify_assessment_numbers.py` patterns).
6. **Classroom questions** — a dedicated 3-question slide per deck plus in-slide
   prompts.
7. **Demonstration instructions** — a closing block per deck with ITI items and
   offline fallbacks (no-device rooms supported throughout).
8. **Summary slide** — one per deck, tied to the next lecture's hook.
9. **Exit-question slide** — one per deck, feeding the matching weekly quiz pool.

## 2. Design decisions

- **Notes stay with slides.** Per-slide blockquotes (rather than a second file per
  lecture) keep deck and delivery guidance in sync; the course deck conventions
  (`lectures/README.md` §Deck conventions) document how to export slides without
  notes.
- **No fake screenshots.** Wherever a screenshot would be natural, decks use real
  printed trace/hex listings from the course capture bundles or labeled synthetic
  excerpts; two demo blocks explicitly state the no-fake-screenshot policy (L24's
  certificate warnings, L29's dashboards).
- **No copyrighted figures.** Every diagram is original Mermaid/ASCII. Textbook
  and RFC citations appear in each deck's references block; edition-sensitive
  readings keep the standing ⚠ verify flags.
- **Ethics gate holds.** No attack tooling or commands appear in any deck (grep
  for common tool names: zero hits); L26 remains concept-level defense analysis.

## 3. QA performed (actual results)

| Check | Result |
|---|---|
| 32/32 decks present, 16–18 slides each (548 total) | ✔ |
| 548/548 slides carry speaker notes (slides=notes per deck) | ✔ |
| Deck outline / demo instructions / references: 32/32 each | ✔ |
| Mermaid scan: no unquoted parens in node labels; one `\n` label fixed to `<br/>` (L24); garbled ASCII channel sketch redrawn (L10) | ✔ |
| Visual-topic coverage (14 topics mapped to decks) | ✔ (see §1.4) |
| Numerics shared with assessment package | ✔ same verified values |
| `audit_lectures.py` regression | **14 PASS / 0 WARN / 0 FAIL** |

Self-caught content fixes during QA: the L24 certificate-chain diagram's line
break, the L10 channel-plan sketch, and the L06 exit-question CRC remainder
(corrected to `111` with the full XOR-division shown — desk-checked).

## 4. Honest limitations

1. **Decks have never been projected.** Layout/overflow under a real projector and
   font requires a classroom pass; the conventions constrain density but cannot
   verify it.
2. **Mermaid renders only via a renderer.** Diagrams were syntax-audited, not
   rendered; a one-click render pass (e.g., VS Code Mermaid preview) over all 32
   decks is a 15-minute instructor task before first use.
3. **ITI demo items remain.** Each deck's demonstration block names its
   capture/asset prerequisites; the teaching image build must satisfy them (same
   ITI register as the labs and worksheets).
4. Slide *count* per 120-min session varies by design (labs/clinics lean shorter
   with more activity time), consistent with the foundation docs' varied timing
   plans.
