# Contribution and Instructor Review Guidance

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`repository-structure.md`](repository-structure.md) · [`lecture-template.md`](lecture-template.md) |

## 1. Roles

| Role | Responsibilities |
|---|---|
| **Course owner (instructor of record)** | Owns syllabus, exams, and grades; approves all published content; completes PLO mapping; signs off the foundation audit |
| **TA / lab demonstrator** | Runs lab blocks; first-line review of lab handouts; reports environment issues |
| **Reviewer (second faculty)** | Moderates exams; double-marks capstones; reviews pedagogy changes |
| **Contributors (optional, e.g., former students)** | May propose lab improvements, typos, and enrichment material via the workflow below — never exam or grade artifacts |

## 2. Workflow (branch-and-review)

1. Branch from `main` with a descriptive name (`lecture-13-subnetting`, `lab-09-netem-fix`).
2. One logical change per branch; follow [`lecture-template.md`](lecture-template.md) for
   lecture folders and [`lab-strategy.md`](lab-strategy.md) §5 for lab submissions.
3. Open a pull request into `main` even for instructor-authored work — the review record is
   part of quality assurance.
4. Every PR states: what changed, which CLOs/lectures are affected, and whether any
   environment-dependent item was re-verified (⚠ items from
   [`lab-strategy.md`](lab-strategy.md) §7).
5. Merge requires one approval (course owner, or reviewer for shared materials).

## 3. Review checklist (applies to any content PR)

- [ ] Technical accuracy verified against the cited RFC/IEEE/textbook section (quote the source)
- [ ] Bloom level matches the master schedule row; questions practice the stated level
- [ ] Required vs enrichment (enr) labeling correct — core is never quietly demoted
- [ ] No vendor-specific content presented as core (vendor-neutral rule)
- [ ] All links resolve; all referenced files exist
- [ ] ⚠ Any ⚠ VERIFY item that this change touches has been re-verified and dated
- [ ] Nothing under `solution/` or `assessments/exams/` leaked into student-visible paths
- [ ] Inclusive-teaching commitments ([`teaching-methodology.md`](teaching-methodology.md) §9) upheld

## 4. Review stamps

Files carry a status line in their header table (`Draft` → `Reviewed` → `Approved`), plus a
`Reviewed by` line with reviewer and date. A document must be `Reviewed` before it is used in
class and `Approved` before it appears on the public GitHub Pages site.

## 5. AI and tooling policy for contributors

- Generative-AI assistance is permitted for drafting prose and checking grammar, but every
  technical claim, citation, command, and measurement must be human-verified against a
  named source before the PR is opened; unverifiable content is rejected.
- Never fabricate: references, tool output, test results, or "example captures" presented as
  real. Synthetic evidence must be labeled synthetic and committed with its generation script
  or capture instructions.
- The automated audit script (`tools/scripts/audit_foundation.py`) must pass on every PR
  that touches foundation documents.

## 6. Versioning and change discipline

- The course carries a version (currently **v0.1**); any syllabus-affecting change (weights,
  calendar, CLO text) bumps the minor version and requires the course owner's approval.
- `docs/audit-reports/` is append-only: new dated reports, old ones never edited.
- Semester-over-semester improvements land in `instructor/misconception-log.md` and the
  teaching-methodology §10 checklist rather than by rewriting history.

## 7. Ethics gate for all contributors

All capture-based and attack-emulation material in this repository runs exclusively on
course-owned VMs, synthetic traces, or networks the contributor demonstrably owns. Contributing
attack instructions targeting real third-party systems is out of scope and will be removed.
