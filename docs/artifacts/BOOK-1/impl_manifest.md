# Implementation Manifest: BOOK-1

## Summary
Added a single Playwright API test that creates a booking via `POST /booking`, retrieves it via `GET /booking/{id}`, and validates the six booking fields (presence, runtime types, ISO dates) and field-for-field equality with the creation payload. No existing files were modified.

## Branch
BOOK-1-retrieve-booking-valid-id (base: main)

## Files
| File | Action (new/modify) | Component | Step |
|---|---|---|---|
| tests/BOOK-1.spec.ts | new | COMP-005 | 1 |

## Commits
None - changes left uncommitted per user request.

## Acceptance Criteria Coverage
| REQ / AC | Test / assertion | Result |
|---|---|---|
| R1 / AC1 | `getBooking()` resolves without exception | Pass |
| R2 / AC2 | `getBooking()` throws on non-200, so a resolved call proves 200 | Pass |
| R3 / AC3 | `typeof` checks, non-empty names, `totalprice >= 0`, `YYYY-MM-DD` regex for dates | Pass |
| R4 / AC4 | `expect(getResponse).toEqual(bookingPayload)` | Pass |

## Design Review Conditions
| Condition | Resolution |
|---|---|
| AC-001 / CR-002 | Payload inlined in spec; API accepted it on first run |
| MC-001 / CR-004 | Observed: API returns `additionalneeds` when supplied; asserted as string |
| MC-002 / CR-005 | Explicit `typeof` and ISO date regex assertions |
| MC-004 / CR-004 | Field-level type assertions with messages, then one `toEqual` deep equality |
| MC-003 / CR-003 | Best-effort `deleteBooking()` in `finally`; failure logged via `console.warn`, never fails the test |
| MC-006 (low) | Known gap: API versioning not covered; no change |

## Test Results
- Baseline: 0 tests (`Error: No tests found`)
- Final: 1 passed / 0 failed; `npx tsc --noEmit` exit 0
- Commands run: `npx playwright test`, `npx playwright test tests/BOOK-1.spec.ts`, `npx tsc --noEmit`

## Hardening Tasks
`implementation_plan.md` was left unchanged per user request, so status is recorded here.
- Logging / Observability: completed (test logs no PII or tokens; cleanup failure logged via `console.warn`).
- Controller, Service, Data Access, Exception Handling, API Contract Documentation: N/A - test-only change, no production layers.

## Deviations from Plan
- Not committed, per explicit user instruction (agent normally commits per step).
- Used `--reporter=list` / `PLAYWRIGHT_HTML_OPEN=never` for runs to avoid the HTML report server blocking.

## Open Issues / Follow-ups
- Existing `authToken` fixture logs the token via `console.log` (out of scope; not changed).
- Shared public Restful-Booker instance may be flaky; no retries by design.

## Review Fixes (Round 1)
| Finding | Status (fixed / not fixed) | Files | Commit | Notes |
|---|---|---|---|---|
| C-001 | fixed (partial; user action required) | `.gitignore`, `.env.example`, `.env` (untracked) | db68f67 | `.env` untracked with `git rm --cached` (local file kept), git-ignored, `.env.example` added with placeholder keys. **User action:** rotate `AUTH_USERNAME` / `AUTH_PASSWORD`, since they remain in history (commit `4ad52ea`); purging history needs a rewrite the agent must not do. |
| M-001 | fixed | `tests/fixtures.ts` | 75d18ae | Replaced the token log with a fixed `Auth token generated` message. Verified token absent from test output. |
| m-001 | fixed | `tests/BOOK-1.spec.ts` | 5de465f | `error instanceof Error ? error.message : String(error)`. |

Verification: baseline 1 passed / 0 failed, `tsc` exit 0 → final 1 passed / 0 failed, `tsc` exit 0.

Observation for re-review (now raised as M-002 and fixed in Round 2): when the best-effort `deleteBooking()` cleanup fails, Playwright's error message includes a call log with the `Cookie: token=...` header, and the spec's `console.warn` printed that message. This was seen once in the baseline run (ECONNRESET on DELETE).

## Review Fixes (Round 2)
| Finding | Status (fixed / not fixed) | Files | Commit | Notes |
|---|---|---|---|---|
| M-002 | fixed | `tests/BOOK-1.spec.ts` | 0c5a3d0 | The cleanup warning now logs only the first line of the error message, dropping Playwright's call log that carries the `Cookie: token=...` header. Confirmed with a scratch script (since removed): a failed DELETE with a fake token has the token in the full message but not in the first line. |

Verification: baseline 1 passed / 0 failed, `tsc` exit 0 → final 1 passed / 0 failed, `tsc` exit 0; token absent from test output.

Still open from Round 1 (user action): rotate `AUTH_USERNAME` / `AUTH_PASSWORD`, since the old `.env` remains in git history (commit `4ad52ea`, which is `origin/main`).

## Review Fixes (Round 3)
Round limit note: `code_review.md` is at Review Round 3 (`max_review_iterations`: 3) and records no authorisation for another round. The user explicitly invoked `@sdlc-review-fix BOOK-1` after being told this, and that invocation was treated as the authorisation. `code_review.md` is read-only for this agent, so the authorisation is recorded here. The next `@code-review` run would be round 4.

| Finding | Status (fixed / not fixed) | Files | Commit | Notes |
|---|---|---|---|---|
| C-002 | fixed (partial; user action required) | `.gitignore`, `.vscode/atlassian-api.local.json` (untracked), `.vscode/atlassian-api.local.example.json` (new) | d6819df | Untracked with `git rm --cached` (local file kept), git-ignored, and an example file added with the same keys and empty values. Verified `git ls-files` no longer lists the real file and `git check-ignore` matches. **User action:** revoke and regenerate the Jira and Confluence API tokens. The old file is on `origin/main` (commit `4ad52ea`) and in local `refs/agents/*` checkpoints; the agent must not rewrite history. |
| m-002 | fixed | `tests/fixtures.ts` | dd3da77 | `const tokenBody: AuthResponse = await authResponse.json();` with the import from `./interfaces/types`. |

Verification: baseline 1 passed / 0 failed, `tsc` exit 0 → final 1 passed / 0 failed, `tsc` exit 0; token absent from test output.

User actions still outstanding: (1) revoke and regenerate the Jira and Confluence API tokens (C-002); (2) rotate `AUTH_USERNAME` / `AUTH_PASSWORD` (C-001).
