---
name: rn-architecture
description: React Native app architecture and project setup. Covers project structure, navigation (React Navigation), state management, native modules, build configuration, and performance patterns. Use when asked to "set up a React Native project", "RN navigation", "mobile app architecture", "Expo setup", "RN state management", or "build React Native app".
---

# React Native Architecture

## Purpose

Build well-structured React Native apps from the start. This skill covers project setup, navigation, state management, build configuration, and performance — everything `rn-debug` doesn't cover (that skill handles diagnosis when things break).

## When to Use

- Setting up a new React Native / Expo project
- Designing navigation structure (stacks, tabs, drawers, auth flow)
- Choosing and implementing state management
- Configuring builds (EAS Build, Fastlane, code signing)
- Optimizing performance (FlatList, Hermes, bundle size)
- Structuring a feature-based codebase

## Examples

**Example 1: New Expo Project**
```
User: "Set up a new React Native app with Expo"
Claude: [Uses rn-architecture]

npx create-expo-app@latest my-app --template tabs
cd my-app

# Add common dependencies
npx expo install expo-router expo-status-bar
npm install zustand @tanstack/react-query zod
npm install react-hook-form @hookform/resolvers

Creating feature-based folder structure...
```

**Example 2: Auth Navigation Flow**
```
User: "Set up auth flow with protected screens"
Claude: [Uses rn-architecture]
Using Expo Router with route groups:

app/
├── (auth)/           # Public routes (no auth required)
│   ├── login.tsx
│   └── signup.tsx
├── (tabs)/           # Protected routes (auth required)
│   ├── _layout.tsx   # Tab navigator
│   ├── home.tsx
│   └── profile.tsx
└── _layout.tsx       # Root layout with auth check
```

## Recommended Stack

| Layer | Tool | Why |
|:------|:-----|:----|
| Framework | Expo SDK 52+ | Managed workflow, OTA updates, EAS Build |
| Navigation | Expo Router (file-based) | Convention over config, deep linking built-in |
| State (local) | Zustand | Minimal boilerplate, no providers, TypeScript-first |
| State (async) | TanStack Query | Cache, refetch, optimistic updates, devtools |
| Forms | React Hook Form + Zod | Performant (no re-renders), type-safe validation |
| Animations | Reanimated 3 | Native thread, gesture integration |
| Styling | StyleSheet + Nativewind | Native perf; Nativewind for Tailwind-like DX |

## Project Structure (Feature-Based)

```
src/
├── app/                    # Expo Router pages (file-based routing)
│   ├── (auth)/
│   │   ├── login.tsx
│   │   └── signup.tsx
│   ├── (tabs)/
│   │   ├── _layout.tsx     # Tab navigator config
│   │   ├── home.tsx
│   │   ├── search.tsx
│   │   └── profile.tsx
│   ├── _layout.tsx         # Root layout (providers, auth guard)
│   └── +not-found.tsx
├── features/               # Feature modules (self-contained)
│   ├── auth/
│   │   ├── useAuth.ts      # Auth hook (Zustand store)
│   │   ├── AuthGuard.tsx   # Redirect if not authenticated
│   │   └── api.ts          # Auth API calls
│   └── projects/
│       ├── useProjects.ts  # TanStack Query hooks
│       ├── ProjectCard.tsx
│       └── api.ts
├── components/             # Shared UI components
│   ├── Button.tsx
│   ├── Input.tsx
│   └── LoadingScreen.tsx
├── lib/                    # Utilities and config
│   ├── supabase.ts         # Supabase client
│   ├── queryClient.ts      # TanStack Query config
│   └── constants.ts
└── types/
    └── database.ts         # Generated Supabase types
```

## Navigation Patterns

### Root Layout with Auth Guard

```typescript
// app/_layout.tsx
import { Slot, useRouter, useSegments } from 'expo-router'
import { useAuth } from '../features/auth/useAuth'
import { useEffect } from 'react'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '../lib/queryClient'

export default function RootLayout() {
  const { user, loading } = useAuth()
  const segments = useSegments()
  const router = useRouter()

  useEffect(() => {
    if (loading) return
    const inAuthGroup = segments[0] === '(auth)'
    if (!user && !inAuthGroup) router.replace('/login')
    if (user && inAuthGroup) router.replace('/home')
  }, [user, loading])

  return (
    <QueryClientProvider client={queryClient}>
      <Slot />
    </QueryClientProvider>
  )
}
```

