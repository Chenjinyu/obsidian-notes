Date: 2026-02-04
Course:
Tags: 

# Content

Excellent questions! Let me clarify these important concepts:

## 1. SQS Visibility Timeout Mechanism ✅

### How SQS Manages Message Visibility

```
┌─────────────────────────────────────────────────────────────┐
│ SQS Message Lifecycle                                       │
└─────────────────────────────────────────────────────────────┘

Time 0s:     Message is VISIBLE in queue
             ↓
             Consumer (Lambda) receives message
             ↓
Time 0s:     SQS AUTOMATICALLY makes message INVISIBLE
             (VisibilityTimeout starts counting)
             ↓
Time 0-900s: Message is INVISIBLE (being processed by Lambda)
             Other consumers CANNOT see this message
             ↓
             ┌─────────────────┬─────────────────┐
             │                 │                 │
         SUCCESS           TIMEOUT/FAILURE   
             │                 │
Time 300s:   │            Time 900s:
Lambda       │            VisibilityTimeout
deletes      │            expires
message      │                 │
             │                 ↓
             │            Message becomes
             │            VISIBLE again
             │            (ready for retry)
             ↓
Message permanently
removed from queue
```

### Your Understanding is CORRECT! ✅

```python
# Example with actual timeline

# Queue Configuration
VisibilityTimeout = 960  # 16 minutes

# Lambda Configuration  
Lambda timeout = 900  # 15 minutes

# Timeline:
# Time 0s:   Lambda receives message
#            → SQS automatically sets visibility timeout to 960s
#            → Message invisible to other consumers

# Time 0-900s: Lambda processing
#            → If Lambda succeeds: deletes message (done!)
#            → If Lambda fails/crashes: does NOT delete message

# Time 900s: Lambda timeout occurs (crashes)
#            → Lambda did NOT delete message
#            → Message still invisible (60s remaining on visibility)

# Time 960s: VisibilityTimeout expires
#            → SQS AUTOMATICALLY makes message visible again
#            → Another Lambda can pick it up for retry
```

### How Does SQS Know When to Make Message Visible?

**SQS uses a simple timer mechanism:**

```python
# Pseudocode of SQS internal logic

class SQSMessage:
    def __init__(self):
        self.visible = True
        self.visibility_timeout = 900
        self.invisible_until = None
    
    def receive_message(self):
        """When Lambda receives the message"""
        if self.visible:
            # Make message invisible
            self.visible = False
            self.invisible_until = current_time() + self.visibility_timeout
            return self
    
    def check_visibility(self):
        """SQS runs this continuously"""
        if not self.visible:
            if current_time() >= self.invisible_until:
                # Visibility timeout expired
                self.visible = True
                self.receive_count += 1  # Track retry attempts
    
    def delete_message(self):
        """Lambda successfully processed and deletes"""
        # Permanently remove from queue
        self.deleted = True
```

### Lambda's Role in Message Deletion

```python
# Lambda with SQS trigger (managed by AWS)

def lambda_handler(event, context):
    """
    AWS manages message deletion automatically!
    """
    
    for record in event['Records']:
        try:
            # Process message
            process_message(record)
            
            # If successful, AWS AUTOMATICALLY deletes the message
            # You don't need to call delete explicitly!
            
        except Exception as e:
            # If exception occurs, AWS does NOT delete message
            # Message becomes visible again after VisibilityTimeout
            raise  # Re-raise to tell AWS the processing failed
```

**Manual deletion (only needed for custom polling):**

```python
# If you're manually polling SQS (not Lambda event source)
import boto3

sqs = boto3.client('sqs')

# Receive message
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,
    VisibilityTimeout=900  # Message invisible for 15 min
)

for message in response['Messages']:
    try:
        # Process message
        process(message)
        
        # MUST manually delete on success
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']  # Unique handle for this delivery
        )
    except:
        # Don't delete - let it become visible again for retry
        pass
```

### Visibility Timeout Best Practices

```python
# ✅ CORRECT: Buffer time for safety
Lambda timeout:        900s (15 min)
VisibilityTimeout:     960s (16 min)  # +60s buffer

# ❌ WRONG: Too short
Lambda timeout:        900s
VisibilityTimeout:     300s  # Message becomes visible while Lambda still processing!
# Result: Message processed TWICE (duplicate!)

# ⚠️ RISKY: Exact match
Lambda timeout:        900s
VisibilityTimeout:     900s  # No buffer
# If Lambda takes 900s, message might become visible just as it finishes

# ✅ BETTER: Generous buffer
Lambda timeout:        900s
VisibilityTimeout:     1200s (20 min)  # +5 min buffer
```

