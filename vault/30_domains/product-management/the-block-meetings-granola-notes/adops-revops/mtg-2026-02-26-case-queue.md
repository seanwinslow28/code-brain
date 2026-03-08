---
granola_id: 61ab6263-960a-4e4d-a2db-e8c79ffb5407
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: AdOps/RevOps meeting about case queue.
context: the-block
created: 2026-02-26
source: granola-sync
attendees:
  - kvallecillo@theblock.co
  - ldanowski@theblock.co
---

# Case Queue

### Support Case Management Overview

- Current system: Emails to support@theblock.co automatically create Salesforce cases
	- Real-time alerts in #salesforce-alerts Slack channel
	- Cases should be assigned out immediately, never left in queue
- Historical issues: 100+ backlogged cases from September, mostly non-sales spam
- Previous ownership: Cam handled all cases when majority were pro customer/sales issues
	- Now stepped back due to shift toward general tech support/spam

### New Responsibility Structure

- Sean: All campus-related inquiries only
- Kvallecillo: Sales inquiries only (sponsored posts, data requests)
- Ldanowski: Everything else (general tech support)
- Volume manageable: ~1-3 cases per week, not 100+ daily

### Case Handling Process

- Monitor #salesforce-alerts Slack channel for new cases
- Workflow for claiming cases:
- Email delivery issue: Support emails often land in spam
	- Solution: Copy yourself on replies to move conversation to personal inbox

### Technical Setup

- Sean added to #salesforce-alerts channel
- Login: Use custom domain bookmark (not salesforce.com) to avoid 2FA
- Case views: “All Open Cases” or “My Open Cases” for personal tracking
- Keep sales reps out of case object - close cases after forwarding to sales team

### Process Changes

- Consolidating email addresses: Removing campus@theblock.co, routing everything through support queue
- Old cases from September: Close out unless recently re-raised by customer
- Documentation: Lil updating process guide with new ownership structure

Chat with meeting transcript: https://notes.granola.ai/t/e13a5dce-8820-41b7-96f9-e5977e5132e6