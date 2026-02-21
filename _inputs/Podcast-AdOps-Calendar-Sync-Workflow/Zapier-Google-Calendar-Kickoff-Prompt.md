You are building a Zapier automation from scratch via Zapier MCP. This Zap will reliably mirror deletions from the "The Block Pods Calendar" into the master calendar "The Block Research & Podcasts". Use the following instructions exactly.

\---

Zap Name:  
"Pods → Research & Pod Master (Delete on Cancel)"

\---

Step 1 — Trigger:  
\- App: Google Calendar  
\- Trigger Event: Event Cancelled (polling)  
\- Calendar: "The Block Pods Calendar"  
\- Include recurring events: TRUE  
\- Expand recurring events: leave as default/false  
\- Output fields to capture: Event ID, Summary, Start/End time

\---

Step 2 — Find Mirrored Event:  
\- App: Google Calendar  
\- Action: Find Event (or Find Events)  
\- Calendar: "The Block Research & Podcasts"  
\- Search Term: "podsync: {{Step1.EventID}}"  
\- Leave all attendee/time filters blank  
\- Successful if no search results are found: TRUE  
\- If multiple search results found: Return first result  
\- Output fields to capture: Event ID of mirrored event (Step2.EventID)

\---

Step 3 — Filter:  
\- App: Filter by Zapier  
\- Condition: Step2.EventID exists / is not empty  
\- Do NOT use "Zap Search Was Found Status"

\---

Step 4 — Delete Event:  
\- App: Google Calendar  
\- Action: Delete Event  
\- Calendar: "The Block Research & Podcasts"  
\- Event ID: Step2.EventID  
\- Notify attendees: NO  
\- Send updates: NO

\---

Optional Step 5 — Robust Storage:  
\- If available, use Storage by Zapier or Zapier Tables  
\- Store key/value: Key \= Step1.EventID, Value \= Step2.EventID  
\- On deletion, clear the storage record to avoid stale keys  
\- This ensures robustness against Google Calendar indexing delays

\---

Testing Instructions:  
1\. Create a unique event in "The Block Pods Calendar"  
2\. Confirm the mirrored event appears in "The Block Research & Podcasts" with description containing "podsync: \<SOURCE\_EVENT\_ID\>"  
3\. Cancel/delete the source event  
4\. Confirm Zap 2 triggers:  
   \- Step2 finds mirrored Event ID  
   \- Filter passes  
   \- Step4 deletes the mirrored event  
5\. Validate that the destination calendar no longer contains the event  
6\. Edge cases:  
   \- Cancel a recurring instance  
   \- Rapid create → delete sequence  
   \- Multiple events with similar titles

\---

Important Notes:  
\- Do NOT add extra filters, attendee filters, or time constraints  
\- Use exact "podsync:" marker in Step2 search  
\- Use Step2.EventID for deletion — never rely on text search  
\- For recurring events, handle series vs instance carefully; optionally ignore single-instance cancellations if unsure  
\- If Storage/Tables is available, prefer it over free-text search for robust deletion

\---

Deliverable:  
\- Fully built Zap 2 ready for testing in Zapier MCP  
\- Include all steps, field mappings, filters, and optional Storage/Tables logic  
\- Ensure mapping and output fields match exactly to this specification