---

## 2. Manual Batching with Redis (Clarification)

You're right to be confused! Let me clarify the **two different architectures**:

### Architecture A: Standard Flow (No Redis Batching)

```
┌──────────┐
│Application│
│  Server  │
└────┬─────┘
     │
     │ Sends messages directly
     ↓
┌─────────┐
│   SQS   │ ← Messages stored here
│  Queue  │
└────┬────┘
     │
     │ SQS automatically batches (batch_size=10)
     │ and triggers Lambda
     ↓
┌─────────┐
│ Lambda  │ ← Receives batch of 10 messages
└────┬────┘
     │
     │ Writes to database
     ↓
┌─────────┐
│Database │
└─────────┘
```

**Code:**

```python
# Application Server
import boto3
sqs = boto3.client('sqs')

# Send message to SQS
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({'user_id': 123, 'data': 'new_data'})
)

# Lambda (automatically receives batches from SQS)
def lambda_handler(event, context):
    # event['Records'] contains up to 10 messages (batched by SQS)
    for record in event['Records']:
        message = json.loads(record['body'])
        write_to_db(message)
```

### Architecture B: Advanced with Redis Batching (RARE!)

```
┌───────────┐
│Application│
│  Server   │
└────┬──────┘
     │
     │ Sends messages
     ↓
┌─────────┐
│   SQS   │
│  Queue  │
└────┬────┘
     │
     │ SQS triggers Lambda (batch_size=10)
     ↓
┌─────────┐
│ Lambda  │ ← Receives 10 messages from SQS
└────┬────┘
     │
     │ Instead of writing to DB immediately,
     │ accumulates in Redis until batch reaches 100
     ↓
┌─────────┐
│  Redis  │ ← Temporary accumulation buffer
└────┬────┘
     │
     │ When 100 messages accumulated
     ↓
┌─────────┐
│Database │ ← Batch write 100 records at once
└─────────┘
```

**Code for Architecture B:**

```python
# Application Server (SAME as Architecture A)
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({'user_id': 123, 'data': 'new_data'})
)

# Lambda (uses Redis as intermediate buffer)
import redis
redis_client = redis.Redis(host='redis-endpoint')

def lambda_handler(event, context):
    """
    SQS → Lambda (10 messages)
    Lambda → Redis (accumulate)
    Redis → Database (when batch = 100)
    """
    
    # Lambda receives 10 messages from SQS
    for record in event['Records']:
        message_body = record['body']
        
        # Push to Redis list (accumulate)
        redis_client.lpush('pending_batch', message_body)
    
    # Check if we have enough for a batch
    batch_size = redis_client.llen('pending_batch')
    
    if batch_size >= 100:
        # Get 100 messages from Redis
        batch = redis_client.lrange('pending_batch', 0, 99)
        
        # Remove those 100 from Redis
        redis_client.ltrim('pending_batch', 100, -1)
        
        # Parse and batch write to database
        records = [json.loads(msg) for msg in batch]
        cursor.executemany(
            "INSERT INTO users VALUES (%s, %s)",
            [(r['user_id'], r['data']) for r in records]
        )
        conn.commit()
```

### Why Use Redis Batching? (Very Specific Use Cases)

```python
# ❌ DON'T USE for most cases - unnecessary complexity

# ✅ USE ONLY when:

# 1. Database has very high per-transaction cost
#    (e.g., expensive database with per-query licensing)
write_cost_per_transaction = $0.01
# Batch of 100 costs $0.01 vs 100 individual writes = $1.00

# 2. Database has strict connection limits
max_connections = 50
concurrent_lambdas = 100  # More Lambdas than DB connections
# Solution: Use Redis to reduce DB connection count

# 3. Need cross-Lambda batching for analytics
# Accumulate events from multiple Lambda invocations
# Then write aggregated stats once
```

### For Most Cases: Use SQS Batching (Architecture A) ✅

```python
# Simple, reliable, no Redis needed!

event_source = event_sources.SqsEventSource(
    queue,
    batch_size=10,  # SQS batches 10 messages
    max_batching_window=cdk.Duration.seconds(5)
)

def lambda_handler(event, context):
    # Receive 10 messages from SQS
    records = [json.loads(r['body']) for r in event['Records']]
    
    # Batch write to database (efficient!)
    cursor.executemany(
        "INSERT INTO users VALUES (%s, %s)",
        [(r['user_id'], r['data']) for r in records]
    )
```

