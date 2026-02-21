---
name: phaser-game-patterns
description: Expert Phaser 3 game development assistant for Game Boy-style 160x144 RPGs. Triggers when user asks about "Phaser config", "game scenes", "sprite animation", "tile maps", "physics", or "fitness RPG mechanics".
---

# Phaser Game Patterns

## Purpose

Implement battle-tested Phaser 3 patterns for a 160x144 pixel art RPG. Focuses on the "16BitFit" architecture: accurate Game Boy resolution scaling, scene management, Arcade Physics for top-down movement, and integrating fitness mechanics into the game loop.

## When to Use

- Setting up a new Phaser 3 project with pixel-perfect scaling
- Implementing scene flow (Boot -> World -> Battle -> UI)
- Creating top-down movement and collision systems
- configuring Tiled map integration
- Debugging sprite animation or physics issues

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

## Success Criteria

- [ ] `pixelArt: true` and `roundPixels: true` are enabled in config
- [ ] Game resolution is exactly 160x144 (scaled via zoom)
- [ ] Physics gravity is 0 for top-down movement
- [ ] Tiled map layers use `setCollisionByExclusion`
- [ ] Player movement includes velocity reset (0) every frame

## Copy/Paste Ready

```
"Set up the Phaser config for a 160x144 Game Boy game"
"Create a BootScene that loads my tilemap and sprites"
"Implement grid-based collision for the WorldScene"
"Add a fitness encounter system using invisible zones"
```
