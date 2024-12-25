import hashlib
import time
import random
import sys
import signal
from itertools import count
import concurrent.futures
import os
import cupy as cp
import numpy as np

# File for storing the mined hashes
tokens_file = "tokens.txt"

def signal_handler(signal, frame):
    print("\n\nMining stopped. Don't forget to claim your TKS using /claim in discord.gg/kvm.\n")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# CPU-based hash generation
def generate_hash_cpu(starting_number):
    rand_seed = random.random()
    hash_input = f"{time.time()}_{rand_seed}_{starting_number}".encode('utf-8')
    hash_output = hashlib.sha256(hash_input).hexdigest()
    return hash_output, starting_number

# GPU-based hash generation using CuPy for parallelism
def generate_hash_gpu(starting_number):
    rand_seed = random.random()
    hash_input = f"{time.time()}_{rand_seed}_{starting_number}".encode('utf-8')

    # Convert data to a GPU-compatible format (CuPy array)
    hash_input_gpu = cp.frombuffer(hash_input, dtype=cp.uint8)

    # Perform parallel computation using GPU for large datasets (example use case)
    # Here we're just using the GPU to store and process data, but the actual hash function still runs on CPU
    # If you need SHA-256 on GPU, you may have to use a different library or implement a custom CUDA kernel
    hash_output = hashlib.sha256(hash_input).hexdigest()  # CPU-based for now
    return hash_output, starting_number

# Show mining startup screen
def start_screen():
    print("")
    print("  _  ____     ____  __       _ _____   _____     _")
    print(" | |/ /\ \   / /  \/  |     (_)___  | |_   _|__ | | _____ _ __  ___ ")
    print(" | ' /  \ \ / /| |\/| |_____| |  / /    | |/ _ \| |/ / _ \ '_ \/ __| ")
    print(" | . \   \ V / | |  | |_____| | / /     | | (_) |   <  __/ | | \__ \ ")
    print(" |_|\_\   \_/  |_|  |_|     |_|/_/      |_|\___/|_|\_\___|_| |_|___/ ")
    print(" Free-Miner | Upgraded by evlolptero (The Best so far!)")
    print("")
    print(" [Y/N] Start Mining\n")
    user_input = input(" > ").strip().lower()
    if user_input == "y":
        return True
    else:
        print("Exiting program. To mine tokens later, run the script again.")
        sys.exit(0)

# Main mining loop
def main():
    if start_screen():
        print("\nMining started...\n")
        with open(tokens_file, 'a') as f:
            starting_number = random.randint(500000, 1000000)
            total_mined = 0
            start_time = time.time()

            # Use both CPU and GPU for parallel mining
            with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                try:
                    futures = []
                    # Submit GPU tasks for 50% of the total tasks
                    for i in range(50000):
                        futures.append(executor.submit(generate_hash_gpu, starting_number + i))

                    # Submit CPU tasks for the remaining 50%
                    for i in range(50000, 100000):
                        futures.append(executor.submit(generate_hash_cpu, starting_number + i))
                    
                    for future in concurrent.futures.as_completed(futures):
                        hash_output, starting_number = future.result()
                        f.write(f"{starting_number} | {hash_output}\n")
                        total_mined += 1

                        if total_mined % 100000 == 0:  # Update every 100k hashes
                            elapsed_time = time.time() - start_time
                            hashrate = total_mined / elapsed_time
                            print(f"\rMined: {total_mined:,} TKS  |  Hashrate: {hashrate:,.2f} Hashes/s", end="")
                
                except KeyboardInterrupt:
                    pass

if __name__ == "__main__":
    main()
