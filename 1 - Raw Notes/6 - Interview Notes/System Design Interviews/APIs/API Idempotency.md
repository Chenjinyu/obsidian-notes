Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-apis
Tags: [[API]] [[interview]]

# Content

A client may experience failures, such as timeouts, server crashes, or network interruptions, while trying to pay for a service. If the client retries the payment and is double-charged, it could be due to any of the following scenarios:

There are 3 potential scenarios when a payment request is made:
1. The initial handshake between the client and server could fail, preventing the payment request from being sent. In this case, the client can retry the request and hope for success without risking double charging.
2. The server receives the payment request but has not yet begun processing it when a failure occurs. The server sends an error code back to the client, and there is no change to the client's account.
3. The server receives the payment request and successfully processes it or is processing it when a failure occurs. However, the failure happens before the server can return the `200` status code to the client. In this scenario, the client may not realize that their account has already been charged and may initiate another payment, leading to double charging.

### Code Example
Server:
```python
from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
import sqlite3
import time
from typing import Optional

DB_PATH = "payments.db"
app = FastAPI(title="Payment Service (Idempotent)")

# ---------- DB helpers ----------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        user_id TEXT PRIMARY KEY,
        balance_cents INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        idempotency_key TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL,          -- RECEIVED | PROCESSING | SUCCESS | FAILED
        charged INTEGER NOT NULL,      -- 0/1
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL,
        error_code TEXT,
        error_message TEXT
    )
    """)

    # Seed one account if missing
    cur.execute("SELECT user_id FROM accounts WHERE user_id = ?", ("u1",))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO accounts(user_id, balance_cents) VALUES(?, ?)", ("u1", 100_00))  # $100.00

    conn.commit()
    conn.close()

@app.on_event("startup")
def _startup():
    init_db()

# ---------- Models ----------
class PaymentRequest(BaseModel):
    user_id: str = "u1"
    amount_cents: int

class PaymentResponse(BaseModel):
    payment_id: int
    status: str
    charged: bool
    balance_cents: int
    idempotency_key: str
    note: Optional[str] = None

# ---------- Core payment logic ----------
def get_balance(conn, user_id: str) -> int:
    cur = conn.cursor()
    cur.execute("SELECT balance_cents FROM accounts WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Account not found")
    return int(row["balance_cents"])

def deduct_balance(conn, user_id: str, amount_cents: int):
    cur = conn.cursor()
    bal = get_balance(conn, user_id)
    if bal < amount_cents:
        raise HTTPException(status_code=409, detail="Insufficient funds")
    cur.execute("UPDATE accounts SET balance_cents = balance_cents - ? WHERE user_id = ?", (amount_cents, user_id))

@app.post("/payments", response_model=PaymentResponse)
def create_payment(
    req: PaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    fail_mode: str = Query(default="none", description="none | before_process | timeout_after_charge")
):
    """
    fail_mode:
      - none: normal success
      - before_process: scenario #2 (server got request but fails before charging; returns error; no account change)
      - timeout_after_charge: scenario #3 (server charges, but client times out before receiving 200)
    """
    now = int(time.time())

    conn = get_conn()
    cur = conn.cursor()

    try:
        # Use an IMMEDIATE txn to avoid double-charging under concurrency
        cur.execute("BEGIN IMMEDIATE")

        # 1) If this idempotency key already exists, return the same result (idempotent behavior)
        cur.execute("SELECT * FROM payments WHERE idempotency_key = ?", (idempotency_key,))
        existing = cur.fetchone()
        if existing:
            balance = get_balance(conn, existing["user_id"])
            conn.commit()
            return PaymentResponse(
                payment_id=int(existing["id"]),
                status=str(existing["status"]),
                charged=bool(existing["charged"]),
                balance_cents=balance,
                idempotency_key=idempotency_key,
                note="Idempotent replay: returning existing payment result"
            )

        # 2) Create a payment record in RECEIVED state immediately
        cur.execute("""
            INSERT INTO payments(user_id, amount_cents, idempotency_key, status, charged, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (req.user_id, req.amount_cents, idempotency_key, "RECEIVED", 0, now, now))
        payment_id = cur.lastrowid

        # Scenario #2: server receives request but fails before processing begins
        if fail_mode == "before_process":
            cur.execute("""
                UPDATE payments
                SET status = ?, updated_at = ?, error_code = ?, error_message = ?
                WHERE id = ?
            """, ("FAILED", int(time.time()), "BEFORE_PROCESS", "Simulated failure before charging", payment_id))
            conn.commit()
            raise HTTPException(status_code=503, detail="Simulated failure before processing (no charge done)")

        # 3) Begin processing
        cur.execute("UPDATE payments SET status = ?, updated_at = ? WHERE id = ?", ("PROCESSING", int(time.time()), payment_id))

        # 4) Charge (deduct balance) exactly once
        deduct_balance(conn, req.user_id, req.amount_cents)

        # 5) Mark payment success
        cur.execute("""
            UPDATE payments
            SET status = ?, charged = ?, updated_at = ?, error_code = NULL, error_message = NULL
            WHERE id = ?
        """, ("SUCCESS", 1, int(time.time()), payment_id))

        conn.commit()

        # Scenario #3: server charged successfully, but client doesn't receive response (timeout)
        # We simulate this by sleeping longer than the client's timeout.
        if fail_mode == "timeout_after_charge":
            time.sleep(10)

        balance = get_balance(conn, req.user_id)
        return PaymentResponse(
            payment_id=payment_id,
            status="SUCCESS",
            charged=True,
            balance_cents=balance,
            idempotency_key=idempotency_key
        )

    except HTTPException:
        # Let FastAPI return the intended error
        raise
    except sqlite3.IntegrityError:
        # Rare race: another request inserted same idempotency key first. Return that result.
        cur.execute("ROLLBACK")
        cur.execute("SELECT * FROM payments WHERE idempotency_key = ?", (idempotency_key,))
        existing = cur.fetchone()
        balance = get_balance(conn, existing["user_id"])
        return PaymentResponse(
            payment_id=int(existing["id"]),
            status=str(existing["status"]),
            charged=bool(existing["charged"]),
            balance_cents=balance,
            idempotency_key=idempotency_key,
            note="Race detected: returning existing payment result"
        )
    finally:
        conn.close()

@app.get("/accounts/{user_id}")
def get_account(user_id: str):
    conn = get_conn()
    try:
        return {"user_id": user_id, "balance_cents": get_balance(conn, user_id)}
    finally:
        conn.close()

```

