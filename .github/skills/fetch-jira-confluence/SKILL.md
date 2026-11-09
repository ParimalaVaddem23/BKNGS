---
name: fetch-jira-confluence
description: 'Fetch Jira ticket and Confluence page details for automation test implementation. Use when: providing an Issue ID to retrieve requirements, acceptance criteria, and documentation for test case generation.'
argument-hint: 'Provide: Issue ID (e.g., PROJ-123)'
user-invocable: true
---

# Fetch Jira Ticket & Confluence Details

## Overview
This skill retrieves Jira ticket information (Key, Summary, Description, Acceptance Criteria) and linked Confluence pages, then outputs structured Markdown for your requirement analysis agent.

## When to Use
- Implementing automation test cases based on Jira tickets
- Need to gather requirements and acceptance criteria for test generation
- Creating requirement documentation from Jira/Confluence sources
- Feeding structured requirements into your analysis agent

## Prerequisites

Create a configuration file at `.vscode/atlassian-api.local.json`:

```json
{
  "jira": {
    "baseUrl": "https://parimalavaddem23.atlassian.net",
    "email": "your-email@example.com",
    "token": "your-api-token"
  },
  "confluence": {
    "baseUrl": "https://parimalavaddem23.atlassian.net",
    "email": "your-email@example.com",
    "token": "your-api-token"
  }
}
```

**Note**: Generate API tokens at `https://id.atlassian.com/manage-profile/security/api-tokens`

⚠️ **Security**: Add `.vscode/atlassian-api.local.json` to `.gitignore` to prevent committing credentials.

## Procedure

### 1. Ensure Configuration File Exists
Verify `.vscode/atlassian-api.local.json` is properly configured with your Jira and Confluence credentials.

### 2. Provide the Jira Issue ID
When invoking this skill, provide the Issue ID (e.g., `PROJ-123`, `AUTO-45`)

### 3. The skill will:
- ✅ Load credentials from `.vscode/atlassian-api.local.json`
- ✅ Connect to your Jira instance using Basic Auth
- ✅ Extract Issue Key, Summary/Title, Description, and Acceptance Criteria
- ✅ Search for linked Confluence pages or documentation
- ✅ Retrieve Confluence page content by Page ID (if specified)
- ✅ Compile all information into structured Markdown format

### 3. Output
The skill creates a Markdown file at:
```
docs/artifacts/{JIRA_ISSUE_ID}/requirements.md
```

Output structure:
```markdown
# Requirements: {ISSUE_KEY} - {SUMMARY}

## Issue Details
- **Key**: PROJ-123
- **Title**: {Summary}
- **Status**: {Current Status}

## Description
{Full ticket description}

## Acceptance Criteria
{Formatted acceptance criteria}

## Related Confluence Pages
- **Page Title**: {Title}
- **Content**: {Page content}
- **Link**: {Confluence URL}

## Notes for Test Implementation
- Key test scenarios extracted from acceptance criteria
- Dependencies and edge cases identified
```

## Usage Examples

### Example 1: Simple Jira Ticket
```
Invoke: fetch-jira-confluence
Input: AUTO-42

Expected Output:
✅ Retrieved requirements from Jira ticket AUTO-42
✅ Generated docs/artifacts/AUTO-42/requirements.md
```

### Example 2: With Confluence Reference
```
Invoke: fetch-jira-confluence
Input: TEST-108 with Confluence page ID: 123456789

Expected Output:
✅ Retrieved Jira ticket TEST-108
✅ Retrieved Confluence page 123456789
✅ Generated docs/artifacts/TEST-108/requirements.md
```

## Integration with Requirement Analysis Agent
After this skill generates the requirements.md file, you can pass it to your requirement analysis agent:

```
Load the file from docs/artifacts/{ISSUE_ID}/requirements.md and use it to generate test cases
```

## Troubleshooting

### Configuration File Not Found
- Verify `.vscode/atlassian-api.local.json` exists in your workspace root
- Create the file with proper JSON structure (see Prerequisites section)
- Check file path: should be `.vscode/atlassian-api.local.json` (not `.vscode\atlassian-api.local.json` on Windows)

### Invalid JSON in Configuration File
- Ensure `.vscode/atlassian-api.local.json` is valid JSON
- Verify all required fields are present: `jira.baseUrl`, `jira.email`, `jira.token`, `confluence.baseUrl`, `confluence.email`, `confluence.token`
- Use a JSON validator (https://jsonlint.com/) to verify syntax

### Authentication Fails (401 Unauthorized)
- Confirm you're using an API token, not your password
- Verify credentials in `.vscode/atlassian-api.local.json` are correct
- Generate new API tokens at https://id.atlassian.com/manage-profile/security/api-tokens
- Ensure your account has access to the Jira/Confluence instance

### Jira Issue Not Found (404 Error)
- Verify the issue key exists and is accessible to your account
- Try accessing it directly: `https://parimalavaddem23.atlassian.net/browse/YOUR_ISSUE_ID`

### Confluence Page Not Found
- Use the Confluence page ID (not the page title) for accurate retrieval
- Verify the page exists and your account has read permissions
- Page ID format: just numbers (e.g., `123456789`)

## Related Skills & Workflows
- After generating requirements.md, use your requirement analysis agent to create test cases
- Credentials are stored locally in `.vscode/` (keep this folder private)

## Script Reference
See [fetch-jira-confluence.py](./scripts/fetch-jira-confluence.py) for implementation details.
