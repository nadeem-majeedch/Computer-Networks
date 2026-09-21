# PB-011 — The Protocol That Can't Find Its Edges (L06, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L06 — Data Link Layer: Framing, Errors & Reliability |
| CLOs | CLO2 (explain framing necessity), CLO4 (analyze a protocol design) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual/design analysis · Topic: Network programming (framing) |
| Evidence policy | Synthetic log fragments, labeled; behavior consistent with delimiter-vs-stuffing theory |

---

## Student version

### Scenario
For the data-science cluster, a student designs a tiny file-transfer protocol: messages
are ASCII commands or binary chunks, separated by the byte `0x0A` (newline). It works in
tests with text. The first real binary payload — a compressed NumPy array — arrives
garbled: messages split at random points.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Text test:   "GET model.bin\n" → parsed perfectly
Binary test: payload contains bytes 0x0A at offsets 1,204 and 8,391
             receiver splits the stream at those offsets → corrupted chunks
Student fix attempt 1: "use a bigger delimiter, 0xFFFFFFFF" → failed on binary again
                         (payload contains 0xFFFFFFFF too)
```

### Problem statement
Explain precisely why sentinel-based framing fails on binary data, why "a bigger
delimiter" doesn't fix it, and what real data-link protocols do instead.

### Evidence pack
The labeled synthetic log. One assumption to test: the sender does no escaping of any
kind (the evidence is consistent with it; state it as assumed).

### Constraints
- Argue from the data, not from "TCP is reliable" (it is — that's not the problem).
- Reference at least one real framing technique from the lecture.

### Student questions
1. Why do offsets 1,204 and 8,391 break the receiver, exactly?
2. Why did the student's "bigger delimiter" fix fail? What property of the payload
   makes *every* fixed sentinel fail eventually?
3. Name two framing techniques from lecture and say which fits this protocol best.
4. The stream never loses or reorders bytes (TCP guarantees this). Why is framing still
   necessary?

### Expected learning outcomes
- Explain why byte-stuffing/escaping (or length prefixes) is mandatory for binary
  streams.
- Distinguish reliability (no loss/reorder) from framing (finding message boundaries).
- Evaluate a protocol design against adversarial data.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The receiver trusts a pattern in the *data stream* to be a *control signal*. When
   does that assumption break?"
2. "Compressed data is statistically indistinguishable from random bytes. What
   probability says about any fixed pattern appearing."

### Solution
1. The payload legitimately contains 0x0A. The receiver cannot tell *data* newlines
   from *delimiter* newlines, so it splits mid-message; both fragments are truncated
   and the stream desynchronizes (the receiver is now waiting for a "message" that is
   really the tail of a binary chunk).
2. Any fixed byte pattern can occur in binary data — compression makes payloads
   effectively random, so longer delimiters only shrink the probability; they never
   reach zero. 0xFFFFFFFF occurs at least once in megabytes of compressed data.
3. Candidates from lecture: (a) byte/bit stuffing (escape the delimiter: PPP-style
   byte stuffing with 0x7D escape) — fits a byte-oriented protocol; (b) length-prefix
   framing (header states the payload length; receiver counts bytes) — simplest fix and
   best fit here; (c) physical-layer B8ZS/4B5B-style coding is out of scope for an
   application protocol. Recommend (b), with (a) as the classic data-link answer.
4. Reliability and framing are orthogonal: TCP delivers a *correct byte stream* with no
   message boundaries at all. Without a framing rule, the receiver knows the bytes are
   right but not where one message ends — "reliable" ≠ "delimited".

### Reasoning process
Facts: payload contains delimiter bytes; receiver splits at them. Model: sentinel
framing requires the delimiter to be impossible in data; escaping or length-counting
restores the invariant. Distinguish facts (observed splits at those offsets) from
assumption (no sender-side escaping) and test it.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Use a longer magic delimiter" | Probability shrinks, never zero; compressed data is near-random |
| "TCP will sort it out" | TCP preserves the stream; it has no message concept |
| "Base64 everything" | Works (encodes binary as safe text) but costs 33% bandwidth; a valid trade-off to *discuss*, not a free fix |
| Blaming the compressor | The bytes are correct; the *framing rule* is broken |

### Extension question
The student switches to length-prefix framing. The first 4-byte header says
`0x00 0x00 0x30 0x39` (=12,345 bytes to follow). Which byte-order question must the
receiver answer before it can read *anything* else, and what happens if the two ends
disagree? (Endianness of the length field — network byte order (big-endian) by
convention; a mismatch yields absurd lengths or hangs, and the desync is total.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Correct mechanism for both failures; recommends and justifies a real technique; reliability-vs-framing distinction explicit |
| 3 Proficient | Explains the failure and one correct technique |
| 2 Developing | Suggests longer delimiters or base64 without trade-off reasoning |
| 1 Beginning | Blames TCP or the compressor |

### References
- PD §2.3 (framing approaches: sentinel, stuffing, length counts)
- Kurose & Ross §2.7.3 (application framing over TCP — byte-stream vs message)
