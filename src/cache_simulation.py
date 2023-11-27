class CacheSimulator:
    def __init__(self, cache_size, block_size):
        self.cache_size = cache_size
        self.block_size = block_size

        # Calculate the number of cache blocks
        self.num_blocks = cache_size // block_size

        # Initialize the cache as a list of dictionaries
        # Each dictionary represents a cache block with an empty slot
        self.cache = [{'valid': False, 'tag': None, 'data': None} for _ in range(self.num_blocks)]

    def run_simulation(self, memory_access_sequence):
        # Cache simulation logic
        hits, misses = 0, 0

        for address in memory_access_sequence:
            block_address, offset = divmod(address, self.block_size)
            index = block_address % self.num_blocks

            if self.cache[index]['valid'] and self.cache[index]['tag'] == block_address:
                # Cache hit
                hits += 1
            else:
                # Cache miss
                misses += 1
                # Update the cache with the new block
                self.cache[index] = {'valid': True, 'tag': block_address, 'data': None}

        return {'hits': hits, 'misses': misses}
