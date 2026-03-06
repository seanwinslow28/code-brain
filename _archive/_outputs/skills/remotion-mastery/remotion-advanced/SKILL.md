---
name: remotion-advanced
description: Advanced Remotion patterns including audio reactive video, 3D graphics with @remotion/three, AI-generated media integration (ElevenLabs, image gen), parametrized video templates with Zod schemas, and Lottie animation embedding. Use when building audio visualizations, 3D scenes, AI-narrated videos, templates for batch rendering, or embedding After Effects animations.
---

# Advanced Patterns — Audio, 3D, AI Media

## Purpose

Extend Remotion into audio-reactive video, 3D graphics, AI-generated content, parametrized templates, and After Effects animations. These patterns go beyond basic 2D composition to build professional production video systems.

## When to Use

- User says "audio visualization", "3D scene", or "AI narration"
- Building templated video systems for batch rendering
- Integrating ElevenLabs TTS or AI-generated images into Remotion
- Embedding Lottie animations from After Effects
- Creating audio-reactive waveforms or visualizers

## Examples

**Example 1: AI narrated video**
```
User: "Create a video with AI voiceover using ElevenLabs"
Claude: [Uses remotion-advanced] Generates audio via ElevenLabs API in calculateMetadata, handles the audio file via staticFile, layers <Audio> with volume control and subtitle timing.
```

**Example 2: 3D product showcase**
```
User: "Build a rotating 3D product demo in Remotion"
Claude: [Uses remotion-advanced] Creates a ThreeCanvas scene with useCurrentFrame driving rotation, lighting setup, and OrbitControls disabled for deterministic output.
```

## Audio Integration

### Basic Audio Playback

```tsx
import { Audio, staticFile, Sequence } from "remotion";

export const AudioScene: React.FC = () => (
  <Sequence from={0}>
    <Audio
      src={staticFile("narration.mp3")}
      volume={0.8}
    />
    {/* Visual content */}
  </Sequence>
);
```

### Volume Control Over Time

```tsx
import { Audio, interpolate, useCurrentFrame } from "remotion";

export const DuckedAudio: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <>
      {/* Background music ducks when narration plays */}
      <Audio
        src={staticFile("background.mp3")}
        volume={(f) =>
          interpolate(f, [0, 30, 60, 90], [0.8, 0.2, 0.2, 0.8], {
            extrapolateRight: "clamp",
          })
        }
      />
      <Audio src={staticFile("narration.mp3")} volume={1} />
    </>
  );
};
```

### Audio Visualization

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { getAudioData, visualizeAudio } from "@remotion/media-utils";
import { staticFile } from "remotion";
import { useEffect, useState } from "react";
import { delayRender, continueRender } from "remotion";

export const AudioVisualizer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [handle] = useState(() => delayRender());
  const [audioData, setAudioData] = useState<ReturnType<typeof getAudioData> | null>(null);

  useEffect(() => {
    getAudioData(staticFile("music.mp3"))
      .then((data) => {
        setAudioData(data);
        continueRender(handle);
      });
  }, [handle]);

  if (!audioData) return null;

  const visualization = visualizeAudio({
    fps,
    frame,
    audioData,
    numberOfSamples: 64,
  });

  return (
    <div style={{ display: "flex", alignItems: "flex-end", height: 400, gap: 2 }}>
      {visualization.map((v, i) => (
        <div
          key={i}
          style={{
            width: 8,
            height: v * 400,
            backgroundColor: `hsl(${(i / visualization.length) * 360}, 80%, 60%)`,
            borderRadius: 4,
          }}
        />
      ))}
    </div>
  );
};
```

## 3D Graphics with @remotion/three

```bash
npm install @remotion/three @react-three/fiber three @types/three
```

```tsx
import { ThreeCanvas, useVideoTexture } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useRef } from "react";
import * as THREE from "three";

