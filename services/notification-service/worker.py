import redis
import json
import time

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

print("Notification service started...")

while True:

    order = redis_client.blpop("orders_queue")

    if order:
        data = json.loads(order[1])

        print("New order received:")
        print(data)

        # simulate sending notification
        print(f"Sending notification for user {data['user_id']}")

    time.sleep(1)