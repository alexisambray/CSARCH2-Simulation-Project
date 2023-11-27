class CacheSimulator:
    def __init__(self, cache_size, block_size):
        self.cache_size = cache_size
        self.block_size = block_size

        # Define the cache line size in words (adjust based on your requirements)
        self.cache_line_size = 64

        # Calculate the number of cache blocks and sets
        self.num_blocks = cache_size // block_size
        self.num_sets = self.num_blocks // 4  # 4-way set-associative

        # Calculate the number of words per block based on the cache line size
        self.num_words_per_block = block_size // self.cache_line_size

        # Initialize the cache as a list of sets, each containing 4 lines (blocks)
        self.cache = [[{'valid': False, 'tag': None, 'data': [None] * self.num_words_per_block} for _ in range(4)] for _ in range(self.num_sets)]

        # LRU counters for each set
        self.lru_counters = [[0] * 4 for _ in range(self.num_sets)]
        
    def run_simulation(self, memory_access_sequence):
        hits, misses = 0, 0
        cache_access_time = 1  # Placeholder for cache access time
        main_memory_access_time = 10  # Placeholder for main memory access time

        for address in memory_access_sequence:
            block_address, offset = divmod(address, self.block_size)
            set_index = (block_address // 4) % self.num_sets
            tag = block_address // self.num_sets

            # Check each line in the set for a hit
            hit = False
            for i in range(4):
                if self.cache[set_index][i]['valid'] and self.cache[set_index][i]['tag'] == tag:
                    # Cache hit
                    hits += 1
                    hit = True
                    # Update LRU counters
                    self.update_lru_counters(set_index, i)
                    break

            if not hit:
                # Cache miss
                misses += 1
                # Find the least recently used line in the set
                lru_index = self.get_lru_index(set_index)
                # Replace the least recently used line with the new block
                self.cache[set_index][lru_index] = {'valid': True, 'tag': tag, 'data': [None] * self.num_words_per_block}
                # Update LRU counters
                self.update_lru_counters(set_index, lru_index)

                # Load data from main memory (placeholder for load-through policy)
                # You need to implement the logic to load data into the cache

        # Calculate cache hit rate, cache miss rate, average memory access time, and total memory access time
        cache_hit_rate = hits / len(memory_access_sequence)
        cache_miss_rate = misses / len(memory_access_sequence)
        average_memory_access_time = cache_hit_rate * cache_access_time + cache_miss_rate * main_memory_access_time
        total_memory_access_time = len(memory_access_sequence) * average_memory_access_time

        # Return statistics
        return {
            'hits': hits,
            'misses': misses,
            'cache_hit_rate': cache_hit_rate,
            'cache_miss_rate': cache_miss_rate,
            'average_memory_access_time': average_memory_access_time,
            'total_memory_access_time': total_memory_access_time
        }

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
