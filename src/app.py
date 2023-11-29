import random
import tkinter as tk
from tkinter import ttk
from src.cache_simulation import CacheSimulator

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Cache Simulator")

        # GUI components
        self.memory_block_label = ttk.Label(master, text="Number of Memory Block:")
        self.memory_block_entry = ttk.Entry(master)
        self.memory_block_label.grid(row=0, column=0, sticky="e")
        self.memory_block_entry.grid(row=0, column=1)

        # Radio buttons for output options
        self.output_option = tk.StringVar(value="final_snapshot")
        self.output_option_label = ttk.Label(master, text="Output Option:")
        self.output_option_label.grid(row=2, column=0, sticky="e")
        self.final_snapshot_radio = ttk.Radiobutton(master, text="Final Memory Snapshot", variable=self.output_option, value="final_snapshot")
        self.final_snapshot_radio.grid(row=2, column=1, sticky="w")
        self.step_by_step_radio = ttk.Radiobutton(master, text="Step-by-Step Animated Tracing", variable=self.output_option, value="step_by_step")
        self.step_by_step_radio.grid(row=3, column=1, sticky="w")

        self.testcase_option = tk.StringVar(value="random")
        self.testcase_option_label = ttk.Label(master, text="Test case Option:")
        self.testcase_option_label.grid(row=4, column=0, sticky="e")
        self.random_radio = ttk.Radiobutton(master, text="Random Sequence", variable=self.testcase_option, value="random")
        self.random_radio.grid(row=4, column=1, sticky="w")
        self.mid_repeat = ttk.Radiobutton(master, text="Mid-Repeat-Sequence", variable=self.testcase_option, value="mid_repeat")
        self.mid_repeat.grid(row=5, column=1, sticky="w")
        self.sequenceial = ttk.Radiobutton(master, text="Sequential Sequence", variable=self.testcase_option, value="sequential")
        self.sequenceial.grid(row=6, column=1, sticky="w")
        

      

        self.start_button = ttk.Button(master, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Create an instance of CacheSimulator
        self.cache_simulator = None

        # Result Label
        self.result_label = ttk.Label(master, text="", wraplength=400)  # Adjust wraplength as needed
        self.result_label.grid(row=8, column=0, columnspan=2, pady=10)

    def start_simulation(self):
        try:
            memory_block = int(self.memory_block_entry.get())
           

            # Create an instance of CacheSimulator
            self.cache_simulator = CacheSimulator()

            # Run the simulation with the specified memory access sequence
            testcase_data = self.testcase_option.get()
            memory_access_sequence = self.generate_memory_access_sequence(n=memory_block,test_case=testcase_data)
            
            output_option_data = self.output_option.get()
            simulation_result = self.cache_simulator.run_simulation(memory_access_sequence, output_option=output_option_data)

            # Display simulation results in the GUI
            result_text = (
                f"Memory Access Count: {len(memory_access_sequence)}\n"
                f"Cache Hit count: {simulation_result['hits']}\n"
                f"Cache Miss count: {simulation_result['misses']}\n"
                f"Cache Hit Rate: {simulation_result['cache_hit_rate']:.2%}\n"
                f"Cache Miss Rate: {simulation_result['cache_miss_rate']:.2%}\n"
                f"Average Memory Access Time: {simulation_result['average_memory_access_time']:.2f}\n"
                f"Total Memory Access Time: {simulation_result['total_memory_access_time']:.2f}\n"
            )

            # Update the label with the simulation results
            self.result_label.config(text=result_text)

            memory_trace = simulation_result.get('memory_trace')
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
    def sequential_sequence(self, n):
        sequence = list(range(2 * n))
        repeated_sequence = sequence * 4
        return repeated_sequence

    def random_sequence(self, n):
        sequence = list(range(4 * n))
        random.shuffle(sequence)
        return sequence


    def mid_repeat_blocks(self, n):
        middle_sequence = list(range(n))
        full_sequence = middle_sequence + list(range(n, 2 * n))
        repeated_sequence = full_sequence * 4
        return repeated_sequence

    def generate_memory_access_sequence(self,n=32,test_case='random'):
        
        if test_case == 'random':
          
            return self.random_sequence(n)
        elif test_case == 'mid_repeat':
          
            return self.mid_repeat_blocks(n)
        else:
            return self.sequential_sequence(n)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
