---
name: phaser-game-patterns
description: Expert Phaser 3 game development assistant for Game Boy-style 160x144 RPGs. Triggers when user asks about "Phaser config", "game scenes", "sprite animation", "tile maps", "physics", or "fitness RPG mechanics".
---

# Phaser Game Patterns

## Purpose

Implement battle-tested Phaser 3 patterns for a 160x144 pixel art RPG. Focuses on the "16BitFit" architecture: accurate Game Boy resolution scaling, scene management, Arcade Physics for top-down movement, and integrating fitness mechanics into the game loop. Also covers React Native integration, reusable game object patterns, and state machines.

## When to Use

- Setting up a new Phaser 3 project with pixel-perfect scaling
- Implementing scene flow (Boot -> World -> Battle -> UI)
- Creating top-down movement and collision systems
- configuring Tiled map integration
- Debugging sprite animation or physics issues
- Building a React Native + Phaser WebView integration
- Creating reusable game objects with composition patterns
- Implementing state machines for character/object behavior

## Examples

**Example 1: Game Configuration**
```
User: "Set up the Phaser config for a Game Boy resolution."
Claude: [Uses phaser-game-patterns]
import Phaser from 'phaser';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  parent: 'game-container',
  // Native Game Boy resolution
  width: 160,
  height: 144,
  // Scale up 4x for modern screens (640x576)
  zoom: 4,
  // CRITICAL: Disable anti-aliasing for crisp pixels
  render: {
    pixelArt: true,
    roundPixels: true,
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 }, // Top-down requirement
      debug: process.env.NODE_ENV === 'development',
    },
  },
  scene: [BootScene, WorldScene, BattleScene, UIScene],
};

export default config;
```

**Example 2: Player Movement**
```
User: "How do I handle top-down player movement with animations?"
Claude: [Uses phaser-game-patterns]
update() {
  const speed = 80; // Tuned for 160x144 resolution
  this.player.setVelocity(0);

  // Horizontal movement
  if (this.cursors.left.isDown) {
    this.player.setVelocityX(-speed);
    this.player.anims.play('walk-left', true);
  } else if (this.cursors.right.isDown) {
    this.player.setVelocityX(speed);
    this.player.anims.play('walk-right', true);
  }

  // Vertical movement
  if (this.cursors.up.isDown) {
    this.player.setVelocityY(-speed);
    this.player.anims.play('walk-up', true);
  } else if (this.cursors.down.isDown) {
    this.player.setVelocityY(speed);
    this.player.anims.play('walk-down', true);
  }

  // Idle state
  if (this.player.body.velocity.x === 0 && this.player.body.velocity.y === 0) {
    this.player.anims.stop();
  }
}
```

## Core Patterns

### 1. Scene Architecture
Separate responsibilities into distinct scenes to manage memory and state.

```typescript
// BootScene.ts - Assets only
export class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
  }

  preload() {
    this.load.image('tiles', 'assets/map/gb_tileset.png');
    this.load.tilemapTiledJSON('map', 'assets/map/world.json');
    this.load.spritesheet('player', 'assets/hero.png', { 
      frameWidth: 16, 
      frameHeight: 16 
    });
  }

  create() {
    this.scene.start('WorldScene');
  }
}

// WorldScene.ts - Exploration & Spawning
export class WorldScene extends Phaser.Scene {
  constructor() {
    super('WorldScene');
  }
  // ... implementation
}
```

### 2. Tiled Map Integration
Use `setCollisionByExclusion` to handle strict tile-based collisions efficiently.

```typescript
create() {
  const map = this.make.tilemap({ key: 'map' });
  const tiles = map.addTilesetImage('gb_tileset', 'tiles');
  
  // Create layers matching Tiled structure
  const ground = map.createLayer('Ground', tiles, 0, 0);
  const walls = map.createLayer('Walls', tiles, 0, 0);
  
  // Collide with everything in 'Walls' layer
  walls.setCollisionByExclusion([-1]);
  
  // Bounds
  this.physics.world.bounds.width = map.widthInPixels;
  this.physics.world.bounds.height = map.heightInPixels;
  
  // Visual Polish: Camera
  this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
  this.cameras.main.startFollow(this.player, true, 0.08, 0.08);
  this.cameras.main.setRoundPixels(true); // Prevent sub-pixel bleeding
}
```

### 3. Fitness RPG Encounter System
Use invisible zones to trigger "real world" activity prompts instead of random battles.

```typescript
createEncounters(mapWidth: number, mapHeight: number) {
  // Group of invisible triggers
  this.spawns = this.physics.add.group({ 
    classType: Phaser.GameObjects.Zone 
  });

  // Generate 10 random workout spots
  for(let i = 0; i < 10; i++) {
    const x = Phaser.Math.RND.between(0, mapWidth);
    const y = Phaser.Math.RND.between(0, mapHeight);
    this.spawns.create(x, y, 20, 20);
  }

  // Overlap handling
  this.physics.add.overlap(
    this.player, 
    this.spawns, 
    this.onMeetEnemy, 
    undefined, 
    this
  );
}

onMeetEnemy(player: Phaser.GameObjects.GameObject, zone: Phaser.GameObjects.GameObject) {
  const encounterZone = zone as Phaser.GameObjects.Zone;
  
  // Visual feedback
  this.cameras.main.shake(300);
  
  // Move zone to prevent immediate re-trigger
  encounterZone.x = Phaser.Math.RND.between(0, this.physics.world.bounds.width);
  encounterZone.y = Phaser.Math.RND.between(0, this.physics.world.bounds.height);
  
  // Pause world, launch battle UI with fitness prompt
  this.scene.pause();
  this.scene.launch('BattleScene', { type: 'SQUATS', count: 10 });
}
```

### 4. Game Object Container Pattern

Use composition over inheritance with `Phaser.GameObjects.Container` to bundle sprites, UI elements, and physics into a single movable entity.

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

### 5. State Machine Pattern

Lightweight reusable state machine for game objects with `transition()`, `onEnter()`, and `onExit()` lifecycle hooks.

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

### 6. Loading Scene with Progress Bar

Separate loading scene with a visual progress bar for better UX. Keep asset loading out of game scenes.

```typescript
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

## React Native WebView Bridge

Bidirectional communication between React Native and a Phaser game running inside a WebView.

```typescript
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

## Success Criteria

- [ ] `pixelArt: true` and `roundPixels: true` are enabled in config
- [ ] Game resolution is exactly 160x144 (scaled via zoom)
- [ ] Physics gravity is 0 for top-down movement
- [ ] Tiled map layers use `setCollisionByExclusion`
- [ ] Player movement includes velocity reset (0) every frame
- [ ] React Native bridge is bidirectional and type-safe
- [ ] No memory leaks (proper cleanup in scene shutdown)
- [ ] Performance: Maintains 60fps on target devices

## Common Gotchas

1. **Physics bodies on containers** - Must enable physics on the container itself, not its children
2. **Memory leaks** - Always call `this.textures.remove()` for dynamic textures on scene shutdown
3. **WebView performance** - Use `renderToHardwareTextureAndroid={true}` on the WebView component
4. **Asset paths** - Different in dev vs production build; use a path helper or config constant

## Copy/Paste Ready

```
"Set up the Phaser config for a 160x144 Game Boy game"
"Create a BootScene that loads my tilemap and sprites"
"Implement grid-based collision for the WorldScene"
"Add a fitness encounter system using invisible zones"
"Create a Player container with sprite, health bar, and state machine"
"Set up a React Native WebView bridge for Phaser"
"Add a loading scene with a visual progress bar"
```
