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

        # Radio buttons for output options
        self.output_option = tk.StringVar(value="final_snapshot")
        self.output_option_label = ttk.Label(master, text="Output Option:")
        self.output_option_label.grid(row=2, column=0, sticky="e")
        self.final_snapshot_radio = ttk.Radiobutton(master, text="Final Memory Snapshot", variable=self.output_option, value="final_snapshot")
        self.final_snapshot_radio.grid(row=2, column=1, sticky="w")
        self.step_by_step_radio = ttk.Radiobutton(master, text="Step-by-Step Animated Tracing", variable=self.output_option, value="step_by_step")
        self.step_by_step_radio.grid(row=3, column=1, sticky="w")

        self.start_button = ttk.Button(master, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Create an instance of CacheSimulator
        self.cache_simulator = None

        # Result Label
        self.result_label = ttk.Label(master, text="", wraplength=400)  # Adjust wraplength as needed
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

    def start_simulation(self):
        try:
            cache_size = int(self.cache_size_entry.get())
            block_size = int(self.block_size_entry.get())

            # Create an instance of CacheSimulator
            self.cache_simulator = CacheSimulator()

            # Run the simulation with the specified memory access sequence
            memory_access_sequence = self.generate_memory_access_sequence(test_case='random')
            output_option = 'final_snapshot'  # Change this to 'step_by_step' if needed
            simulation_result = self.cache_simulator.run_simulation(memory_access_sequence, output_option=output_option)

            # Display simulation results in the GUI
            result_text = (
                f"Memory Access Sequence: {memory_access_sequence}\n"
                f"Number of Memory Blocks (n): {cache_size // 2}\n"
                f"Cache Hits: {simulation_result['hits']}\n"
                f"Cache Misses: {simulation_result['misses']}\n"
                f"Cache Hit Rate: {simulation_result['cache_hit_rate']:.2%}\n"
                f"Cache Miss Rate: {simulation_result['cache_miss_rate']:.2%}\n"
                f"Average Memory Access Time: {simulation_result['average_memory_access_time']:.2f}\n"
                f"Total Memory Access Time: {simulation_result['total_memory_access_time']:.2f}"
            )

            # Update the label with the simulation results
            self.result_label.config(text=result_text)

            # Display the final memory snapshot if available
            memory_trace = simulation_result.get('memory_trace')
            if memory_trace is not None and output_option == 'final_snapshot':
                self.display_final_memory_snapshot(memory_trace)

        except ValueError as e:
            # Handle the ValueError (e.g., show an error message)
            self.result_label.config(text=str(e))

    def display_final_memory_snapshot(self, memory_snapshot):
        # Create a new window for displaying the final memory snapshot
        snapshot_window = tk.Toplevel(self.master)
        snapshot_window.title("Final Memory Snapshot")

        # Create a text widget to show the memory snapshot
        text_widget = tk.Text(snapshot_window, wrap="none", height=20, width=60)
        text_widget.pack()

        # Insert the memory snapshot data into the text widget
        for set_index, cache_set in enumerate(memory_snapshot):
            text_widget.insert(tk.END, f"Set {set_index}:\n")
            for line_index, cache_line in enumerate(cache_set):
                line_text = f"  Line {line_index}: {cache_line}\n"
                text_widget.insert(tk.END, line_text)

        # Make the text widget read-only
        text_widget.config(state=tk.DISABLED)

    def generate_memory_access_sequence(self, test_case='random'):
        if test_case == 'random':
            # Generate a random memory access sequence
            # This is just a placeholder; you may want to replace it with your own logic
            return [random.randint(0, 1023) for _ in range(100)]
        else:
            # Implement other test cases as needed
            pass

    def show_step_by_step_memory_trace(self, memory_trace):
        # Implement the logic to display the memory trace step by step
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
