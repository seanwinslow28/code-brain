# **🔹 Workflow Instructions for MCP Agent**

## **Step 0 — Name & Meta**

* **Zap name:** `Pods → Research & Pod Master (Delete on Cancel)`

* **Goal:** Delete mirrored events when source events are canceled

* **Notes for agent:** Avoid adding any extra filters or time constraints; attendee/time constraints should be blank.

---

## **Step 1 — Trigger**

1. **App:** Google Calendar

2. **Trigger Event:** Event Cancelled *(polling only, instant triggers not available)*

3. **Calendar:** `The Block Pods Calendar`

4. **Options:**

   * Include recurring events: `TRUE` (for series or instance cancellation)

   * Expand recurring events: leave as default/false (we will handle individual cancellations in the logic)

5. **Output mapping needed:**

   * Event ID (`Step1.EventID`) — primary key for identifying the mirrored event

   * Event Title (`Step1.Summary`) — optional for logging/debugging

   * Start/End Time — optional for logging/debugging

6. **MCP Instruction:** Ensure the agent uses exact field names in the Zapier editor so they can be referenced downstream.

---

## **Step 2 — Find Mirrored Event**

1. **App:** Google Calendar

2. **Action:** Find Event *(or Find Events, whichever is available in MCP)*

3. **Calendar:** `The Block Research & Podcasts`

4. **Search Term:** `podsync: {{Step1.EventID}}`

5. **Field Mapping:**

   * Summary: leave blank

   * Date/time filters: leave blank

   * Attendees: leave blank

6. **Options:**

   * `Successful if no search results are found?` → **TRUE** (prevents halting if no match exists)

   * `If multiple search results are found?` → **Return first result**

7. **Output mapping needed:**

   * Event ID of destination event (`Step2.EventID`) — this will be used in Step 4 Delete action

**MCP Instruction:** Do not add any additional filters; ensure the agent uses the `podsync:` marker exactly as typed.

---

## **Step 3 — Filter**

**Purpose:** Only delete the mirrored event if it actually exists.

1. **App:** Filter by Zapier

2. **Condition:**

   * Step: Step2 → Event ID

   * Condition: `Exists / Is Not Empty`

**Notes for MCP:**

* Do **not** use `Zap Search Was Found Status`; it is unreliable.

* Ensure the filter passes only when a valid destination Event ID is returned.

---

## **Step 4 — Delete Mirrored Event**

1. **App:** Google Calendar

2. **Action:** Delete Event

3. **Calendar:** `The Block Research & Podcasts`

4. **Event:** Use **Custom Event ID** → map `Step2.EventID`

5. **Options:**

   * Notify attendees: **No**

   * Send updates: **No**

**MCP Instruction:** Always map **exact Event ID**. Do not rely on search terms or description text for deletion.

---

## **Step 5 — Optional: Logging / Storage Cleanup**

* If using **Storage by Zapier** or **Zapier Tables** for a robust solution:

  1. Retrieve mapped destination ID from storage in Step 2 (instead of free-text search)

  2. Delete event using the stored ID in Step 4

  3. Clear storage key for deleted source event to avoid stale mappings

**MCP Instruction:** Storage/Table steps are optional but recommended for high reliability, especially if Zap 1 has delays or recurring events are in play.

---

# **🔹 Guardrails / Pitfalls**

1. **Recurring events:**

   * Canceling a single instance vs series may produce different IDs. The agent must decide whether to delete only if the `podsync:` marker matches exactly.

   * If unsure, implement filter: `Step1.EventID does NOT contain "_"` to ignore recurring instances temporarily.

2. **Delays / indexing issues:**

   * Google Calendar may not index new events immediately, which could cause Step 2 search to fail if deletion happens right after creation.

   * Optionally, use **Storage mapping** to bypass free-text search completely.

3. **Duplicates:**

   * Ensure Zap 1 doesn’t create multiple mirrored events with the same marker.

   * MCP should include logic to handle multiple matches (loop through and delete all).

4. **Testing:**

   * Use test events with unique titles or markers

   * Always verify mirrored event deletion in Zap History before considering deployment.

---

# **🔹 Step-by-step Test Plan for MCP Agent**

1. **Create** a new event on `The Block Pods Calendar` with a unique title.

2. **Confirm** Zap 1 mirrors it into `The Block Research & Podcasts` with `podsync: <SOURCE_EVENT_ID>` in the description.

3. **Cancel/delete** the source event.

4. **Confirm** Zap 2 triggers:

   * Step 2 finds the mirrored event

   * Filter passes

   * Step 4 deletes the mirrored event

5. **Validate** destination calendar is empty (or only remaining correct events exist).

6. **Edge case tests:**

   * Recurring instance canceled

   * Rapid create → cancel

   * Test multiple events with same titles (ensure marker disambiguates)

---

# **🔹 Summary for MCP**

* **Trigger:** Google Calendar → Event Cancelled → `Pods Calendar`

* **Search Step:** Google Calendar → Find Event → `Research & Podcasts Calendar` → search term `podsync: {{Step1.EventID}}` → return first result → success if empty

* **Filter:** Continue if `Step2.EventID exists`

* **Delete Step:** Google Calendar → Delete Event → use `Step2.EventID`

* **Optional Storage/Table:** Replace Step 2 search with lookup by `SOURCE_EVENT_ID` → delete exact mapped `DESTINATION_EVENT_ID`

**Key Notes:**

* Leave attendee/time filters blank

* Use exact text marker for reliable matching

* Avoid “Zap Search Was Found Status”

* Storage mapping is optional but highly recommended if Zap 1 delays persist

