import random
import tkinter as tk
from tkinter import ttk
from src.cache_simulation import CacheSimulator

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Cache Simulator")

        # GUI components
        self.cache_size_label = ttk.Label(master, text="Cache Size:")
        self.cache_size_entry = ttk.Entry(master)
        self.cache_size_label.grid(row=0, column=0, sticky="e")
        self.cache_size_entry.grid(row=0, column=1)

        self.block_size_label = ttk.Label(master, text="Block Size:")
        self.block_size_entry = ttk.Entry(master)
        self.block_size_label.grid(row=1, column=0, sticky="e")
        self.block_size_entry.grid(row=1, column=1)

        self.start_button = ttk.Button(master, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create an instance of CacheSimulator
        self.cache_simulator = None

        # Result Label
        self.result_label = ttk.Label(master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2)

    def start_simulation(self):
        try:
            cache_size = int(self.cache_size_entry.get())
            block_size = int(self.block_size_entry.get())

            # Create an instance of CacheSimulator
            self.cache_simulator = CacheSimulator()

            # Run the simulation with a random memory access sequence
            memory_access_sequence = [
                random.randint(0, 2 * (cache_size // 2) - 1) for _ in range(4 * (cache_size // 2))
            ]
            results = self.cache_simulator.run_simulation(memory_access_sequence)

            # Display simulation results in the GUI
            result_text = (
                f"Memory Access Sequence: {memory_access_sequence}\n"
                f"Number of Memory Blocks (n): {cache_size // 2}\n"
                f"Cache Hits: {results['hits']}\n"
                f"Cache Misses: {results['misses']}\n"
                f"Cache Hit Rate: {results['cache_hit_rate']:.2%}\n"
                f"Cache Miss Rate: {results['cache_miss_rate']:.2%}\n"
                f"Average Memory Access Time: {results['average_memory_access_time']:.2f}\n"
                f"Total Memory Access Time: {results['total_memory_access_time']:.2f}"
            )

            # Update the label with the simulation results
            self.result_label.config(text=result_text)

        except ValueError as e:
            # Handle the ValueError (e.g., show an error message)
            self.result_label.config(text=str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
