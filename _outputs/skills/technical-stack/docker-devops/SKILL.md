---
name: docker-devops
description: Docker containerization and DevOps assistant. Generates optimized multi-stage Dockerfiles, manages local development with docker-compose, and helps debug container failures. Use when containerizing React/Python apps, setting up local envs, or troubleshooting deployments.
---

# Docker & DevOps Basics

## Purpose

Simplify containerization and deployment. This skill provides production-ready patterns for Dockerfiles (multi-stage builds), local development orchestration (docker-compose), and systematic debugging workflows for common container issues (OOM, networking).

## When to Use

- Writing proper key patterns for Dockerfiles
- Setting up local development with database/cache services
- Debugging container crashes (Exit 137, connection refused)
- managing secrets in Docker (env vs secrets)
- Basic deployment to container registries

## Examples

**Example 1: Multi-Stage React Build**
```
User: "Containerize my React app for production"
Claude: [Uses docker-devops]
I'll use a multi-stage release build to keep the image small (Alpine Nginx):

# Stage 1: Build
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Example 2: Debugging Crash**
```
User: "My container keeps exiting with code 137"
Claude: [Uses docker-devops]
Exit 137 indicates the generic OOM (Out Of Memory) killer.
1. Check memory limits in docker-compose.yml
2. Analyze logs for "Killed" messages
3. Increase memory reservation:

services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
```

## Domain Content

### 1. Dockerfile Patterns

**React (Vite) Pattern**
Always separate build dependencies from runtime.

```dockerfile
# See Example 1 above for full syntax
# Key: COPY --from=builder /app/dist /usr/share/nginx/html
```

**Python Pattern**
Use a non-root user and minimal base image.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy code
COPY . .
# Security: Non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["python", "app.py"]
```

### 2. Local Development (Docker Compose)

Orchestrate App + DB + Redis easily.

```yaml
version: '3.8'
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env.local
    depends_on:
      - db
      - redis
      
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: devpassword
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine

volumes:
  db_data:
```

### 3. Debugging Workflows

**Common Exit Codes**
- **137**: OOM (Out of Memory). Solution: Increase RAM.
- **127**: Command not found. Solution: Check CMD path or PATH env.
- **1**: Application error. Solution: Check app logs.

**Debugging Network**
Start a temporary container in the same network to test connectivity.
```bash
docker run --rm --network myapp_default curlimages/curl http://app:3000
```

### 4. Secret Management

**DO NOT** bake secrets into images.

**Safe**: Env file at runtime
`docker run --env-file .env.prod myimage`

**Safer**: Docker Secrets (Swarm/K8s) or Cloud Secret Manager.

**Supabase Local**:
`supabase functions serve --env-file .env.local`

## Success Criteria

- [ ] Dockerfiles use multi-stage builds (reduce size)
- [ ] Images do not run as root (security best practice)
- [ ] Secrets injected at runtime, not build time
- [ ] `.dockerignore` excludes node_modules and .git
- [ ] Compose files use named volumes for persistence

## Copy/Paste Ready

```
"Create a Dockerfile for [app]"
"Debug container exit code [code]"
"Set up docker-compose with Postgres"
"Optimize this Docker image size"
```
