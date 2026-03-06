---
name: react-native-animations
description: React Native animation patterns with Reanimated 3 and Gesture Handler 2. Build native-feel interactions including draggable elements, bottom sheets, shared element transitions, staggered lists, and pinch-to-zoom. Use when adding animation to React Native or Expo apps, implementing gestures, building bottom sheets, or optimizing animation performance on the UI thread.
---

# React Native Animations

## Purpose

Implement 60fps animations and gesture-driven interactions in React Native using Reanimated 3 and Gesture Handler 2. All animation logic runs on the UI thread, bypassing the JavaScript bridge for native performance.

## When to Use

- Adding animation to any React Native or Expo component
- Building gesture-driven UI (drag, pinch, tap, swipe)
- Implementing bottom sheets, shared element transitions, or list staggering
- Optimizing animation performance (avoiding JS thread bottleneck)
- Integrating haptic feedback with gesture interactions

## Examples

**Example 1: Draggable card**
```
User: "Make this card draggable with momentum when released"
Claude: [Uses react-native-animations] Uses Gesture.Pan() with onStart
storing context, onUpdate for position, onEnd with withDecay for momentum.
Clamps to boundaries with rubberBandEffect: true.
```

**Example 2: Bottom sheet**
```
User: "Build a pull-up bottom sheet"
Claude: [Uses react-native-animations] Uses Gesture.Pan() with spring
snapping to two positions (closed at 0, open at MAX_TRANSLATE_Y).
damping: 50 for smooth snap. Tracks context for drag offset.
```

## Core Hooks

### useSharedValue

Store animation values on the UI thread. Does not trigger React re-renders.

```typescript
import Animated, { useSharedValue } from "react-native-reanimated";

const translateX = useSharedValue(0);
```

### useAnimatedStyle

Return a style object that updates when shared values change:

```typescript
import { useAnimatedStyle } from "react-native-reanimated";

const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ translateX: translateX.value }],
}));
```

### Animation Functions

| Function | Type | Use Case |
|---|---|---|
| withSpring | Physics-based | Tactile feedback, snap back |
| withTiming | Duration-based | Controlled transitions |
| withDecay | Momentum-based | Post-drag momentum |

## Draggable Element with Decay

```typescript
import React from "react";
import { StyleSheet, View } from "react-native";
import {
  GestureDetector,
  Gesture,
  GestureHandlerRootView,
} from "react-native-gesture-handler";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withDecay,
} from "react-native-reanimated";

const DraggableBall: React.FC = () => {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  const context = useSharedValue({ x: 0, y: 0 });

  const pan = Gesture.Pan()
    .onStart(() => {
      context.value = { x: translateX.value, y: translateY.value };
    })
    .onUpdate((event) => {
      translateX.value = event.translationX + context.value.x;
      translateY.value = event.translationY + context.value.y;
    })
    .onEnd((event) => {
      translateX.value = withDecay({
        velocity: event.velocityX,
        clamp: [-150, 150],
        rubberBandEffect: true,
      });
      translateY.value = withDecay({
        velocity: event.velocityY,
        clamp: [-150, 150],
      });
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={pan}>
      <Animated.View style={[styles.ball, animatedStyle]} />
    </GestureDetector>
  );
};

const styles = StyleSheet.create({
  ball: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: "blue",
  },
});
```

## Bottom Sheet with Snap Points

```typescript
import { Dimensions } from "react-native";
import { GestureDetector, Gesture } from "react-native-gesture-handler";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from "react-native-reanimated";

const { height: SCREEN_HEIGHT } = Dimensions.get("window");
const MAX_TRANSLATE_Y = -SCREEN_HEIGHT + 50;

export const BottomSheet: React.FC = () => {
  const translateY = useSharedValue(0);
  const context = useSharedValue({ y: 0 });

  const gesture = Gesture.Pan()
    .onStart(() => {
      context.value = { y: translateY.value };
    })
    .onUpdate((event) => {
      translateY.value = Math.max(
        event.translationY + context.value.y,
        MAX_TRANSLATE_Y
      );
    })
    .onEnd(() => {
      if (translateY.value > -SCREEN_HEIGHT / 3) {
        translateY.value = withSpring(0, { damping: 50 });
      } else {
        translateY.value = withSpring(MAX_TRANSLATE_Y, { damping: 50 });
      }
    });

  const rStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={[styles.sheet, rStyle]}>
        <View style={styles.handle} />
      </Animated.View>
    </GestureDetector>
  );
};
```

## Staggered List Entries

Use Layout Animations with delays for staggered effects:

```typescript
import Animated, { FadeInDown } from "react-native-reanimated";

interface ListItem {
  id: string;
  title: string;
}

const StaggeredList: React.FC<{ items: ListItem[] }> = ({ items }) => (
  <View>
    {items.map((item, index) => (
      <Animated.View
        key={item.id}
        entering={FadeInDown.delay(index * 100).springify()}
        style={styles.card}
      >
        <Text>{item.title}</Text>
      </Animated.View>
    ))}
  </View>
);
```

## Shared Element Transitions

Use `sharedTransitionTag` to morph elements between screens:

```typescript
// Screen A
<Animated.View
  sharedTransitionTag="hero-image"
  style={{ width: 100, height: 100, backgroundColor: "red" }}
/>

// Screen B (element morphs into this)
<Animated.View
  sharedTransitionTag="hero-image"
  style={{ width: 300, height: 200, backgroundColor: "red" }}
/>
```

Requires `react-native-screens` and `NativeStack` navigator.

## Haptic Feedback with Gestures

Use `runOnJS` to call JavaScript functions from worklets:

```typescript
import * as Haptics from "expo-haptics";
import { runOnJS } from "react-native-reanimated";

const gesture = Gesture.Tap()
  .onStart(() => {
    runOnJS(Haptics.impactAsync)(Haptics.ImpactFeedbackStyle.Light);
  });
```

## Pinch and Double-Tap Zoom

```typescript
const scale = useSharedValue(1);
const savedScale = useSharedValue(1);

const pinch = Gesture.Pinch()
  .onUpdate((e) => {
    scale.value = savedScale.value * e.scale;
  })
  .onEnd(() => {
    savedScale.value = scale.value;
  });

const doubleTap = Gesture.Tap()
  .numberOfTaps(2)
  .onEnd(() => {
    scale.value = withSpring(1);
    savedScale.value = 1;
  });

const gesture = Gesture.Race(doubleTap, pinch);
```

## Performance Rules

1. Keep logic in worklets (runs on UI thread)
2. Avoid `runOnJS` in `onUpdate` (hot path). Use only in `onEnd`
3. Use `useDerivedValue` for computed values
4. Animate only transform and opacity, not width/height/margin
5. Memoize complex styles with `useMemo`

## Success Criteria

- [ ] All animations use useSharedValue, not useState
- [ ] Gesture logic runs onUpdate without runOnJS calls
- [ ] Bottom sheets snap to defined positions with withSpring
- [ ] Staggered lists use entering={FadeInDown.delay(index * N)}
- [ ] App wraps in GestureHandlerRootView

## Copy/Paste Ready

```
"Make this element draggable with spring snap-back"
"Build a bottom sheet that snaps to half and full screen"
"Add a staggered entrance animation to this FlatList"
"Implement pinch-to-zoom on this image"
"Add haptic feedback to this button press"
```
