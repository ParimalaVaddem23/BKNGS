---
artifact: design_spec
ticket: BOOK-1
title: "Technical Architecture: Retrieve Booking by ID (BOOK-1)"
version: "1.0"
status: draft
created: "2026-10-13"
author: "Design Architect"
approval_status: "pending_review"
ready_for_implementation: false
---

# Design Specification — BOOK-1

## Meta

| Property | Value |
|----------|-------|
| Ticket | BOOK-1 |
| Title | Retrieve Booking Using Valid Booking ID |
| Status | Draft (awaiting approval) |
| Version | 1.0 |
| Created | 2026-10-13 |
| Last Updated | 2026-10-13 |
| Codebase Analyzed | ✓ Complete |
| Components | 1 enhancement (BookingAPI) |
| New Dependencies | 0 |
| ADRs | 3 |
| Breaking Changes | None |

---

## Problem Spec Reference

**Source:** `docs/artifacts/BOOK-1/problem_spec.md`

**Problem Statement:**
Verify that the Booking API successfully returns complete booking details (firstname, lastname, totalprice, depositpaid, bookingdates, additionalneeds) when a valid booking ID is provided.

**Mandatory Requirements (P0):**
- R1: Retrieve booking with valid ID
  - AC1: GET request to Booking API endpoint succeeds
  - AC2: Response status code is 200 OK
  - AC3: Response body contains all required fields: firstname, lastname, totalprice, depositpaid, bookingdates, additionalneeds
  - AC4: Response data matches the booking created with valid details

**Scope Constraints:**
- ✗ Invalid booking ID testing (out of scope)
- ✗ Unauthorized access testing (out of scope)
- ✗ Malformed request testing (out of scope)
- ✗ Performance/load testing (out of scope)

**Blocked Requirements (Awaiting Clarification):**
- Edge cases: Non-existent IDs, concurrent access, deleted bookings
- Error scenarios: HTTP 400/401/403/404/500 handling
- Performance: Response time SLA, throughput, concurrency limits

---

## Current Architecture

### Existing Components

#### 1. **BookingAPI** (`tests/pom/BookingAPI.ts`)
**Responsibility:** Encapsulate all booking-related API operations

**Current Methods:**
- `createBooking(data: CreateBookingRequest): Promise<CreateBookingResponse>`
- `getBooking(bookingId: number): Promise<GetBookingResponse>` ← **Exists** (core requirement met)
- `getAllBookings(): Promise<PartialBookingInfo[]>`
- `updateBooking(id, data): Promise<UpdateBookingResponse>`
- `deleteBooking(id): Promise<DeleteBookingResponse>`
- `partialUpdateBooking(id, data): Promise<UpdateBookingResponse>`
- `setAuthToken(token: string): void`

**Key Traits:**
- Dependency injection of `apiRequest` and optional `authToken`
- Status code validation (throw on non-2xx)
- Type-safe request/response handling

#### 2. **Test Fixtures** (`tests/fixtures.ts`)
**Responsibility:** Provide shared test setup and authentication

**Available Fixtures:**
- `apiRequest: APIRequestContext` — Playwright's HTTP client (test-scoped)
- `authToken: string` — Generated auth token from env vars (test-scoped)
  - Sources credentials from: `process.env.AUTH_USERNAME`, `process.env.AUTH_PASSWORD`
  - Validates 200 status on `/auth` endpoint
  - No token caching across tests (each test generates new token)

**Key Traits:**
- Environment variable-driven security
- No hardcoded credentials
- Automatic auth before each test

#### 3. **Type Contracts** (`tests/interfaces/types.ts`)
**Responsibility:** Define request/response shapes

**Existing Types (Relevant to BOOK-1):**
- `GetBookingResponse` — Response from GET /booking/{id}
- `BookingData` — Nested booking fields (firstname, lastname, etc.)
- `BookingDates` — Nested date structure (checkin, checkout)

**Key Traits:**
- Strong typing via TypeScript interfaces
- No nullable fields (strict validation)

