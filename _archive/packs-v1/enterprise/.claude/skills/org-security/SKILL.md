---
name: org-security
description: Enforces organizational security policies and best practices in code and operations
---

# Organization Security Skill

## When to Use

Use this skill when:
- Reviewing code for security vulnerabilities
- Implementing security policies
- Auditing access controls
- Ensuring compliance with security standards
- Handling sensitive data

## Examples

**Example 1: Security code review**
```
User: "Review this code for security issues"
Claude: [Uses org-security skill] Security review findings:

**Critical:**
- Hardcoded API key in source code (line 42)
- SQL injection risk in user input (line 89)

**High:**
- Missing input validation on file upload
- Sensitive data logged in plaintext

**Recommendations:**
- Move API key to environment variables
- Use parameterized queries
- Add file type validation
- Remove sensitive data from logs
```

**Example 2: Security policy enforcement**
```
User: "Check if this follows our security policies"
Claude: [Uses org-security skill] Policy compliance check:

✓ All secrets in environment variables
✓ HTTPS enforced for all external calls
✓ Input validation implemented
✓ Authentication required for sensitive endpoints
⚠ Missing rate limiting on API endpoints
⚠ No audit logging for admin actions
```

## Security Standards

This skill enforces:
- No hardcoded secrets or credentials
- Input validation and sanitization
- Authentication and authorization checks
- Secure communication (HTTPS/TLS)
- Data encryption at rest and in transit
- Audit logging for sensitive operations
- Dependency vulnerability scanning
- Compliance with organizational policies

## Copy/Paste Ready

To use this skill:
- "Review this code for security issues"
- "Check security policy compliance"
- "Audit this feature for security"
