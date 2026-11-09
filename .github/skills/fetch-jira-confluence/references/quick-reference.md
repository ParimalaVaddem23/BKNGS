# Quick Reference: Using fetch-jira-confluence Skill

## One-Time Setup

```powershell
# Set environment variables in PowerShell
$env:JIRA_USERNAME = "your-email@example.com"
$env:JIRA_PASSWORD = "your-api-token"
$env:CONFLUENCE_USERNAME = "your-email@example.com"
$env:CONFLUENCE_PASSWORD = "your-api-token"
$env:ATLASSIAN_BASE_URL = "https://parimalavaddem23.atlassian.net"
```

See [setup.md](./setup.md) for permanent configuration options.

---

## Using the Skill

### Method 1: In Chat (Easiest)
```
/fetch-jira-confluence
Input: AUTO-42
```

### Method 2: Direct Python Script
```bash
python .github/skills/fetch-jira-confluence/scripts/fetch-jira-confluence.py AUTO-42
```

### Method 3: With Confluence Page
```bash
python .github/skills/fetch-jira-confluence/scripts/fetch-jira-confluence.py AUTO-42 123456789
```

---

## Output Location

Results saved to: `docs/artifacts/{ISSUE_ID}/requirements.md`

Example: `docs/artifacts/AUTO-42/requirements.md`

---

## What Gets Extracted from Jira

- ✅ Issue Key (AUTO-42)
- ✅ Summary/Title
- ✅ Full Description
- ✅ Acceptance Criteria (automatically extracted)
- ✅ Issue Status
- ✅ Issue Type
- ✅ Assignee
- ✅ Story Points
- ✅ Labels
- ✅ Created Date
- ✅ Jira Link

---

## What Gets Extracted from Confluence

- ✅ Page Title
- ✅ Page Content (HTML body)
- ✅ Status
- ✅ Labels/Tags
- ✅ Confluence Link

---

## Next Step: Feed to Analysis Agent

After generating requirements.md:

```
Load docs/artifacts/AUTO-42/requirements.md and generate test cases from the acceptance criteria
```

Your requirement analysis agent can then:
- Parse acceptance criteria
- Generate BDD/Gherkin scenarios
- Create test case templates
- Identify test scenarios and edge cases

---

## Troubleshooting Checklist

- [ ] API tokens created? (https://id.atlassian.com/manage-profile/security/api-tokens)
- [ ] All 5 environment variables set?
- [ ] Using API token, not password?
- [ ] Issue key is correct? (e.g., AUTO-42, not auto-42)
- [ ] Confluence page ID format correct? (numbers only)
- [ ] Terminal restarted after setting environment variables?

---

## Common Workflows

### Workflow: Process Jira Ticket → Generate Tests

1. **Fetch requirements**
   ```
   /fetch-jira-confluence
   Input: PROJ-123
   ```

2. **Review generated file**
   ```
   Open: docs/artifacts/PROJ-123/requirements.md
   ```

3. **Feed to analysis agent**
   ```
   Generate test cases from docs/artifacts/PROJ-123/requirements.md
   ```

4. **Create test scripts** (using your test framework)

---

## File Structure

```
.github/skills/fetch-jira-confluence/
├── SKILL.md                           # Main skill documentation
├── scripts/
│   └── fetch-jira-confluence.py      # Python implementation
└── references/
    ├── setup.md                       # Detailed setup guide
    └── quick-reference.md             # This file
```

---

## API Rate Limits

- Jira: 60 API calls per minute (standard)
- Confluence: 60 API calls per minute (standard)
- No caching implemented yet; each run makes fresh API calls

---

## Next: Extend the Skill

Possible enhancements:
- [ ] Cache results to reduce API calls
- [ ] Extract test case templates (Gherkin format)
- [ ] Fetch related child issues/subtasks
- [ ] Generate HTML report in addition to Markdown
- [ ] Extract test data and test scenarios automatically