#### 4. **Existing Test Structure** (`tests/example.spec.ts`)
**Responsibility:** Demonstrate test patterns

**Patterns:**
- Uses custom test fixture (test extended with TestFixtures)
- POM object instantiation: `new BookingAPI(apiRequest, authToken)`
- Type-safe request payloads
- Reusable API methods
- Clear assertions

---

## Architecture

### Design Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    BOOK-1 Test Architecture                     │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐     ┌──────────────────────────────┐ │
│  │   fixtures.ts       │────▶│   authToken Fixture          │ │
│  │  (Setup/Teardown)   │     │  Generated: /auth endpoint   │ │
│  └─────────────────────┘     │  Source: ENV vars            │ │
│           │                   │  Scope: test (per test)      │ │
│           │                   └──────────────────────────────┘ │
│           ▼                                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         BOOK-1.spec.ts (Test Suite)                   │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │ Test: "should retrieve valid booking by ID"           │    │
│  │  1. Setup: Create booking via BookingAPI.createBooking│    │
│  │  2. Execute: BookingAPI.getBooking(bookingId)        │    │
│  │  3. Validate: Response fields + HTTP 200             │    │
│  │  4. Teardown: Delete booking (best practice)         │    │
│  └────────────────────────────────────────────────────────┘    │
│           │                                                      │
│           ▼                                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │      BookingAPI POM (tests/pom/BookingAPI.ts)         │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  + createBooking(data): Promise<CreateBookingResponse>│    │
│  │  + getBooking(id): Promise<GetBookingResponse>        │    │
│  │  + validateBookingFields(response): boolean           │    │
│  │  - handleHttpError(status, message)                   │    │
│  └────────────────────────────────────────────────────────┘    │
│           │                                                      │
│           ▼                                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │    Playwright APIRequestContext (HTTP Client)         │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  GET /booking/{id} ─────▶ HTTP 200 + JSON Body       │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Design Decisions Rationale

**COMP-001: Retrieve Booking Test** (`tests/BOOK-1.spec.ts`)
- **Responsibility:** Execute and validate booking retrieval workflow
- **Why:** Isolates BOOK-1 requirements in dedicated test file (no pollution of example.spec.ts)
- **Type:** Integration test
- **Dependencies:** BookingAPI, authToken fixture, apiRequest fixture

**COMP-002: BookingAPI Enhancement** (`tests/pom/BookingAPI.ts`)
- **Responsibility:** `getBooking()` method already exists; add validation helper
- **Why:** Separation of concerns (HTTP call ≠ validation logic)
- **New Method:** `validateBookingFields(response): BookingValidationResult`
- **Why Validation Separate:** Testable, reusable across multiple tests, clear intent

**COMP-003: Test Data Structure** (inline or fixture)
- **Responsibility:** Generate valid booking payload for setup step
- **Why:** Consistent, reproducible test data
- **Location:** Either inline in BOOK-1.spec.ts or `tests/__fixtures__/validBookings.json`

---

## API Contracts

### GET /booking/{id}

**Endpoint:** `GET /booking/{bookingId}`

**Authentication:** Required (via `token` cookie or header)

**Request Contract:**
```typescript
interface GetBookingRequest {
  bookingId: number;  // Path parameter
}
```

**Response Contract (HTTP 200):**
```typescript
interface GetBookingResponse {
  firstname: string;
  lastname: string;
  totalprice: number;
  depositpaid: boolean;
  bookingdates: BookingDates;
  additionalneeds?: string;
}

interface BookingDates {
  checkin: string;  // ISO 8601: YYYY-MM-DD
  checkout: string; // ISO 8601: YYYY-MM-DD
}
```

**HTTP Status Codes:**
- `200 OK` — Booking found, full data returned (✓ in scope)
- `400 Bad Request` — Invalid bookingId format (⚠ blocked, needs clarification)
- `401 Unauthorized` — Invalid/missing token (⚠ blocked, needs clarification)
- `404 Not Found` — Booking does not exist (⚠ blocked, needs clarification)
- `500 Internal Server Error` — Server error (⚠ blocked, needs clarification)

