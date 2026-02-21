---
name: react-native-phaser
description: Assists with React Native and Phaser game development, including integration patterns and best practices
---

# React Native + Phaser Skill

## When to Use

Use this skill when:
- Building mobile games with React Native and Phaser
- Integrating Phaser games into React Native apps
- Optimizing game performance on mobile
- Handling game state management
- Creating game UI overlays

## Examples

**Example 1: Phaser integration**
```
User: "How do I integrate a Phaser game into my React Native app?"
Claude: [Uses react-native-phaser skill] Here's the integration pattern:

1. Use react-native-webview or react-native-game-engine
2. Create Phaser game as separate bundle
3. Bridge communication between RN and Phaser:

// React Native side
import { WebView } from 'react-native-webview';

<WebView
  source={{ uri: 'file:///path/to/game.html' }}
  onMessage={(event) => {
    const data = JSON.parse(event.nativeEvent.data);
    // Handle game events
  }}
/>

// Phaser side
window.ReactNativeWebView.postMessage(JSON.stringify({
  type: 'GAME_EVENT',
  data: { score: 100 }
}));
```

**Example 2: Performance optimization**
```
User: "My Phaser game is laggy on mobile"
Claude: [Uses react-native-phaser skill] Mobile optimization tips:
- Reduce particle count (max 50-100)
- Use object pooling for bullets/enemies
- Lower texture resolution (512x512 max)
- Enable WebGL with fallback to Canvas
- Throttle frame rate to 30fps on low-end devices
- Use texture atlases instead of individual sprites
```

## Best Practices

This skill covers:
- React Native + Phaser integration patterns
- Performance optimization for mobile
- Game state management (Redux/MobX integration)
- Touch input handling
- Asset loading and management
- Memory management and cleanup
- Testing game logic

## Copy/Paste Ready

To use this skill:
- "Help me integrate Phaser into React Native"
- "Optimize this Phaser game for mobile"
- "Create a game component using react-native-phaser patterns"
