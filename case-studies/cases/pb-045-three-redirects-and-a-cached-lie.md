# PB-045 — Three Redirects and a Cached Lie (L23, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L23 — Core Application Protocols: HTTP/1.1 → HTTP/3, SMTP & SSH |
| CLOs | CLO2 (HTTP method/status semantics), CLO6 (diagnose from response evidence) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: Application protocols |
| Evidence policy | Synthetic request/response traces, labeled; redirect semantics per RFC 9110 |

---

## Student version

### Scenario
The analytics API moved from `api.meridian.example/v1/…` to `api2.meridian.example/v2/…`.
The dev team answered the old paths with `301 Moved Permanently` + `Location:` and
shipped. Within days, mobile clients and one test browser *keep* hitting the old host
— even after the team reverted the redirect "to test something".

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative traces):**

```
Day 1  GET api.meridian.example/v1/users → 301, Location: api2.meridian.example/v2/users
       Client follows; new host returns 200.
Day 3  Team reverts redirect (old host: 404) to debug.
       curl (fresh):          404 Not Found            (correct, redirect gone)
       Mobile app:            GET api.meridian.example/v1/users → 301 → api2…
                              (observed in app logs! but server now returns 404)
       One test browser:      same phantom 301 behavior
Explanation candidates on the table:
  A) "The mobile app caches responses for a day"
  B) "Something between client and server still answers 301"
  C) "The client cached the redirect itself"
```

### Problem statement
Identify the correct explanation, explain the HTTP semantics that produce it (why 301
persists and why 302 wouldn't), and give the migration rule (which status for which
purpose + the cache-busting escape hatch).

### Evidence pack
The labeled synthetic traces. Facts: fresh curl sees 404; mobile + one browser still
follow a 301 that the server no longer sends.

### Constraints
- Cite the semantic difference between 301 and 302 (who is *allowed* to cache and for
  how long, per RFC 9110 semantics ⚠).
- The escape hatch must work without server access to the clients.

### Student questions
1. Which candidate (A/B/C) fits the evidence, and which observation rules out the
   others?
2. Why did the *curl* test not reproduce the problem? What makes curl's view "fresh"?
3. If the team had used 302 instead: what would clients have done on Day 3, and what
   is the cost of 302 during the *life* of the migration?
4. Give the status-code rule (when 301 vs 302/307) and the escape hatch for a
   botched 301.

### Expected learning outcomes
- Distinguish permanent vs temporary redirect caching semantics.
- Explain why different clients show different views of the same server.
- Apply redirect status codes deliberately in migrations.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The server *stopped* sending 301, yet some clients still receive one. Who could
   still be speaking?"
2. "curl without a cache is a newborn client. The app and that one browser are
   veterans — what do veterans carry?"

### Solution
1. **C**. Ruling out: A predicts *all* responses cached — but the app follows a 301
   specifically, and the server no longer sends one (fresh curl proves it); B has no
   mechanism — intermediaries don't invent redirects, and curl (same path) sees 404.
   C fits: the client (app HTTP stack; that browser's disk cache) cached the 301
   from Day 1.
2. curl holds no cached redirect (fresh state, and `curl` doesn't consult the
   browser/app cache); it sees the *server's current truth* — 404. The mismatch
   between fresh and veteran views is the diagnostic signature of client-side
   caching.
3. With 302: clients would re-ask the old host (302 is not required to be cached —
   typically re-fetched every time ⚠ semantics: "temporary"), so Day 3's revert takes
   effect immediately. Cost during migration: every request pays the redirect hop
   (latency, load on the old host) for the whole migration period — you trade
   permanence for controllability.
4. Rule: 301/308 when the move is *permanent and final* (clients/intermediaries may
   cache indefinitely; 308 also preserves method/body); 302/303/307 when the redirect
   is *operational or provisional* (303 for POST→GET semantics; 307 preserves method
   like 308). Escape hatch: you cannot un-cache a 301 you no longer serve — you must
   *re-serve* it: point the old host's 301 at the new location again (or serve a
   short-TTL 302 chain) until client caches refresh; for browsers, users can hard-
   reload/clear cache; apps need a server-side fix because you can't reach into
   them. The lesson: 301 is a promise — break it only with a plan.

### Reasoning process
Facts: fresh 404 vs veteran 301; two client classes. Model: redirect caching
semantics (301 cacheable-indefinitely; 302 refresh-per-use) + client cache diversity.
Candidate elimination by mechanism. Rule + escape hatch follow from semantics.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The proxy still redirects" (B) | Same-path curl disproves any network-level 301 |
| "404 the old host and move on" | Breaks every client that cached 301→*different* path? No — cached 301 points to api2 which still works; the 404 only hurts *fresh* clients; the real victims are those whose 301 cache outlived the test |
| "307 everywhere" | Overcorrects; 307 is for method preservation, not cache control |
| "Clear the app's cache in the next release" | Slow (release cycles), and doesn't help current installs |

### Extension question
The team needs POST /v1/orders redirected to v2 with the *body* intact. Which codes
preserve method+body (307/308) and which silently downgrade to GET (301/302/303)?
Why did a payment integration once break with a 301 on a POST? ⚠ (301/302 historically
allowed clients to switch POST→GET; 303 mandates GET; 307/308 preserve. A POST
dropped to GET loses the body — payments arrive empty; RFC 9110 documents the
history.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Candidate elimination by mechanism; 301/302 semantics precise; escape hatch realistic (re-serve plan); method-preservation nuance |
| 3 Proficient | Correct diagnosis; semantics partially stated |
| 2 Developing | "Caching" invoked generically, codes interchangeable |
| 1 Beginning | "Clear your cookies" |

### References
- RFC 9110 §15.4 (redirection 3xx semantics) ⚠ verify section
- PD §2.2/§2.4 (HTTP basics) ⚠ verify section mapping; Kurose & Ross §2.2 (HTTP)
