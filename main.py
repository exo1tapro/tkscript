# Under the GPL.
import hashlib
import time
import random
import sys
import signal
from itertools import count

tokens_file = "tokens.txt"

def signal_handler(signal, frame):
    print("\n\nMining stopped. Don't forget to claim your TKS using /claim in discord.gg/kvm.\n")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_hash(starting_number):
    while True:
        rand_seed = random.random()
        hash_input = f"{time.time()}_{rand_seed}_{starting_number}".encode('utf-8')
        hash_output = hashlib.sha256(hash_input).hexdigest()
        yield hash_output, starting_number
        starting_number += random.randint(1, 5)

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

def main():
    if start_screen():
        print("\nMining started...\n")
        with open(tokens_file, 'a') as f:
            starting_number = random.randint(500000, 1000000)
            hash_generator = generate_hash(starting_number)
            total_mined = 0
            start_time = time.time()
            try:
                for _ in count():  # Infinite loop
                    hash_output, starting_number = next(hash_generator)
                    f.write(f"{starting_number} | {hash_output}\n")
                    total_mined += 1

                    if total_mined % 10000 == 0:  # Update every 10k hashes
                        elapsed_time = time.time() - start_time
                        hashrate = total_mined / elapsed_time
                        print(f"\rMined: {total_mined:,} TKS  |  Hashrate: {hashrate:,.2f} Hashes/s", end="")
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    main()
