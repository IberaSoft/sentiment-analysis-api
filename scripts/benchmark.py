"""Benchmark API performance."""
import argparse
import time
import statistics
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def benchmark_endpoint(
    url: str,
    num_requests: int = 100,
    num_threads: int = 10,
    payload: dict = None
):
    """Benchmark an API endpoint."""
    print(f"Benchmarking {url}")
    print(f"Requests: {num_requests}, Threads: {num_threads}")
    
    times = []
    errors = 0
    
    def make_request():
        start = time.time()
        try:
            response = requests.post(url, json=payload, timeout=30)
            elapsed = time.time() - start
            if response.status_code == 200:
                times.append(elapsed * 1000)  # Convert to ms
                return True
            else:
                errors += 1
                return False
        except Exception as e:
            errors += 1
            return False
    
    # Run requests in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [f.result() for f in as_completed(futures)]
    
    if times:
        print(f"\nResults:")
        print(f"Successful requests: {len(times)}")
        print(f"Errors: {errors}")
        print(f"Mean latency: {statistics.mean(times):.2f} ms")
        print(f"Median latency: {statistics.median(times):.2f} ms")
        print(f"P95 latency: {statistics.quantiles(times, n=20)[18]:.2f} ms")
        print(f"P99 latency: {statistics.quantiles(times, n=100)[98]:.2f} ms")
        print(f"Throughput: {len(times) / sum(times) * 1000:.2f} req/s")
    else:
        print("No successful requests!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark API performance")
    parser.add_argument("--url", default="http://localhost:8000/api/v1/predict")
    parser.add_argument("--num-requests", type=int, default=100)
    parser.add_argument("--num-threads", type=int, default=10)
    parser.add_argument("--text", default="This is a test review for benchmarking")
    
    args = parser.parse_args()
    
    payload = {"text": args.text}
    benchmark_endpoint(args.url, args.num_requests, args.num_threads, payload)

