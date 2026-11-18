# Code Review: BOOK-1

## Summary
Round 4 re-review after `@sdlc-review-fix` round 3. All findings from rounds 1-3 are fixed in the code and the fix diff introduces no regressions. No new findings. `npx tsc --noEmit` exits 0 and `npm audit` reports 0 vulnerabilities. Two user-only credential actions remain (see below); they are not code findings.

## Review Round
4 (re-review after fixes). `max_review_iterations`: 3. The limit was exceeded with explicit user authorisation: the user invoked `@sdlc-review-fix BOOK-1` after the round 3 escalation, recorded in `impl_manifest.md` (Review Fixes (Round 3)).

## Scope
| File | Lines reviewed |
|---|---|
| tests/fixtures.ts | 1-46 |
| tests/BOOK-1.spec.ts | 1-57 (target) |
| .gitignore, .env.example, .vscode/atlassian-api.local.example.json | all |
| Fix diff `5b0989e..HEAD` (`.gitignore`, `tests/fixtures.ts`, Atlassian file swap) | all |
| Tracked files | sensitive-file and long-credential scan (values not printed) |

Completeness check: all checklist rows applied to all files; every path a token or credential can reach was traced.

## Verdict
approve — Critical: 0, Major: 0, Minor: 0.

## Critical
None

## Major
None

## Minor
None

## Prior Findings Status
| ID | Status (fixed / not fixed) | Evidence |
|---|---|---|
| C-002 | Fixed in code | No `.env` or `local.json` files are tracked; `.gitignore` lines 11-12 match both; the example files have only empty values; the local Atlassian file is kept. |
| m-002 | Fixed | `tests/fixtures.ts:35` types the auth response as `AuthResponse`, imported at line 2. |
| M-002 | Fixed | `tests/BOOK-1.spec.ts:50-52` log only the first line of the cleanup error. |
| C-001 | Fixed in code | `.env` is untracked and git-ignored; `.env.example` has empty values. |
| M-001 | Fixed | `tests/fixtures.ts:38` logs only `Auth token generated`. |
| m-001 | Fixed | The spec uses `error instanceof Error ? error.message : String(error)`. |

## Fix Worklist for @sdlc-review-fix
None. No outstanding findings.

## User-only actions (not code findings)
Both sets of credentials are already on `origin/main` (commit `4ad52ea`) and in local `refs/agents/*` checkpoints, and removing the files does not undo that:
- Revoke and regenerate the Jira and Confluence API tokens (C-002).
- Rotate `AUTH_USERNAME` and `AUTH_PASSWORD` (C-001).

## Plan / AC Conformance
| REQ / AC | Covered by | Status |
|---|---|---|
| R1 / AC1 | `getBooking()` resolves (`tests/BOOK-1.spec.ts:28`) | Met |
| R2 / AC2 | `getBooking()` throws on non-200 (`tests/pom/BookingAPI.ts:41`), noted in the spec comment at line 27 | Met (implicit, as the plan allows) |
| R3 / AC3 | `typeof`, non-empty, `>= 0`, ISO-regex assertions (spec lines 31-42) | Met |
| R4 / AC4 | `toEqual(bookingPayload)` (spec line 45) | Met |

## Human Approval
- Round 4: approved by user at the gate (reply: `approved`). Adjustments: none.
- Next stage: Phase 8, PR Creation.

---

# Round 3 record (re-review)

Verdict: request_changes — Critical: 1, Major: 0, Minor: 1. C-002 and m-002 were fixed in commits `d6819df` and `dd3da77`.

## Scope (round 3)
| File | Lines reviewed |
|---|---|
| tests/BOOK-1.spec.ts | 1-57 (target) |
| tests/fixtures.ts | 1-43 |
| tests/pom/AuthAPI.ts, tests/pom/BookingAPI.ts, tests/interfaces/types.ts | all (context) |
| playwright.config.ts, package.json, .gitignore, .env.example | all (context) |
| All 27 git-tracked files | secrets scan (values not printed) |
| Git refs (`origin/main`, branch, `refs/agents/*`) | exposure check |

Completeness check: all checklist rows applied to all files; every path a token or credential can reach was traced.

## Verdict (round 3)
request_changes — Critical: 1, Major: 0, Minor: 1 (round 3, both new and missed in round 1). Earlier rounds: round 1 was Critical: 1, Major: 1, Minor: 1; round 2 was Major: 1.

## Critical (round 3)

### C-002: Jira and Confluence API tokens are tracked in git and already pushed
- Location: `.vscode/atlassian-api.local.json` (tracked since `4ad52ea`, which is `origin/main`). `.gitignore` has no entry for it.
- Severity: Critical
- Category: Security
- Issue: The file has `jira.token` and `confluence.token` (192 characters each) plus emails and base URLs. None look like placeholders. The skill's own `.github/skills/fetch-jira-confluence/SKILL.md` line 40 says to git-ignore this file, and it isn't. No values were printed during review. Local checkpoint refs (`refs/agents/*`) also hold copies.
- Required change:
  1. Untrack the file with `git rm --cached .vscode/atlassian-api.local.json`, keeping the local copy.
  2. Add `.vscode/atlassian-api.local.json` to `.gitignore`.
  3. Add `.vscode/atlassian-api.local.example.json` with the same keys (`jira.baseUrl/email/token`, `confluence.baseUrl/email/token`) and empty values.
