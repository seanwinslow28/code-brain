---
name: personal-app-patterns
description: Opinionated starter patterns for personal apps and side projects using React + Vite + Tailwind + Supabase. Use when asked to "start a new app", "scaffold personal project", "my standard stack", "new side project", "set up auth", or "standard folder structure".
---

# Personal App Patterns

## Purpose

Codify the standard architecture for personal apps and side projects. Instead of re-deriving the same patterns from individual stack skills each time, this skill provides the complete, opinionated setup: folder structure, auth flow, database patterns, deployment config, and common features. Get from zero to building in minutes.

## When to Use

- Starting a new personal app or side project
- Setting up the standard React + Vite + Tailwind + Supabase stack
- Adding auth, protected routes, or database tables to an existing project
- Deploying to Vercel or Supabase
- Adding common features (dark mode, toasts, forms, data tables)

## Examples

**Example 1: New Project**
```
User: "Start a new personal app for tracking animation projects"
Claude: [Uses personal-app-patterns]
Setting up with the standard stack...

npm create vite@latest animation-tracker -- --template react-ts
cd animation-tracker
npm install @supabase/supabase-js @tanstack/react-query zod react-hook-form
npm install -D tailwindcss @tailwindcss/vite

Creating folder structure, auth context, Supabase client, and base layout...
```

**Example 2: Add Auth to Existing App**
```
User: "Add login/signup to my project"
Claude: [Uses personal-app-patterns]
Adding Supabase Auth with the standard pattern:
1. AuthContext provider with session management
2. ProtectedRoute wrapper component
3. Login/Signup page with email+password
4. Redirect logic (login → dashboard, no-auth → login)
```

## Standard Stack

| Layer | Tool | Why |
|:------|:-----|:----|
| Build | Vite | Fast HMR, TypeScript out of the box |
| UI | React + TypeScript | Component model, ecosystem |
| Styling | Tailwind CSS v4 | Utility-first, no CSS files to manage |
| Backend | Supabase | Auth + Postgres + RLS + Edge Functions + Realtime |
| Forms | React Hook Form + Zod | Validation with type inference |
| Async State | TanStack Query | Caching, refetching, optimistic updates |
| Hosting | Vercel (frontend) | Zero-config deploy from git |

## Canonical Folder Structure

```
src/
├── components/          # Shared UI components
│   ├── Layout.tsx       # Shell: sidebar + header + main
│   ├── ProtectedRoute.tsx
│   ├── DataTable.tsx    # Reusable sortable table
│   ├── Modal.tsx        # Dialog wrapper
│   └── Toast.tsx        # Notification system
├── features/            # Feature modules (self-contained)
│   ├── auth/
│   │   ├── AuthContext.tsx
│   │   ├── LoginPage.tsx
│   │   └── SignupPage.tsx
│   └── dashboard/
│       ├── DashboardPage.tsx
│       └── StatsCard.tsx
├── hooks/               # Shared custom hooks
│   ├── useAuth.ts       # Re-exports from AuthContext
│   └── useSupabase.ts   # Typed Supabase client hook
├── lib/                 # Utilities and config
│   ├── supabase.ts      # Supabase client singleton
│   ├── constants.ts     # App-wide constants
│   └── utils.ts         # Shared helpers
├── types/               # TypeScript types (generated + custom)
│   └── database.ts      # Supabase generated types
├── App.tsx              # Router + providers
├── main.tsx             # Entry point
└── index.css            # Tailwind imports
```

## Core Patterns

### 1. Supabase Client Setup

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from '../types/database'

export const supabase = createClient<Database>(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_ANON_KEY
)
```

### 2. Auth Context

```typescript
// src/features/auth/AuthContext.tsx
import { createContext, useContext, useEffect, useState } from 'react'
import type { Session, User } from '@supabase/supabase-js'
import { supabase } from '../../lib/supabase'

interface AuthState { user: User | null; session: Session | null; loading: boolean }
const AuthContext = createContext<AuthState>({ user: null, session: null, loading: true })

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({ user: null, session: null, loading: true })

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setState({ user: session?.user ?? null, session, loading: false })
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setState({ user: session?.user ?? null, session, loading: false })
    })
    return () => subscription.unsubscribe()
  }, [])

  return <AuthContext.Provider value={state}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
```

### 3. Protected Route

```typescript
// src/components/ProtectedRoute.tsx
import { Navigate } from 'react-router-dom'
import { useAuth } from '../features/auth/AuthContext'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="flex h-screen items-center justify-center">Loading...</div>
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}
```

### 4. Common Database Tables

```sql
-- profiles (extends auth.users)
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own profile" ON public.profiles
  FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles
  FOR UPDATE USING (auth.uid() = id);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, display_name)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'display_name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### 5. Dark Mode Toggle

```typescript
// In Layout.tsx or a ThemeProvider
const [dark, setDark] = useState(() =>
  localStorage.getItem('theme') === 'dark' ||
  (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
)
useEffect(() => {
  document.documentElement.classList.toggle('dark', dark)
  localStorage.setItem('theme', dark ? 'dark' : 'light')
}, [dark])
```

## Deployment Checklist

1. **Environment variables**: Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in Vercel dashboard
2. **Supabase project**: Create via `npx supabase init` → `npx supabase link` → `npx supabase db push`
3. **Auth redirect URLs**: Add your Vercel URL to Supabase Auth → URL Configuration
4. **Generate types**: `npx supabase gen types typescript --linked > src/types/database.ts`
5. **Vercel deploy**: Connect git repo, framework preset = Vite, build = `npm run build`, output = `dist`

## Success Criteria

- [ ] Vite dev server starts without errors
- [ ] Tailwind classes render correctly
- [ ] Auth flow works (signup → confirm → login → dashboard)
- [ ] RLS policies block unauthorized access
- [ ] Protected routes redirect unauthenticated users
- [ ] Dark mode persists across page reloads
- [ ] TypeScript types generated from Supabase schema

## Related Skills

- `react-vite-tailwind` — Detailed React component and Tailwind patterns
- `supabase-backend` — Advanced RLS, Edge Functions, real-time
- `prototype-scaffold` — Quick scaffolding for throwaway prototypes

## Copy/Paste Ready

```
"Start a new personal app"
"Set up my standard stack"
"Add auth to this project"
"Create the standard folder structure"
"Add a data table with sorting"
"Deploy this to Vercel"
```