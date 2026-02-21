---
name: animation-library-mastery
description: Animation library selection and implementation for React web and React Native. Choose between Motion (Framer Motion), React Spring, GSAP, and CSS animations. Use when adding animation, transitions, spring physics, scroll effects, layout animation, or gesture-driven motion to any component.
---

# Animation Library Mastery

## Purpose

Select the right animation library for each use case and implement animations with correct spring parameters, accessibility handling, and GPU-optimized performance. Default to Motion for React web and Reanimated for React Native unless a specific use case demands an alternative.

## When to Use

- Adding any animation or transition to a React component
- Choosing between Motion, React Spring, GSAP, or CSS for a project
- Implementing spring physics, layout animations, or scroll-driven effects
- Configuring spring parameters for specific motion styles
- Ensuring animations respect prefers-reduced-motion

## Examples

**Example 1: Choosing a library for a dashboard**
```
User: "I need to animate card entrances and a sidebar toggle in my Next.js dashboard"
Claude: [Uses animation-library-mastery] Recommends Motion for both:
- Cards use variants with staggerChildren for entrance
- Sidebar uses layout prop for smooth width transition
- Wraps motion in useReducedMotion check
```

**Example 2: Complex scroll choreography**
```
User: "I want a hero section where elements pin and animate as the user scrolls"
Claude: [Uses animation-library-mastery] Recommends GSAP ScrollTrigger:
- Uses gsap.context() in useLayoutEffect for React cleanup
- Configures timeline with scrub: 1 and pin: true
- Adds prefers-reduced-motion media query fallback
```

**Example 3: Physics-based drag interaction**
```
User: "Make this card draggable with a springy snap-back"
Claude: [Uses animation-library-mastery] Recommends React Spring + use-gesture:
- useSpring for x/y with immediate: true during drag
- Spring-back on release with default config
- No duration needed since springs are physics-based
```

## Library Decision Framework

| Requirement | Library | Reason |
|---|---|---|
| Simple UI transitions (hover, fade) | CSS / Tailwind | Zero runtime overhead |
| React UI, gestures, layout animation | Motion | Declarative API, `layout` prop, `whileHover` |
| Complex scroll choreography | GSAP + ScrollTrigger | Timeline control, scrub, pin |
| Physics-based interruptible motion | React Spring | No duration, responds to mid-animation input |
| Data visualization transitions | React Move / D3 | Granular SVG and data point animation |

## Motion (Framer Motion) Patterns

Motion is the default for React web. Import from `"motion/react"`.

### Variants and Staggering

```tsx
import { motion } from "motion/react";

interface StaggerListProps {
  items: Array<{ id: string; text: string }>;
}

const listVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { x: -20, opacity: 0 },
  visible: { x: 0, opacity: 1 },
};

export const StaggerList: React.FC<StaggerListProps> = ({ items }) => (
  <motion.ul variants={listVariants} initial="hidden" animate="visible">
    {items.map((item) => (
      <motion.li key={item.id} variants={itemVariants}>
        {item.text}
      </motion.li>
    ))}
  </motion.ul>
);
```

### Layout Animation

Use the `layout` prop to animate layout changes automatically. Use `layoutId` to morph shared elements between views.

```tsx
<motion.div layout className="card">
  {isExpanded && <motion.p layout>Extra content</motion.p>}
</motion.div>
```

### Accessibility

```tsx
import { useReducedMotion, motion } from "motion/react";

const FadeIn: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const shouldReduce = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduce ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {children}
    </motion.div>
  );
};
```

## GSAP with React

Use `gsap.context()` in `useLayoutEffect` for proper cleanup.

```tsx
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const ScrollHero: React.FC = () => {
  const comp = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: ".hero",
          start: "top top",
          end: "+=500",
          scrub: 1,
          pin: true,
        },
      });
      tl.to(".title", { scale: 2, opacity: 0 })
        .from(".image", { y: 100, opacity: 0 }, "<");
    }, comp);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={comp}>
      <div className="hero">
        <h1 className="title">Scroll Me</h1>
        <img className="image" src="/hero.jpg" alt="" />
      </div>
    </div>
  );
};
```

## Performance Rules

| Property | Render Cost | Use for Animation? |
|---|---|---|
| opacity | Low (Composite) | Yes |
| transform (translate, scale, rotate) | Low (Composite) | Yes |
| filter (blur, contrast) | Medium/High | Caution (GPU dependent) |
| width, height | High (Layout) | Avoid (causes reflow) |
| top, left, margin | High (Layout) | Avoid (causes reflow) |

For spring parameter reference and React Spring configuration, see `references/spring-parameters.md`.

## Duration Guidelines

- Micro-interactions (hover, click): 100-200ms
- Transitions (modals, drawers): 200-350ms
- Complex / large movement: 400-500ms
- Avoid durations > 500ms for UI (unless decorative)

## Easing Defaults

- UI entrance: `ease-out` (starts fast, slows)
- UI exit: `ease-in` (starts slow, speeds up)
- Natural feel: `cubic-bezier(0.4, 0.0, 0.2, 1)` (Material standard)

## Success Criteria

- [ ] Library choice matches the use case (see decision framework)
- [ ] Spring parameters use specific numeric values, not defaults
- [ ] All animations handle prefers-reduced-motion
- [ ] Only transform and opacity are animated (no layout properties)
- [ ] GSAP components use gsap.context() for React cleanup

## Copy/Paste Ready

```
"Animate these cards on entrance with a stagger effect"
"Add a spring animation to this button"
"Which animation library should I use for scroll-driven parallax?"
"Make this modal slide in with Motion"
"Add hover and tap animations to this card"
```
