# Implementation Plan: BOOK-1

## Pipeline Context

- **Ticket:** BOOK-1
- **Mode:** gated (standard Copilot SDLC)
- **Pipeline state:** .vscode/sdlc-checkpoints/BOOK-1/pipeline_state.json
- **Artifacts:** docs/artifacts/BOOK-1/ (problem_spec.md, design_spec.md, design_review.md)

## Problem Summary

Verify that the Booking API (Restful-Booker, `GET /booking/{id}`) returns complete booking details (firstname, lastname, totalprice, depositpaid, bookingdates, additionalneeds) when a valid booking ID is provided. "Valid booking" means one created via `POST /booking` with valid details. The deliverable is a single Playwright API test; no production code changes.

## Key Requirements & Constraints

| ID | Priority | Description |
|---|---|---|
| R1 / AC1 | P0 | `GET /booking/{bookingId}` succeeds without exception |
| R2 / AC2 | P0 | Response status code is exactly 200 |
| R3 / AC3 | P0 | Response contains `firstname` (non-empty string), `lastname` (non-empty string), `totalprice` (number ≥ 0), `depositpaid` (boolean), `bookingdates` (`checkin`/`checkout` ISO 8601), `additionalneeds` (string, optional) |
| R4 / AC4 | P0 | Retrieved data matches the creation payload field-for-field |

P1 / P2: none identified.

**Constraints:**
- Target API: https://restful-booker.herokuapp.com (from `BASE_URL` in `.env`); real backend, no mocking.
- Auth token via `authToken` fixture (`AUTH_USERNAME` / `AUTH_PASSWORD` env vars); no hardcoded credentials.
- Single happy-path scenario: create booking → retrieve → validate.
- No retry logic; Playwright default timeouts; fail fast.
- Zero modifications to existing files (additive only).

**Non-Goals:**
- Invalid / non-existent booking IDs, unauthorized access, malformed requests.
- Performance / load testing, concurrent access, deleted-booking retrieval.
- HTTP error-code handling (400/401/403/404/500) and error message formats.

## Architecture Summary

- Pattern: Page Object Model + Playwright custom fixtures + Arrange-Act-Assert.
- Existing, unchanged components: COMP-001 `tests/pom/BookingAPI.ts` (`createBooking`, `getBooking`; both throw on non-200), COMP-002 `tests/pom/AuthAPI.ts`, COMP-003 `tests/fixtures.ts` (`apiRequest`, `authToken`), COMP-004 `tests/interfaces/types.ts` (`CreateBookingRequest`, `CreateBookingResponse`, `GetBookingResponse`, `BookingData`, `BookingDates`).
- New component: COMP-005 `tests/BOOK-1.spec.ts` with one `test.describe('BOOK-1: Retrieve Booking by Valid ID')` containing `test('should retrieve booking with all required fields')`.
- Data flow: fixtures inject `apiRequest` + `authToken` → `new BookingAPI(apiRequest, authToken)` → `createBooking(bookingPayload)` returns `bookingid` → `getBooking(bookingId)` → assert presence, types, values → fixture teardown.
- ADRs: ADR-001 reuse existing `getBooking()`; ADR-002 inline test data; ADR-003 validate all fields.
- Naming: `bookingPayload`, `createResponse`, `getResponse`, `bookingId`, `expected*` prefixes; assertions via `expect(value, 'message')`.

## Design Review Conditions

Verdict: `approve_with_concerns` (score 78/100, 0 critical, 0 blocking). All concerns are medium/low and are to be resolved during implementation and code review:

1. **AC-001 / CR-002:** Confluence booking data is not embedded. Inline the exact payload in the spec file and confirm it is accepted by the API.
2. **MC-001 / CR-004:** `additionalneeds` behavior (present / omitted / null) is unspecified. Verify actual API behavior and assert accordingly.
3. **MC-002 / CR-005 (new):** Add explicit runtime type checks (`typeof` for string/number/boolean, ISO 8601 date pattern for `checkin` / `checkout`); TypeScript only covers compile time.
4. **MC-004 / CR-004:** Choose one assertion style (`toEqual` deep equality vs. field-by-field `toBe`) and add descriptive messages.
5. **MC-003 / CR-003:** Decide on cleanup. If `deleteBooking()` is called, make it best-effort (catch failures, log WARN) so cleanup never fails the test.
6. **MC-006 (low):** API versioning / backward compatibility not discussed; record as a known gap (no change required).

Blocked flags (out of scope, no tests): FLAG-001 non-existent ID, FLAG-002 concurrent access, FLAG-003 HTTP error codes, FLAG-004 performance SLA.

## Pre-Implementation Baseline

- Run: `npx playwright test` and record pass/fail counts **before** any change.
- Expected: 0 tests (`tests/createbooking.spec.ts` is currently empty and `package.json` has no scripts). Record the actual output.
- Prerequisite: `.env` contains `BASE_URL`, `AUTH_USERNAME`, `AUTH_PASSWORD`. Do not print or commit their values.

## Implementation Steps

### Execution Mode: inline

### Step 1: tests/BOOK-1.spec.ts (new) [COMP-005]