- Files to change: `.gitignore`, `.vscode/atlassian-api.local.json` (untrack only), `.vscode/atlassian-api.local.example.json` (new)
- Verify by: `git ls-files .vscode/atlassian-api.local.json` prints nothing. `git check-ignore -v .vscode/atlassian-api.local.json` matches. The example file has no non-empty values.
- User action: revoke and regenerate both Atlassian API tokens. The commit is on `origin/main`, and removing the file now doesn't undo that.

## Major (round 3)
None

## Minor (round 3)

### m-002: Untyped auth response in the fixture
- Location: `tests/fixtures.ts:34-35`
- Severity: Minor
- Category: Type Safety
- Issue: `await authResponse.json()` is untyped, so `token` is `any`. `tests/pom/AuthAPI.ts:20` already types this same response with `AuthResponse`.
- Required change: `import { AuthResponse } from './interfaces/types';` and use `const tokenBody: AuthResponse = await authResponse.json();`.
- Files to change: `tests/fixtures.ts`
- Verify by: `npx tsc --noEmit` exits 0 and `npx playwright test` still passes 1/1.
- User action: none

## Prior Findings Status (round 3)
| ID | Status (fixed / not fixed) | Evidence |
|---|---|---|
| M-002 | Fixed | `tests/BOOK-1.spec.ts:50-52` log only `message.split('\n')[0]`. |
| C-001 | Fixed in code; credentials exposed on the remote | `.env` is untracked and ignored. `origin/main` is commit `4ad52ea`, which contains `.env`, so `AUTH_USERNAME` / `AUTH_PASSWORD` are already on GitHub. Rotation is mandatory. |
| M-001 | Fixed | `tests/fixtures.ts:37` logs only `Auth token generated`. |
| m-001 | Fixed | The spec uses `error instanceof Error ? error.message : String(error)`. |

## Fix Worklist (round 3)
Status: **executed** in commits `d6819df` (C-002) and `dd3da77` (m-002) after the user authorised another round.

| # | ID | Severity | File:Line | Required change | Files to change | Verify by | User action |
|---|---|---|---|---|---|---|---|
| 1 | C-002 | Critical | `.vscode/atlassian-api.local.json` | Untrack, git-ignore, add example file | `.gitignore`, the json (untrack only), `.vscode/atlassian-api.local.example.json` | `git ls-files` empty, `check-ignore` matches | Revoke and regenerate both Atlassian tokens |
| 2 | m-002 | Minor | `tests/fixtures.ts:34-35` | Type with `AuthResponse` | `tests/fixtures.ts` | `tsc` clean, tests 1/1 | none |

### Fix Instructions (round 3)
- Order: C-002, then m-002, with one commit per item and the IDs in the message.
- Verification to run after all fixes: `npx tsc --noEmit` and `npx playwright test`; expected result is no regressions against the 1/1 baseline.
- Out of scope: the spec, `tests/pom/BookingAPI.ts`, `tests/pom/AuthAPI.ts`, and the skill files.
- User-only actions to report back: revoke and regenerate the Jira and Confluence API tokens (C-002); rotate `AUTH_USERNAME` / `AUTH_PASSWORD` (C-001).
- Carried over from earlier rounds (still open): the C-001 credential rotation.

## Plan / AC Conformance (round 3)
| REQ / AC | Covered by | Status |
|---|---|---|
| R1 / AC1 | `getBooking()` resolves (`tests/BOOK-1.spec.ts:28`) | Met |
| R2 / AC2 | `getBooking()` throws on non-200 (`tests/pom/BookingAPI.ts:41`), noted in the spec comment at line 27 | Met (implicit, as the plan allows) |
| R3 / AC3 | `typeof`, non-empty, `>= 0`, ISO-regex assertions (spec lines 31-42) | Met |
| R4 / AC4 | `toEqual(bookingPayload)` (spec line 45) | Met |

## Human Approval (round 3)
- Round 3: approved by user at the gate (reply: `approved`). Critical finding C-002 acknowledged. Adjustments: none.
- Another fix round: initially not authorised, so the loop was escalated. The user then explicitly invoked `@sdlc-review-fix BOOK-1`, which was treated as the authorisation (recorded in `impl_manifest.md`, Review Fixes (Round 3)).

---

# Round 2 record (re-review)

Verdict: request_changes — Critical: 0, Major: 1, Minor: 0. M-002 was fixed in commit `0c5a3d0`.

