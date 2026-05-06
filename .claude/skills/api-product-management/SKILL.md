---
name: api-product-management
description: API product management for data API products like a crypto market data API. Generates API documentation (OpenAPI/Swagger), endpoint specifications, SDK scaffolding, developer portal content, rate limiting docs, versioning strategies, and DX optimization. Use when writing API specs, designing developer portals, creating endpoint documentation, planning API versioning, or specifying data API features.
---

# API Product Management

## Purpose

Provide API product management patterns for data API products. Enable Claude to generate API specifications, developer documentation, SDK scaffolding, and DX-optimized portal content. Tailored for data APIs in the crypto/financial data space like a crypto market data API's API.

## When to Use

- Writing API endpoint specifications or OpenAPI schemas
- Creating developer portal content or API guides
- Designing SDK structure for data API consumers
- Planning API versioning or migration strategies
- Specifying rate limiting, authentication, or access tiers
- Generating API documentation from existing endpoints

## Examples

**Example 1: API endpoint specification**
```
User: "Spec out a new API endpoint for historical token price data"
Claude: [Uses api-product-management]

### GET /v2/tokens/{symbol}/prices

**Description:** Retrieve historical OHLCV price data for a token.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| symbol | string | Yes | Token symbol (e.g., "ETH", "BTC") |

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| interval | enum | "1d" | Candle interval: 1m, 5m, 1h, 4h, 1d, 1w |
| start | ISO-8601 | 30d ago | Start date (inclusive) |
| end | ISO-8601 | now | End date (inclusive) |
| currency | string | "USD" | Quote currency |

**Response (200):**
```json
{
  "symbol": "ETH",
  "interval": "1d",
  "data": [
    {
      "timestamp": "2024-01-15T00:00:00Z",
      "open": 2524.30,
      "high": 2567.80,
      "low": 2498.15,
      "close": 2543.60,
      "volume": 18234567890.50
    }
  ],
  "meta": {
    "source": "aggregated",
    "sources_count": 5,
    "staleness_ms": 12000
  }
}
```

**Rate Limits:** 100 req/min (Basic), 1000 req/min (Pro), 10000 req/min (Enterprise)
**Authentication:** Bearer token via `Authorization` header
```

**Example 2: Developer portal quick-start**
```
User: "Write a quick-start guide for a crypto market data API API"
Claude: [Uses api-product-management]

# Quick Start Guide

## 1. Get Your API Key
Sign up at developer.example-data-co and generate an API key from your dashboard.

## 2. Make Your First Request
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://api.example-crypto.com/v2/tokens/ETH/prices?interval=1d&start=2024-01-01"
```

## 3. Install the SDK
```bash
npm install @example-data-co/data-sdk
```

## 4. TypeScript Example
```typescript
import { ExampleDataClient } from "@example-data-co/data-sdk";

const client = new ExampleDataClient({ apiKey: "YOUR_API_KEY" });
const prices = await client.tokens.prices("ETH", {
  interval: "1d",
  start: "2024-01-01",
});
```
```

## API Specification Template

### OpenAPI Endpoint Pattern

Use this structure for every new endpoint specification:

```yaml
paths:
  /v{version}/{resource}/{id}/{sub-resource}:
    get:
      summary: "[Action] [resource] [detail]"
      description: |
        [One paragraph explaining what this returns and common use cases]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          description: "[What this identifies]"
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
            maximum: 1000
          description: "Maximum results per page"
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
          description: "Pagination offset"
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResponseSchema"
        "401":
          description: "Invalid or missing API key"
        "429":
          description: "Rate limit exceeded"
```

### Endpoint Specification Checklist

For every new endpoint, document:

```markdown
- [ ] HTTP method and path (RESTful naming)
- [ ] All path and query parameters with types and defaults
- [ ] Request body schema (for POST/PUT)
- [ ] Response schema with example payload
- [ ] Error responses (400, 401, 403, 404, 429, 500)
- [ ] Rate limits per tier
- [ ] Authentication requirements
- [ ] Pagination strategy (cursor vs offset)
- [ ] Data freshness / staleness metadata
- [ ] Changelog entry for version history
```

## SDK Scaffolding Pattern

### TypeScript SDK Structure

```typescript
// Client configuration
interface ClientConfig {
  apiKey: string;
  baseUrl?: string;       // Default: "https://api.example-crypto.com"
  version?: string;       // Default: "v2"
  timeout?: number;       // Default: 30000ms
  retries?: number;       // Default: 3
}

