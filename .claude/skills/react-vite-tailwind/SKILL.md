---
name: react-vite-tailwind
description: Modern frontend development assistant. Generates React components with Tailwind utilities, sets up Vite projects, and implements state management patterns. Use when asked to create components, scaffold apps, style UIs, or handle React logic.
---

# React + Vite + Tailwind Development

## Purpose

Create production-ready React applications using the modern stack: Vite for build tooling, Tailwind CSS for utility-first styling, and TypeScript for type safety. This skill enforces atomic design principles, proper hook usage, and responsive patterns.

## When to Use

- Scaffolding new React projects or components
- Styling interfaces with Tailwind utility classes
- Implementing state management (useState, Context, React Query)
- Creating reusable custom hooks
- setting up forms with validation (Zod + React Hook Form)

## Examples

**Example 1: Component Creation**
```
User: "Create a reusable Card component with a hover state"
Claude: [Uses react-vite-tailwind]
Here is a flexible Card component using Tailwind for styling and TypeScript interfaces for props:

import { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'hoverable';
}

export function Card({ children, className, variant = 'default', ...props }: CardProps) {
  const baseStyles = "flex flex-col bg-white dark:bg-slate-800 rounded-xl shadow-md overflow-hidden";
  const hoverStyles = variant === 'hoverable' ? "hover:shadow-lg transition-shadow duration-200" : "";
  
  return (
    <div className={`${baseStyles} ${hoverStyles} ${className}`} {...props}>
      {children}
    </div>
  );
}
```

**Example 2: Data Fetching Hook**
```
User: "I need a hook to fetch user data with loading states"
Claude: [Uses react-vite-tailwind]
I'll create a generic `useApi` hook that handles loading, error, and data states:

import { useState, useEffect } from 'react';

export function useApi<T>(
  apiFunction: () => Promise<T>,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await apiFunction();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, dependencies);

  return { data, loading, error, refetch: () => fetchData() };
}
```

## Domain Content

### 1. Vite Project Configuration

Use this standard `vite.config.ts` for React + TypeScript projects to support path aliases (`@/`) and optimal build settings.

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
  }
});
```

Ensure `tsconfig.json` matches the alias config:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

### 2. Project Structure

Organize files by feature domain rather than technical type for scalability.

```text
src/
├── components/          # Shared atomic components
│   ├── ui/              # Primitives (Button, Input)
│   └── layout/          # Layout wrappers
├── features/            # Feature-specific logic
│   ├── auth/            # Auth forms, hooks, types
│   └── dashboard/       # Dashboard widgets
├── hooks/               # Global hooks (useMediaQuery)
├── context/             # Global providers
├── types/               # Shared interfaces
└── utils/               # Formatters and validators
```

### 3. Tailwind Usage Patterns

**Essential Utility Patterns**
- **State Variants**: `hover:bg-blue-600`, `disabled:opacity-50`, `focus:ring-2`
- **Responsive**: `sm:grid-cols-2`, `lg:grid-cols-4` (Mobile-first default)
- **Dark Mode**: `dark:bg-slate-900` (Use with `darkMode: 'class'` in config)
- **Arbitrary Values**: `h-[500px]` (Use sparingly)

**Configuration (`tailwind.config.js`)**
Extend the theme to match design tokens.

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "hsl(var(--primary))", // CSS variable mapped
        destructive: "hsl(var(--destructive))",
      },
      borderRadius: {
        lg: "var(--radius)",
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### 4. Robust Form Handling

Combine **React Hook Form** and **Zod** for type-safe validation.

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

type FormData = z.infer<typeof formSchema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(formSchema)
  });

  const onSubmit = async (data: FormData) => {
    // API call here
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <input {...register('email')} className="border p-2 rounded w-full" />
      {errors.email && <span className="text-red-500">{errors.email.message}</span>}
      <button disabled={isSubmitting} className="bg-blue-600 text-white p-2 rounded">
        Login
      </button>
    </form>
  );
}
```

### 5. Advanced State Management

**Server State**: Use React Query for async data.
```typescript
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/api';

export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => apiClient.getUser(userId),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}
```

**Global UI State**: Use Context + useReducer for complex local state generally.

```typescript
type Action = { type: 'TOGGLE_SIDEBAR' } | { type: 'SET_THEME'; payload: 'light' | 'dark' };
type State = { isSidebarOpen: boolean; theme: 'light' | 'dark' };

function uiReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR': return { ...state, isSidebarOpen: !state.isSidebarOpen };
    case 'SET_THEME': return { ...state, theme: action.payload };
    default: return state;
  }
}
```

## Success Criteria

- [ ] Components use Tailwind for all styling (no .css files)
- [ ] TypeScript interfaces defined for all Props and State
- [ ] No `any` types used; generics used for reusable hooks
- [ ] Forms use Zod validation
- [ ] Directory structure follows the feature-based pattern

## Copy/Paste Ready

```
"Create a React component for [feature]"
"Scaffold a new Vite + Tailwind project"
"Add a custom hook for [functionality]"
"Setup a global context for [state]"
```
