---
granola_id: 1183da1a-a24d-43cf-b4e4-160b487ab4d2
title: "Test AdOp"
type: note
created: 2026-03-16T17:30:00.272Z
updated: 2026-03-16T17:57:53.714Z
attendees: 
  - kvallecillo@theblock.co
  - ldanowski@theblock.co
  - erupkus@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Test AdOp-transcript.md]]"
---
### Zapier Ad Ops Automation Testing

- Created test deals in Salesforce to validate automation workflow
- Testing different scenarios to ensure proper triggering and filtering
	- Pro/Campus deals (should not trigger)
	- Membership and renewal record types (should not trigger)
	- Single sponsorship product deals
	- Multiple product bundles with mixed trigger conditions
- Automation triggers on “Closed Won” stage for sponsorship record type only
- Filters based on product names containing: newsletter, sponsored post, display ads
	- Uses “contains” formula to identify qualifying products
	- Non-qualifying products (podcasts, research) should stop the workflow

### Product Naming Convention Updates

- Removing “theblock.co” from product names
- Newsletter and display ad core terms will remain unchanged
- Carla to send updated naming list to Sean for filter adjustments
- Considering switch to product IDs instead of name-based filtering
	- More reliable than text matching
	- 18-digit unique identifiers that never change
	- Same ID regardless of quantity (bundles vs individual)

### Asset Management Process

- One-pager PDFs needed for each product type
- Carla creating additional PDFs for missing products (article button, one other)
- Sean to determine integration method:
	- Within automation steps vs included in outbound emails
- Current client asset collection via email/Telegram

### Email Workflow Questions

- Testing whether multiple qualifying products trigger:
	- Single email with all products listed
	- Multiple separate emails per product
- Need to validate behavior when deals contain mix of qualifying/non-qualifying products

### Next Steps

- Sean: Continue testing automation with created test deals
- Sean: Determine PDF integration approach once received
- Carla: Send product ID list with names for more reliable filtering
- Carla: Complete remaining one-pager PDFs today
- Carla: Provide updated product naming conventions
- Team: Delete test records after validation complete

Chat with meeting transcript: https://notes.granola.ai/t/f3894ef7-7439-4ee2-a1c6-90e7d1b08d65
