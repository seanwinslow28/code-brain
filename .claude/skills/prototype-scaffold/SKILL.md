---
name: prototype-scaffold
description: Rapid project scaffolding for prototypes. Gets you coding in under 2 minutes with sensible defaults.
---

# Prototype Scaffold Skill

## Purpose

Zero-to-coding in under 2 minutes. Scaffold prototypes with your preferred stack, skip the boilerplate, start building.

## Clarifying Interview

```
Prototype Scaffold Setup:

1. **What are you building?** Web app | API | CLI | Game | Script | Automation
2. **Stack preference:**
   - Web: React | Next.js | Vanilla | Vue
   - Backend: Python | Node | Supabase edge functions
   - Game: Phaser | React Native + Phaser
3. **Complexity:** Throwaway | Might keep | Production-bound
4. **Features needed:** Auth | DB | API | Real-time | None
5. **Deploy target:** Local only | Vercel | Supabase | None yet
```

## Scaffold Templates

### React + Vite (Fast Web Prototype)

```bash
# One-liner setup
npm create vite@latest my-prototype -- --template react-ts && cd my-prototype && npm install

# Minimal App.tsx
```

```typescript
// src/App.tsx
import { useState } from 'react'

function App() {
  const [data, setData] = useState(null)

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>Prototype</h1>
      {/* Start building here */}
    </div>
  )
}

export default App
```

### Python Script (Quick Automation)

```bash
# Setup
mkdir my-script && cd my-script
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install requests python-dotenv
```

```python
# main.py
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main entry point."""
    print("Starting...")
    # Your code here

if __name__ == "__main__":
    main()
```

```
# .env
API_KEY=your_key_here
```

### Supabase + React (Full-Stack Prototype)

```bash
# Setup
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @supabase/supabase-js
```

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseKey)
```

```typescript
// src/App.tsx
import { useEffect, useState } from 'react'
import { supabase } from './lib/supabase'

function App() {
  const [items, setItems] = useState<any[]>([])

  useEffect(() => {
    loadItems()
  }, [])

  async function loadItems() {
    const { data } = await supabase.from('items').select('*')
    setItems(data || [])
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Items</h1>
      <ul>
        {items.map(item => <li key={item.id}>{item.name}</li>)}
      </ul>
    </div>
  )
}

export default App
```

### Phaser 3 Game (Minimal)

```bash
npm create vite@latest my-game -- --template vanilla-ts
cd my-game
npm install phaser
```

```typescript
// src/main.ts
import Phaser from 'phaser'

class MainScene extends Phaser.Scene {
  constructor() {
    super({ key: 'MainScene' })
  }

  preload() {
    // Load assets
  }

  create() {
    this.add.text(400, 300, 'Hello Phaser!', { fontSize: '32px' }).setOrigin(0.5)
  }
}

new Phaser.Game({
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  scene: MainScene,
  parent: 'app',
  backgroundColor: '#1a1a2e'
})
```

### Node.js API (Express Minimal)

```bash
mkdir my-api && cd my-api
npm init -y
npm install express cors dotenv
npm install -D typescript @types/node @types/express ts-node nodemon
npx tsc --init
```

```typescript
// src/index.ts
import express from 'express'
import cors from 'cors'

const app = express()
app.use(cors())
app.use(express.json())

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' })
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000')
})
```

```json
// package.json scripts
{
  "scripts": {
    "dev": "nodemon --exec ts-node src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

## File Structure Patterns

### Minimal (Throwaway)
```
project/
├── src/
│   └── main.ts
├── package.json
└── .env
```

### Standard (Might Keep)
```
project/
├── src/
│   ├── components/
│   ├── lib/
│   ├── utils/
│   └── main.ts
├── public/
├── .env
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

## Success Criteria

- [ ] Project runs with single command (`npm run dev`)
- [ ] No unnecessary dependencies
- [ ] Environment variables externalized
- [ ] Can start building feature immediately (no more setup)

## Verification Steps

1. **Run Check:** Does `npm run dev` (or equivalent) work?
2. **Edit Check:** Can you modify code and see changes?
3. **Clean Check:** Any unused boilerplate to delete?
4. **Env Check:** Are secrets in .env, not committed?

## Essential .gitignore

```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Environment
.env
.env.local

# Build
dist/
build/
.next/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

## Copy/Paste Ready

```
/prototype-scaffold React app with Supabase
/prototype-scaffold Python script for API automation
/prototype-scaffold Phaser 3 game minimal
/prototype-scaffold Express API with TypeScript
/prototype-scaffold CLI tool in Node
```
