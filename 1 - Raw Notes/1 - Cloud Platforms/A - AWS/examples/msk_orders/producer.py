import json
import os
from confluent_kafka import Producer
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider


def iam_token(_):
    token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(
        os.environ["AWS_REGION"]
    )
    return token, expiry_ms / 1000


def delivered(error, message):
    if error is not None:
        raise RuntimeError(f"Delivery failed: {error}")
    print(
        f"Sent: {message.topic()} / partition {message.partition()} "
        f"/ offset {message.offset()}"
    )


producer = Producer({
    "bootstrap.servers": os.environ["MSK_BOOTSTRAP"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "OAUTHBEARER",
    "oauth_cb": iam_token,
    "acks": "all",
    "partitioner": "murmur2_random",
})

order = {"order_id": "order-1001", "customer_id": "customer-42"}
producer.produce(
    topic="orders",
    key=order["customer_id"],
    value=json.dumps(order),
    on_delivery=delivered,
)
if producer.flush(10):
    raise TimeoutError("Delivery is unconfirmed; the outcome is unknown.")
