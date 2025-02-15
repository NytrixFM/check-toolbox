import psutil
import cpuinfo
import GPUtil
import timeit
import numpy as np
import shutil
import time
import os
import matplotlib.pyplot as plt

def get_system_info():
    print("=== Informations Système ===")
    print(f"Processeur : {cpuinfo.get_cpu_info()['brand_raw']}")
    print(f"Nombre de cœurs : {psutil.cpu_count(logical=False)} physiques, {psutil.cpu_count(logical=True)} logiques")
    print(f"Mémoire RAM totale : {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
    print(f"Disque : {shutil.disk_usage('/') .total // (1024**3)} GB")
    
    gpus = GPUtil.getGPUs()
    if gpus:
        for gpu in gpus:
            print(f"Carte Graphique : {gpu.name}, {gpu.memoryTotal} MB VRAM")
    else:
        print("Aucune carte graphique détectée.")
    print("===================================\n")

def benchmark_cpu():
    print("[TEST] Benchmark CPU en cours...")
    time_taken = timeit.timeit(stmt="sum(range(10**6))", number=100)
    score = max(0, 100 - (time_taken * 10))
    print(f"Score CPU : {round(score, 2)}/100\n")
    return score

def benchmark_ram():
    print("[TEST] Benchmark RAM en cours...")
    start_time = time.time()
    array = np.random.rand(5000, 5000)
    _ = np.dot(array, array)
    end_time = time.time()
    score = max(0, 100 - ((end_time - start_time) * 20))
    print(f"Score RAM : {round(score, 2)}/100\n")
    return score

def benchmark_disk():
    print("[TEST] Benchmark Disque en cours...")
    filename = "test_benchmark_disk.tmp"
    data = os.urandom(50 * 1024 * 1024)
    
    start_time = time.time()
    with open(filename, "wb") as f:
        f.write(data)
    end_time = time.time()
    write_time = end_time - start_time
    
    start_time = time.time()
    with open(filename, "rb") as f:
        _ = f.read()
    end_time = time.time()
    read_time = end_time - start_time
    
    os.remove(filename)
    
    score = max(0, 100 - ((write_time + read_time) * 50))
    print(f"Écriture : {round(write_time, 4)} sec, Lecture : {round(read_time, 4)} sec (plus bas est mieux)")
    print(f"Score Disque : {round(score, 2)}/100\n")
    return score

def benchmark_gpu():
    print("[TEST] Benchmark GPU en cours...")
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("Aucune carte graphique détectée. Test annulé.\n")
        return 0
    
    start_time = time.time()
    x = np.random.rand(1000, 1000)
    for _ in range(100):
        _ = np.linalg.inv(x)
    end_time = time.time()
    score = max(0, 100 - ((end_time - start_time) * 20))
    print(f"Score GPU : {round(score, 2)}/100\n")
    return score

def generate_benchmark_image(scores):
    labels = ["CPU", "RAM", "Disque", "GPU"]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, scores, color=['red', 'blue', 'green', 'purple'])
    plt.ylim(0, 100)
    plt.xlabel("Composants")
    plt.ylabel("Score")
    plt.title("Résultats du Benchmark")
    plt.savefig("benchmark_result.png")
    print("Image du benchmark générée : benchmark_result.png\n")

def run_benchmarks():
    get_system_info()
    cpu_score = benchmark_cpu()
    ram_score = benchmark_ram()
    disk_score = benchmark_disk()
    gpu_score = benchmark_gpu()
    scores = [cpu_score, ram_score, disk_score, gpu_score]
    generate_benchmark_image(scores)
    print("=== Benchmark terminé ===")

if __name__ == "__main__":
    run_benchmarks()
