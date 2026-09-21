# CLO Assessment Mapping — Item Level

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Parent | [`../docs/clo-mapping.md`](../docs/clo-mapping.md) (CLO definitions, lecture matrix) · [`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) |

[`../docs/clo-mapping.md`](../docs/clo-mapping.md) §2 maps **instruments** to CLOs. This
document goes one level down: **which artifacts in this package** carry each CLO, so an
instructor can confirm coverage without opening every file. CLO definitions are quoted
abbreviated from [`../docs/learning-outcomes-clos.md`](../docs/learning-outcomes-clos.md).

| CLO | Summary | Measured by (package artifact → CLOs tagged on items) |
|---|---|---|
| CLO1 | Explain network architecture, layering, encapsulation | Quizzes W01–W03, W08 · Banks: conceptual §B1, short-answer §SA1 · Midterm §A · Final §A |
| CLO2 | Explain physical/data-link operation and media trade-offs | Quizzes W03–W05 · Banks: conceptual §B2, packet-analysis §PA1 · Midterm §A/§C · Final §A |
| CLO3 | Design IPv4/IPv6 addressing & subnet plans | Subnetting problem set (whole instrument) · Quizzes W06–W08 · Bank: numerical §N · Midterm §B · Final §B |
| CLO4 | Capture, dissect and interpret packets/protocol behavior | Quizzes W02, W06–W12 (dissection items) · Bank: packet-analysis (whole) · Midterm §C · Final §C · Practical bank items |
| CLO5 | Build and measure small networks & transport endpoints | Practical bank §PR · Reliable-transport project brief · Labs rubric · Final §D |
| CLO6 | Diagnose, evaluate and troubleshoot networks/designs | Bank: routing-troubleshooting (whole) · Quizzes W04–W05, W13–W15 (scenario items) · Case bank PB-xxx (formative rehearsal) · Final §D |
| CLO7 | Analyze threats and select layered defenses | Quizzes W12–W13 · Banks: conceptual §B4, short-answer §SA4 · Case bank PB-047…PB-052 · Final §C |
| CLO8 | Integrate skills in a full design lifecycle | Capstone rubric (whole) · Final synthesis question §E · Bank: long-answer §LA4 |

## Coverage checks (verdicts from actual package contents)

| Check | Result |
|---|---|
| Every CLO measured by ≥2 package artifacts (CLO8 excepted by design) | ✔ — see [`../docs/clo-mapping.md`](../docs/clo-mapping.md) §2 note on CLO8 |
| Every graded instrument's item pool exists in this package | ✔ quizzes → weekly papers; subnetting PS → brief + bank §N overlap; midterm/final → exams/; transport project → brief; capstone → rubric; case write-ups → scenario packets in case-study-strategy (CS bundles themselves remain unbuilt — see report) |
| Difficulty mix per bank: all four tiers B/I/A/E present | ✔ verified by `audit_assessment.py` (per-file minimums) |
| Bloom progression matches [`../docs/clo-mapping.md`](../docs/clo-mapping.md) §3 | ✔ M1–M2 items skew C1–C3; M3–M5 C3–C4; M6–M8 C4–C6 |

## Item-source dedup rule

Where a bank item and an exam/quiz item test the same skill, they must differ in at least
one of: numbers, topology, protocol, or required reasoning step. `audit_assessment.py`
checks for exact-duplicate question stems across the package (normalized whitespace, first
60 characters). Near-duplicates with changed wording are an instructor-review task, not an
automatable one — flagged for the pre-release solve-through.
