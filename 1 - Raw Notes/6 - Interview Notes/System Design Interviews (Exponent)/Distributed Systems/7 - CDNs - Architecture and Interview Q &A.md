Date: 2026-02-17
Course:
Tags: 

# Content
```text
CDN ARCHITECTURE & DEPLOYMENT WORKFLOW
=======================================

## CRITICAL CONCEPT: You Don't Push TO the CDN, You Push TO the Origin

┌──────────────────────────────────────────────────────────────────┐
│                         CDN ARCHITECTURE                         │
└──────────────────────────────────────────────────────────────────┘

   Developer                  Origin Storage              CDN Edge           End User
   (You)                      (Where files live)          (Cache layer)      (Browser)
     │                              │                          │                 │
     │  1. Upload file              │                          │                 │
     │─────── app.js ──────────────>│                          │                 │
     │                              │                          │                 │
     │                              │  2. User requests file   │                 │
     │                              │<──── GET app.js ─────────│<────────────────│
     │                              │                          │                 │
     │                              │  3. CDN pulls from       │                 │
     │                              │     origin (first time)  │                 │
     │                              │───────── app.js ────────>│                 │
     │                              │                          │                 │
     │                              │                          │  4. CDN serves  │
     │                              │                          │─── app.js ─────>│
     │                              │                          │                 │
     │                              │                          │  5. Next user   │
     │                              │     CDN has cached it,   │    (from cache) │
     │                              │     no origin request    │                 │
     │                              │                          │─── app.js ─────>│


┌──────────────────────────────────────────────────────────────────┐
│                    EXAMPLE: AWS CLOUDFRONT                       │
└──────────────────────────────────────────────────────────────────┘

Origin = S3 Bucket

Developer Terminal:
  $ aws s3 cp app.js s3://my-bucket/assets/app.js
  
  ✅ File is now in S3 (the origin)
  
  CDN URL: https://d1234567890.cloudfront.net/assets/app.js
           └─ CloudFront domain (auto-assigned)
  
  When user requests this URL:
    1. Request hits CloudFront edge in user's region
    2. If not cached: CloudFront fetches from S3
    3. CloudFront caches it at that edge location
    4. Future requests served from edge cache


┌──────────────────────────────────────────────────────────────────┐
│                   CACHE INVALIDATION WORKFLOW                    │
└──────────────────────────────────────────────────────────────────┘

SCENARIO: You updated app.js with a bug fix

                                Old Version           Updated Version
                                   │                        │
   S3 Bucket:                      │                        ▼
     app.js ─────────────── (v1.0, has bug) ───────> (v2.0, bug fixed)
                                                           │
   CloudFront Edge Cache:                                  │
     ┌─────────────┐                                       │
     │ Tokyo Edge  │ ──── still has v1.0 cached            │
     ├─────────────┤                                       │
     │ London Edge │ ──── still has v1.0 cached            │
     ├─────────────┤                                       │
     │ NYC Edge    │ ──── still has v1.0 cached            │
     └─────────────┘                                       │
                                                           │
   ❌ PROBLEM: Users see old version for hours/days        │
              (until cache expires)                        │
                                                           │
   ✅ SOLUTION: Create invalidation request                │
                                                           │
      aws cloudfront create-invalidation \                 │
        --distribution-id E2QWRTY \                        │
        --paths "/assets/app.js"                           │
                                                           │
      This tells all edge locations:                       │
        "Delete cached app.js, fetch fresh from S3" ───────┘


┌──────────────────────────────────────────────────────────────────┐
│              BETTER APPROACH: CACHE BUSTING                      │
└──────────────────────────────────────────────────────────────────┘

Instead of invalidating, use versioned filenames:

Build Process:
  app.js  ──[hash]──>  app.a3f8d2.js
  
Upload:
  $ aws s3 cp dist/assets/app.a3f8d2.js s3://bucket/assets/app.a3f8d2.js
  
  Set Cache-Control: max-age=31536000, immutable
  (Cache forever — file will NEVER change)

Update HTML:
  <script src="https://cdn.example.com/assets/app.a3f8d2.js"></script>
                                                      └─ new hash

Result:
  ✅ Old version (app.f2d9e1.js) stays cached — no one uses it anymore
  ✅ New version (app.a3f8d2.js) fetched once, then cached
  ✅ No invalidation needed — zero cost
  ✅ No race conditions (old cache can't serve wrong version)


┌──────────────────────────────────────────────────────────────────┐
│                  TYPICAL DEPLOYMENT WORKFLOW                     │
└──────────────────────────────────────────────────────────────────┘

Step 1: Build Frontend
  $ npm run build
  
  Output:
    dist/
      ├── index.html
      ├── assets/
      │   ├── app.a3f8d2.js    (hashed)
      │   ├── style.f9e2b1.css (hashed)
      │   └── logo.png

Step 2: Upload Static Assets (CSS, JS, images)
  $ aws s3 sync dist/assets/ s3://bucket/assets/ \
      --cache-control "public, max-age=31536000, immutable"
  
  These get LONG cache (1 year) because filename changes on every update

Step 3: Upload HTML
  $ aws s3 cp dist/index.html s3://bucket/index.html \
      --cache-control "public, max-age=3600" \
      --content-type "text/html"
  
  HTML gets SHORT cache (1 hour) because it references the new asset filenames

Step 4: (Optional) Invalidate HTML
  $ aws cloudfront create-invalidation \
      --distribution-id E2QWRTY \
      --paths "/" "/index.html"
  
  Only invalidate HTML — assets use cache busting


┌──────────────────────────────────────────────────────────────────┐
│                    CDN PROVIDER COMPARISON                       │
└──────────────────────────────────────────────────────────────────┘

┌─────────────┬────────────────┬──────────────┬─────────────────┐
│ Provider    │ Origin Options │ Invalidation │ Cost            │
├─────────────┼────────────────┼──────────────┼─────────────────┤
│ CloudFront  │ S3, EC2,       │ $0.005/path  │ $0.085/GB       │
│             │ custom         │ (1000 free)  │                 │
├─────────────┼────────────────┼──────────────┼─────────────────┤
│ Cloudflare  │ R2, S3,        │ FREE         │ Free tier or    │
│             │ custom server  │ (unlimited)  │ $20/month       │
├─────────────┼────────────────┼──────────────┼─────────────────┤
│ Azure CDN   │ Blob Storage,  │ Via Portal/  │ $0.081/GB       │
│             │ custom         │ CLI          │                 │
├─────────────┼────────────────┼──────────────┼─────────────────┤
│ Fastly      │ Custom server  │ Instant      │ $0.12/GB        │
│             │ (no storage)   │ (real-time)  │ (pay as you go) │
└─────────────┴────────────────┴──────────────┴─────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                    CACHE CONTROL CHEAT SHEET                     │
└──────────────────────────────────────────────────────────────────┘

File Type          Cache-Control Header               Reasoning
─────────────────────────────────────────────────────────────────
app.abc123.js      public, max-age=31536000,          Versioned filename
style.def456.css   immutable                          Never changes, cache forever

index.html         public, max-age=3600               Frequently updated
about.html                                            References new assets
                                                      Short cache (1 hour)

logo.png           public, max-age=2592000            Static image
(no hash)                                             Medium cache (30 days)

api/data.json      no-cache, must-revalidate          Dynamic content
                                                      Always check if stale

user/profile       private, no-cache                  User-specific
                                                      Never cache


┌──────────────────────────────────────────────────────────────────┐
│                  WHEN DO YOU NEED TO PUSH FILES?                 │
└──────────────────────────────────────────────────────────────────┘

✅ YOU PUSH FILES WHEN:

1. Initial deployment (first time setting up site)
2. Updating code (new features, bug fixes)
3. Content changes (new blog posts, images)
4. Replacing assets (updated logos, styles)

❌ YOU DON'T PUSH FILES FOR:

1. CDN configuration changes (TTL, headers)
   → Change CDN settings, no file upload needed

2. Traffic spikes
   → CDN handles this automatically

3. Geographic distribution
   → CDN replicates automatically to edge locations


┌──────────────────────────────────────────────────────────────────┐
│              AUTOMATED DEPLOYMENT (CI/CD EXAMPLE)                │
└──────────────────────────────────────────────────────────────────┘

GitHub Actions Example:

name: Deploy to CDN
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build
        run: npm install && npm run build
      
      - name: Upload to S3
        run: |
          aws s3 sync dist/ s3://my-bucket/ \
            --delete \
            --cache-control "public, max-age=31536000"
      
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CF_DIST_ID }} \
            --paths "/*"


┌──────────────────────────────────────────────────────────────────┐
│                    INTERVIEW TALKING POINTS                      │
└──────────────────────────────────────────────────────────────────┘

Q: "Do you push files directly to the CDN?"
A: "No, you push files to the ORIGIN (like S3 or Blob Storage). 
    The CDN pulls from the origin and caches at edge locations.
    The CDN acts as a cache layer, not a storage layer."

Q: "When do you need to invalidate cache?"
A: "When you update a file but keep the same filename. However,
    best practice is to use cache busting (versioned filenames)
    so you never need to invalidate. Only invalidate HTML files
    which have short TTLs anyway."

Q: "How does cache busting work?"
A: "Build tools add a content hash to filenames (app.a3f8d2.js).
    When you update the file, the hash changes, so it's a new
    filename. Old version stays cached harmlessly, new version
    gets fetched. This avoids invalidation costs and race conditions."

Q: "What's the difference between CloudFront and S3?"
A: "S3 is storage (the origin). CloudFront is the CDN (caching layer).
    You upload to S3. CloudFront pulls from S3 and caches globally.
    Users request from CloudFront, not S3 directly."

Q: "Why use a CDN?"
A: "1) Speed - serve from edge near users (lower latency)
    2) Scale - CDN handles traffic, reduces origin load
    3) Cost - cheaper bandwidth than serving from origin
    4) DDoS protection - CDN absorbs attacks
    5) SSL/HTTPS - CDN handles certificates"
```

