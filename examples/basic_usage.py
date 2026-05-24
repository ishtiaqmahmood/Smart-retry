from smart_retry import retry
import random

# 1. Simple retry on any exception
@retry(max_attempts=3)
def unstable_network_call():
    print("Attempting network call...")
    if random.random() < 0.7:
        raise ConnectionError("Network is unstable!")
    return "Data fetched successfully!"

# 2. Retry with specific configuration and hooks
def on_retry(error, attempt):
    print(f"  [Hook] Attempt {attempt} failed: {error}. Retrying...")

@retry(
    max_attempts=5,
    exceptions=(ValueError,),
    on_retry=on_retry
)
def processing_task(data):
    if not data:
        raise ValueError("Data cannot be empty")
    return f"Processed: {data}"

if __name__ == "__main__":
    print("--- Example 1: Unstable Network Call ---")
    try:
        result = unstable_network_call()
        print(result)
    except Exception as e:
        print(f"Final failure: {e}")

    print("\n--- Example 2: Targeted Retry ---")
    try:
        # This will trigger retries because it raises ValueError
        processing_task("")
    except Exception as e:
        print(f"Final failure: {e}")
