import asyncio
import random
from smart_retry import retry

# 1. Async retry with exponential backoff
@retry(max_attempts=4)
async def async_fetch_data():
    print("Async attempting to fetch data...")
    await asyncio.sleep(0.1)
    if random.random() < 0.6:
        raise RuntimeError("Database connection failed")
    return {"status": "ok", "data": [1, 2, 3]}

async def main():
    print("--- Async Example ---")
    try:
        result = await async_fetch_data()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Async final failure: {e}")

if __name__ == "__main__":
    asyncio.run(main())
