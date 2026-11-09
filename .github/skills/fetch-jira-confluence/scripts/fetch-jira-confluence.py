#!/usr/bin/env python3
"""
Fetch Jira and Confluence details for test automation implementation.

Usage:
    python fetch-jira-confluence.py <ISSUE_ID> [CONFLUENCE_PAGE_ID]

Configuration:
    Reads Jira and Confluence credentials from .vscode/atlassian-api.local.json
    File format:
    {
        "jira": {
            "baseUrl": "https://your-instance.atlassian.net",
            "email": "your-email@example.com",
            "token": "your-api-token"
        },
        "confluence": {
            "baseUrl": "https://your-instance.atlassian.net",
            "email": "your-email@example.com",
            "token": "your-api-token"
        }
    }
"""

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

class JiraConfluenceFetcher:
    def __init__(self):
        # Load configuration from .vscode/atlassian-api.local.json
        # Use current working directory (workspace root) to locate the config file
        config_file = Path.cwd() / '.vscode' / 'atlassian-api.local.json'
        self.config = self._load_config(config_file)
        
        # Jira configuration
        self.base_url = self.config['jira']['baseUrl']
        self.jira_username = self.config['jira']['email']
        self.jira_password = self.config['jira']['token']
        
        # Confluence configuration
        self.confluence_username = self.config['confluence']['email']
        self.confluence_password = self.config['confluence']['token']
        
        self.jira_auth = HTTPBasicAuth(self.jira_username, self.jira_password)
        self.confluence_auth = HTTPBasicAuth(self.confluence_username, self.confluence_password)
        
        self.jira_api_url = urljoin(self.base_url, '/rest/api/3/')
        self.confluence_api_url = urljoin(self.base_url, '/wiki/rest/api/')
    
    def _load_config(self, config_file: Path) -> dict:
        """Load configuration from atlassian-api.local.json file."""
        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}\n"
                f"Please create .vscode/atlassian-api.local.json with Jira and Confluence credentials."
            )
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Validate required fields
            required_jira = ['baseUrl', 'email', 'token']
            required_confluence = ['baseUrl', 'email', 'token']
            
            for field in required_jira:
                if field not in config.get('jira', {}):
                    raise ValueError(f"Missing jira.{field} in configuration")
            
            for field in required_confluence:
                if field not in config.get('confluence', {}):
                    raise ValueError(f"Missing confluence.{field} in configuration")
            
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def fetch_jira_issue(self, issue_key):
        """Fetch Jira issue details including description and acceptance criteria."""
        try:
            url = urljoin(self.jira_api_url, f'issue/{issue_key}')
            response = requests.get(url, auth=self.jira_auth, timeout=10)
            response.raise_for_status()
            
            issue = response.json()
            fields = issue.get('fields', {})
            
            # Extract key fields
            issue_data = {
                'key': issue.get('key'),
                'summary': fields.get('summary'),
                'description': fields.get('description'),
                'status': fields.get('status', {}).get('name'),
                'issuetype': fields.get('issuetype', {}).get('name'),
                'assignee': fields.get('assignee', {}).get('displayName'),
                'created': fields.get('created'),
                'acceptance_criteria': self._extract_acceptance_criteria(fields),
                'labels': fields.get('labels', []),
                'story_points': fields.get('customfield_10016'),  # Common Story Points field
                'url': f"{self.base_url}/browse/{issue.get('key')}"
            }
            
            return issue_data
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching Jira issue {issue_key}: {e}")
            return None
    
    def _extract_acceptance_criteria(self, fields):
        """Extract acceptance criteria from issue description or custom field."""
        description = fields.get('description', '')
        
        # Try to find acceptance criteria in description (ADF format)
        if isinstance(description, dict):
            # Parse ADF format and extract readable text
            criteria = self._parse_adf_document(description)
            if criteria:
                return criteria
        elif isinstance(description, str):
            # Plain text format
            if 'acceptance criteria' in description.lower():
                lines = description.split('\n')
                criteria_section = False
                criteria = []
                for line in lines:
                    if 'acceptance criteria' in line.lower():
                        criteria_section = True
                        continue
                    if criteria_section and line.strip():
                        criteria.append(line.strip())
                    elif criteria_section and not line.strip():
                        break
                return '\n'.join(criteria) if criteria else description
        
        return description
    
    def _parse_adf_document(self, adf_doc):
        """Parse Atlassian Document Format (ADF) and extract readable text."""
        if not isinstance(adf_doc, dict):
            return None
        
        content = adf_doc.get('content', [])
        text_parts = []
        
        for item in content:
            extracted = self._parse_adf_node(item)
            if extracted:
                text_parts.append(extracted)
        
        return '\n\n'.join(text_parts) if text_parts else None
    
    def _parse_adf_node(self, node):
        """Parse individual ADF nodes and convert to readable text."""
        if not isinstance(node, dict):
            return ''
        
        node_type = node.get('type', '')
        content = node.get('content', [])
        
        # Handle text nodes
        if node_type == 'text':
            return node.get('text', '')
        
        # Handle paragraph nodes
        elif node_type == 'paragraph':
            text_parts = []
            for child in content:
                text = self._parse_adf_node(child)
                if text:
                    text_parts.append(text)
            return ''.join(text_parts).strip()
        
        # Handle heading nodes
        elif node_type == 'heading':
            level = node.get('attrs', {}).get('level', 1)
            text_parts = []
            for child in content:
                text = self._parse_adf_node(child)
                if text:
                    text_parts.append(text)
            text = ''.join(text_parts).strip()
            return f"{'#' * level} {text}"
        
        # Handle bullet list nodes
        elif node_type == 'bulletList':
            items = []
            for item in content:
                text = self._parse_adf_node(item)
                if text:
                    items.append(f"• {text}")
            return '\n'.join(items)
        
        # Handle ordered list nodes
        elif node_type == 'orderedList':
            items = []
            order = node.get('attrs', {}).get('order', 1)
            for i, item in enumerate(content, start=order):
                text = self._parse_adf_node(item)
                if text:
                    items.append(f"{i}. {text}")
            return '\n'.join(items)
        
        # Handle list item nodes
        elif node_type == 'listItem':
            text_parts = []
            for child in content:
                text = self._parse_adf_node(child)
                if text:
                    text_parts.append(text)
            return ''.join(text_parts).strip()
        
        # Handle inline card/link nodes
        elif node_type == 'inlineCard':
            url = node.get('attrs', {}).get('url', '')
            return f"[Link: {url}]"
        
        # Handle other block elements
        else:
            text_parts = []
            for child in content:
                text = self._parse_adf_node(child)
                if text:
                    text_parts.append(text)
            return ''.join(text_parts).strip()
    
    def _extract_text_from_adf_node(self, node):
        """Legacy method - extract plain text from ADF node."""
        if node.get('type') == 'text':
            return node.get('text', '')
        
        text_parts = []
        for child in node.get('content', []):
            if child.get('type') == 'text':
                text_parts.append(child.get('text', ''))
        
        return ''.join(text_parts)
    
    def fetch_confluence_page(self, page_id):
        """Fetch Confluence page content by page ID."""
        try:
            url = urljoin(self.confluence_api_url, f'pages/{page_id}')
            params = {'expand': 'body.storage,metadata.labels'}
            response = requests.get(url, auth=self.confluence_auth, params=params, timeout=10)
            response.raise_for_status()
            
            page = response.json()
            
            page_data = {
                'id': page.get('id'),
                'title': page.get('title'),
                'status': page.get('status'),
                'body': page.get('body', {}).get('storage', {}).get('value'),
                'labels': [label.get('name') for label in page.get('metadata', {}).get('labels', [])],
                'url': page.get('_links', {}).get('base') + page.get('_links', {}).get('webui', '')
            }
            
            return page_data
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Warning: Could not fetch Confluence page {page_id}: {e}")
            return None
    
    def generate_markdown(self, issue_data, confluence_data=None):
        """Generate Markdown document from fetched data."""
        markdown = f"""# Requirements: {issue_data['key']} - {issue_data['summary']}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Issue Details

| Field | Value |
|-------|-------|
| **Issue Key** | {issue_data['key']} |
| **Title** | {issue_data['summary']} |
| **Type** | {issue_data['issuetype']} |
| **Status** | {issue_data['status']} |
| **Assignee** | {issue_data['assignee'] or 'Unassigned'} |
| **Story Points** | {issue_data['story_points'] or 'N/A'} |
| **Created** | {issue_data['created']} |
| **Jira Link** | [{issue_data['key']}]({issue_data['url']}) |

## Description

{issue_data['description'] or 'No description provided'}

## Acceptance Criteria

{issue_data['acceptance_criteria'] or 'No acceptance criteria defined'}

## Labels

{', '.join(f'`{label}`' for label in issue_data['labels']) if issue_data['labels'] else 'None'}

"""
        
        if confluence_data:
            markdown += f"""## Related Confluence Documentation

### {confluence_data['title']}

**Status**: {confluence_data['status']}
**Labels**: {', '.join(f'`{label}`' for label in confluence_data['labels']) if confluence_data['labels'] else 'None'}
**URL**: [{confluence_data['title']}]({confluence_data['url']})

#### Content
{confluence_data['body'] or 'No content'}

"""
        
        markdown += f"""## Test Implementation Notes

### Key Scenarios
Based on the acceptance criteria above, the following test scenarios should be implemented:
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test scenario 3

### Dependencies & Preconditions
- List any dependencies here

### Edge Cases
- List any edge cases identified in the requirements

---

*This document was auto-generated from Jira issue {issue_data['key']} and linked Confluence pages.*
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return markdown
    
    def save_markdown(self, issue_key, markdown_content):
        """Save Markdown to docs/artifacts/{ISSUE_KEY}/requirements.md"""
        output_dir = Path('docs') / 'artifacts' / issue_key
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / 'requirements.md'
        output_file.write_text(markdown_content, encoding='utf-8')
        
        return str(output_file)


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch-jira-confluence.py <ISSUE_ID> [CONFLUENCE_PAGE_ID]")
        print("\nConfiguration:")
        print("  Reads credentials from: .vscode/atlassian-api.local.json")
        print("\nExample ISSUE_ID: BOOK-1")
        print("Example with Confluence: BOOK-1 123456789")
        sys.exit(1)
    
    issue_id = sys.argv[1]
    confluence_page_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        fetcher = JiraConfluenceFetcher()
        
        print(f"📋 Fetching Jira issue: {issue_id}")
        issue_data = fetcher.fetch_jira_issue(issue_id)
        
        if not issue_data:
            print(f"❌ Failed to fetch Jira issue {issue_id}")
            sys.exit(1)
        
        print(f"✅ Retrieved Jira issue: {issue_data['summary']}")
        
        confluence_data = None
        if confluence_page_id:
            print(f"📄 Fetching Confluence page: {confluence_page_id}")
            confluence_data = fetcher.fetch_confluence_page(confluence_page_id)
            if confluence_data:
                print(f"✅ Retrieved Confluence page: {confluence_data['title']}")
            else:
                print(f"⚠️  Confluence page {confluence_page_id} not found")
        
        # Generate Markdown
        markdown = fetcher.generate_markdown(issue_data, confluence_data)
        
        # Save to file
        output_file = fetcher.save_markdown(issue_id, markdown)
        print(f"✅ Generated requirements document: {output_file}")
        
        # Print content to stdout
        print("\n" + "="*60)
        print(markdown)
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