---

## 3. Where to Configure SQS Batch Size

### Option 1: AWS CDK (Python)

```python
from aws_cdk import (
    aws_lambda as lambda_,
    aws_sqs as sqs,
    aws_lambda_event_sources as event_sources,
    Duration
)

# Create Lambda
my_lambda = lambda_.Function(
    self, "MyLambda",
    runtime=lambda_.Runtime.PYTHON_3_11,
    handler="index.handler",
    code=lambda_.Code.from_asset("lambda")
)

# Create SQS Queue
my_queue = sqs.Queue(
    self, "MyQueue",
    visibility_timeout=Duration.seconds(960)
)

# Configure Event Source Mapping (THIS IS WHERE YOU SET BATCH SIZE)
my_lambda.add_event_source(
    event_sources.SqsEventSource(
        my_queue,
        batch_size=10,                              # ← Batch size
        max_batching_window=Duration.seconds(5),    # ← Wait time
        report_batch_item_failures=True             # ← Partial failures
    )
)
```

### Option 2: AWS Console (UI)

```
1. Go to AWS Lambda Console
2. Select your Lambda function
3. Click "Configuration" tab
4. Click "Triggers" section
5. Click "Add trigger"
6. Select "SQS"
7. Configure:
   - SQS queue: [Select your queue]
   - Batch size: 10                    ← Set here
   - Batch window: 5 seconds           ← Set here
   - Report batch item failures: Yes
8. Click "Add"
```

### Option 3: Terraform

```hcl
# Lambda function
resource "aws_lambda_function" "my_lambda" {
  function_name = "my-function"
  runtime       = "python3.11"
  handler       = "index.handler"
  timeout       = 900
}

# SQS Queue
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.my_queue.arn
  function_name    = aws_lambda_function.my_lambda.arn
  
  batch_size                         = 10    # ← Batch size
  maximum_batching_window_in_seconds = 5     # ← Wait time
  
  function_response_types = ["ReportBatchItemFailures"]
  
  scaling_config {
    maximum_concurrency = 100
  }
}
```

### Option 4: AWS CLI

```bash
aws lambda create-event-source-mapping \
  --function-name my-function \
  --event-source-arn arn:aws:sqs:us-east-1:123456789012:my-queue \
  --batch-size 10 \
  --maximum-batching-window-in-seconds 5 \
  --function-response-types ReportBatchItemFailures
```

### Option 5: CloudFormation

```yaml
Resources:
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: my-function
      Runtime: python3.11
      Handler: index.handler
      Timeout: 900

  MySQSQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: my-queue
      VisibilityTimeout: 960

  LambdaEventSourceMapping:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      FunctionName: !Ref MyLambdaFunction
      EventSourceArn: !GetAtt MySQSQueue.Arn
      BatchSize: 10                          # ← Batch size
      MaximumBatchingWindowInSeconds: 5      # ← Wait time
      FunctionResponseTypes:
        - ReportBatchItemFailures
      ScalingConfig:
        MaximumConcurrency: 100
```

## Summary

1. ✅ **SQS Visibility**: SQS automatically manages visibility using a timer. Sets invisible when delivered, makes visible again after timeout expires.
2. ✅ **Redis Batching**: Architecture B is for ADVANCED use cases only. Standard flow (Architecture A) is: App → SQS → Lambda → Database (no Redis needed).
3. ✅ **Batch Size Config**: Set in the **Event Source Mapping** (not in SQS queue or Lambda itself). This is the connector between SQS and Lambda.
    

# How does SQS manage message's visibility with lambda

## How SQS Knows Success vs Failure
### The Secret: Receipt Handle & Delete Message API
```
┌─────────────────────────────────────────────────────────────┐
│ SQS Message Delivery Lifecycle                              │
└─────────────────────────────────────────────────────────────┘

Step 1: Lambda polls SQS (or SQS triggers Lambda)
        ↓
Step 2: SQS returns message + ReceiptHandle (unique token)
        {
          "MessageId": "msg-123",
          "Body": "{...}",
          "ReceiptHandle": "AQEBxxx...unique-token"  ← Key!
        }
        ↓
Step 3: Message becomes INVISIBLE (visibility timeout starts)
        ↓
Step 4a: SUCCESS PATH
        Lambda processes successfully
        → Lambda calls DeleteMessage(ReceiptHandle)
        → SQS receives delete request
        → SQS permanently removes message
        → DONE! ✅
        
Step 4b: FAILURE PATH  
        Lambda crashes/times out/throws exception
        → Lambda does NOT call DeleteMessage
        → Visibility timeout expires
        → SQS makes message VISIBLE again
        → Ready for retry ⚠️
```

