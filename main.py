import requests
import time
import urllib3
import numpy as np
import matplotlib.pyplot as plt
import threading
import RequiredPackages

def main():

    # Insitall Requirements
    RequiredPackages.install_requirements()

    url = input("Enter URL => ")

    request_count = int(input("Enter number of request => "))

    x_values = []  # List to store latency values
    colors = ['b']

    fig, ax = plt.subplots(figsize=(12, 6))


    threads = []
    for i in range(request_count+1):
        thread = threading.Thread(target=send_request, args=(url,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        update_plot()


plt.show()



def update_plot():
    global x_values

    ax.cla()

    ax.plot(range(len(x_values)), x_values, label=f"Latency", color=colors[0])
    plt.xlabel("Count of requests")
    plt.ylabel("Latency (ms)")
    plt.title("latency of urls")
    plt.grid(True)

    # Set axis limits
    ax.set_xlim(0, len(x_values))
    ax.set_ylim(min(x_values), max(x_values))

    # Update title
    ax.set_title(f"Website Latency (Requests: {len(x_values)})")

    # Pause for smooth animation
    plt.pause(0.01)


def measure_throughput(url, duration=10, repetitions=10):
    http = urllib3.PoolManager()
    total_bytes = 0
    start_time = time.time()
    for _ in range(repetitions):
        response = http.request('GET', url)
        total_bytes += len(response.data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    throughput = (total_bytes / elapsed_time) / 1024
    return throughput


def measure_percentiles(url, repetitions=100):
    latencies = []
    for _ in range(repetitions):
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        latencies.append(latency)
    percentiles = np.percentile(latencies, [50, 90, 99])
    return {"50th": percentiles[0], "90th": percentiles[1], "99th": percentiles[2]}


url1 = "https://www.uma.ac.ir"
url2 = "https://www.google.com"

# ============================================================================ #
# duration = 10
# repetitions = 10

# throughput1 = measure_throughput(url1, duration, repetitions)
# throughput2 = measure_throughput(url2, duration, repetitions)

# x_labels = [url1, url2]
# y_values = [throughput1, throughput2]

# plt.figure(figsize=(10, 6))
# plt.bar(x_labels, y_values, color=['b', 'g'])
# plt.xlabel("URL")
# plt.ylabel("Throughput (KB/s)")
# plt.title("Throughput of urls")
# plt.grid(True)

# plt.show()

# ============================================================================ #
# repetitions = 100

# percentiles1 = measure_percentiles(url1, repetitions)
# percentiles2 = measure_percentiles(url2, repetitions)

# percentiles_names = ["50th", "90th", "99th"]
# url_labels = [url1, url2]

# x_values = []
# for percentile_name in percentiles_names:
#   x_values.append([percentiles1[percentile_name], percentiles2[percentile_name]])

# colors = ['b', 'g']

# plt.figure(figsize=(12, 6))
# for i, (values, color) in enumerate(zip(x_values, colors)):
#   plt.plot(url_labels, values, label=f"{percentiles_names[i]} Percentile", color=color)
# plt.xlabel("URL")
# plt.ylabel("Latency (ms)")
# plt.title("Percentiles of urls")
# plt.grid(True)
# plt.legend()

# plt.show()

# ============================================================================ #
latency_list = []
counter = 1


def send_request(url1):
    global counter
    start_time = time.time()
    try:
        counter = counter+1
        response = requests.get(url)
        elapsed_time = time.time() - start_time
        latency_list.append(elapsed_time)
        x_values.append(elapsed_time)
    except requests.exceptions.RequestException as e:
        print(f"Request {counter} to {url} failed: {e}")


if __name__ == "__main__":
    main()
