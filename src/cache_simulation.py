class CacheSimulator:
    def __init__(self):
        # Fixed cache size and block size as per instructions
        self.cache_size = 32
        self.block_size = 64

        # Fixed cache line size in words as per instructions
        self.cache_line_size = 64

        # Calculate the number of cache blocks and sets
        self.num_blocks = max(self.cache_size // self.block_size, 1)  # Ensure num_blocks is at least 1
        self.num_sets = max(self.num_blocks // 4, 1)  # Ensure num_sets is at least 1

        # Calculate the number of words per block based on the cache line size
        self.num_words_per_block = self.block_size // self.cache_line_size

        # Initialize the cache as a list of sets, each containing 4 lines (blocks)
        self.cache = [
            [{'valid': False, 'tag': None, 'data': [None] * self.num_words_per_block} for _ in range(4)]
            for _ in range(self.num_sets)
        ]

        # LRU counters for each set
        self.lru_counters = [[0] * 4 for _ in range(self.num_sets)]

        # Variables to store cache memory trace
        self.cache_memory_trace = []

        # Variables to store simulation results
        self.hits = 0
        self.misses = 0
        
    def run_simulation(self, memory_access_sequence, output_option='final_snapshot'):
        for address in memory_access_sequence:
            block_address, offset = divmod(address, self.block_size)
            set_index = (block_address // self.block_size) % self.num_sets
            tag = block_address // self.num_blocks

            # Check each line in the set for a hit
            hit = False
            for i in range(4):
                if self.cache[set_index][i]['valid'] and self.cache[set_index][i]['tag'] == tag:
                    # Cache hit
                    self.hits += 1
                    hit = True
                    # Update LRU counters
                    self.update_lru_counters(set_index, i)
                    break

            if not hit:
                # Cache miss
                self.misses += 1
                # Find the least recently used line in the set
                lru_index = self.get_lru_index(set_index)
                # Replace the least recently used line with the new block
                self.cache[set_index][lru_index] = {'valid': True, 'tag': tag, 'data': [None] * self.num_words_per_block}
                # Update LRU counters
                self.update_lru_counters(set_index, lru_index)

            # Log the cache memory state for each memory access
            self.cache_memory_trace.append([line.copy() for line in self.cache])

        # Calculate cache hit rate, cache miss rate, average memory access time, and total memory access time
        cache_hit_rate = self.hits / len(memory_access_sequence)
        cache_miss_rate = self.misses / len(memory_access_sequence)
        average_memory_access_time = cache_hit_rate * 1 + cache_miss_rate * 10  # Placeholder values for access times
        total_memory_access_time = len(memory_access_sequence) * average_memory_access_time

        # Return simulation results and memory trace
        if output_option == 'final_snapshot':
            return {
                'hits': self.hits,
                'misses': self.misses,
                'cache_hit_rate': cache_hit_rate,
                'cache_miss_rate': cache_miss_rate,
                'average_memory_access_time': average_memory_access_time,
                'total_memory_access_time': total_memory_access_time,
                'memory_trace': self.cache_memory_trace[-1]  # Return the final snapshot
            }
        elif output_option == 'step_by_step':
            return {
                'hits': self.hits,
                'misses': self.misses,
                'cache_hit_rate': cache_hit_rate,
                'cache_miss_rate': cache_miss_rate,
                'average_memory_access_time': average_memory_access_time,
                'total_memory_access_time': total_memory_access_time,
                'memory_trace': self.cache_memory_trace  # Return the full memory trace for step-by-step tracing
            }
        else:
            raise ValueError("Invalid output option. Choose 'final_snapshot' or 'step_by_step'")

    def handle_cache_miss(self, set_index, tag, block_address):
        # Fetch data from main memory (simulate load-through)
        data = self.fetch_data_from_memory(block_address)

        # Find the least recently used line in the set
        lru_index = self.get_lru_index(set_index)

        # Update cache with the fetched data
        self.cache[set_index][lru_index] = {'valid': True, 'tag': tag, 'data': data}

        # Update LRU counters
        self.update_lru_counters(set_index, lru_index)

    def fetch_data_from_memory(self, block_address):
        # Simulate fetching data from main memory
        # This can be replaced with actual memory access logic
        return [None] * self.num_words_per_block

    def update_lru_counters(self, set_index, accessed_line):
        # Increment the counter of the accessed line and reset others in the set
        for i in range(4):
            if i == accessed_line:
                self.lru_counters[set_index][i] = 0
            else:
                self.lru_counters[set_index][i] += 1

    def get_lru_index(self, set_index):
        # Find the line with the maximum counter in the set (LRU)
        return self.lru_counters[set_index].index(max(self.lru_counters[set_index]))
