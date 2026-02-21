---
name: supabase-backend
description: Supabase architecture assistant. Designs secure schemas with RLS policies, writes Deno Edge Functions, and optimizes real-time subscriptions. Use when asked to setup databases, implement auth, security policies, or backend logic.
---

# Supabase Backend Development

## Purpose

Architect scalable and secure Supabase backends. This skill focuses on multi-tenant schema design, performance-critical RLS policies (using Security Definer functions), cost-optimized real-time patterns, and TypeScript Edge Functions.

## When to Use

- Designing database schemas (tables, relationships, indexes)
- Writing Row Level Security (RLS) policies
- Implementing Edge Functions (Deno) for custom logic
- Optimizing Real-time subscriptions (filtering, broadcast)
- Configuring Authentication (Auth providers, helpers)

## Examples

**Example 1: Secure RLS Policy**
```
User: "Create an RLS policy so users can only see projects in their organization"
Claude: [Uses supabase-backend]
I'll use a high-performance policy pattern that avoids joins in the policy itself:

-- 1. Create a helper function to check membership (Security Definer)
CREATE OR REPLACE FUNCTION public.is_org_member(org_id uuid)
RETURNS boolean AS $$
SELECT EXISTS (
  SELECT 1 FROM public.members
  WHERE organization_id = org_id
  AND user_id = auth.uid()
);
$$ LANGUAGE sql SECURITY DEFINER SET search_path = public;

-- 2. Apply the policy using the helper
CREATE POLICY "Members can view org projects" ON public.projects
FOR SELECT TO authenticated
USING (is_org_member(organization_id));
```

**Example 2: Real-time Subscription**
```
User: "Listen for new messages in a chat room"
Claude: [Uses supabase-backend]
I'll set up a filtered subscription to minimize data transfer:

const channel = supabase
  .channel('room-1')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'messages',
      filter: 'room_id=eq.123' // Crucial for performance
    },
    (payload) => {
      console.log('New message:', payload.new);
    }
  )
  .subscribe();
```

## Domain Content

### 1. Schema Design Hierarchy

Follow this hierarchy for multi-tenant apps.

- **Organization**: Top-level tenant
- **Project**: Scoped to Organization
- **Resource**: Scoped to Project

**Optimization Strategy**:
Index columns used in RLS policies (e.g., `organization_id`) to prevent table scans on every query.

```sql
CREATE INDEX idx_project_org ON public.projects(organization_id);
CREATE INDEX idx_members_user ON public.members(user_id);
```

### 2. Row Level Security (RLS)

Use **Security Definer** functions to check permissions securely without exposing underlying tables.

```sql
-- Pattern: Is User Owner?
CREATE OR REPLACE FUNCTION is_owner(resource_id uuid)
RETURNS boolean AS $$
SELECT auth.uid() = owner_id 
FROM public.resources 
WHERE id = resource_id;
$$ LANGUAGE sql SECURITY DEFINER;
```

### 3. Edge Functions (Deno)

Use Edge Functions for logic needing higher privileges or external APIs.

**Secret Access**
```typescript
// index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

Deno.serve(async (req) => {
  // Service Key bypasses RLS - Handle with care!
  const supabaseAdmin = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )
  
  const { data, error } = await supabaseAdmin.from('users').select('*');
  
  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } })
})
```

**Development**: `supabase functions serve --env-file .env.local`

### 4. Real-time Best Practices

Optimize for "Message Volume" based on pricing tiers.

- **Broadcast Channels**: Use for ephemeral events (cursors, typing) to bypass the database completely.
- **Postgres Changes**: MUST use `filter` parameter.

**Broadcast Example (Typing Indicator)**:
```javascript
channel.send({
  type: 'broadcast',
  event: 'typing',
  payload: { user: 'sean', isTyping: true }
})
```

### 5. Client Connection Pattern

Isolate subscription logic to prevent memory leaks in React.

```typescript
useEffect(() => {
  const channel = supabase.channel('room-1')
    .on('postgres_changes', /* ... */)
    .subscribe();

  return () => {
    supabase.removeChannel(channel); // Cleanup execution
  };
}, []);
```

## Success Criteria

- [ ] RLS policies enable on ALL public tables
- [ ] Helper functions used for complex RLS logic (no nested SELECTs in policies)
- [ ] Indexes exist for all foreign keys used in RLS
- [ ] Real-time subscriptions include a `filter` clause
- [ ] Edge Functions use correct import URLs (esm.sh or deno.land)

## Copy/Paste Ready

```
"Create a database schema for [app]"
"Write an RLS policy for [table]"
"Create an Edge Function to [task]"
"Optimized real-time subscription for [event]"
```
