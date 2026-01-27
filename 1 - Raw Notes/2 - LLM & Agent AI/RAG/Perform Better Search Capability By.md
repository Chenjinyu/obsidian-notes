Date: 2026-01-26
Course:
Tags: [[RAG]] [[LLM]] [[AI]] [[Agentic]]

# Content
how to enhance chunk
1. improve chunk
    1. resume, each job and experience, the education in one chunk, certificate in one chunk, basic info in ono chunk
    2. blog, each paragraph in one chunk
    3. pdf, uses langchian recursiveTextSpliter  

2. add context to each chunk.
    eg: 
```json
{
  "category": "work_experience",
  "company": "Capital One",
  "role": "Senior Software Engineer",
  "tech": ["AWS", "Kubernetes", "Python"],
  "desc": "Built microservices for data processing"
}
```
to natural language

ategory: Work Experience

Company: Capital One
Role: Senior Software Engineer

Description:
Built microservices for data processing using AWS, Kubernetes, and Python.

below are more close to human natual language.
Work Experience at Capital One.

I worked as a Senior Software Engineer where I built microservices for data processing using AWS, Kubernetes, and Python.

use json format to store orginal text, and use natural language store content with embeded.

3. Contextual enhancement( add more related natural language info)
eg: 
Resume section: work experience. 
Company: Captial One
Role: xxx
I worked as a Senior Software Engineer where I built microservices for data processing using AWS, Kubernetes, and Python.


4. Metadata enrichment
use metadata to filter the content during the search
```json
{
  "title": "My Resume",
  "section": "Work Experience",
  "company": "Capital One",
  "year": "2022-2025"
}
```

```sql

SELECT
  id,
  content,
  metadata,
  1 - (embedding <=> :query_embedding) AS similarity
FROM embeddings
WHERE metadata->>'section' = 'Work Experience'
  AND metadata->>'company' = 'Capital One'
ORDER BY embedding <=> :query_embedding
LIMIT 10;
```

with @> (includes)

```sql
CREATE FUNCTION match_embeddings(
  query_embedding vector,
  match_count int,
  filters jsonb
)
RETURNS TABLE (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE sql
AS $$
  SELECT
    id,
    content,
    metadata,
    1 - (embedding <=> query_embedding) AS similarity
  FROM embeddings
  WHERE metadata @> filters
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;
```

5. add reranker after
```sql
WHERE (metadata->>'start_year')::int <= 2024
  AND (metadata->>'end_year')::int >= 2024
```


only resume: metadata->>'title' = 'My Resume'

only work experience:  metadata->>'section' = 'Work Experience'
only company: metadata->>'company' = 'Capital One'
only blog: metadata->>'source_type' = 'blog'


5. have better leverage with LLM
Short answer: yes — and this is exactly how modern RAG systems + agentic search are built.
Long answer: you should treat the LLM as an intent + filter generator, not just a text generator.

You ask the LLM:
```txt
👉 “Convert the user’s question into structured search filters (JSON)”
Then you:
👉 use that JSON to filter metadata during vector search.
This is called:
semantic → structured query translation
(Big tech uses this everywhere.)
```

the LLM output should be:
```json
{
  "filters": {
    "section": "Work Experience",
    "company": "Capital One"
  },
  "search_query": "backend microservices AWS Kubernetes experience"
}
```

6. enhance the prompt pattern
```txt

You are a query analyzer for a vector database.

Given a user question, extract relevant metadata filters as JSON.

Available metadata fields:
- category (work_experience, education, skills, projects, blog)
- section
- company
- title
- start_year
- end_year

Rules:
- Only include fields that are clearly implied
- Use exact known values when possible
- If nothing applies, return {}

User question:
"{question}"

Return ONLY valid JSON.
```


# Note


# Reference

