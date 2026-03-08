---
granola_id: 4187266a-fc3a-46f3-8265-894e663d00b3
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: "Campus team sync on .co > campus auth."
context: the-block
created: 2026-03-02
source: granola-sync
attendees:
  - mvitebsky@theblock.co
  - bmendoza@theblock.co
  - erupkus@theblock.co
  - mprice@theblock.co
---

# .Co > Campus Auth

### Authentication System Unification

- Backend infrastructure ready for .co and campus login integration
	- CryptoIQ authentication already implemented
	- iOS app authentication tie-in deploying soon
	- User state reflection between platforms established
- Shared component approach for profile creation
	- Same codebase supports both .co and campus
	- Component reusability for future .co authentication rollout

### Sponsored Courses Implementation

- Authentication flow through campus after .co CTA
	- Users don’t return to .co once they hit sponsored course CTA
	- No .co login button in navigation yet - only in sponsored courses flow
- Polymarket prize validation requirements
	- Need X account verification to prevent multi-account abuse
	- Same validation logic as CryptoIQ implementation
	- Email and wallet support planned for future

### Design Strategy Decisions

- Limited .co authentication exposure initially
	- Only sponsored courses flow gets authentication
	- No general .co profiles or login value proposition ready
	- Substantial design effort required for broader .co authentication
- Backend prepared for future .co authentication expansion
	- One opportunity to get users to authenticate on .co generally
	- Current sponsored courses insufficient as sole authentication driver

### Next Steps

- Design discussion with campus dev team and David tomorrow
	- Upsell opportunities for sponsored course completers
	- Path from sponsored courses to 101, 201, certification programs

Chat with meeting transcript: https://notes.granola.ai/t/bcfe32b4-54ec-4af8-8336-fe84b791a2c6