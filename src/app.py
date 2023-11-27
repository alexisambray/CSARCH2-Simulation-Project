import tkinter as tk
from tkinter import ttk
from src.cache_simulation import CacheSimulator  # Adjust import path

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

    def start_simulation(self):
        # Retrieve user inputs
        cache_size = int(self.cache_size_entry.get())
        block_size = int(self.block_size_entry.get())

        # Create an instance of CacheSimulator
        self.cache_simulator = CacheSimulator(cache_size, block_size)

        # Run the simulation with a sample memory access sequence (modify as needed)
        memory_access_sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        results = self.cache_simulator.run_simulation(memory_access_sequence)

        # Display simulation results
        result_label = ttk.Label(self.master, text=f"Cache Hits: {results['hits']}, Cache Misses: {results['misses']}")
        result_label.grid(row=3, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
