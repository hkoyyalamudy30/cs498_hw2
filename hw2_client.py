import time
import uuid
import statistics
import requests

US_BASE = "http://34.10.21.241:8080"   
EU_BASE = "http://34.53.192.102:8080"  

N_REQUESTS = 10
LOOPS = 100


def measure_register_latency(base_url):
    times = []
    for _ in range(N_REQUESTS):
        username = "lat_" + uuid.uuid4().hex
        start = time.perf_counter()
        requests.post(f"{base_url}/register", json={"username": username})
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return statistics.mean(times)


def measure_list_latency(base_url):
    times = []
    for _ in range(N_REQUESTS):
        start = time.perf_counter()
        requests.get(f"{base_url}/list")
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return statistics.mean(times)


def eventual_consistency_test():
    misses = 0
    for _ in range(LOOPS):
        username = "ec_" + uuid.uuid4().hex
        requests.post(f"{US_BASE}/register", json={"username": username})
        response = requests.get(f"{EU_BASE}/list").json()
        if username not in response.get("users", []):
            misses += 1
    return misses


if __name__ == "__main__":
    print("Measuring Latency...\n")

    us_reg = measure_register_latency(US_BASE)
    eu_reg = measure_register_latency(EU_BASE)
    us_list = measure_list_latency(US_BASE)
    eu_list = measure_list_latency(EU_BASE)

    print("Average Latencies (ms)")
    print(f"US /register: {us_reg:.2f}")
    print(f"EU /register: {eu_reg:.2f}")
    print(f"US /list: {us_list:.2f}")
    print(f"EU /list: {eu_list:.2f}")

    print("\nTesting Eventual Consistency...\n")
    misses = eventual_consistency_test()

    print(f"Misses (not found immediately): {misses} out of {LOOPS}")
