# Setup Guide: Environment Variables & Credentials

## 1. Generate API Tokens

### For Jira
1. Visit: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "Test Automation Skill")
4. Copy the token immediately (it won't be shown again)
5. Use your **email** as `JIRA_USERNAME` and the **token** as `JIRA_PASSWORD`

### For Confluence
1. Same process as Jira (same token works for both)
2. Or create a separate token specifically for Confluence
3. Use your **email** as `CONFLUENCE_USERNAME` and the **token** as `CONFLUENCE_PASSWORD`

---

## 2. Set Environment Variables

### Option A: Permanent (Recommended for Development)

#### Windows PowerShell
```powershell
$env:JIRA_USERNAME = "your-email@example.com"
$env:JIRA_PASSWORD = "your-api-token"
$env:CONFLUENCE_USERNAME = "your-email@example.com"
$env:CONFLUENCE_PASSWORD = "your-api-token"
$env:ATLASSIAN_BASE_URL = "https://parimalavaddem23.atlassian.net"
```

Add to your PowerShell profile (`$profile`) for persistence:
```powershell
[System.Environment]::SetEnvironmentVariable("JIRA_USERNAME", "your-email@example.com", "User")
[System.Environment]::SetEnvironmentVariable("JIRA_PASSWORD", "your-api-token", "User")
[System.Environment]::SetEnvironmentVariable("CONFLUENCE_USERNAME", "your-email@example.com", "User")
[System.Environment]::SetEnvironmentVariable("CONFLUENCE_PASSWORD", "your-api-token", "User")
[System.Environment]::SetEnvironmentVariable("ATLASSIAN_BASE_URL", "https://parimalavaddem23.atlassian.net", "User")
```

#### macOS/Linux Bash
```bash
export JIRA_USERNAME="your-email@example.com"
export JIRA_PASSWORD="your-api-token"
export CONFLUENCE_USERNAME="your-email@example.com"
export CONFLUENCE_PASSWORD="your-api-token"
export ATLASSIAN_BASE_URL="https://parimalavaddem23.atlassian.net"
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

### Option B: Using .env File (Development Only)

Create `.env` in your workspace root:
```
JIRA_USERNAME=your-email@example.com
JIRA_PASSWORD=your-api-token
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_PASSWORD=your-api-token
ATLASSIAN_BASE_URL=https://parimalavaddem23.atlassian.net
```

Load it before running the script:
```bash
source .env  # macOS/Linux
```

⚠️ **Never commit `.env` to version control. Add it to `.gitignore`.**

### Option C: VS Code Secrets (Most Secure for Production)
Use VS Code's built-in secrets storage via the `python-dotenv` package:

```python
from dotenv import load_dotenv
import os

# Loads from VS Code secrets or environment
load_dotenv()

username = os.getenv('JIRA_USERNAME')
```

---

## 3. Verify Setup

### Test Jira Connection
```bash
python fetch-jira-confluence.py <YOUR_ISSUE_ID>
```

### Test with Confluence
```bash
python fetch-jira-confluence.py <YOUR_ISSUE_ID> <CONFLUENCE_PAGE_ID>
```

### Verify Environment Variables Are Set
```powershell
# Windows PowerShell
$env:JIRA_USERNAME

# macOS/Linux Bash
echo $JIRA_USERNAME
```

---

## 4. Troubleshooting

### "Missing environment variables" Error
- Verify all 5 variables are set (see step 2)
- Restart your terminal after setting variables
- Check spelling (environment variables are case-sensitive on macOS/Linux)

### "Authentication Failed" (401 Unauthorized)
- Confirm you're using an **API token**, not your password
- Regenerate the token at https://id.atlassian.com/manage-profile/security/api-tokens
- Ensure your account has access to the Jira/Confluence instance
- Check that your email is correct

### "Issue Not Found" (404 Error)
- Verify the issue key exists and is accessible to your account
- Try accessing it directly: `https://parimalavaddem23.atlassian.net/browse/YOUR_ISSUE_ID`

### "Confluence Page Not Found"
- Ensure you're using the **page ID** (not title)
- Find the page ID in the Confluence URL: `/pages/12345...`
- Verify your account has read permission on the page

---

## 5. Security Best Practices

1. **Never commit credentials** to version control
2. **Use API tokens**, not passwords
3. **Rotate tokens regularly** at https://id.atlassian.com/manage-profile/security/api-tokens
4. **Restrict token permissions** to minimum required (Jira & Confluence read access)
5. **Use separate tokens** for different applications if possible
6. **For team use**: Consider using a shared service account with limited permissions

---

## 6. Next Steps

Once credentials are set up:
1. Run `/fetch-jira-confluence` skill with a Jira issue ID
2. The skill will generate `docs/artifacts/{ISSUE_ID}/requirements.md`
3. Feed the output to your requirement analysis agent

