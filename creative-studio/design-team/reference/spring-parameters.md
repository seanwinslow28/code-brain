# Spring Parameter Reference

## React Spring Presets

Use these in the `config` prop of `useSpring`, `useSprings`, or `useTrail`.

| Preset | Mass | Tension | Friction | Feel |
|---|---|---|---|---|
| Default | 1 | 170 | 26 | Balanced, snappy |
| Gentle | 1 | 120 | 14 | Soft, slow acceleration |
| Wobbly | 1 | 180 | 12 | Highly elastic, lots of overshoot |
| Stiff | 1 | 210 | 20 | Very fast, abrupt stop |
| Molasses | 1 | 280 | 120 | High friction, moves through thick fluid |

```tsx
import { useSpring, animated, config } from "@react-spring/web";

// Using presets
const props = useSpring({ opacity: 1, config: config.wobbly });

// Custom config
const custom = useSpring({
  opacity: 1,
  config: { mass: 1, tension: 300, friction: 10 },
});
```

## Motion (Framer Motion) Spring Configs

Use these in the `transition` prop with `type: "spring"`.

| Style | stiffness | damping | Feel |
|---|---|---|---|
| Bouncy | 300 | 10 | Playful overshoot |
| Smooth | 100 | 30 | Gentle, no overshoot |
| Snappy | 500 | 30 | Quick, precise |
| Heavy | 100 | 50 | Slow, weighty |
| Elastic | 200 | 8 | Rubber-band bounce |

```tsx
import { motion } from "motion/react";

// Bouncy spring
<motion.div
  animate={{ scale: 1 }}
  transition={{ type: "spring", stiffness: 300, damping: 10 }}
/>

// Smooth spring
<motion.div
  animate={{ y: 0 }}
  transition={{ type: "spring", stiffness: 100, damping: 30 }}
/>
```

## React Spring Draggable Card

Complete pattern for drag-and-release with spring physics:

```tsx
import { useSpring, animated } from "@react-spring/web";
import { useDrag } from "@use-gesture/react";

interface DragCardProps {
  children: React.ReactNode;
}

export const DragCard: React.FC<DragCardProps> = ({ children }) => {
  const [{ x, y }, api] = useSpring(() => ({ x: 0, y: 0 }));

  const bind = useDrag(({ down, movement: [mx, my] }) => {
    api.start({ x: down ? mx : 0, y: down ? my : 0, immediate: down });
  });

  return (
    <animated.div {...bind()} style={{ x, y, touchAction: "none" }}>
      {children}
    </animated.div>
  );
};
```

## Reanimated 3 Spring Configs (React Native)

Use in `withSpring(targetValue, config)`:

| Style | damping | stiffness | mass | Feel |
|---|---|---|---|---|
| Default | 10 | 100 | 1 | Standard bounce |
| Snappy | 20 | 200 | 0.5 | Quick response |
| Gentle | 15 | 50 | 1 | Slow, smooth |
| Heavy | 30 | 300 | 2 | Weighty, minimal bounce |

```typescript
import { withSpring } from "react-native-reanimated";

// Snappy spring
translateX.value = withSpring(0, {
  damping: 20,
  stiffness: 200,
  mass: 0.5,
});
```

## CSS Easing Curves

| Name | Value | Use Case |
|---|---|---|
| Material Standard | cubic-bezier(0.4, 0.0, 0.2, 1) | General transitions |
| Material Decelerate | cubic-bezier(0.0, 0.0, 0.2, 1) | Entrances |
| Material Accelerate | cubic-bezier(0.4, 0.0, 1, 1) | Exits |
| Ease Out Back | cubic-bezier(0.34, 1.56, 0.64, 1) | Playful overshoot |
| Smooth Power | cubic-bezier(0.25, 0.8, 0.25, 1) | Premium card hover |