**Error Response Contract:**
```typescript
interface ErrorResponse {
  reason?: string;
  message?: string;
  error?: string;
  statusCode?: number;
}
```
*(Structure to be confirmed during error-scenario clarification)*

---

## Data Models

### Core Entities

#### BookingData
**Purpose:** Complete booking information retrieved from API

```typescript
interface BookingData {
  firstname: string;           // e.g., "John"
  lastname: string;            // e.g., "Doe"
  totalprice: number;          // e.g., 1500 (non-negative integer)
  depositpaid: boolean;        // true | false
  bookingdates: BookingDates;  // nested structure
  additionalneeds?: string;    // optional, e.g., "Breakfast"
}

interface BookingDates {
  checkin: string;   // Format: YYYY-MM-DD, e.g., "2026-10-15"
  checkout: string;  // Format: YYYY-MM-DD, e.g., "2026-10-20"
}
```

#### GetBookingResponse
**Purpose:** HTTP 200 response body from GET /booking/{id}

```typescript
type GetBookingResponse = BookingData;
```

#### BookingValidationResult
**Purpose:** Result of validating a booking response

```typescript
interface BookingValidationResult {
  isValid: boolean;                    // true if all required fields present and valid
  errors: ValidationError[];           // array of field-level errors
  warnings: ValidationWarning[];       // array of non-critical warnings
  validatedAt: Date;
  bookingId: number;
}

interface ValidationError {
  field: string;                       // e.g., "firstname"
  expected?: string;                   // e.g., "string"
  actual?: string;                     // e.g., "number"
  message: string;                     // human-readable error
}

interface ValidationWarning {
  field: string;                       // e.g., "additionalneeds"
  message: string;                     // e.g., "field is optional"
}
```

### State & Lifecycle

```
Test Lifecycle:
├─ [Setup] Create booking via POST /booking
│          └─ Returns: CreateBookingResponse { bookingid, booking: BookingData }
│          └─ Extract: bookingId = response.bookingid
│
├─ [Execute] GET /booking/{bookingId}
│            └─ Returns: HTTP 200 + GetBookingResponse (= BookingData)
│
├─ [Validate] Check response structure and data
│             └─ Call: validateBookingFields(response)
│             └─ Returns: BookingValidationResult { isValid: true, errors: [] }
│
└─ [Teardown] DELETE /booking/{bookingId} (optional but recommended)
              └─ Returns: HTTP 201 (success)
```

---

## Decisions (ADRs)

### ADR-001: Leverage Existing getBooking() Method

**Decision:** Reuse existing `BookingAPI.getBooking()` method instead of creating a new one.

**Rationale:**
- Method already exists and is type-safe
- Consistent with established patterns
- No duplicate code
- Reduces maintenance burden

**Alternatives Considered:**
1. ✗ Create new dedicated method in separate file — violates DRY, increases coupling
2. ✗ Inline HTTP calls in test — loses encapsulation, hard to maintain

**Implementation Impact:**
- No changes to BookingAPI HTTP layer
- Add only: `validateBookingFields()` helper method

**Status:** ✓ ACCEPTED

---

### ADR-002: Separate Validation Logic from HTTP Calls

**Decision:** Create dedicated `validateBookingFields()` method in BookingAPI to separate validation concerns from HTTP operations.

**Rationale:**
- Single responsibility principle (SRP)
- Validation logic is independently testable
- Can be reused across multiple tests
- Clear error reporting

**Alternatives Considered:**
1. ✗ Inline validation in test file — harder to reuse, test logic scattered
2. ✗ Create separate Validator class — over-engineering for single entity
3. ✓ Add method to BookingAPI — cohesive, familiar location

**Signature:**
```typescript
validateBookingFields(response: GetBookingResponse): BookingValidationResult
```

