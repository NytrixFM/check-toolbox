import psutil
import cpuinfo
import GPUtil
import timeit
import numpy as np
import shutil
import time
import os

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

def benchmark_ram():
    print("[TEST] Benchmark RAM en cours...")
    start_time = time.time()
    array = np.random.rand(5000, 5000)  # Création d'un tableau massif
    _ = np.dot(array, array)  # Calcul intensif sur la RAM
    end_time = time.time()
    score = max(0, 100 - ((end_time - start_time) * 20))
    print(f"Score RAM : {round(score, 2)}/100\n")

def benchmark_disk():
    print("[TEST] Benchmark Disque en cours...")
    filename = "test_benchmark_disk.tmp"
    data = os.urandom(50 * 1024 * 1024)  # 50 MB
    
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

def benchmark_gpu():
    print("[TEST] Benchmark GPU en cours...")
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("Aucune carte graphique détectée. Test annulé.\n")
        return
    
    start_time = time.time()
    x = np.random.rand(1000, 1000)
    for _ in range(100):
        _ = np.linalg.inv(x)  # Inversion de matrice, stress sur GPU si pris en charge
    end_time = time.time()
    score = max(0, 100 - ((end_time - start_time) * 20))
    print(f"Score GPU : {round(score, 2)}/100\n")

def run_benchmarks():
    get_system_info()
    benchmark_cpu()
    benchmark_ram()
    benchmark_disk()
    benchmark_gpu()
    print("=== Benchmark terminé ===")

if __name__ == "__main__":
    run_benchmarks()
