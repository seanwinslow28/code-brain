---
name: micro-interaction-patterns
description: Micro-interaction pattern library for UI polish. Copy-paste patterns for button feedback, form animations, navigation transitions, scroll reveals, state changes, and attention indicators. Use when adding hover effects, loading states, form validation animation, scroll animation, expand/collapse, or notification badges.
---

# Micro-Interaction Pattern Library

## Purpose

Provide ready-to-use micro-interaction patterns that make UI feel responsive and alive. Every pattern includes exact timing values, accessibility handling, and complete code. Organize by interaction type for quick lookup during component development.

## When to Use

- Adding hover, active, or focus feedback to buttons or cards
- Animating form fields (floating labels, validation, focus glow)
- Building navigation transitions (tab indicators, menu reveals)
- Implementing scroll-driven reveals or parallax
- Adding loading-to-loaded state transitions
- Creating attention indicators (pulse, ping, bounce)

## Examples

**Example 1: Interactive button**
```
User: "Make this submit button feel more interactive"
Claude: [Uses micro-interaction-patterns] Adds hover:scale-105, active:scale-95,
focus-visible:ring-2, and a loading spinner state with opacity transition.
Timing: hover 200ms ease-out, active 100ms.
```

**Example 2: Staggered card entrance**
```
User: "These cards should animate in when they scroll into view"
Claude: [Uses micro-interaction-patterns] Uses CSS scroll-driven animation
with animation-timeline: view(). Each card fades up with translateY(50px)
over the entry range. Wraps in prefers-reduced-motion check.
```

## Button Feedback

Timing: hover 200ms, click 100-150ms.

```html
<button class="
  bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md
  transform transition-all duration-200 ease-out
  hover:bg-blue-700 hover:scale-105 hover:shadow-lg
  active:scale-95 active:bg-blue-800
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500
    focus-visible:ring-offset-2
  disabled:opacity-70 disabled:cursor-not-allowed
  motion-reduce:transition-none motion-reduce:transform-none
">
  Submit
</button>
```

## Form Floating Labels

Use the `peer` modifier so the label reacts to input state:

```html
<div class="relative mt-4">
  <input
    type="text"
    id="email"
    class="peer block w-full rounded-md border border-gray-300 bg-transparent
           px-3 pb-2 pt-5 text-sm text-gray-900
           focus:border-blue-600 focus:outline-none focus:ring-1 focus:ring-blue-600"
    placeholder=" "
  />
  <label
    for="email"
    class="absolute left-3 top-4 z-10 origin-left -translate-y-4 scale-75
           transform text-sm text-gray-500 duration-300
           peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100
           peer-focus:-translate-y-4 peer-focus:scale-75 peer-focus:text-blue-600"
  >
    Email Address
  </label>
  <p class="mt-1 hidden text-xs text-red-500 peer-invalid:block">
    Please enter a valid email.
  </p>
</div>
```

Validate on blur, not while typing, to avoid premature errors.

## Navigation Tab Indicator

Use Motion `layoutId` to slide the active indicator between tabs:

```tsx
import { useState } from "react";
import { motion } from "motion/react";

interface TabNavProps {
  tabs: string[];
}

export const TabNav: React.FC<TabNavProps> = ({ tabs }) => {
  const [selected, setSelected] = useState(tabs[0]);

  return (
    <div className="flex space-x-4 border-b">
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => setSelected(tab)}
          className="relative px-4 py-2 text-sm font-medium"
        >
          {selected === tab && (
            <motion.div
              layoutId="underline"
              className="absolute bottom-0 left-0 right-0 h-1 bg-blue-500"
            />
          )}
          <span className="relative z-10">{tab}</span>
        </button>
      ))}
    </div>
  );
};
```

## Expand/Collapse (CSS Grid Trick)

Animate height without JavaScript by transitioning grid rows:

```html
<details class="group">
  <summary class="flex w-full cursor-pointer justify-between py-2 font-bold">
    <span>Click to Expand</span>
    <span class="transition-transform group-open:rotate-180">&#9660;</span>
  </summary>
  <div class="grid grid-rows-[0fr] transition-[grid-template-rows]
              duration-300 ease-out group-open:grid-rows-[1fr]">
    <div class="overflow-hidden">
      <div class="pb-4 text-gray-600">
        Content expands smoothly via grid-template-rows transition.
      </div>
    </div>
  </div>
</details>
```

## Scroll Reveal (CSS Only)

Modern CSS scroll-driven animation with no JavaScript:

```css
@keyframes slide-up-fade {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal-on-scroll {
  @media (prefers-reduced-motion: no-preference) {
    animation: slide-up-fade linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 30%;
  }
}
```

## Attention Indicators

```html
<!-- Notification ping badge -->
<span class="relative flex h-3 w-3">
  <span class="animate-ping absolute inline-flex h-full w-full
               rounded-full bg-sky-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-3 w-3 bg-sky-500"></span>
</span>

<!-- Scroll-down bounce indicator -->
<svg class="animate-bounce w-6 h-6 text-gray-500" fill="none"
     stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M19 14l-7 7m0 0l-7-7m7 7V3" />
</svg>
```

## Timing Reference

| Interaction Type | Duration | Easing |
|---|---|---|
| Hover / click feedback | 100-150ms | ease-out |
| Simple transitions (fade, slide) | 200-300ms | ease-out |
| Complex animations (expand) | 300-500ms | ease-out |
| Stagger delay between items | 50-100ms | - |
| Reduced motion fallback | 0ms or fade only | - |

## Success Criteria

- [ ] Every interactive element has hover, active, and focus-visible states
- [ ] Timing values follow the reference table (no arbitrary durations)
- [ ] All motion wraps in prefers-reduced-motion handling
- [ ] Only transform and opacity are animated (no layout properties)
- [ ] Stagger delays create a natural cascade, not simultaneous entrance

## Copy/Paste Ready

```
"Add hover and click feedback to this button"
"Make these form fields have floating labels"
"Animate this accordion expand/collapse"
"Add a scroll reveal to these cards"
"Create a loading spinner for this button"
```