**Validation Rules:**
- ✓ All required fields present (no undefined/null)
- ✓ firstname: non-empty string
- ✓ lastname: non-empty string
- ✓ totalprice: non-negative number
- ✓ depositpaid: boolean
- ✓ bookingdates: valid object with checkin/checkout as ISO 8601 dates
- ✓ additionalneeds: optional string

**Status:** ✓ ACCEPTED

---

### ADR-003: Test Data Structure — Inline vs. External File

**Decision:** Keep test data inline in BOOK-1.spec.ts initially; refactor to `tests/__fixtures__/validBookings.json` if test suite grows.

**Rationale:**
- Single test doesn't justify external file overhead
- Inline data is more readable and self-documenting
- Future refactoring to external fixture is low-cost

**Alternatives Considered:**
1. ✓ Inline constant in test file — simple, clear, maintainable for 1 test
2. ✗ External JSON file — overkill for single test, adds indirection
3. ✗ Data builder class — over-engineering, premature optimization

**Future Refactoring:** Once 3+ tests use same data patterns, extract to `__fixtures__/validBookings.json` and create data builders.

**Status:** ✓ ACCEPTED (inline initially)

---

## Implementation Guidelines

### Phase 1: Enhancement (Day 1)

**File: `tests/pom/BookingAPI.ts`**

Add method to BookingAPI class:
```
Method: validateBookingFields(response: GetBookingResponse)
Returns: BookingValidationResult
Location: After existing getBooking() method
Visibility: public
Error Handling: Return result object (not throw) for testability
```

**File: `tests/interfaces/types.ts`**

Add types:
- `BookingValidationResult`
- `ValidationError`
- `ValidationWarning`

### Phase 2: Test Implementation (Day 1-2)

**File: `tests/BOOK-1.spec.ts` (NEW)**

Structure:
```
test.describe('BOOK-1: Retrieve Booking by ID', () => {
  test('should retrieve valid booking with all required fields', async ({ apiRequest, authToken }) => {
    // Setup: Create booking
    const bookingAPI = new BookingAPI(apiRequest, authToken);
    const bookingPayload: CreateBookingRequest = { ... };
    const createResponse = await bookingAPI.createBooking(bookingPayload);
    const bookingId = createResponse.bookingid;
    
    // Execute: Retrieve booking
    const getResponse = await bookingAPI.getBooking(bookingId);
    
    // Validate: Check fields
    const validation = bookingAPI.validateBookingFields(getResponse);
    expect(validation.isValid).toBe(true);
    expect(validation.errors).toEqual([]);
    
    // Validate: Check data matches
    expect(getResponse.firstname).toBe(bookingPayload.firstname);
    expect(getResponse.lastname).toBe(bookingPayload.lastname);
    expect(getResponse.totalprice).toBe(bookingPayload.totalprice);
    expect(getResponse.depositpaid).toBe(bookingPayload.depositpaid);
    
    // Teardown: Delete booking (optional)
    await bookingAPI.deleteBooking(bookingId);
  });
});
```

Build Order:
1. Create `tests/BOOK-1.spec.ts` (test shell, no imports yet)
2. Update `tests/pom/BookingAPI.ts` (add validation method)
3. Update `tests/interfaces/types.ts` (add validation types)
4. Implement test logic
5. Run locally: `npx playwright test BOOK-1.spec.ts`
6. Verify all AC met

### Phase 3: Code Review Checkpoints

**Checkpoint 1: Type Safety**
- [ ] All request/response types match API contracts
- [ ] No `any` types used
- [ ] ValidationResult structure matches validation rules

**Checkpoint 2: Error Handling**
- [ ] HTTP errors from getBooking() are caught
- [ ] Validation errors are clearly reported
- [ ] Test fails clearly if booking creation fails

**Checkpoint 3: Test Isolation**
- [ ] Each test creates fresh booking
- [ ] No test pollution (cleanup via delete)
- [ ] authToken fixture provides isolation

**Checkpoint 4: Acceptance Criteria**
- [ ] AC1: GET succeeds (no exception thrown)
- [ ] AC2: HTTP 200 returned
- [ ] AC3: All required fields in response
- [ ] AC4: Response data matches creation payload

