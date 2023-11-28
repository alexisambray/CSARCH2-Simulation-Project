import tkinter as tk
from tkinter import messagebox

class CacheSimulator:
    def __init__(self):
        self.cache_blocks = 32
        self.cache_line_size = 64
        self.read_policy = "load-through"
        self.memory_blocks = 0
        self.sequence = []
        self.cache = {}

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("Cache Simulator")
        self.create_gui_elements()

    def create_gui_elements(self):
        # Labels
        tk.Label(self.root, text="Number of Memory Blocks:").grid(row=0, column=0)
        tk.Label(self.root, text="Memory Access Sequence (comma-separated):").grid(row=1, column=0)

        # Entry Widgets
        self.memory_blocks_entry = tk.Entry(self.root)
        self.memory_blocks_entry.grid(row=0, column=1)
        self.sequence_entry = tk.Entry(self.root)
        self.sequence_entry.grid(row=1, column=1)

        # Button
        tk.Button(self.root, text="Simulate", command=self.run_simulation).grid(row=2, column=0, columnspan=2)

    def parse_user_input(self):
        try:
            self.memory_blocks = int(self.memory_blocks_entry.get())
            self.sequence = list(map(int, self.sequence_entry.get().split(',')))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid integers.")
            return False
        return True

    def run_simulation(self):
        if not self.parse_user_input():
            return

        # Initialize cache
        self.cache = {block: [None] * self.cache_line_size for block in range(self.cache_blocks)}

        # Simulation logic (implement your cache simulation logic here)
        memory_access_count = 0
        cache_hit_count = 0
        cache_miss_count = 0

        for address in self.sequence:
            block_number = address // self.cache_line_size

            if block_number in self.cache:
                if address in self.cache[block_number]:
                    cache_hit_count += 1
                else:
                    cache_miss_count += 1
                    # Implement load-through policy if needed
                    self.cache[block_number][address] = True
            else:
                cache_miss_count += 1
                # Implement cache replacement policy if needed
                self.cache[block_number] = {address: True}

            memory_access_count += 1

        # Calculate metrics
        cache_hit_rate = cache_hit_count / memory_access_count
        cache_miss_rate = cache_miss_count / memory_access_count
        average_memory_access_time = 1 + cache_miss_rate  # Assume cache miss penalty = 1

        # Display results
        messagebox.showinfo(
            "Simulation Results",
            f"Memory Access Count: {memory_access_count}\n"
            f"Cache Hit Count: {cache_hit_count}\n"
            f"Cache Miss Count: {cache_miss_count}\n"
            f"Cache Hit Rate: {cache_hit_rate:.2%}\n"
            f"Cache Miss Rate: {cache_miss_rate:.2%}\n"
            f"Average Memory Access Time: {average_memory_access_time:.2f}\n"
            f"Total Memory Access Time: {memory_access_count * average_memory_access_time:.2f}"
        )

    def start(self):
        self.root.mainloop()

# Run the simulation
simulator = CacheSimulator()
simulator.start()