export const Scene3D: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const rotation = (frame / fps) * Math.PI * 0.5;

  return (
    <ThreeCanvas
      orthographic={false}
      camera={{ position: [0, 0, 5], fov: 75 }}
      width={1920}
      height={1080}
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <mesh rotation={[0, rotation, 0]}>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="#E94560" />
      </mesh>
    </ThreeCanvas>
  );
};
```

3D Rules:
- Drive ALL rotation/position from `useCurrentFrame()` — never use useFrame from R3F
- Disable OrbitControls (non-deterministic user interaction)
- Use `<ThreeCanvas>` from `@remotion/three`, not raw `<Canvas>`
- Set explicit `width`/`height` matching Composition dimensions
- Use `useVideoTexture()` for videos mapped to 3D surfaces

## AI Media Integration — ElevenLabs TTS

Generate narration at build time and include as static audio:

```tsx
import { Composition } from "remotion";
import { z } from "zod";

const schema = z.object({
  narrationText: z.string(),
  audioUrl: z.string().optional(),
});

export const NarratedVideo = () => (
  <Composition
    id="NarratedVideo"
    component={NarratedScene}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={300}
    schema={schema}
    defaultProps={{ narrationText: "Hello, welcome to the demo." }}
    calculateMetadata={async ({ props }) => {
      // Generate audio via ElevenLabs API
      const response = await fetch("https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID", {
        method: "POST",
        headers: {
          "xi-api-key": process.env.ELEVENLABS_API_KEY!,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: props.narrationText,
          model_id: "eleven_monolingual_v1",
        }),
      });
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      return {
        props: { ...props, audioUrl },
        durationInFrames: 300, // Calculate from audio duration
      };
    }}
  />
);
```

## Parametrized Video Templates

Use Zod schemas for type-safe video templates suitable for batch rendering.

```tsx
import { z } from "zod";
import { Composition } from "remotion";

// Define schema
const ProductCardSchema = z.object({
  productName: z.string(),
  price: z.number(),
  imageUrl: z.string().url(),
  accentColor: z.string().default("#E94560"),
});

type ProductCardProps = z.infer<typeof ProductCardSchema>;

// Component
const ProductCard: React.FC<ProductCardProps> = ({
  productName, price, imageUrl, accentColor,
}) => {
  // ... render product card with animations
  return null;
};

// Register with schema validation
<Composition
  id="ProductCard"
  component={ProductCard}
  schema={ProductCardSchema}
  width={1080}
  height={1080}
  durationInFrames={150}
  fps={30}
  defaultProps={{
    productName: "Sample Product",
    price: 29.99,
    imageUrl: "https://example.com/product.jpg",
    accentColor: "#E94560",
  }}
/>
```

Batch render from JSON:

```bash
# render-all.sh
while IFS= read -r line; do
  npx remotion render src/index.ts ProductCard "out/product-$(echo $line | jq -r '.productName').mp4" \
    --props="$line"
done < products.jsonl
```

## Lottie Animations

Embed After Effects animations via Lottie JSON.

```bash
npm install @remotion/lottie lottie-web
```

```tsx
import { Lottie, LottieAnimationData } from "@remotion/lottie";
import { useEffect, useState } from "react";
import { continueRender, delayRender, staticFile } from "remotion";

export const LottieScene: React.FC = () => {
  const [handle] = useState(() => delayRender("Loading Lottie"));
  const [animationData, setAnimationData] = useState<LottieAnimationData | null>(null);

  useEffect(() => {
    fetch(staticFile("animation.json"))
      .then((res) => res.json())
      .then((data) => {
        setAnimationData(data);
        continueRender(handle);
      });
  }, [handle]);

  if (!animationData) return null;

  return (
    <Lottie
      animationData={animationData}
      style={{ width: 400, height: 400 }}
    />
  );
};
```

Lottie is automatically synced to Remotion's frame, so playback is deterministic.

## Success Criteria

- [ ] Audio uses `<Audio>` component, not HTML `<audio>` element
- [ ] 3D uses `<ThreeCanvas>` from `@remotion/three`, motion driven by useCurrentFrame
- [ ] AI media generated in `calculateMetadata`, not during render
- [ ] Templates use Zod schemas for prop validation
- [ ] Lottie uses `@remotion/lottie`, which auto-syncs to frame
- [ ] No non-deterministic code (Math.random, Date.now, useFrame from R3F)

## Copy/Paste Ready

```
"Add background music with volume ducking"
"Create an audio visualization waveform"
"Build a 3D rotating product showcase"
"Add AI narration with ElevenLabs"
"Create a Remotion template for batch rendering"
"Embed a Lottie animation in my video"
```
