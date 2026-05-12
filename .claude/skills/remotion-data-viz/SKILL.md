---
name: remotion-data-viz
description: Data visualization animation patterns for Remotion. Builds animated bar charts, line charts with SVG path drawing, donut charts, counters, and crypto-specific visualizations like price charts and market cap comparisons. Use when creating chart animations, metric counters, data-driven videos, or crypto data visualizations in Remotion.
---

# Data Visualization Animations

## Purpose

Provide complete data visualization animation patterns for Remotion. Cover bar charts, line charts, donut charts, counter animations, and crypto-specific visualizations. Include patterns for feeding real API data into compositions via calculateMetadata and delayRender.

## When to Use

- User says "data visualization", "chart animation", or "animated chart"
- Building crypto data videos, market data visualizations, or metrics reports
- User needs counter animations (number counting up), progress bars, or comparison graphics
- Feeding API data (CoinGecko, JSON) into Remotion compositions

## Examples

**Example 1: Crypto bar chart**
```
User: "Create an animated bar chart comparing crypto market caps"
Claude: [Uses remotion-data-viz] Creates a BarChart component with staggered spring animations (frame - index * 5), feeds data via calculateMetadata from CoinGecko API, renders bars growing from zero with brand colors.
```

**Example 2: Counter animation**
```
User: "Animate a number counting up from 0 to $42,000"
Claude: [Uses remotion-data-viz] Creates an AnimatedCounter component using interpolate(frame, [0, 60], [0, 42000]) with Math.floor and toLocaleString for formatting.
```

## Animated Bar Chart

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface BarData {
  label: string;
  value: number;
  color: string;
}

interface BarChartProps {
  data: BarData[];
  maxValue: number;
}

export const BarChart: React.FC<BarChartProps> = ({ data, maxValue }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, width: "100%", padding: 40 }}>
      {data.map((item, index) => {
        const width = spring({
          frame: frame - index * 5,
          fps,
          from: 0,
          to: (item.value / maxValue) * 100,
          config: { damping: 100, stiffness: 200 },
        });

        return (
          <div key={item.label} style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ width: 120, fontSize: 18, color: "#FFFFFF" }}>{item.label}</span>
            <div
              style={{
                width: `${width}%`,
                height: 40,
                backgroundColor: item.color,
                borderRadius: 4,
              }}
            />
          </div>
        );
      })}
    </div>
  );
};
```

## Line Chart with Path Animation

Uses `@remotion/paths` for SVG path drawing.

```tsx
import React from "react";
import { evolvePath } from "@remotion/paths";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

interface LineChartProps {
  pathData: string;
  color?: string;
}

export const LineChart: React.FC<LineChartProps> = ({
  pathData,
  color = "#E94560",
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames * 0.7], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const evolution = evolvePath(progress, pathData);

  return (
    <svg viewBox="0 0 500 200" width="100%">
      <path
        d={pathData}
        stroke={color}
        strokeWidth={3}
        fill="none"
        strokeDasharray={evolution.strokeDasharray}
        strokeDashoffset={evolution.strokeDashoffset}
      />
    </svg>
  );
};
```

## Donut Chart

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface DonutChartProps {
  percentage: number;
  color: string;
  label?: string;
}

export const DonutChart: React.FC<DonutChartProps> = ({
  percentage,
  color,
  label,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const animatedValue = spring({
    frame,
    fps,
    from: 0,
    to: percentage,
    config: { damping: 100, stiffness: 80 },
  });

  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const dashLength = (animatedValue / 100) * circumference;

  return (
    <div style={{ textAlign: "center" }}>
      <svg width="200" height="200" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} stroke="#333" strokeWidth="10" fill="none" />
        <circle
          cx="60"
          cy="60"
          r={radius}
          stroke={color}
          strokeWidth="10"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={`${dashLength} ${circumference}`}
          transform="rotate(-90 60 60)"
        />
        <text x="60" y="65" textAnchor="middle" fill="white" fontSize="20" fontWeight="bold">
          {Math.floor(animatedValue)}%
        </text>
      </svg>
      {label && <div style={{ color: "#FFFFFF", fontSize: 16, marginTop: 8 }}>{label}</div>}
    </div>
  );
};
```

## Counter Animation

```tsx
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

interface AnimatedCounterProps {
  endValue: number;
  prefix?: string;
  suffix?: string;
  durationFrames?: number;
}

export const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  endValue,
  prefix = "$",
  suffix = "",
  durationFrames = 60,
}) => {
  const frame = useCurrentFrame();

  const value = interpolate(frame, [0, durationFrames], [0, endValue], {
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ fontSize: 100, fontFamily: "monospace", color: "#FFFFFF" }}>
      {prefix}
      {Math.floor(value).toLocaleString()}
      {suffix}
    </div>
  );
};
```

## Feeding Real Data via calculateMetadata

```tsx
import { Composition } from "remotion";
import { CryptoChart } from "./scenes/CryptoChart";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CryptoChart"
      component={CryptoChart}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
      calculateMetadata={async () => {
        const response = await fetch(
          "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10"
        );
        const coins = await response.json();
        return {
          props: { chartData: coins },
          durationInFrames: coins.length * 30,
        };
      }}
    />
  );
};
```

For render-time data fetching (legacy), use `delayRender` / `continueRender`:

```tsx
import { useState, useEffect } from "react";
import { continueRender, delayRender, cancelRender } from "remotion";

export const DataComponent: React.FC = () => {
  const [handle] = useState(() => delayRender("Fetching data..."));
  const [data, setData] = useState<unknown>(null);

  useEffect(() => {
    fetch("https://api.example.com/data")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
  }, [handle]);

  if (!data) return null;
  return <div>{/* render data */}</div>;
};
```

## Success Criteria

- [ ] Charts animate from zero/empty state to final values
- [ ] Bar charts use staggered spring delays (frame - index * N)
- [ ] Line charts use evolvePath or strokeDasharray SVG technique
- [ ] Counters use interpolate with Math.floor, not setInterval
- [ ] Data comes from calculateMetadata (preferred) or delayRender
- [ ] All components accept typed data arrays as props

## Copy/Paste Ready

```
"Create an animated bar chart for crypto market caps"
"Build a line chart that draws itself for BTC price history"
"Add a counter animation counting up to $42,000"
"Create a donut chart showing portfolio allocation"
"Make a data visualization video from this JSON"
```
