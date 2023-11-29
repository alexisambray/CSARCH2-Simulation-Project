import tkinter as tk
from tkinter import ttk
from random import sample

class CacheSimulator:
    def __init__(self, num_cache_blocks, cache_line_size, read_policy, num_memory_blocks, cache_associativity):
        self.num_cache_blocks = num_cache_blocks
        self.cache_line_size = cache_line_size
        self.read_policy = read_policy
        self.num_memory_blocks = num_memory_blocks
        self.cache_associativity = cache_associativity

        self.cache_memory = {i: {'blocks': ['X'] * self.cache_associativity, 'lru': list(range(self.cache_associativity))}
                             for i in range(self.num_cache_blocks)}

        self.memory_blocks = list(range(self.num_memory_blocks))
        self.cache_trace = []  # Cache memory trace for logging
        self.memory_access_count = 0
        self.cache_hit_count = 0
        self.cache_miss_count = 0
        self.total_memory_access_time = 0

    def simulate(self, test_case, step_by_step=True):
        if test_case == 'Sequential':
            sequence = list(range(2 * self.num_cache_blocks)) * 4
        elif test_case == 'Random':
            sequence = sample(range(4 * self.num_cache_blocks), 4 * self.num_cache_blocks)
        elif test_case == 'Mid-Repeat':
            sequence = list(range(self.num_cache_blocks)) * 2 + list(range(2 * self.num_cache_blocks)) * 2
        else:
            raise ValueError("Invalid test case")

        for step, block in enumerate(sequence, start=1):
            self.access_memory(block)
            if step_by_step:
                self.cache_trace.append(self.get_cache_memory_snapshot(step, block))

        if not step_by_step:
            self.cache_trace.append(self.get_cache_memory_snapshot(len(sequence), None))

        # Calculate statistics
        self.calculate_statistics()

    def access_memory(self, block):
        self.memory_access_count += 1
        cache_index = block % self.num_cache_blocks
        if block in self.cache_memory[cache_index]['blocks']:
            self.cache_hit_count += 1
            block_index = self.cache_memory[cache_index]['blocks'].index(block)
            self.cache_memory[cache_index]['lru'].remove(block_index)
            self.cache_memory[cache_index]['lru'].append(block_index)
        else:
            self.cache_miss_count += 1
            if len(self.cache_memory[cache_index]['blocks']) < self.cache_associativity:
                self.cache_memory[cache_index]['blocks'][0] = block
            else:
                lru_index = self.cache_memory[cache_index]['lru'].pop(0)
                self.cache_memory[cache_index]['blocks'][lru_index] = block
                self.cache_memory[cache_index]['lru'].append(lru_index)

    def get_cache_memory_snapshot(self, step, current_block):
        snapshot = f"Step: {step}, Current Cache Memory:\n"
        if current_block is not None:
            snapshot += f"Block {current_block} {'miss' if 'X' in self.cache_memory[current_block % self.num_cache_blocks]['blocks'] else 'hit'}\n"
        snapshot += "---------------------\n"
        snapshot += "| Cache Index | Data |\n"
        snapshot += "---------------------\n"
        for index, data in enumerate(self.cache_memory.values()):
            snapshot += f"| {index:12d} | {', '.join(map(str, data['blocks']))} |\n"
        snapshot += "---------------------\n\n"
        return snapshot

    def calculate_statistics(self):
        cache_hit_rate = self.cache_hit_count / self.memory_access_count * 100 if self.memory_access_count > 0 else 0
        cache_miss_rate = self.cache_miss_count / self.memory_access_count * 100 if self.memory_access_count > 0 else 0
        average_memory_access_time = 1 + 4 * (cache_miss_rate / 100)
        total_memory_access_time = self.memory_access_count * average_memory_access_time

        # Display statistics
        self.cache_trace.append(f"Simulation Statistics:\n")
        self.cache_trace.append(f"1. Memory Access Count: {self.memory_access_count}\n")
        self.cache_trace.append(f"2. Cache Hit Count: {self.cache_hit_count}\n")
        self.cache_trace.append(f"3. Cache Miss Count: {self.cache_miss_count}\n")
        self.cache_trace.append(f"4. Cache Hit Rate: {cache_hit_rate:.2f}%\n")
        self.cache_trace.append(f"5. Cache Miss Rate: {cache_miss_rate:.2f}%\n")
        self.cache_trace.append(f"6. Average Memory Access Time: {average_memory_access_time:.2f} cycles\n")
        self.cache_trace.append(f"7. Total Memory Access Time: {total_memory_access_time:.2f} cycles\n")

class CacheSimulatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cache Simulator")
        self.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Cache Simulator - 4-way BSA + LRU", font=("Helvetica", 16))
        label.pack(pady=10)

        input_frame = tk.Frame(self)
        input_frame.pack(side=tk.LEFT, padx=10)

        cache_blocks_label = tk.Label(input_frame, text="Number of Cache Blocks:")
        cache_blocks_label.pack()
        self.cache_blocks_entry = tk.Entry(input_frame)
        self.cache_blocks_entry.pack()

        test_case_label = tk.Label(input_frame, text="Choose Test Case:")
        test_case_label.pack()
        self.test_case_var = tk.StringVar()
        test_case_options = ['Sequential', 'Random', 'Mid-Repeat']
        self.test_case_dropdown = ttk.Combobox(input_frame, textvariable=self.test_case_var, values=test_case_options)
        self.test_case_dropdown.set(test_case_options[0])
        self.test_case_dropdown.pack(pady=10)

        step_by_step_var = tk.BooleanVar()
        step_by_step_checkbox = tk.Checkbutton(input_frame, text="Step-by-Step", variable=step_by_step_var)
        step_by_step_checkbox.pack()

        run_button = tk.Button(input_frame, text="Run Simulation", command=lambda: self.run_simulation(step_by_step_var.get()))
        run_button.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(input_frame, text="Reset", command=self.reset_display)
        reset_button.pack(side=tk.LEFT, padx=10)

        result_frame = tk.Frame(self)
        result_frame.pack(side=tk.RIGHT, padx=10)

        scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL)
        self.result_text = tk.Text(result_frame, height=20, width=55, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.pack()

    def run_simulation(self, step_by_step):
        try:
            num_cache_blocks = int(self.cache_blocks_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number of cache blocks.")
            return

        self.result_text.delete(1.0, tk.END)  # Clear previous content

        simulator = CacheSimulator(num_cache_blocks, 64, 'load-through', num_cache_blocks, 4)

        test_case = self.test_case_var.get()
        simulator.simulate(test_case, step_by_step)

        if step_by_step:
            for cache_snapshot in simulator.cache_trace:
                self.result_text.insert(tk.END, cache_snapshot)
        else:
            self.result_text.insert(tk.END, "".join(simulator.cache_trace))

        self.result_text.insert(tk.END, "Simulation Completed!\n")

    def reset_display(self):
        self.result_text.delete(1.0, tk.END)
        self.cache_blocks_entry.delete(0, tk.END)
        self.test_case_var.set('')
        self.cache_blocks_entry.focus()

if __name__ == "__main__":
    app = CacheSimulatorGUI()
    app.mainloop()
