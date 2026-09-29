import asyncio
from time import perf_counter

import httpx2

URLS = [
    "https://www.python.org",
    "https://github.com",
    "https://www.wikipedia.org",
    "https://www.cloudflare.com",
    "https://www.bilibili.com/",
]


async def check_url(client: httpx2.AsyncClient, url: str):
    start = perf_counter()

    try:
        response = await client.get(url)
        status = response.status_code
    except httpx2.TimeoutException:
        status = "TIMEOUT"

    elapsed = perf_counter() - start

    return url, status, elapsed


async def run_checks():
    start = perf_counter()

    async with httpx2.AsyncClient(timeout=3.0) as client:

        results = await asyncio.gather(*(check_url(client, url) for url in URLS))

    elapsed = perf_counter() - start

    return results, elapsed


async def main():
    results, elapsed = await run_checks()

    print(f"{'URL':<32} {'STATUS':>6} {'LATENCY':>10}")
    print("-" * 52)

    for url, status, latency in results:
        print(f"{url:32} {status:>6} {latency:>9.4f} s")

    print(f"Total: {elapsed:.4f} s")


if __name__ == "__main__":
    asyncio.run(main())