## Detailed Flow

### 1. SQS Delivers Message with Receipt Handle
```python
# What SQS actually sends to Lambda
{
  "Records": [
    {
      "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
      "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",  # ← Unique token
      "body": "{\"user_id\": 123, \"data\": \"new_data\"}",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      }
    }
  ]
}
```

### 2. Lambda Runtime Manages Deletion (Automatic)
```python
# AWS Lambda Runtime (hidden from you)

def lambda_runtime_wrapper(event, context, user_handler):
    """
    This is what AWS actually runs (simplified)
    You don't see this code - it's built into Lambda service
    """
    
    successful_messages = []
    failed_messages = []
    
    try:
        # Call your handler function
        result = user_handler(event, context)
        
        # If no exception and no batch failures reported
        if result is None or 'batchItemFailures' not in result:
            # SUCCESS! Delete all messages
            for record in event['Records']:
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=record['receiptHandle']  # ← Key!
                )
                successful_messages.append(record['messageId'])
        else:
            # Partial batch failure
            failed_ids = {f['itemIdentifier'] for f in result['batchItemFailures']}
            
            for record in event['Records']:
                if record['messageId'] in failed_ids:
                    # DON'T delete - let it retry
                    failed_messages.append(record['messageId'])
                else:
                    # Delete successful ones
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=record['receiptHandle']
                    )
                    successful_messages.append(record['messageId'])
    
    except Exception as e:
        # FAILURE! Don't delete ANY messages
        # Let visibility timeout expire and retry all
        failed_messages = [r['messageId'] for r in event['Records']]
        raise
    
    return {
        'successful': successful_messages,
        'failed': failed_messages
    }
```

### 3. Your Lambda Handler (What You Write)
```python
# Your code - Lambda runtime wraps this
def lambda_handler(event, context):
    """
    You just write business logic
    Lambda runtime handles SQS message deletion automatically
    """
    
    for record in event['Records']:
        message = json.loads(record['body'])
        
        # Process message
        write_to_database(message)
        
        # That's it! No need to manually delete
        # If this succeeds, Lambda runtime deletes the message
        # If this throws exception, Lambda runtime does NOT delete

# Example with partial batch failure
def lambda_handler(event, context):
    """
    Report which specific messages failed
    """
    
    failed_items = []
    
    for record in event['Records']:
        try:
            message = json.loads(record['body'])
            write_to_database(message)
            # Success - will be deleted
            
        except Exception as e:
            # Failure - mark for retry
            print(f"Failed to process {record['messageId']}: {e}")
            failed_items.append({
                'itemIdentifier': record['messageId']
            })
    
    # Return failed message IDs
    # Lambda runtime will:
    # - Delete successful messages
    # - NOT delete failed messages (they'll retry)
    if failed_items:
        return {
            'batchItemFailures': failed_items
        }
```

## Behind the Scenes: AWS APIs

### What Lambda Runtime Actually Calls
```python
import boto3

sqs = boto3.client('sqs')

# When Lambda receives messages from SQS
response = sqs.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/123456789012/my-queue',
    MaxNumberOfMessages=10,
    VisibilityTimeout=900,  # Makes messages invisible for 15 min
    WaitTimeSeconds=20      # Long polling
)

# Response looks like:
# {
#   'Messages': [
#     {
#       'MessageId': 'msg-123',
#       'ReceiptHandle': 'AQEBxxx...unique-token',  ← Used for deletion
#       'Body': '{"user_id": 123}',
#       'Attributes': {...}
#     }
#   ]
# }

# On SUCCESS - Lambda runtime calls this:
for message in response['Messages']:
    sqs.delete_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/123456789012/my-queue',
        ReceiptHandle=message['ReceiptHandle']  # ← Proves we have this message
    )
    # SQS receives delete request and permanently removes message

# On FAILURE - Lambda runtime does NOT call delete_message
# Visibility timeout expires, message becomes visible again
```

## Key Concepts

