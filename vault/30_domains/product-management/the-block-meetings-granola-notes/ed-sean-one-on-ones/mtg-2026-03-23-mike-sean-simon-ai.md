---
granola_id: 188a6ab8-2563-4bcf-a86a-0d365d337e64
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: "1:1 with Ed covering mike / sean - simon ai."
context: the-block
created: 2026-03-23
source: granola-sync
attendees:
  - mprice@theblock.co
  - erupkus@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Mike _ Sean - Simon AI-transcript.md]]"
---

## Private Notes

Show mike this tweet: 

[https://x.com/maxwallenberg/status/2036093827400798522?s=20](https://x.com/maxwallenberg/status/2036093827400798522?s=20) 

## Enhanced Notes

### X402 Payment Protocol Discussion

- Mike has implemented self-service API with X402 payment protocol
	- Agent makes request → receives 402 error → pays automatically → gets response
	- Fully automated agent-to-agent payments
	- Can work with MCP (Model Context Protocol)
- Testing approach: reduce price to $0.0001 for initial trials
- Show Mike this tweet: https://x.com/maxwallenberg/status/2036093827400798522?s=20
	- Related to open wallet concept they discussed

### Current LLM Infrastructure

- Using Claude Sonnet 4.5 for API calls
- Claude Pro subscription ($2/month) provides extensive usage across 4 developers
	- Running 10+ projects without hitting quotas
	- Cost currently negligible for projected usage
- OpenAI embeddings still required (locked in)
- Model abstraction layer allows easy switching between providers
	- Configuration change only, no code changes needed

### Block Pro API Development

- New self-service Pro API built in Rust for performance
	- Replaces old Django-based system that had performance issues
	- Memory efficient and fast
- Pixel tracking implementation
	- 3 encrypted pixels embedded in content
	- Tracks where content is used
	- Enforces citation requirements and no-index/no-follow tags
	- Automatic access termination for violations
- Admin dashboard in development for usage metrics visibility

### Pro Plan Integration Strategy

- Existing Pro users can migrate API keys to new system
- Self-service model with paid tiers (no free trial confirmed)
- Working with Jeff on pricing structure
- Documentation complete and refined

### Next Steps

- Sean to test X402 implementation this afternoon
- Mike to adjust pricing for testing
- Meeting with Matt about Pro plan future
- Admin dashboard completion for usage tracking

Chat with meeting transcript: https://notes.granola.ai/t/ca34364b-ea4b-4dfa-8119-a02fbf14cadf
