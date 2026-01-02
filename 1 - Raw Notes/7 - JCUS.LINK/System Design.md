Date: 2026-01-01
Course:
Tags: 

# Content
## Summary

Your architecture is solid. Main issues and recommendations:
### Critical issue: MCP server deployment
Problem: MCP server on localhost:8080 won't work in production on Vercel.
Solutions:
1. Deploy MCP server separately (recommended)
	* Railway, Render, or Fly.io
	* Update MCP_SERVER_URL in Vercel env vars
2. Convert to Vercel serverless functions
	- Move MCP tools to /api/mcp/* routes
	- Simpler deployment, but Python cold starts are slower
### Architecture assessment
What's working:
- Clear separation: simple queries (Next.js → Supabase) vs complex ops (MCP)
- Intelligent tool selection
- Good use of vector search
What to improve:
1. Database connections: Direct Drizzle connection is fine for reads, but:
	- Use Supabase connection pooler URL
	- Consider Supabase RPC functions for better performance
	- Add caching for embeddings
2. Request flow:
	- Simple queries: Keep direct connection (low latency)
	- Complex ops: MCP server is appropriate
	- Consider pre-processing job descriptions to cache embeddings
3. Error handling:
	- Add retry logic for MCP calls
	- Implement fallbacks if MCP server is down
	- Add request timeouts
### Recommended architecture
Next.js (Vercel)
├── Simple Queries → Supabase (Direct, with connection pooler)
└── Complex Ops → MCP Server (Deployed) → Supabase → LLM

# Architecture Review & Recommendations
## Current Architecture
```

┌─────────────────┐

│ Next.js (Vercel) │

│ - Chat Interface │

│ - API Routes │

└────────┬─────────┘

│

┌────┴────┐

│ │

▼ ▼

┌─────────┐ ┌──────────────────┐

│ Supabase│ │ MCP Server │

│ (Direct) │ │ (localhost:8080) │

│ │ │ │

│ Simple │ │ Complex Ops │

│ Queries │ │ - Resume Gen │

└─────────┘ │ - Job Analysis │

│ │

└─────────┬─────────┘

│

▼

┌─────────┐

│ Supabase│

│ (Vector)│

└─────────┘

```

## Critical Issues

### 1. ❌ MCP Server Deployment
**Problem**: MCP server runs on `localhost:8080` - won't work in production on Vercel
**Solutions**:
- **Option A (Recommended)**: Deploy MCP server separately
	- Railway, Render, Fly.io, or AWS Lambda (with container)
	- Update `MCP_SERVER_URL` env var in Vercel
- **Option B**: Use Vercel Serverless Functions for Python
	- Convert MCP server to serverless functions
	- Higher latency, but simpler deployment
- **Option C**: Use Edge Functions
	- Deploy MCP logic as Vercel Edge Functions
	- Limited Python support, may need rewrite
### 2. ⚠️ Direct Database Connection from Next.js
**Problem**:
- Connection pooling issues with serverless functions
- Security: DB credentials in Next.js environment
- Cold starts create new connections each time
  
**Current Implementation** (`app/lib/embedding.ts`):
```typescript

// Direct Drizzle ORM connection

export const findRelevantContent = async (userQuery: string) => {
const userQueryEmbedded = await generateEmbedding(userQuery);
const similarGuides = await db
	.select({ name: embeddings.content, similarity })
	.from(embeddings)
	.where(gt(similarity, 0.5))
	.orderBy(t => desc(t.similarity))
	.limit(4);
return simailarJointStr;
};

```


**Recommendations**:
- ✅ **Keep for simple queries** (low latency, acceptable for read-only)
- ⚠️ **Add connection pooling** via Supabase connection pooler
- ⚠️ **Use Supabase RPC functions** instead of direct queries when possible
- ✅ **Consider caching** for frequently accessed embeddings

### 3. 🔄 Architecture Optimization
## Recommended Architecture

```
┌─────────────────────────────────────┐
│      Next.js (Vercel)               │
│  ┌───────────────────────────────┐  │
│  │  Chat Interface (Frontend)    │  │
│  └──────────────┬────────────────┘  │
│                 │                   │
│  ┌──────────────▼────────────────┐  │
│  │  API Routes                   │  │
│  │  /api/chat                    │  │
│  │  /api/search                  │  │
│  └──────┬──────────────┬─────────┘  │
└─────────┼──────────────┼────────────┘
          │              │
    ┌─────▼───-──-┐  ┌───▼────────────────┐
    │             │  │                    │
    │ Supabase    │  │  MCP Server        │
    │ (Direct)    │  │  (Deployed)        │
    │             │  │  - Railway/Render  │
    │ Simple      │  │  - Or Vercel Edge  │
    │ Queries     │  │                    │
    │             │  │  Complex Ops:      │
    │ - Similarity│  │  - Resume Gen      │
    │ - Search    │  │  - Job Analysis    │
    └─────┬─────--┘  │  - File Processing │
          │          └──────┬─────────────┘
          │                 │
          └──────┬──────---─┘
                 │
          ┌──────▼─────-─┐
          │  Supabase    │
          │  (Vector DB) │
          │  - pgvector  │
          │  - Embeddings│
          └─────────────-┘
```

## Detailed Recommendations
### 1. MCP Server Deployment Strategy
#### Option A: Separate Deployment (Recommended)
```bash
# Deploy to Railway
railway up
# Or Render
# Create render.yaml with FastMCP service
# Environment Variables:
MCP_SERVER_URL=https://your-mcp-server.railway.app/mcp

```
**Pros**:
- ✅ Independent scaling
- ✅ Better for long-running operations
- ✅ Can use connection pooling
- ✅ Easier debugging
**Cons**:
- ⚠️ Additional service to manage
- ⚠️ Network latency between services

#### Option B: Vercel Serverless Functions
Convert MCP tools to individual serverless functions:
```
/api/mcp/upload-job-description
/api/mcp/search-resumes
/api/mcp/generate-resume
```
**Pros**:
- ✅ Same deployment as Next.js
- ✅ No separate service
- ✅ Automatic scaling

**Cons**:
- ⚠️ Cold starts (Python functions slower)
- ⚠️ 10s timeout limit (can extend to 60s)
- ⚠️ More complex to maintain MCP protocol
### 2. Database Connection Optimization

#### Current: Direct Connection
```typescript
// app/lib/embedding.ts
import { db } from '../../db'; // Drizzle ORM
```

#### Recommended: Use Supabase RPC Functions
```typescript
// Create SQL function in Supabase
CREATE OR REPLACE FUNCTION search_similar_content(
  query_embedding vector(1536),
  similarity_threshold float DEFAULT 0.5,
  result_limit int DEFAULT 4
)
RETURNS TABLE (
  content text,
  similarity float
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    e.content,
    1 - (e.embedding <=> query_embedding) as similarity
  FROM embeddings e
  WHERE 1 - (e.embedding <=> query_embedding) > similarity_threshold
  ORDER BY similarity DESC
  LIMIT result_limit;
END;
$$ LANGUAGE plpgsql;

// Then in Next.js
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export const findRelevantContent = async (userQuery: string) => {
  const embedding = await generateEmbedding(userQuery);
  
  const { data, error } = await supabase.rpc('search_similar_content', {
    query_embedding: embedding,
    similarity_threshold: 0.5,
    result_limit: 4
  });
  
  return data?.map(d => d.content).join('\n') || '';
};
```

**Benefits**:
- ✅ Connection pooling via Supabase
- ✅ Better performance (server-side execution)
- ✅ Reduced cold start impact
- ✅ More secure (no direct DB access)

### 3. Caching Strategy

Add caching for frequently accessed embeddings:

```typescript
// app/lib/cache.ts
import { Redis } from '@upstash/redis'; // Vercel-compatible Redis

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

export const getCachedEmbedding = async (text: string) => {
  const key = `embedding:${hash(text)}`;
  const cached = await redis.get(key);
  if (cached) return cached;
  
  const embedding = await generateEmbedding(text);
  await redis.set(key, embedding, { ex: 3600 }); // 1 hour TTL
  return embedding;
};
```
### 4. Request Flow Optimization

#### Simple Queries (Current - Keep)
```
User Query → Next.js API → Direct Supabase → Response
Latency: ~100-200ms
```
#### Complex Operations (Current - Improve)
```
User Query → Next.js API → MCP Server → Supabase → LLM → Response
Latency: ~2-5s
```

**Optimization**: Pre-process job descriptions
```
Upload Job → MCP Server → Store in DB → Return Job ID
Query Match → Next.js → Direct Supabase (use stored job embedding)
Generate Resume → MCP Server → Use cached matches
```
### 5. Error Handling & Resilience
Add retry logic and fallbacks:

```typescript
// app/utils/mcp-client-sdk.ts
import { retry } from 'ts-retry';

export async function generateResume(...) {
  return await retry(
    async () => {
      const client = await getMCPClient();
      return await client.callTool('generate_resume', {...});
    },
    {
      retries: 3,
      delay: 1000,
      backoff: 'EXPONENTIAL',
      onRetry: (error, attempt) => {
        console.log(`Retry attempt ${attempt} for generateResume`);
      }
    }
  );
}
```

### 6. Monitoring & Observability
Add logging and metrics:

```typescript
// app/api/chat/route.ts
import { log } from '@vercel/analytics';

export async function POST(req: Request) {
  const startTime = Date.now();
  
  try {
    // ... existing code ...
    
    log('chat_request', {
      model: selectedModel,
      hasAttachments: attachments.length > 0,
      mcpToolsUsed: mcpToolSelection.tools,
    });
    
    return response;
  } finally {
    const duration = Date.now() - startTime;
    console.log(`[METRICS] Chat request took ${duration}ms`);
  }
}
```

## Implementation Priority

### Phase 1: Critical (Do First)
1. ✅ Deploy MCP server to production (Railway/Render)
2. ✅ Update `MCP_SERVER_URL` environment variable
3. ✅ Add connection pooling for Supabase (use connection string with pooler)
4. ✅ Add error handling and retries

### Phase 2: Optimization (Do Next)
1. ⚠️ Migrate simple queries to Supabase RPC functions
2. ⚠️ Add caching for embeddings
3. ⚠️ Implement request queuing for MCP operations
4. ⚠️ Add monitoring and analytics

### Phase 3: Enhancement (Nice to Have)
1. 💡 Add WebSocket support for real-time resume generation
2. 💡 Implement streaming responses for long operations
3. 💡 Add rate limiting per user
4. 💡 Cache generated resumes

## Environment Variables Checklist

```env
# Next.js (Vercel)
DATABASE_URL=postgresql://... (with connection pooler)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
MCP_SERVER_URL=https://your-mcp-server.railway.app/mcp

# MCP Server (Railway/Render)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
LLM_API_KEY=xxx
HOST=0.0.0.0
PORT=8000
```

## Testing Strategy

1. **Local Development**:
   - MCP server: `localhost:8080`
   - Next.js: `localhost:3000`
   - Test full flow end-to-end

2. **Staging**:
   - Deploy MCP server to staging
   - Deploy Next.js to Vercel preview
   - Test with production-like data

3. **Production**:
   - Monitor latency and errors
   - Set up alerts for MCP server downtime
   - Track usage metrics

## Summary

Your architecture is **solid** with good separation of concerns. Main improvements needed:

1. **Deploy MCP server** to production (not localhost)
2. **Optimize database connections** (use Supabase RPC + connection pooler)
3. **Add caching** for frequently accessed data
4. **Improve error handling** with retries and fallbacks

The direct DB connection for simple queries is **acceptable** but can be optimized further with RPC functions and caching.