## Scope (round 2)
| File | Lines reviewed |
|---|---|
| tests/BOOK-1.spec.ts | 1-57 (target) |
| tests/fixtures.ts | 1-43 (context) |
| .gitignore, .env.example | all (context) |
| docs/artifacts/BOOK-1/impl_manifest.md | Review Fixes (Round 1) section |
| tests/pom/BookingAPI.ts, tests/interfaces/types.ts, playwright.config.ts, package.json | round 1 context, unchanged |

## Verdict (round 2)
request_changes — Critical: 0, Major: 1, Minor: 0 (round 2). Round 1 was Critical: 1, Major: 1, Minor: 1.

## Critical (round 2)
None

## Major (round 2)

### M-002: Cleanup warning can print the auth token
- Location: `tests/BOOK-1.spec.ts:50-51`
- Severity: Major
- Category: Security
- Issue: When `deleteBooking()` fails, Playwright's error message includes a call log with the `Cookie: token=…` request header. The warning prints that whole message. The fix run's baseline hit exactly this: an ECONNRESET on the DELETE call printed a live token to the console and HTML report. M-001 removed the fixture's token log, so this is the remaining way the token reaches output. The manifest records it as an open observation.
- Suggestion: Log only the first line of the message, for example `reason.split('\n')[0]`, or log a fixed message with the booking ID and the HTTP status. Never print the full Playwright error.

## Minor (round 2)
None

## Prior Findings Status (round 2)
| ID | Status (fixed / not fixed) | Evidence |
|---|---|---|
| C-001 | Fixed in code; user action outstanding | `git ls-files .env` is empty; `.gitignore:11` ignores `.env`; `.env.example` lists the 4 keys with empty values. The old `.env` remains in history (`4ad52ea`), so `AUTH_USERNAME` / `AUTH_PASSWORD` must be rotated by the user. |
| M-001 | Fixed | `tests/fixtures.ts:37` logs only `Auth token generated`. |
| m-001 | Fixed | `tests/BOOK-1.spec.ts:50-51` use `error instanceof Error ? error.message : String(error)`. |

## Plan / AC Conformance (round 2)
| REQ / AC | Covered by | Status |
|---|---|---|
| R1 / AC1 | `getBooking()` resolves (`tests/BOOK-1.spec.ts:28`) | Met |
| R2 / AC2 | `getBooking()` throws on non-200 (`tests/pom/BookingAPI.ts:41`), noted in the spec comment at line 27 | Met (implicit, as the plan allows) |
| R3 / AC3 | `typeof`, non-empty, `>= 0`, ISO-regex assertions (spec lines 31-42) | Met |
| R4 / AC4 | `toEqual(bookingPayload)` (spec line 45) | Met |

Notes (not findings): the fixes are committed locally on the feature branch and nothing is pushed. `implementation_plan.md` still references `@security-scan`.

## Human Approval (rounds 1-2)
- Round 2: approved by user at the gate. Adjustments: none.
- Round 1: approved by user; Critical finding C-001 explicitly acknowledged at the gate. Adjustments: none.

---

# Round 1 record (initial review)

Verdict: request_changes — Critical: 1, Major: 1, Minor: 1. All three were handed to `@sdlc-review-fix` and fixed in commits `db68f67` (C-001), `75d18ae` (M-001) and `5de465f` (m-001).

## Critical (round 1)

### C-001: `.env` with credentials is committed and not git-ignored
- Location: `.gitignore:1-8` and `.env` (tracked since commit `4ad52ea`)
- Severity: Critical
- Category: Security
- Issue: `git ls-files .env` lists the file and `.gitignore` has no `.env` entry. `.env` holds `AUTH_USERNAME` / `AUTH_PASSWORD`, read by `tests/fixtures.ts:16-17`. The implementation plan's risk table required confirming `.env` is git-ignored; it is not. Opening a PR would expose the credentials. Values were not read or printed during review.
- Suggestion: Add `.env` to `.gitignore` and run `git rm --cached .env`. Add a `.env.example` with placeholder keys. Rotate the credentials, since they are already in history.

## Major (round 1)

### M-001: Auth token logged to console and reports
- Location: `tests/fixtures.ts:37`
- Severity: Major
- Category: Security
- Issue: `console.log('Auth Token Generated:', token)` writes a live token to every run's output, which the HTML reporter in `playwright.config.ts` can also capture. `tests/BOOK-1.spec.ts` triggers it through the `authToken` fixture. Flagged by the manifest and plan; the file is existing code that BOOK-1 exercises, not changed by BOOK-1.
- Suggestion: Remove the log, or log a fixed message without the token value.

## Minor (round 1)

### m-001: Unchecked `error as Error` cast in cleanup
- Location: `tests/BOOK-1.spec.ts:50`
- Severity: Minor
- Category: Type Safety
- Issue: `(error as Error).message` assumes the thrown value is an `Error`; a non-`Error` throw prints `undefined` and loses the cause.
- Suggestion: Use `error instanceof Error ? error.message : String(error)`.
