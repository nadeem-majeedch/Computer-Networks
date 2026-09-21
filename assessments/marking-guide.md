# Marking Guide — Shared Conventions

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Applies to | Every marking scheme in [`exams/`](exams/), [`assignments/`](assignments/), [`rubrics/`](rubrics/), and the instructor keys in [`quizzes/`](quizzes/) · [`banks/`](banks/) |

## 1. Mark-award philosophy

1. **Method marks outrank answer marks.** A wrong final answer with correct, clearly
   stated reasoning earns most marks; a correct guess with no reasoning earns almost none.
2. **State-assumptions credit.** Numerical questions allocate explicit marks for stating
   assumptions (unit conversions, simplifications). An unexplained "correct" number can
   lose the assumption marks.
3. **Units are content.** Wrong/missing units on a dimensional quantity lose the
   accuracy mark for that step even if the number is right.
4. **Significant figures.** Accept answers to within rounding of the exact result
   (±1 in the last shown digit unless the scheme states tolerance). Never demand more
   precision than the inputs justify.
5. **No negative marking** anywhere in this package.
6. **Alternative valid methods** score full marks; schemes list the common ones where
   known and mark unlisted-but-sound methods at the equivalent difficulty point
   (moderation sample required — §4).

## 2. Answer-key authority and limits

- Keys marked **[MC]** were script-verified (`tools/scripts/verify_assessment_numbers.py`);
  keys marked **[DC]** are desk-checked only. Re-verify [DC] before first use.
- Where a key states a *representative* answer for open-ended items (design, long-answer),
  it defines the expected reasoning chain, not a unique solution; other defensible chains
  score equally.
- Protocol-behavior keys cite the standard (RFC/802.x) or the course textbook where the
  behavior is standards-sensitive; if neither is cited, the behavior is course-level
  simplification and the key says so.

## 3. Mark-band language used in schemes

| Term in schemes | Meaning |
|---|---|
| **Full credit** | Correct result via sound reasoning, assumptions stated |
| **Method mark (M)** | Correct setup/step even if later arithmetic fails |
| **Accuracy mark (A)** | Correct numeric/result dependent on the preceding M |
| **Communication mark (C)** | Clear notation, units, labeled diagram, or prose quality (used in long-answer & design items) |
| **Ecf** | "Error carried forward" — a wrong early answer used correctly afterward earns later marks |

## 4. Moderation workflow (per strategy §4)

1. Second instructor marks a 10% sample of each exam/scripts and any full-mark and
   zero-mark scripts (boundary check).
2. Lab rubrics spot-checked weekly by the course owner against the
   [`rubrics/practical-work-rubric.md`](rubrics/practical-work-rubric.md).
3. Capstone double-marked (instructor + second marker) per strategy §3.7.
4. Discrepancies >10% of instrument total between markers trigger a full re-mark of the
   instrument.
5. Record moderation outcomes in the course file; adjust schemes *for the next cohort*
   unless an error is proven in the paper (then fix for everyone, before return).

## 5. Feedback discipline

Per strategy §6: quizzes/labs within 1 week; problem set and midterm within 2 weeks;
case write-ups 2 weeks; capstone stage gates 1 week. Marked scripts are returned with the
scheme's M/A/C annotations visible so students see *where* marks lived — this is also the
cheapest form of formative feedback the package provides.

## 6. Borderline and viva rules

- A script within 2% of a grade band boundary is re-read in full before release.
- Suspected unexplained-correct answers (see §1.1) may be probed with a 5-minute viva on
  the specific item; the viva outcome adjusts that item's marks only.
