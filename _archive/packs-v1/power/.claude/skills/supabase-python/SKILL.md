---
name: supabase-python
description: Assists with Supabase integration in Python projects, including auth, database, and real-time features
---

# Supabase Python Skill

## When to Use

Use this skill when:
- Setting up Supabase in Python projects
- Implementing authentication
- Working with Supabase database queries
- Setting up real-time subscriptions
- Managing storage and file uploads

## Examples

**Example 1: Authentication setup**
```
User: "Set up Supabase auth in my Python app"
Claude: [Uses supabase-python skill] Here's the setup:

from supabase import create_client, Client

url = "https://your-project.supabase.co"
key = "your-anon-key"
supabase: Client = create_client(url, key)

# Sign up
user = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "secure-password"
})

# Sign in
session = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "secure-password"
})

# Get current user
user = supabase.auth.get_user()
```

**Example 2: Database queries**
```
User: "Query users table with filters"
Claude: [Uses supabase-python skill] Query examples:

# Select with filters
response = supabase.table("users")\
    .select("id, email, created_at")\
    .eq("status", "active")\
    .order("created_at", desc=True)\
    .limit(10)\
    .execute()

# Insert
data = {"email": "new@example.com", "name": "New User"}
result = supabase.table("users").insert(data).execute()

# Update
supabase.table("users")\
    .update({"status": "inactive"})\
    .eq("id", user_id)\
    .execute()
```

## Supabase Features

This skill covers:
- Authentication (sign up, sign in, sessions)
- Database operations (CRUD, filters, joins)
- Real-time subscriptions
- Storage (upload, download, public URLs)
- Row Level Security (RLS) policies
- Edge functions integration
- Error handling and retries

## Copy/Paste Ready

To use this skill:
- "Set up Supabase auth in Python"
- "Query Supabase database with filters"
- "Create a Supabase real-time subscription"
