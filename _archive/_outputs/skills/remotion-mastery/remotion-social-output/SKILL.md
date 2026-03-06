---
name: remotion-social-output
description: Social media format specifications and rendering output configuration for Remotion. Covers platform-specific dimensions (Instagram Reels, YouTube Shorts, TikTok, Twitter/X, LinkedIn), codec options (H.264, VP9, ProRes), GIF creation, CRF quality settings, multi-format rendering from single compositions, and batch render scripts. Use when rendering videos for social media, creating GIFs, or configuring output formats.
---

# Social Media and Output Formats

## Purpose

Define platform-specific video dimensions, codec settings, and rendering workflows for Remotion. Provide ready-to-use CLI commands and responsive composition patterns so a single codebase can render videos for every major social platform.

## When to Use

- User says "social media video", "Instagram Reel", "YouTube Short", "TikTok", or "GIF"
- Configuring render outputs for specific platforms
- User needs quality/size tradeoff settings
- Rendering the same video in multiple aspect ratios
- Creating GIFs for email or social preview

## Examples

**Example 1: Render for Instagram Reels**
```
User: "Render my video for Instagram Reels"
Claude: [Uses remotion-social-output] Runs: npx remotion render src/index.ts MyComp out/reel.mp4 --codec=h264 --crf=18 with the composition set to 1080x1920 at 30fps.
```

**Example 2: Create a GIF preview**
```
User: "Make a GIF version of this video for Twitter"
Claude: [Uses remotion-social-output] Runs: npx remotion render src/index.ts MyComp out/preview.gif --codec=gif --every-nth-frame=2 --scale=0.5 for a 15fps half-resolution GIF.
```

## Platform Format Specifications

| Platform | Orientation | Resolution | Aspect Ratio | Notes |
|----------|-------------|-----------|--------------|-------|
| Instagram Reels | Vertical | 1080x1920 | 9:16 | Universal vertical standard |
| YouTube Shorts | Vertical | 1080x1920 | 9:16 | Same as Reels |
| TikTok | Vertical | 1080x1920 | 9:16 | Avoid text in bottom 20% |
| Twitter/X | Landscape | 1280x720 | 16:9 | Max 512MB upload |
| Twitter/X | Square | 1080x1080 | 1:1 | Best feed engagement |
| LinkedIn | Landscape | 1920x1080 | 16:9 | Professional content |
| LinkedIn | Square | 1080x1080 | 1:1 | Feed-friendly |
| YouTube | Landscape | 1920x1080 | 16:9 | Standard HD |

Safe zone: For TikTok/Reels, keep important text out of the bottom 200px (UI overlay area).

## Rendering Commands

```bash
# Basic MP4 render
npx remotion render src/index.ts MyComposition out/video.mp4

# Specify codec explicitly
npx remotion render src/index.ts MyComp out/video.mp4 --codec=h264

# High quality (CRF 18)
npx remotion render src/index.ts MyComp out/reel.mp4 --codec=h264 --crf=18

# With specific dimensions
npx remotion render src/index.ts ShortsComp out/shorts.mp4 --width=1080 --height=1920
```

## Codec Options

| Codec | Flag | Format | Use Case |
|-------|------|--------|----------|
| H.264 | `--codec=h264` | MP4 | Default. Universal social media |
| H.265 | `--codec=h265` | MP4 | Smaller files, limited browser support |
| VP8 | `--codec=vp8` | WebM | Web playback, transparency |
| VP9 | `--codec=vp9` | WebM | Better compression, transparency |
| ProRes | `--codec=prores` | MOV | Editing in Premiere/Final Cut |
| GIF | `--codec=gif` | GIF | Previews, email, looping clips |

## Quality vs Size (CRF)

CRF = Constant Rate Factor. Lower = higher quality, larger file.

| Codec | High Quality | Balanced | Small File |
|-------|-------------|----------|------------|
| H.264 | `--crf=18` | `--crf=23` | `--crf=28` |
| H.265 | `--crf=23` | `--crf=28` | `--crf=33` |

For strict size limits: `--video-bitrate=5M` (5 Mbps for HD), `--video-bitrate=15M` (4K).

## GIF Creation

```bash
# Basic GIF
npx remotion render src/index.ts MyComp out/output.gif --codec=gif

# Optimized: 15fps, half-resolution, infinite loop
npx remotion render src/index.ts MyComp out/preview.gif \
  --codec=gif \
  --every-nth-frame=2 \
  --scale=0.5 \
  --number-of-gif-loops=0
```

GIF tips:
- `--every-nth-frame=2` renders every 2nd frame (15fps if base is 30fps)
- `--scale=0.5` halves resolution for smaller file size
- `--number-of-gif-loops=0` sets infinite loop (1 = play once)
- Keep GIFs under 480px wide for reasonable file sizes

## Multi-Format Rendering

Reuse a single component for all formats by making layout responsive.

```tsx
import React from "react";
import { AbsoluteFill, useVideoConfig, Composition } from "remotion";

const ResponsiveVideo: React.FC<{ title: string }> = ({ title }) => {
  const { width, height } = useVideoConfig();
  const isVertical = height > width;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1A1A2E",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1
        style={{
          fontSize: isVertical ? 72 : 100,
          color: "#FFFFFF",
          textAlign: "center",
          padding: 40,
        }}
      >
        {title}
      </h1>
    </AbsoluteFill>
  );
};
```

Register multiple compositions from the same component in Root.tsx:

```tsx
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Reel" component={ResponsiveVideo}
      durationInFrames={150} fps={30} width={1080} height={1920}
      defaultProps={{ title: "My Video" }} />
    <Composition id="Twitter" component={ResponsiveVideo}
      durationInFrames={150} fps={30} width={1280} height={720}
      defaultProps={{ title: "My Video" }} />
    <Composition id="LinkedIn" component={ResponsiveVideo}
      durationInFrames={150} fps={30} width={1920} height={1080}
      defaultProps={{ title: "My Video" }} />
  </>
);
```

Batch render all formats:

```bash
npx remotion render src/index.ts Reel out/reel.mp4 --codec=h264 --crf=18
npx remotion render src/index.ts Twitter out/twitter.mp4 --codec=h264 --crf=20
npx remotion render src/index.ts LinkedIn out/linkedin.mp4 --codec=h264 --crf=18
```

## Best Practices

- Stick to 30fps for social media (60fps doubles file size with minimal visual gain)
- Use `--color-space=bt709` for accurate color on mobile devices
- Use H.264 + AAC audio (default) for maximum platform compatibility
- Start with CRF 18 and increase if file size is a concern

## Success Criteria

- [ ] Compositions use correct dimensions for target platform
- [ ] Render commands include explicit codec and CRF flags
- [ ] GIFs use reduced fps and scale for reasonable file sizes
- [ ] Multi-format outputs share a single responsive component
- [ ] Safe zones respected for vertical formats (no text in bottom 200px)

## Copy/Paste Ready

```
"Render this video for Instagram Reels"
"Create a GIF preview of my Remotion video"
"Set up multi-format rendering for social media"
"What codec should I use for YouTube?"
"Optimize my video file size for Twitter upload"
```
