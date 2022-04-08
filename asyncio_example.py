import asyncio
import time

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        # time.sleep(1)
        f *= i
    print_hello(name)
    print(f"Task {name}: factorial({number}) = {f}")
    return f

def print_hello(name):
    print("Hello from", name)

async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 10),
        factorial("B", 30),
        factorial("C", 50),
    )
    print(L)

asyncio.run(main())