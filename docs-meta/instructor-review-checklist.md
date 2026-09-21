# Instructor Manual Review Checklist, Known Issues & Next Steps — 2026-09-20

For instructor-of-record sign-off before first delivery. Suggested order:
skim → verify → decide → stamp. Companion: `final-course-inventory.md`.

## 1. Decide (instructor-owned choices the material deliberately defers)

- [ ] **Quiz windows**: strategy §2 says W4/W7/W10/W13; syllabus + calendar say
  W4/W12. Pick one; propagate (~4 files + `_calendar.yml` default).
- [ ] **Weightings**: the assessment strategy's weights are *proposed* (exam
  totals are instrument-local: 60/70 marks) — confirm or adjust against
  departmental rules.
- [ ] **Semester dates**: fill `site-src/_calendar.yml` from the university
  academic calendar (never invented in the material). Validate with
  `python tools/scripts/calendar_lib.py --validate`.
- [ ] **Editions**: confirm latest print editions (Kurose & Ross ⚠ flag);
  update `docs/textbooks-references.md` if the 9th ed. is adopted.

## 2. Verify (spot-check with answer keys in hand)

- [ ] **L06 CRC after QA fix** — re-derive one example by hand before teaching:
  M=`111000`, G=`1011` → remainder `110`, codeword `111000110`; M=`101101`,
  G=`1101` → `010` / `101101010` (machine-verified; previously wrong).
- [ ] **242 ⚠ verify flags** across lectures/labs/docs — each marks a claim an
  instructor must confirm (tool versions, editions, URL details). Highest-value
  ones: lab VM/hypervisor versions, textbook editions.
- [ ] **Numerics**: run `python tools/scripts/verify_assessment_numbers.py`
  (99/99 expected) after *any* change to a bank or exam.
- [ ] **One full lecture dry-run** (suggest L18 TCP): notes pacing vs real time.
- [ ] **One lab end-to-end** (suggest LAB-02): netns commands, expected
  observations, worksheet flow, instructor key correctness.
- [ ] **Site render pass** once deployed: Mermaid diagrams, tables, mobile nav.

## 3. Known issues & warnings (evidence-based; none hidden)

| ID | Severity | Issue | Impact / action |
|---|---|---|---|
| H-1 | High | VM teaching image does not exist; template gate requires demo verification on it | Build image or downgrade gate; record SHA-256 per lab-strategy |
| H-2 | High | Graded CS-01…CS-04 bundles unbuilt (25% of course weight referenced, 0 files) | Build before semester start; lecture kickoffs (L03/L11/L23/L26) reference them |
| H-3 | High | No real capture assets in repo (0 `.pcap*`); 11 decks + CS-01 promise "provided capture" | Capture/prepare ~10–15 small traces; all current transcripts are labeled synthetic so nothing is misrepresented |
| C-1 | Critical → **fixed** | L06 CRC examples were wrong (111/100 → corrected 110/010), with false "desk-checked" claims | Fixed & machine-verified in QA review; re-derive by hand once (§2) |
| M-1 | Medium | Quiz-window discrepancy (see §1) | One-time decision |
| M-2 | Medium | DS contextualization thin outside case bank & L31 | Optional: weave DS examples into Module 4, L27, L29 |
| M-3 | Medium | Textbook edition verification outstanding | §1 |
| M-4 | Medium | Worksheets lack per-item points (rubrics live in assessment package) | Acceptable under completion-based GA credit; add points if TAs need them |
| M-5 | Medium | Accessibility untested beyond theme defaults | Run axe/Lighthouse once on the live site |
| L-1/L-3/L-4 | Low | Two INFO-level links in `lectures/README.md`; calendar sample holiday date; schedule L12 wording ("classes→CIDR") vs taught prefix notation | Optional cosmetic fixes |
| L-2 | Low | `mkdocs serve` 404 quirk in build environment (built output verified correct via static serving) | Sanity-check `mkdocs serve` locally; deployed site unaffected |

## 4. Suggested next steps (priority order)

1. **Build CS-01…CS-04** (H-2) — the only gap that touches the published
   assessment plan; kickoff dates are already on the calendar.
2. **Capture the asset set** (H-1, H-3): VM image + the ~10–15 small traces;
   then stamp the template's demo-verification gate with real dates.
3. **Make the §1 decisions** and propagate.
4. **Run the review process** (`contributing-instructor-review.md`) on a
   per-module basis; stamp Reviewed/Approved in package metadata.
5. **Commit, push, publish** per `website-publication-checklist.md` §2–§3.
6. Optional polish: M-2 DS examples, M-4 worksheet points, L-item cosmetics.

## 5. Handover integrity statement

- Every number in these handover documents comes from commands run on the
  final tree during this session (commands and outputs summarized in
  `final-course-inventory.md` §1/§3).
- No commit or push has been performed — the workspace has no `.git`
  directory; version control begins with the instructor's `git init`.
- Deployment status: **not performed**; the site URL remains an expectation
  until the checklist §2 verification passes.