### Tab Navigator

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Ionicons } from '@expo/vector-icons'

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#6366f1' }}>
      <Tabs.Screen name="home" options={{
        title: 'Home',
        tabBarIcon: ({ color, size }) => <Ionicons name="home" size={size} color={color} />
      }} />
      <Tabs.Screen name="profile" options={{
        title: 'Profile',
        tabBarIcon: ({ color, size }) => <Ionicons name="person" size={size} color={color} />
      }} />
    </Tabs>
  )
}
```

## State Management

### Zustand Store (Auth Example)

```typescript
// features/auth/useAuth.ts
import { create } from 'zustand'
import { supabase } from '../../lib/supabase'
import type { User, Session } from '@supabase/supabase-js'

interface AuthState {
  user: User | null
  session: Session | null
  loading: boolean
  initialize: () => void
  signOut: () => Promise<void>
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  session: null,
  loading: true,
  initialize: () => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      set({ user: session?.user ?? null, session, loading: false })
    })
    supabase.auth.onAuthStateChange((_event, session) => {
      set({ user: session?.user ?? null, session, loading: false })
    })
  },
  signOut: async () => {
    await supabase.auth.signOut()
    set({ user: null, session: null })
  },
}))
```

### TanStack Query (Data Fetching)

```typescript
// features/projects/useProjects.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { supabase } from '../../lib/supabase'

export function useProjects() {
  return useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const { data, error } = await supabase.from('projects').select('*').order('created_at', { ascending: false })
      if (error) throw error
      return data
    },
  })
}

export function useCreateProject() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (project: { name: string; description: string }) => {
      const { data, error } = await supabase.from('projects').insert(project).select().single()
      if (error) throw error
      return data
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['projects'] }),
  })
}
```

## Build Configuration

### EAS Build Setup

```bash
# Install EAS CLI
npm install -g eas-cli

# Initialize
eas init
eas build:configure

# Build profiles (eas.json)
```

```json
{
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal" },
    "production": {}
  }
}
```

### Environment Configs

```bash
# .env.development
EXPO_PUBLIC_SUPABASE_URL=https://dev-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=dev-key

# .env.production
EXPO_PUBLIC_SUPABASE_URL=https://prod-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=prod-key
```

Access in code: `process.env.EXPO_PUBLIC_SUPABASE_URL`

## Performance Patterns

| Pattern | When | How |
|:--------|:-----|:----|
| FlatList over ScrollView | Lists > 20 items | `keyExtractor`, `getItemLayout`, `maxToRenderPerBatch` |
| `React.memo` | Expensive child components | Wrap with `memo()`, ensure stable props |
| `useCallback` for handlers | Handlers passed to memoized children | Wrap event handlers |
| Image optimization | Many images | `expo-image` (replaces Image), set `cachePolicy` |
| Hermes engine | Always (Expo default) | Verify with `global.HermesInternal` check |
| Avoid inline styles | Render-heavy screens | Use `StyleSheet.create()` outside component |

## Success Criteria

- [ ] Project uses feature-based folder structure
- [ ] Navigation handles auth/unauth states correctly
- [ ] State management separates local (Zustand) from async (TanStack Query)
- [ ] Environment variables configured per build profile
- [ ] FlatList used for lists, with proper key extraction
- [ ] TypeScript strict mode enabled

## Related Skills

- `rn-debug` — When things break (build failures, red screens, crashes)
- `react-native-animations` — Reanimated 3 + Gesture Handler patterns
- `phaser-game-patterns` — Embedding Phaser games via WebView bridge

## Copy/Paste Ready

```
"Set up a new React Native project"
"Add navigation with auth flow"
"Set up state management with Zustand"
"Configure EAS Build profiles"
"Optimize FlatList performance"
"Add Supabase to my RN app"
```