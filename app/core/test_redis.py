from app.core.redis import redis_client


redis_client.set(
    "test",
    "hello redis",
)

value = redis_client.get("test")

print(value)