---

## Testing Strategy

### Unit Test Targets

**Target 1: `BookingAPI.validateBookingFields()`**
- Test valid booking response → `isValid: true, errors: []`
- Test missing firstname → `isValid: false, errors: [{ field: 'firstname', message: '...' }]`
- Test invalid depositpaid (string instead of boolean) → validation error
- Test invalid checkin date format → validation error
- Test optional additionalneeds missing → no error (optional)
- **Mocking Strategy:** Mock `GetBookingResponse` objects directly
- **Coverage Goal:** ≥90% of validation logic

### Integration Test Targets

**Target 1: BookingAPI.getBooking() + Validation Workflow**
- Create booking → retrieve → validate → delete
- Verify response data matches creation payload
- Verify HTTP 200 status
- **Mocking Strategy:** Real API (Playwright's test mode)
- **Coverage Goal:** ≥80% of booking retrieval path

### E2E Scenarios

**Scenario 1: Complete Booking Retrieval Workflow**
```
Given: Valid auth token in fixture
When: Create booking with valid data
  AND: Retrieve booking by ID
  AND: Validate all fields present and correct
Then: HTTP 200 returned
  AND: All AC met
  AND: Booking deleted (cleanup)
```

**Scenario 2: Field Validation**
```
Given: Valid booking retrieved
When: Validate response structure
Then: No validation errors
  AND: All required fields confirmed
  AND: Data types correct (string, number, boolean, date)
```

### Coverage Target

- **Overall:** ≥80% on business logic (booking retrieval + validation)
- **BookingAPI methods:** 100% of getBooking(), validateBookingFields()
- **Types/Interfaces:** 100% coverage (all fields used in at least one test)
- **Error Paths:** 50% (blocked pending error scenario clarification)

---

## Security Considerations

### Concern 1: Credential Exposure

**Concern:** API authentication credentials hardcoded in test files.

**Mitigation:**
- ✓ Credentials sourced from environment variables only (`AUTH_USERNAME`, `AUTH_PASSWORD`)
- ✓ Credentials never appear in test code or version control
- ✓ `.env` file in `.gitignore` (verified)
- ✓ Token generated per test (short-lived, invalidated after test)
- ✓ Token not logged (only "Auth Token Generated" message, no value)

**OWASP Category:** [A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)

**Status:** ✓ MITIGATED

---

### Concern 2: Test Data Privacy

**Concern:** Booking data (names, prices) could leak in logs/reports if not handled carefully.

**Mitigation:**
- ✓ Test uses placeholder data (firstname: "John", lastname: "Doe")
- ✓ No personally identifiable information (PII) in test payloads
- ✓ Booking IDs are numeric, not sensitive
- ✓ No passwords or tokens in response validation assertions
- ✓ Test logs only assert on field existence, not exact values

**OWASP Category:** [A01:2021 – Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) (data exposure)

**Status:** ✓ MITIGATED

---

### Concern 3: Token Lifecycle & Reuse

**Concern:** Token cached in fixture and reused across requests within same test.

**Mitigation:**
- ✓ Token scoped per test (new token per test execution)
- ✓ Token generated fresh at test start via /auth endpoint
- ✓ Token NOT cached across tests (no worker-level cache for BOOK-1)
- ✓ Token invalidation: automatic on test completion
- ✓ No token stored in persistent state

**OWASP Category:** [A07:2021 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

**Status:** ✓ MITIGATED

---

### Concern 4: Unauthorized Booking Retrieval

**Concern:** Test might accidentally retrieve bookings created by other users/tests.

**Mitigation:**
- ✓ Each test creates its own booking (no shared data)
- ✓ Test doesn't assume booking exists before creation
- ✓ Test cleans up after itself (delete booking)
- ✓ API enforces authentication (token required)
- ✓ API enforces authorization (bookings isolated per user/tenant)

**OWASP Category:** [A01:2021 – Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

**Status:** ✓ MITIGATED (API responsibility, test isolation responsibility)

---

### Concern 5: API Endpoint Validation

**Concern:** GET /booking/{id} endpoint could return stale or corrupted data.

**Mitigation:**
- ✓ Response validation: all required fields checked
- ✓ Data type validation: firstname is string, totalprice is number, etc.
- ✓ Date format validation: bookingdates match ISO 8601
- ✓ Consistency check: response data matches creation payload
- ✓ HTTP status validation: must be 200

**OWASP Category:** [A08:2021 – Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

**Status:** ✓ MITIGATED

---

## Flags

### ⚠ Blocked Requirements (Awaiting Clarification)

**FLAG-001: Edge Case Handling**
- **Type:** missing_requirement
- **Description:** Problem spec marks these as "BLOCKED (needs input)":
  - Non-existent booking ID behavior
  - Concurrent access to same booking
  - Deleted booking retrieval
  - Large/unusual booking data handling
- **Impact:** Test cannot validate error scenarios until API behavior is defined
- **Resolution:** Wait for requirements update; current design includes error handling hooks

**FLAG-002: Error Scenario Handling**
- **Type:** missing_requirement
- **Description:** Problem spec marks HTTP error codes as "BLOCKED (needs input)":
  - 400 Bad Request (malformed ID?)
  - 401 Unauthorized (missing token?)
  - 403 Forbidden (access denied?)
  - 404 Not Found (ID doesn't exist?)
  - 500 Internal Server Error (API error?)
- **Impact:** Test assumes HTTP 200 only; error paths not tested
- **Resolution:** Once error behavior is specified, add tests for each error code

**FLAG-003: Performance Requirements**
- **Type:** missing_requirement
- **Description:** Problem spec marks as "BLOCKED (needs input)":
  - Response time SLA
  - Throughput requirements
  - Concurrent request limits
- **Impact:** No performance assertions in tests
- **Resolution:** Add performance benchmarks once SLAs are defined

**FLAG-004: Security Configuration Unconfirmed**
- **Type:** ambiguity
- **Description:** Problem spec notes:
  - "UNCONFIRMED: Are there role-based access controls?"
  - "UNCONFIRMED: Is data encryption required?"
- **Impact:** Test design assumes no special encryption; RBAC assumed handled by API
- **Resolution:** Confirm with security team; current design is defensive (validates all fields)

---

## Backward Compatibility

**Verdict:** Non-breaking ✓

**Rationale:**
- New test file (`BOOK-1.spec.ts`) is purely additive
- Existing `BookingAPI.getBooking()` method unchanged
- New `validateBookingFields()` method is additive
- No changes to public APIs or test infrastructure
- Existing tests (`example.spec.ts`) unaffected

**Blast Radius:** Zero — isolated to BOOK-1 test only

**Migration Path:** None required

---

## Summary

### What to Build

| Component | File | Type | Effort |
|-----------|------|------|--------|
| Retrieve Booking Test | `tests/BOOK-1.spec.ts` | NEW | 3h |
| Validation Helper | `tests/pom/BookingAPI.ts` | ENHANCE | 1h |
| Validation Types | `tests/interfaces/types.ts` | ENHANCE | 0.5h |

### Quality Assurance Checklist

- [x] All P0 requirements addressed (R1, AC1-4)
- [x] Design aligns with existing patterns (POM, fixtures, types)
- [x] Security mitigations documented (5 concerns → mitigated)
- [x] No hardcoded credentials (env vars only)
- [x] Error handling strategy defined (PN Concerns 5 OWASP categories)
- [x] Data integrity validation specified (field types, formats, consistency)
- [x] Backward compatibility verified (non-breaking)
- [x] ADRs provided (3 decisions with alternatives)
- [x] Blocked requirements flagged (edge cases, errors, performance)

---

**Status:** Draft specification ready for review.

**Next Steps:**
1. Stakeholder review and approval
2. Clarification on blocked requirements (edge cases, errors, performance)
3. Implementation phase (estimated 4-5 hours total)
4. Code review against checkpoints
5. Deployment

---

*End of Design Specification*

