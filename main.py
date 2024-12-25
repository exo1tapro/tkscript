import numpy as np
import time
from numba import cuda

# Constants
HASHES_PER_BATCH = 1000000  # Number of hashes per batch
TOKENS_FILE = "tokens.txt"

# GPU Kernel for SHA-256 (simplified dummy hash function for demonstration)
@cuda.jit
def generate_hashes(starting_numbers, results):
    idx = cuda.grid(1)
    if idx < starting_numbers.size:
        seed = starting_numbers[idx]
        # Simulate hashing by creating a dummy hash result
        hash_value = 0
        for i in range(10):
            hash_value += (seed * 31) % 1000000007
        results[idx] = hash_value

def gpu_hashing(start_numbers):
    # Allocate memory for results
    results = np.zeros_like(start_numbers, dtype=np.int64)

    # Define GPU grid and block dimensions
    threads_per_block = 256
    blocks_per_grid = (start_numbers.size + (threads_per_block - 1)) // threads_per_block

    # Launch the GPU kernel
    generate_hashes[blocks_per_grid, threads_per_block](start_numbers, results)

    # Wait for GPU to finish
    cuda.synchronize()
    return results

def main():
    total_mined = 0
    start_time = time.time()

    with open(TOKENS_FILE, "a") as f:
        while True:
            # Generate random starting numbers
            start_numbers = np.random.randint(1, 1000000, size=HASHES_PER_BATCH, dtype=np.int64)

            # Generate hashes using the GPU
            hashes = gpu_hashing(start_numbers)

            # Write results to the file
            for number, hash_value in zip(start_numbers, hashes):
                f.write(f"{number} | {hash_value}\n")

            # Update statistics
            total_mined += HASHES_PER_BATCH
            elapsed_time = time.time() - start_time
            hashrate = total_mined / elapsed_time

            # Print live statistics
            print(f"\rMined: {total_mined:,} TKS  |  Hashrate: {hashrate:,.2f} Hashes/s", end="")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMining stopped.")