Client
This client demostrates:
- Scenario #1: handshake/connection failed (safe to retry, server never got it)
- Scenario #2: server returns error before processing (safe to retry)
- #### Scenario #3: server charges but client times out; retry with same idempotency key prevents double charge

```python
import requests
import uuid
import time

BASE_URL = "http://127.0.0.1:8000"

def make_payment(amount_cents: int, fail_mode: str, timeout_seconds: float, max_retries: int = 3):
    idem_key = str(uuid.uuid4()) # <----- here is the key to keep the transaction is idempotency. JC
    print(f"\n=== Make payment: amount={amount_cents} idem_key={idem_key} fail_mode={fail_mode} timeout={timeout_seconds}s ===")

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(
                f"{BASE_URL}/payments",
                headers={"Idempotency-Key": idem_key},
                json={"user_id": "u1", "amount_cents": amount_cents},
                params={"fail_mode": fail_mode},
                timeout=timeout_seconds,
            )
            print(f"Attempt {attempt}: HTTP {resp.status_code}")
            if resp.ok:
                data = resp.json()
                print("Response:", data)
                return data
            else:
                print("Error:", resp.text)
                # For many 5xx errors, we retry with same idempotency key
                if 500 <= resp.status_code < 600:
                    time.sleep(0.5)
                    continue
                return None

        except requests.exceptions.ConnectionError as e:
            # Scenario #1: handshake failed / server unreachable
            print(f"Attempt {attempt}: ConnectionError (handshake/server unreachable): {e}")
            time.sleep(0.5)
            continue

        except requests.exceptions.Timeout as e:
            # Scenario #3: client timed out; server may have charged already
            print(f"Attempt {attempt}: Timeout (unknown outcome): {e}")
            print("Retrying with SAME idempotency key to avoid double charge...")
            time.sleep(0.5)
            continue

    print("Max retries reached.")
    return None

def get_balance():
    r = requests.get(f"{BASE_URL}/accounts/u1", timeout=5)
    return r.json()

if __name__ == "__main__":
    print("Initial balance:", get_balance())

    # Scenario #2: server receives request but fails before charging (503). Safe to retry.
    make_payment(amount_cents=25_00, fail_mode="before_process", timeout_seconds=2, max_retries=3)
    print("Balance after scenario #2 (should be unchanged):", get_balance())

    # Scenario #3: server charges but client times out. Retry should not double charge.
    make_payment(amount_cents=10_00, fail_mode="timeout_after_charge", timeout_seconds=1, max_retries=3)
    print("Balance after scenario #3 (should be charged once):", get_balance())

    # Normal success
    make_payment(amount_cents=5_00, fail_mode="none", timeout_seconds=2, max_retries=2)
    print("Final balance:", get_balance())

```

Overall, the first two scenarios are acceptable, but the last scenario is problematic and could result in unintentional double charging.
**Possible solution**
To address this problem, we need to develop an idempotent payment API. An idempotent API ensures that only the first call generates the expected result and subsequent calls are no-ops.
1. Require clients to generate a unique key in the request header when initiating a request to the payment server.
2. The key is sent to the server along with other payment-related information.
3. The server stores the key and process status.
4. If the client receives a failure, it can safely retry the request with the same key in the header, and the payment server can recognize this as a duplicate request and take appropriate action.

For example, if the previous failure interrupted an ongoing payment processing, the payment server might restore the state and continue processing.
_Non-mutating APIs_, such as `GET`, are generally idempotent.
_Mutating(突变) APIs_, such as `PUT`, update a resource's state. This means that executing the same `PUT` API multiple times updates the resource only once, while subsequent calls overwrite the resource with the same value. Therefore, `PUT` APIs are usually idempotent.
Similarly, the mutating API, `DELETE`, only takes effect during the first call, returning a `200` ( `OK`) status, while subsequent calls return `404` (`Not Found`).
The last mutating API, `POST`, creates a new resource.
However, receiving multiple requests can cause servers to allocate different places for the new resource. Therefore, the `POST` API is usually **not** idempotent.

# Note


# Reference

