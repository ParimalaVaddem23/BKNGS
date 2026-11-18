---
name: sdlc-impl-planning
description: >
  Produce `implementation_plan.md` from approved SDLC artifacts for a Jira
  ticket. Invoke as `@sdlc-impl-planning BOOK-123` or via handoff from `@sdlc`
  after a green design review. Self-contained so a fresh Copilot session can
  execute it. Not for requirements, architecture, or writing implementation
  code.
tools:
  - read
  - search
  - edit
  - execute
---

# SDLC Implementation Planning

Produce a self-contained implementation plan from prior SDLC artifacts. The plan must contain enough context that a fresh Copilot session (no prior history) can execute it correctly and continue through the remaining pipeline phases.

## Invocation

```
@sdlc-impl-planning STEP-123
```

## Inputs (read in this order)

From `docs/artifacts/<TICKET>/`:

1. `design_spec.md` — focus on `implementation_guidelines`, `components`, `testing_strategy`, `data_flow`.
2. `design_review.md` — focus on `verdict`, `conditions`, `concerns`, `findings`.
3. `problem_spec.md` — focus on `requirements`, `constraints`, `edge_cases`, `assumptions`, `non_goals`.

If any are missing, **HALT** and report:

```
Missing artifact: <file> at docs/artifacts/<TICKET>/
Cannot produce implementation plan. Run the preceding phase first.
```

## Process

### 1. Build the ordered file list

From `design_spec.components[]`, list every file to create or modify (path, new|modify, owning `COMP-###`). Verify each path and existing patterns against the codebase using `search` / `search/codebase` / `read`.

### 2. Compute the dependency graph and wave assignments

- Derive dependencies between components (a file depends on the `COMP-###` IDs it imports or calls).
- Assign waves topologically: Wave 0 has no dependencies; Wave N depends only on waves < N.
- Execution mode: `inline` if ≤ 8 files, otherwise `waves`.

### 3. Map acceptance criteria → files

From `problem_spec.requirements[]`, map every `REQ-###` / `AC-###` to the file(s) that satisfy it. Every requirement must map to at least one file; flag unmapped requirements.

### 4. Map test strategy per file

From `design_spec.testing_strategy`, assign each file a specific, runnable verify command (unit, integration, or e2e as defined by the spec and the repo's test setup, e.g. `package.json`, `playwright.config.ts`). Identify the pre-implementation baseline test command.

### 5. Identify risks and backward-compat concerns

Combine `design_review.md` conditions/concerns, `problem_spec` assumptions/edge cases, and anything found in the codebase (shared fixtures, public interfaces, existing tests) into the Risks table.

### 6. Draft the plan

Draft `implementation_plan.md` using the template below, incorporating steps 1–5. Explore the codebase as needed (`search`, `search/codebase`, `read`) to verify file paths, existing patterns, and dependencies.

**Before writing the artifact**, present the draft plan summary in chat and ask the user:

> "Draft plan ready — `<N>` files across `<W>` waves. Reply `approved` to write the artifact, or describe changes."

Wait for `approved`. On anything else, revise and re-present.

### 7. Write the artifact

Write `docs/artifacts/<TICKET>/implementation_plan.md` using the template. Then call `sdlc.validateArtifact(schema="implementation_plan", path=<path>)` and fix any reported issues. If the `sdlc/validateArtifact` tool is unavailable, self-check that every template section is present and say validation was skipped.

### 8. Create the feature branch and commit the plan

Via the `execute` tool (terminal):

```
git checkout -b <TICKET>-<short-description>
git add docs/artifacts/<TICKET>/implementation_plan.md
git commit -m "<TICKET>: add implementation plan"
```

`<short-description>` is derived from the problem summary — lowercase, hyphenated, max 4 words. Example: `STEP-123-add-social-login`.

Confirm: `Feature branch <branch-name> created with implementation plan committed.`

## Constraints

- DO NOT write implementation code, requirements, or architecture.
- DO NOT modify source files, `problem_spec.md`, `design_spec.md`, or `design_review.md`.
- ONLY write `implementation_plan.md` (and run the git commands in step 8).
- If `design_review.md` verdict is `reject`, HALT and route back to `@sdlc-architecture`.
- Non-Functional Hardening items that do not apply to the project (e.g. controller/service layers in a test-only project) are kept in the plan and marked N/A with a one-line justification at implementation time.

## `implementation_plan.md` Template

````markdown
# Implementation Plan: <TICKET>

## Pipeline Context

- **Ticket:** <TICKET>
- **Mode:** gated (standard Copilot SDLC)
- **Pipeline state:** .vscode/sdlc-checkpoints/<TICKET>/pipeline_state.json
- **Artifacts:** docs/artifacts/<TICKET>/ (problem_spec.md, design_spec.md, design_review.md)

## Problem Summary

<2–3 sentences from problem_spec.problem_statement>

## Key Requirements & Constraints

| ID | Priority | Description |
|---|---|---|
| REQ-001 | P0 | … |
| REQ-002 | P1 | … |

**Constraints:** …
**Non-Goals:** …

## Architecture Summary

<Key decisions from design_spec: patterns, component structure, data flow summary>

## Design Review Conditions

<Any conditions or concerns from design_review.md>

## Pre-Implementation Baseline

- Run: `<test command>` and record pass/fail counts **before** any change.

## Implementation Steps

### Execution Mode: <inline|waves>

### Step N: <file path> (<new|modify>) [COMP-###]

- **Purpose:** …
- **Dependencies:** <COMP-### IDs that must exist first>
- **Key notes:** …
- **Acceptance criteria:** <REQ-### AC-### mappings>
- **Verify:** `<specific test command>`

## Wave Plan

<Include if >8 files or waves requested. Otherwise: "N/A — inline execution (≤8 files)">

| Wave | Files | Deps satisfied | Test command |
|---|---|---|---|
| 0 | types.ts, constants.ts | none | `<cmd>` |
| 1 | service.ts | Wave 0 | `<cmd>` |

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| … | … | … |

## Edge Cases (from problem_spec)

| ID | Scenario | Expected behavior |
|---|---|---|
| EC-001 | … | … |

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
- Phase 7: Code Review (`@code-review`); findings loop to `@sdlc-review-fix`, then re-review
- Phase 8: PR Creation (`/create-pr` prompt)

**Do not skip phases 6–8.**

Resume: `@sdlc resume <TICKET>`
````

## On Completion

Report:

```
Impl plan complete — docs/artifacts/<TICKET>/implementation_plan.md
- Files: <N> (new <M>, modify <K>)
- Waves: <W>
- Branch: <TICKET>-<short-description>
- Key risks: <...>
```