### 1. Receipt Handle = Proof of Delivery
```python
# Receipt Handle is like a "claim ticket"

# Analogy: Dry Cleaning
# 1. You drop off clothes → Get claim ticket (ReceiptHandle)
# 2. Clothes invisible to others (VisibilityTimeout)
# 3. You return with ticket → Get clothes (DeleteMessage)
# 4. If you lose ticket (timeout) → Clothes available again

# SQS Receipt Handle
receipt_handle = "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a..."

# Only this specific receipt handle can delete this message delivery
# Same message can be delivered multiple times with different receipt handles
```

### 2. Message Lifecycle States
```python
# Message has internal state machine in SQS

class MessageState:
    AVAILABLE = "visible"      # Can be received by consumers
    IN_FLIGHT = "invisible"    # Being processed (visibility timeout active)
    DELETED = "deleted"        # Permanently removed
    
# State transitions:
# AVAILABLE → (receive_message) → IN_FLIGHT
# IN_FLIGHT → (delete_message) → DELETED  ✅ Success
# IN_FLIGHT → (timeout) → AVAILABLE       ⚠️ Retry
```

### 3. How SQS Detects Failure
```python
# SQS doesn't actively "detect" failure
# It uses TIMEOUT as the failure signal

# Timeline:
Time 0s:    Message delivered (IN_FLIGHT state)
            Visibility timeout = 900s starts

Time 0-900s: Waiting...
            - If delete_message received → Move to DELETED ✅
            - If nothing received → Keep waiting

Time 900s:  Timeout expires!
            - No delete_message received = FAILURE
            - Move to AVAILABLE state (retry)

# SQS logic (pseudocode):
def check_message_timeout():
    while True:
        for message in in_flight_messages:
            if current_time() > message.invisible_until:
                if not message.deleted:
                    # No delete received = failure
                    message.state = AVAILABLE
                    message.receive_count += 1
```

## Complete Example: Manual SQS Polling
```python
# If you were manually polling SQS (without Lambda event source)
import boto3
import time

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'

while True:
    # 1. Receive messages
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=900,  # 15 min invisible
        WaitTimeSeconds=20
    )
    
    if 'Messages' not in response:
        continue
    
    for message in response['Messages']:
        message_id = message['MessageId']
        receipt_handle = message['ReceiptHandle']  # ← Important!
        body = message['Body']
        
        try:
            # 2. Process message
            process_message(json.loads(body))
            
            # 3. SUCCESS - Tell SQS to delete
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle  # ← Proves we processed this delivery
            )
            print(f"✅ Deleted message {message_id}")
            
        except Exception as e:
            # 4. FAILURE - Do NOT delete
            # Message will become visible again after 900s
            print(f"❌ Failed {message_id}: {e}")
            # No delete_message call = automatic retry
```

## Visibility Timeout Extension
```python
# If processing takes longer than expected, you can extend visibility

def lambda_handler(event, context):
    for record in event['Records']:
        receipt_handle = record['receiptHandle']
        
        # Start processing
        long_running_task()
        
        # Oh no! This will take longer than visibility timeout
        # Extend visibility to prevent duplicate processing
        sqs.change_message_visibility(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle,
            VisibilityTimeout=1800  # Extend to 30 minutes
        )
        
        continue_long_task()
        
        # Lambda runtime will still delete on success
```

## Monitoring: How to See What's Happening
```python
# CloudWatch metrics to monitor

# 1. NumberOfMessagesReceived
# How many times messages were delivered (includes retries)

# 2. NumberOfMessagesDeleted  
# How many delete_message calls succeeded

# 3. ApproximateNumberOfMessagesVisible
# Messages available for processing

# 4. ApproximateNumberOfMessagesNotVisible
# Messages currently being processed (in-flight)

# 5. ApproximateAgeOfOldestMessage
# How long oldest message has been waiting

# If messages not being deleted:
# NumberOfMessagesReceived > NumberOfMessagesDeleted
# → Lambda is failing to process messages
```

## Summary

**How SQS knows SUCCESS:**
- Lambda runtime calls `delete_message(ReceiptHandle)`
- SQS receives delete request → permanently removes message

**How SQS knows FAILURE:**

- Lambda does NOT call `delete_message`
- Visibility timeout expires → SQS automatically makes message visible again
- SQS doesn't need explicit "failure" signal - timeout = failure

**Key takeaway:** SQS uses **absence of deletion** + **timeout** to detect failure, not active monitoring! 🎯

# Note


# Reference