- **Purpose:** Implement the P0 test: create a booking, retrieve it by ID, and validate status, fields, types, and values.
- **Dependencies:** COMP-001 (`BookingAPI`), COMP-003 (`test`/`expect` from `./fixtures`), COMP-004 (types). All already exist.
- **Key notes:**
  - Import `test, expect` from `./fixtures` (not `@playwright/test`) so `apiRequest` and `authToken` fixtures are available.
  - Instantiate `new BookingAPI(apiRequest, authToken)`.
  - Define the payload inline as `CreateBookingRequest` with realistic values, non-empty names, `totalprice ≥ 0`, `YYYY-MM-DD` dates, and `additionalneeds` populated.
  - Status 200 (AC2): `BookingAPI.getBooking()` returns only the parsed body and throws on non-200, so a resolved call proves 200. State this in a comment; do not modify `BookingAPI.ts` to expose the status.
  - Assert presence of all six fields, runtime types (`typeof`), ISO date format, then value equality against the payload. Add descriptive assertion messages.
  - Resolve the `additionalneeds` behavior empirically on the first run and assert accordingly.
  - Cleanup: if used, call `deleteBooking(bookingId)` best-effort in a `finally` / `afterEach` with a WARN log on failure; otherwise document why it is skipped. Do not log the token or PII.
  - Do not modify any existing file; `tests/example.spec.ts` referenced in design_spec does not exist, so ignore that reference.
- **Acceptance criteria:** R1/AC1, R2/AC2, R3/AC3, R4/AC4.
- **Verify:** `npx playwright test tests/BOOK-1.spec.ts` and `npx tsc --noEmit`

## Wave Plan

N/A — inline execution (≤8 files)

| Wave | Files | Deps satisfied | Test command |
|---|---|---|---|
| 0 | tests/BOOK-1.spec.ts | all dependencies already exist | `npx playwright test tests/BOOK-1.spec.ts` |

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Confluence payload not embedded; payload may not match API expectations | Test fails at runtime with unclear error | Inline payload, validate on first run (CR-002) |
| `additionalneeds` returned as omitted/null/empty | False failure on field assertion | Observe actual response and assert accordingly (CR-004) |
| Shared public Restful-Booker instance is flaky / rate-limited | Intermittent failures | Fail fast, rerun; no retries per constraints; note flakiness in PR |
| Leftover bookings on shared instance without cleanup | Data pollution | Best-effort `deleteBooking()` (CR-003) or documented skip |
| Status 200 not directly observable via `getBooking()` | AC2 asserted only implicitly | Document in test comment; do not change COMP-001 (zero-change constraint) |
| Design spec lists nonexistent `tests/example.spec.ts`; `createbooking.spec.ts` is empty | Misleading baseline | Treat as spec inaccuracy; baseline expected 0 tests |
| `authToken` fixture logs the token via `console.log` (existing) | Secret exposure in logs/reports | Out of scope to change; do not add new token logging; flag in review |
| Credentials in `.env` | Secret leakage | Never print or commit values; confirm `.env` is git-ignored |
| No npm scripts defined | Unclear run commands | Use `npx playwright test ...` directly |

## Edge Cases (from problem_spec)

| ID | Scenario | Expected behavior |
|---|---|---|
| EC-001 | Non-existent booking ID | BLOCKED (needs input) — out of scope, no test |
| EC-002 | Concurrent access to same booking | BLOCKED — out of scope, no test |
| EC-003 | Deleted booking retrieval | BLOCKED — out of scope, no test |
| EC-004 | Large/unusual booking data | BLOCKED — out of scope, no test |

## Non-Functional Hardening Tasks

### Controller / API Boundary
- [ ] All path inputs validated (null, blank, case contract)
- [ ] All new response fields: null fallback defined
- [ ] API documentation annotations: auth per role, case-sensitivity, all error conditions

### Service Layer
- [ ] Every map lookup: explicit null handling
- [ ] Every data-anomaly handler (merge, dedup): WARN-level log with context
- [ ] Every nullable entity field read: null guard with descriptive exception

### Data Access / Query Layer
- [ ] Every non-trivial query: algorithm comment
- [ ] Every filter/join on non-PK columns: inline comment noting required index
- [ ] GROUP BY on nullable: NOT NULL filter

### Exception Handling
- [ ] Every custom exception: verified in centralized error handler
- [ ] Exception messages include the triggering value

### Logging / Observability
- [ ] No INFO+ logs emit raw emails / names / PII
- [ ] Every swallowed exception: WARN or ERROR with the original attached

### API Contract Documentation
- [ ] design_spec API contracts reflected in API docs (Swagger / OpenAPI)
- [ ] Case-sensitivity / casing contract documented

## Post-Implementation Checklist

- [ ] All tests pass (no regressions from baseline)
- [ ] `impl_manifest.md` written with accurate file lists
- [ ] Health-check endpoints verified (if applicable)
- [ ] All Non-Functional Hardening Tasks completed or marked N/A with one-line justification

## Pipeline Continuation

After implementation completes, the `@sdlc` orchestrator continues through:

- Phase 6: Implementation
- Phase 7: Review (`@code-review` + `@security-scan`)
- Phase 8: PR Creation (`/create-pr` prompt)

**Do not skip phases 6–8.**

Resume: `@sdlc resume BOOK-1`
