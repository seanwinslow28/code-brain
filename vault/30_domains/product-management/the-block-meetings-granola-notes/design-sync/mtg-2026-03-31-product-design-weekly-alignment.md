---
granola_id: 535edff8-6985-411b-a319-95c0b5fe0dbc
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Design sync discussing product + design weekly alignment.
context: the-block
created: 2026-03-31
source: granola-sync
attendees:
  - jgragg@theblock.co
  - erupkus@theblock.co
  - melshahat@theblock.co
  - mvitebsky@theblock.co
  - sho@theblock.co
  - jcarusi@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Product + Design Weekly Alignment-transcript.md]]"
---

### Step 4 (Jira Software Cloud — Update Issue) has its Description field stuck in the "Extra Fields" section, making it read-only. I need you to delete Step 4 and recreate it as a fresh step.

HERE IS WHAT TO DO:

1. Navigate to Path A > Step 4 (Jira Software Cloud — Update Issue)

2. DELETE this step entirely

3. Add a NEW step in the same position (Path A, Step 4): "Jira Software Cloud — Update Issue"

4. Configure the new step:

   ACTION: Update Issue

   ISSUE field: Insert the pill for "Jira Issue Key" from Step 3 (Find Issue by Key). In test data this showed "AD-60".

   STATUS field: Leave as "Choose value..." — do NOT set a status. Step 6 handles the transition.

   DESCRIPTION field: Build this content in Jira Wiki Markup. Type the static text and insert pills where indicated by curly braces:

h2. Assets Received — Price Page Buy Button

Submitted At: {pill: search "Submitted At" from Step 1}

Company: {pill: search "Client Name" from Step 1}

Contact: {pill: search "Contact Name" from Step 1} ({pill: search "Contact Email" from Step 1})

Request Type: {pill: search "Request Type" from Step 1 — expand and use the Label sub-property}

h3. Buy Button Details

Buy Button Text: {pill: search "Buy Button Text" from Step 1 — this is a text field, insert directly}

Buy Button Affiliate Link: {pill: search "Buy Button Affiliate Link" from Step 1 — this is a URL field, expand to URL sub-property}

Tracking URL: {pill: search "Tracking URL" or "F 35" from Step 1 — this is a URL field, MUST expand to URL sub-property so it reads "F 35 > URL" or "Tracking URL > URL"}

Assets submitted via Zapier Form. View full record in Zapier Tables.

5. Do NOT add any other fields (no Reporter, no extra fields)

6. Save/Continue the step

7. Do NOT publish yet

CRITICAL RULES:

- URL/link-type pills MUST be expanded to the "> URL" sub-property. Without expanding, they render blank at runtime. This applies to: Buy Button Affiliate Link, Tracking URL.

- Text-type pills (Buy Button Text) are inserted directly — no expansion needed.

- The "Request Type" pill should use the "> Label" sub-property.

- Contact format: {name} ({email}) — with parentheses, not pipes.

- Do NOT set the Status field.

After recreating, tell me: Is the Description field in the main Configure panel (not "Extra Fields")? Show me what the full Description looks like.Josh’s Recovery Update & Work Status

- Broken collarbone from bicycle accident - existing hardware bent but held bone together
- Experienced amnesia for ~2 days - no memory of hospital visit or conversations
- Back to work after 3 weeks absence
- Ready to resume normal responsibilities

### Current Project Status & Deliverables

- App store graphics ready but need re-export
	- Josh will deliver today along with ACS module UI updates
	- Matt can preview before app store submission
- Sponsored course work nearly complete
	- Claudine delivered most assets including LinkedIn shareables
	- Sean double-checking completion flow elements for dev team
- CTO homepage redesign in progress
	- Serena exploring concepts to reduce drop-off rates
	- Focus on bringing lower page content higher up
	- Review meeting pushed to Monday (Josh’s request)

### Branding & Video Projects

- “Priced In” podcast branding for Polymarket
	- Josh sketching concepts, team review Friday
	- Revenue model: transaction fees, not house betting
- Election coverage video for Polymarket
	- Script complete but requires significant motion work
	- May simplify to talking head + screen captures vs full product walkthrough
	- Davis meeting Wednesday to clarify ownership/timeline
- Singular software implementation
	- HTML/CSS overlays for Starting Block live broadcast
	- Josh volunteering alongside Brian for development
	- Focus on lower thirds with animation capabilities
	- Data requirements scoped with dev team Friday

### Next Steps

- Josh: Export app store graphics, complete ACS module updates (today)
- Sean: Verify sponsored course completion status for dev team
- Team: CTO review meeting Monday
- Brand team: “Priced In” concepts by Friday
- Josh: Begin Singular lower thirds development

Chat with meeting transcript: https://notes.granola.ai/t/29d05afa-bdab-4e61-9ec9-c5a3cff73669
