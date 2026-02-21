---
name: phaser-pattern
description: Phaser 3 game development patterns, code snippets, and architecture guidance for React Native integration.
---

# Phaser Pattern Skill

## Purpose

Accelerate Phaser 3 game development with battle-tested patterns. Specifically optimized for React Native + Phaser integration.

## Clarifying Interview

```
Phaser Pattern Setup:

1. **What are you building?** Scene | Game object | Animation | Physics | UI | Audio
2. **Integration:** Standalone web | React Native (Expo) | React Native (bare)
3. **Game type:** Platformer | Puzzle | Arcade | Idle | Other
4. **Current issue:** New feature | Bug | Performance | Architecture
5. **Phaser version:** 3.x (specify if known)
```

## Pattern Categories

### Scene Management

```typescript
// Scene lifecycle pattern
export class GameScene extends Phaser.Scene {
  constructor() {
    super({ key: 'GameScene' });
  }

  init(data: { level: number }) {
    // Reset state, receive data from previous scene
    this.level = data.level;
  }

  preload() {
    // Load assets - keep minimal, use LoadingScene for heavy assets
  }

  create() {
    // Setup game objects, physics, input
    this.setupWorld();
    this.setupPlayer();
    this.setupInput();
  }

  update(time: number, delta: number) {
    // Game loop - keep lightweight
    this.player.update(delta);
  }
}
```

### React Native Integration

```typescript
// WebView bridge pattern for React Native
// In your React Native component:
import { WebView } from 'react-native-webview';

const GameWebView = () => {
  const webViewRef = useRef<WebView>(null);

  const sendToGame = (action: string, payload: any) => {
    webViewRef.current?.injectJavaScript(`
      window.gameInstance.events.emit('RN_MESSAGE', ${JSON.stringify({ action, payload })});
      true;
    `);
  };

  const handleMessage = (event: any) => {
    const { action, payload } = JSON.parse(event.nativeEvent.data);
    // Handle game events in RN
  };

  return (
    <WebView
      ref={webViewRef}
      source={{ uri: 'game/index.html' }}
      onMessage={handleMessage}
    />
  );
};

// In your Phaser game:
window.sendToRN = (action: string, payload: any) => {
  window.ReactNativeWebView?.postMessage(JSON.stringify({ action, payload }));
};
```

### Game Object Pattern

```typescript
// Composition over inheritance
export class Player extends Phaser.GameObjects.Container {
  private sprite: Phaser.GameObjects.Sprite;
  private healthBar: HealthBar;
  private stateMachine: StateMachine;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y);

    this.sprite = scene.add.sprite(0, 0, 'player');
    this.healthBar = new HealthBar(scene, 0, -20);

    this.add([this.sprite, this.healthBar]);
    scene.add.existing(this);

    // Enable physics on container
    scene.physics.add.existing(this);
    (this.body as Phaser.Physics.Arcade.Body).setSize(32, 48);

    this.stateMachine = new StateMachine(this, 'idle');
  }

  update(delta: number) {
    this.stateMachine.update(delta);
  }
}
```

### State Machine Pattern

```typescript
// Lightweight state machine for game objects
type State = 'idle' | 'walk' | 'jump' | 'attack';

class StateMachine {
  private currentState: State;
  private owner: any;

  constructor(owner: any, initialState: State) {
    this.owner = owner;
    this.currentState = initialState;
  }

  transition(newState: State) {
    if (this.currentState === newState) return;

    this.onExit(this.currentState);
    this.currentState = newState;
    this.onEnter(newState);
  }

  private onEnter(state: State) {
    switch (state) {
      case 'idle': this.owner.sprite.play('idle'); break;
      case 'walk': this.owner.sprite.play('walk'); break;
      case 'jump': this.owner.sprite.play('jump'); break;
    }
  }

  private onExit(state: State) {
    // Cleanup for state
  }
}
```

### Asset Loading Pattern

```typescript
// Separate loading scene for better UX
export class LoadingScene extends Phaser.Scene {
  constructor() {
    super({ key: 'LoadingScene' });
  }

  preload() {
    // Progress bar
    const progressBar = this.add.graphics();
    this.load.on('progress', (value: number) => {
      progressBar.clear();
      progressBar.fillStyle(0xffffff, 1);
      progressBar.fillRect(100, 280, 600 * value, 30);
    });

    // Load assets
    this.load.atlas('sprites', 'assets/sprites.png', 'assets/sprites.json');
    this.load.audio('bgm', 'assets/music.mp3');
  }

  create() {
    this.scene.start('GameScene');
  }
}
```

## Success Criteria

- [ ] Code follows Phaser 3 best practices (not Phaser 2 patterns)
- [ ] React Native bridge is bidirectional and type-safe
- [ ] No memory leaks (proper cleanup in scene shutdown)
- [ ] Performance: Maintains 60fps on target devices
- [ ] Architecture supports scene transitions without state loss

## Verification Steps

1. **Memory Check:** Does the scene properly destroy() resources on shutdown?
2. **Bridge Check:** Can you send/receive messages between RN and Phaser?
3. **Performance Check:** Profile with Phaser debug plugin - any frame drops?
4. **State Check:** Does game state persist correctly across scene changes?

## Context Gathering (Minimal)

Only pull:
- `game/scenes/` - Existing scene structure
- `game/objects/` - Game object patterns in use
- `package.json` - Phaser version

**Do NOT pull:** All assets, unrelated React Native code

## Common Gotchas

1. **Physics bodies on containers** - Must enable physics on container, not children
2. **Memory leaks** - Always call `this.textures.remove()` for dynamic textures
3. **WebView performance** - Use `renderToHardwareTextureAndroid={true}`
4. **Asset paths** - Different in dev vs production build

## Copy/Paste Ready

```
/phaser-pattern player movement with state machine
/phaser-pattern sprite sheet animation setup
/phaser-pattern React Native WebView bridge
/phaser-pattern object pooling for bullets
/phaser-pattern scene transition with data passing
```
