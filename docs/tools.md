# MCP Tools

## `jira_search`

Input:

```json
{
  "jql": "project = ABC ORDER BY updated DESC",
  "limit": 20
}
```

Response:

```json
{
  "issues": [
    {
      "key": "ABC-123",
      "summary": "Fix auth issue",
      "status": "In Progress",
      "assignee": "Jane Doe",
      "url": "https://example.atlassian.net/browse/ABC-123"
    }
  ],
  "count": 1
}
```

## `jira_get_issue`

Input:

```json
{
  "issue_key": "ABC-123"
}
```

Response:

```json
{
  "key": "ABC-123",
  "summary": "Fix auth issue",
  "status": "In Progress",
  "assignee": "Jane Doe",
  "url": "https://example.atlassian.net/browse/ABC-123"
}
```

## `jira_add_comment`

Input:

```json
{
  "issue_key": "ABC-123",
  "text": "Shipped to staging, ready for QA."
}
```

Response:

```json
{
  "ok": true,
  "message": "comment added",
  "issue": {
    "key": "ABC-123"
  }
}
```

## `jira_transition_issue`

Input:

```json
{
  "issue_key": "ABC-123",
  "transition": "Done"
}
```

Response:

```json
{
  "ok": true,
  "transition": "Done",
  "issue": {
    "key": "ABC-123"
  }
}
```

## Error format

Errors are normalized:

```json
{
  "ok": false,
  "error": {
    "type": "PolicyError",
    "message": "Invalid issue_key format. Expected format like ABC-123."
  }
}
```