# PRACTICAL EXAMPLE: Upload script you'd actually use
```python
import os
import glob
import hashlib
import boto3

def deploy_to_s3_cloudfront(build_dir='dist', bucket='my-cdn-bucket'):
    """
    Real deployment script.
    
    Workflow:
      1. Upload assets with long cache (versioned filenames)
      2. Upload HTML with short cache
      3. Invalidate HTML only
    """
    s3 = boto3.client('s3')
    
    # Step 1: Assets (CSS, JS, images) - long cache
    print("📦 Uploading assets...")
    for file_path in glob.glob(f'{build_dir}/assets/**/*', recursive=True):
        if not os.path.isfile(file_path):
            continue
        
        s3_key = file_path.replace(f'{build_dir}/', '')
        content_type = 'application/javascript' if file_path.endswith('.js') else \
                       'text/css' if file_path.endswith('.css') else \
                       'image/png' if file_path.endswith('.png') else \
                       'application/octet-stream'
        
        s3.upload_file(
            file_path, bucket, s3_key,
            ExtraArgs={
                'ContentType': content_type,
                'CacheControl': 'public, max-age=31536000, immutable',
                'ACL': 'public-read'
            }
        )
        print(f"  ✅ {s3_key}")
    
    # Step 2: HTML files - short cache
    print("\n📄 Uploading HTML...")
    for html in glob.glob(f'{build_dir}/**/*.html', recursive=True):
        s3_key = html.replace(f'{build_dir}/', '')
        s3.upload_file(
            html, bucket, s3_key,
            ExtraArgs={
                'ContentType': 'text/html',
                'CacheControl': 'public, max-age=3600',
                'ACL': 'public-read'
            }
        )
        print(f"  ✅ {s3_key}")
    
    # Step 3: Invalidate HTML only
    print("\n🔄 Invalidating HTML cache...")
    cloudfront = boto3.client('cloudfront')
    cloudfront.create_invalidation(
        DistributionId='E2QWRTYUIOP',
        InvalidationBatch={
            'Paths': {'Quantity': 2, 'Items': ['/', '/index.html']},
            'CallerReference': str(os.urandom(8).hex())
        }
    )
    
    print("\n✅ Deployment complete!")
    print(f"🌐 Live at: https://d1234567890.cloudfront.net/")


if __name__ == '__main__':
    # Show the architecture explanation
    print(__doc__)

```

# Note


# Reference

