import json
import os
from confluent_kafka import Consumer, KafkaException
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider


def iam_token(_):
    token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(
        os.environ["AWS_REGION"]
    )
    return token, expiry_ms / 1000


consumer = Consumer({
    "bootstrap.servers": os.environ["MSK_BOOTSTRAP"],
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "OAUTHBEARER",
    "oauth_cb": iam_token,
    "group.id": "orders-workers",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})
consumer.subscribe(["orders"])

try:
    while True:
        message = consumer.poll(1)
        if message is None:
            continue
        if message.error():
            raise KafkaException(message.error())
        order = json.loads(message.value().decode("utf-8"))
        print(
            f"Process {order} from {message.topic()} "
            f"/ partition {message.partition()} / offset {message.offset()}"
        )
        # Replace print with successful business work before committing.
        consumer.commit(message=message, asynchronous=False)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