// Resource pattern - each API domain gets a resource class
interface TokensResource {
  list(params?: ListParams): Promise<PaginatedResponse<Token>>;
  get(symbol: string): Promise<Token>;
  prices(symbol: string, params?: PriceParams): Promise<PriceData[]>;
  metrics(symbol: string): Promise<TokenMetrics>;
}

interface PriceParams {
  interval: "1m" | "5m" | "1h" | "4h" | "1d" | "1w";
  start?: string;   // ISO-8601
  end?: string;     // ISO-8601
  currency?: string;
}

// Pagination pattern
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    limit: number;
    offset: number;
    has_more: boolean;
  };
}

// Error handling pattern
interface ApiError {
  status: number;
  code: string;        // Machine-readable: "RATE_LIMIT_EXCEEDED"
  message: string;     // Human-readable: "Rate limit exceeded. Retry after 60s."
  retry_after?: number; // Seconds until retry is safe
}
```

## Rate Limiting Documentation

### Tier Structure Template

| Tier | Requests/min | Requests/day | Historical Data | WebSocket Streams |
|------|-------------|-------------|-----------------|-------------------|
| Free | 10 | 1,000 | 30 days | 0 |
| Basic | 100 | 50,000 | 1 year | 2 |
| Pro | 1,000 | 500,000 | Full history | 10 |
| Enterprise | 10,000 | Unlimited | Full history | Unlimited |

### Rate Limit Headers

Every response must include:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1706180400
Retry-After: 60  (only on 429 responses)
```

## API Versioning Strategy

### URL-Based Versioning (Recommended for Data APIs)

```
/v1/tokens/ETH/prices   <- Original schema
/v2/tokens/ETH/prices   <- Added 'meta.staleness_ms' field
```

### Version Lifecycle

| Phase | Duration | Description |
|-------|----------|-------------|
| Current | Ongoing | Active development, new features |
| Supported | 12 months from next version | Bug fixes only, no new features |
| Deprecated | 6 months warning | Returns `Sunset` header, migration guide available |
| Retired | After deprecation | Returns 410 Gone |

### Breaking vs Non-Breaking Changes

| Change Type | Breaking? | Versioning Required? |
|------------|-----------|---------------------|
| Add optional field to response | No | No |
| Add required query parameter | Yes | Yes, new version |
| Remove field from response | Yes | Yes, new version |
| Change field type | Yes | Yes, new version |
| Add new endpoint | No | No |
| Change error response format | Yes | Yes, new version |

## Developer Portal Content Structure

### Required Portal Sections

```markdown
1. **Getting Started**
   - Authentication guide
   - Quick-start with curl + SDK
   - API key management

2. **API Reference**
   - Auto-generated from OpenAPI spec
   - Interactive "Try It" console
   - Response examples for every endpoint

3. **Guides**
   - Common use cases with full code examples
   - Data freshness and caching recommendations
   - Pagination best practices

4. **SDKs and Libraries**
   - Official: TypeScript, Python
   - Community: Go, Rust (with disclaimers)
   - Code samples in each language

5. **Changelog**
   - Dated entries with version tags
   - Breaking changes highlighted
   - Migration guides for version bumps

6. **Status and Support**
   - API status page link
   - Rate limit dashboard
   - Support channels
```

## MCP Server Pattern for AI-Native APIs

Modern data APIs serve AI agents directly via MCP:

```typescript
import { tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const dataApiMcp = createSdkMcpServer({
  name: "example-data",
  version: "1.0.0",
  tools: [
    tool(
      "get_token_metrics",
      "Retrieve current metrics for a cryptocurrency token",
      {
        symbol: z.string().describe("Token symbol (e.g., ETH, BTC)"),
        metrics: z.array(z.enum([
          "price", "market_cap", "volume_24h", "tvl"
        ])).optional().describe("Specific metrics to retrieve"),
      },
      async (args) => {
        const data = await fetchMetrics(args.symbol, args.metrics);
        return {
          content: [{
            type: "text",
            text: JSON.stringify(data, null, 2),
          }],
        };
      }
    ),
  ],
});
```

## Success Criteria

- [ ] Every endpoint has complete request/response documentation
- [ ] Rate limits documented per tier with headers specification
- [ ] SDK patterns include proper TypeScript interfaces
- [ ] Versioning strategy clearly defines breaking vs non-breaking changes
- [ ] Developer portal covers getting started through advanced usage
- [ ] Error responses include machine-readable codes

## Copy/Paste Ready

```
"Write an API spec for a new endpoint on a crypto market data API"
"Generate OpenAPI documentation for our token metrics API"
"Design the rate limiting tiers for our data API"
"Create a quick-start guide for developers using our API"
"Spec out the SDK structure for our TypeScript client"
```
