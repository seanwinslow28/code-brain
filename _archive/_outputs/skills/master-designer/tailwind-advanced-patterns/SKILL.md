---
name: tailwind-advanced-patterns
description: Advanced Tailwind CSS patterns for premium visual design. Covers gradient techniques (mesh, animated, text), glassmorphism, layered shadow systems, animation plugins (tailwindcss-motion), dark mode theming, and responsive motion. Use when building premium UI aesthetics, implementing gradients, glassmorphism, neon glows, staggered hover effects, or dark mode with Tailwind.
---

# Tailwind CSS Advanced Patterns

## Purpose

Achieve high-end visual design using only Tailwind utility classes and minimal custom CSS. Cover gradient techniques, glass effects, depth systems, orchestrated animations, and accessible dark mode patterns. Every pattern is copy-paste ready.

## When to Use

- Creating premium visual effects (glass, glow, depth, gradients)
- Building cards, buttons, or hero sections that need to feel high-end
- Implementing dark mode with proper token-based theming
- Adding staggered or orchestrated animations without JavaScript
- Making animation responsive across breakpoints

## Examples

**Example 1: Premium feature card**
```
User: "Build a feature card that feels like an Apple product page"
Claude: [Uses tailwind-advanced-patterns] Creates a card with mesh gradient
background, animated blob, glass content layer, staggered text reveal on
hover, and border glow effect. Uses delay-75 and delay-150 for waterfall.
```

**Example 2: Neon glow button**
```
User: "Make this button glow on hover"
Claude: [Uses tailwind-advanced-patterns] Uses arbitrary shadow values
for neon glow and ring + ring-offset for sharp separation depth.
```

## Text Gradient with Shimmer

```html
<h1 class="bg-gradient-to-r from-blue-600 via-purple-500 to-indigo-400
           bg-clip-text text-transparent bg-[length:200%_auto]
           animate-[shimmer_3s_linear_infinite]">
  Premium Aesthetic
</h1>

<style>
@theme {
  @keyframes shimmer {
    0% { background-position: 200% center; }
    100% { background-position: -200% center; }
  }
}
</style>
```

The `bg-[length:200%_auto]` creates a wider background canvas so the gradient slides across.

## Glassmorphism Card

```html
<div class="relative overflow-hidden rounded-2xl border border-white/20
            bg-white/10 backdrop-blur-xl shadow-2xl">
  <!-- Noise texture layer for realism -->
  <div class="absolute inset-0 bg-[url('/noise.png')] opacity-10
              mix-blend-overlay"></div>

  <div class="relative p-8 text-white">
    <h3 class="font-bold tracking-wide">Glass Panel</h3>
    <p class="text-white/80">Content above the blurred background.</p>
  </div>
</div>
```

Always add a semi-transparent border (`border-white/20`) to define glass edges.

## Neon Glow Button

```html
<button class="rounded-lg bg-indigo-600 px-6 py-3 text-white transition-all
               shadow-[0_0_20px_rgba(79,70,229,0.3)]
               hover:shadow-[0_0_30px_rgba(79,70,229,0.6)]
               hover:ring-2 hover:ring-indigo-400
               hover:ring-offset-2 hover:ring-offset-black">
  Neon Action
</button>
```

## Staggered Hover Card

Use `group`, `delay-*`, and `translate` for a waterfall reveal:

```html
<div class="group relative cursor-pointer overflow-hidden rounded-xl
            bg-slate-900 p-8">
  <!-- Background gradient reveal -->
  <div class="absolute inset-0 bg-gradient-to-br from-indigo-500
              to-purple-600 opacity-0 transition-opacity duration-500
              group-hover:opacity-20"></div>

  <div class="relative z-10">
    <!-- Title moves up on hover -->
    <div class="transition-transform duration-300
                group-hover:-translate-y-1">
      <h3 class="text-xl font-bold text-white">Project Title</h3>
    </div>
    <!-- Description fades in with delay -->
    <p class="mt-2 translate-y-4 opacity-0 transition-all duration-300
              delay-75 group-hover:translate-y-0 group-hover:opacity-100
              text-slate-300">
      Reveal this description smoothly.
    </p>
  </div>
</div>
```

The `delay-75` on the description creates the staggered waterfall effect.

## tailwindcss-motion Plugin

Composable utility API for complex entrances without keyframes:

```html
<div class="motion-preset-slide-up motion-duration-700
            motion-ease-spring-bounciest">
  <div class="motion-delay-100">Item 1</div>
  <div class="motion-delay-200">Item 2</div>
  <div class="motion-delay-300">Item 3</div>
</div>
```

Uses pure CSS with spring physics utilities. Install: `npm install tailwindcss-motion`.

## Dark Mode with Data Attributes

Use `group-data-[...]` to cascade theme decisions without per-element JavaScript:

```html
<div class="group" data-theme="dark">
  <div class="bg-white text-slate-900
              group-data-[theme=dark]:bg-slate-900
              group-data-[theme=dark]:text-white
              transition-colors duration-300">

    <span class="text-blue-600 group-data-[theme=dark]:text-blue-400">
      Themed Accent
    </span>
  </div>
</div>
```

## Responsive Animation

Animate CSS variables that change at breakpoints:

```html
<div class="[--entry-y:20px] md:[--entry-y:50px]
            animate-[slideIn_0.5s_ease-out_forwards]"
     style="transform: translateY(var(--entry-y))">
  Responsive Entry
</div>
```

## Motion-Safe Fallback

Always provide reduced-motion fallbacks:

```html
<div class="animate-bounce motion-reduce:animate-none">
  <span class="motion-reduce:hidden">Bouncing Icon</span>
  <span class="hidden motion-reduce:block">Static Icon</span>
</div>
```

For critical transitions, switch from translate to opacity:
`motion-reduce:transition-opacity`.

## Interactive 3D Depth

Simulate physical lift with scale and shadow transitions:

```html
<div class="transition-all duration-300
            ease-[cubic-bezier(0.25,0.8,0.25,1)]
            hover:-translate-y-2 hover:shadow-2xl">
  <!-- Card content -->
</div>
```

Use physics-based easing for a premium, weighty feel.

## Success Criteria

- [ ] Gradients use bg-clip-text for text effects with animated background-position
- [ ] Glassmorphism includes backdrop-blur, semi-transparent bg, and border
- [ ] Shadows use layered approach (shadow + ring for depth)
- [ ] Staggered effects use delay-* utilities for waterfall timing
- [ ] All animations include motion-reduce fallbacks

## Copy/Paste Ready

```
"Make this card look premium with glassmorphism"
"Add a gradient shimmer to this heading"
"Create a neon glow effect on this button"
"Build a dark mode toggle with smooth transitions"
"Make these list items animate in with a stagger effect"
```
