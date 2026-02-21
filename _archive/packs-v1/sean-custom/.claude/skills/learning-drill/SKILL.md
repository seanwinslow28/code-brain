---
name: learning-drill
description: Generates focused practice exercises for building coding muscle memory. Spaced repetition for skills.
---

# Learning Drill Skill

## Purpose

Build coding muscle memory through deliberate practice. Generates exercises at your level, tracks what you've practiced, and gradually increases difficulty.

## Clarifying Interview

```
Learning Drill Setup:

1. **What skill?** React | Python | TypeScript | SQL | Git | CSS | Testing | Other
2. **Your level:** Beginner | Intermediate | Know basics, want fluency
3. **Time available:** 5 min | 15 min | 30 min
4. **Focus area:** [Specific topic, or "surprise me"]
5. **Learning style:** Explain first | Jump into code | Mix
```

## Drill Formats

### Code Completion Drill
```markdown
## Drill: Array Methods (JavaScript)

**Level:** Beginner → Intermediate
**Time:** 10 minutes
**Goal:** Complete without looking up documentation

### Exercise 1: Filter & Map
Given this data:
```javascript
const users = [
  { name: 'Alice', age: 25, active: true },
  { name: 'Bob', age: 30, active: false },
  { name: 'Carol', age: 35, active: true }
];
```

Write a one-liner to get names of active users:
```javascript
const activeNames = // Your code here
// Expected: ['Alice', 'Carol']
```

<details>
<summary>Hint</summary>
Use .filter() then .map()
</details>

<details>
<summary>Solution</summary>
```javascript
const activeNames = users.filter(u => u.active).map(u => u.name);
```
</details>
```

### Bug Hunt Drill
```markdown
## Drill: Find the Bug (React)

**Level:** Intermediate
**Time:** 5 minutes

### The Bug
This component doesn't update when the button is clicked. Why?

```jsx
function Counter() {
  let count = 0;

  const increment = () => {
    count = count + 1;
    console.log(count); // This logs correctly!
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Add</button>
    </div>
  );
}
```

**Your task:** Identify the bug and fix it.

<details>
<summary>Explanation</summary>
`count` is a regular variable, not React state. Changes to regular variables don't trigger re-renders.
</details>

<details>
<summary>Fixed Code</summary>
```jsx
function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(count + 1);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Add</button>
    </div>
  );
}
```
</details>
```

### Explain It Drill
```markdown
## Drill: Explain This Code (TypeScript)

**Level:** Intermediate
**Time:** 5 minutes

### The Code
```typescript
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? DeepReadonly<T[P]>
    : T[P];
};
```

**Your task:** Explain what this type does in plain English.

**Bonus:** Give an example of when you'd use it.

<details>
<summary>Explanation</summary>
This creates a recursive type that makes all properties of an object readonly, including nested objects. It:
1. Iterates over all keys `P` in type `T`
2. For each key, checks if the value is an object
3. If yes, recursively applies DeepReadonly
4. If no, keeps the type as-is but adds readonly

Use case: Ensuring immutability of complex config objects or state.
</details>
```

### Speed Drill
```markdown
## Drill: Type It Fast (Git)

**Level:** Any
**Time:** 2 minutes

### Commands
Type these git commands from memory as fast as possible:

1. Check current status: ___
2. Stage all changes: ___
3. Commit with message "fix bug": ___
4. Push to origin main: ___
5. Pull with rebase: ___
6. Create and switch to new branch "feature": ___
7. Stash current changes: ___
8. Apply most recent stash: ___

<details>
<summary>Answers</summary>
1. `git status`
2. `git add .` or `git add -A`
3. `git commit -m "fix bug"`
4. `git push origin main`
5. `git pull --rebase`
6. `git checkout -b feature` or `git switch -c feature`
7. `git stash`
8. `git stash pop`
</details>
```

### Build From Scratch Drill
```markdown
## Drill: Build Without References (React)

**Level:** Intermediate
**Time:** 15 minutes

### Challenge
Build a todo list component from scratch. No documentation, no copying.

**Requirements:**
- [ ] Add new todo with input + button
- [ ] Display list of todos
- [ ] Mark todo as complete (strikethrough)
- [ ] Delete todo

**Rules:**
- Don't look up any documentation
- Don't copy from existing code
- If stuck, take a guess before checking hint

**After completing:** Compare with your previous implementations. What patterns are becoming automatic?
```

## Drill Progressions

### React Fundamentals (4-week progression)
```
Week 1: Components & Props
- Day 1: Create static components
- Day 2: Pass and use props
- Day 3: Conditional rendering
- Day 4: List rendering with keys
- Day 5: Review drill (build from memory)

Week 2: State & Events
- Day 1: useState basics
- Day 2: Event handlers
- Day 3: Controlled inputs
- Day 4: State lifting
- Day 5: Review drill

Week 3: Effects & Lifecycle
- Day 1: useEffect basics
- Day 2: Cleanup functions
- Day 3: Dependency arrays
- Day 4: Data fetching pattern
- Day 5: Review drill

Week 4: Patterns & Composition
- Day 1: Custom hooks
- Day 2: Context API
- Day 3: Component patterns (compound, render props)
- Day 4: Error boundaries
- Day 5: Build complete app from scratch
```

## Success Criteria

- [ ] Completed without looking up documentation
- [ ] Code works on first or second try
- [ ] Time was under target
- [ ] Can explain why the solution works

## Verification Steps

1. **Syntax Check:** Does it run without errors?
2. **Logic Check:** Does it produce expected output?
3. **Understanding Check:** Can you explain it to someone else?
4. **Retention Check:** Can you do it again tomorrow?

## Tracking Progress

```markdown
## Drill Log

| Date | Topic | Drill Type | Time | Result | Notes |
|------|-------|-----------|------|--------|-------|
| 01/15 | React useState | Code completion | 5m | ✅ | Easy now |
| 01/16 | Array methods | Speed drill | 3m | ⚠️ | Forgot reduce |
| 01/17 | TypeScript generics | Explain it | 10m | ✅ | Need more practice |
```

## Copy/Paste Ready

```
/learning-drill React hooks 15 minutes
/learning-drill Python: list comprehensions, beginner
/learning-drill TypeScript types, intermediate, explain first
/learning-drill SQL joins, surprise me
/learning-drill Git commands, speed drill
/learning-drill Build from scratch: form validation
```
