from time import perf_counter

import httpx2

from config import TIMEOUT, URLS


def check_url(client: httpx2.Client, url: str):
    start = perf_counter()

    try:
        response = client.get(url)
        status = response.status_code

    except httpx2.TimeoutException:
        status = "TIMEOUT"

    except httpx2.RequestError:
        status = "ERROR"

    elapsed = perf_counter() - start

    return url, status, elapsed


def run_checks():
    start = perf_counter()

    with httpx2.Client(timeout=TIMEOUT) as client:

        results = []

        for url in URLS:
            results.append(check_url(client, url))

    elapsed = perf_counter() - start

    return results, elapsed


def main():
    results, elapsed = run_checks()

    print(f"{'URL':<32} {'STATUS':>6} {'LATENCY':>10}")
    print("-" * 52)

    for url, status, latency in results:
        print(f"{url:32} {status:>6} {latency:>9.4f} s")

    print(f"\nTotal: {elapsed:.4f} s")


if __name__ == "__main__":
    main()
