from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json

app = FastAPI(root_path="/api/orders")

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int


@app.get("/")
def health():
    return {"status": "order service running"}


@app.post("/create")
def create_order(order: Order):

    order_data = order.dict()

    # Push order event to Redis queue
    redis_client.rpush("orders_queue", json.dumps(order_data))

    return {
        "message": "order created",
        "order": order_data
    }