# CSARCH2 Cache Simulation Project S12

## Type of cache memory: 4-way BSA + LRU

### PG5:

- AMBRAY, ALEXIS SOFIA BUGIA
- MALIA, GIDEON ANDREW LIMPIADA
- MARTINEZ, MICHELLLE ANDREA HERVAS
- RACELA, MEL GEOFFREY FRANCISCO

### Link to the walkthrough vide:

- https://drive.google.com/file/d/1IBvfmw3l8LmQRca3sYFN-XVClvCdcnfz/view?usp=sharing

### How to run the program

1. Go to the directory where main.py is located.
2. In that directory, open Command Prompt.
3. Type 'python main.py'
4. Enter the number of blocks
5. Choose a test case
6. Select 'Step-by-Step' if you want the step-by-step animated tracing. Leave the checkbox unchecked if you only want the final memory snapshot to be displayed.
7. Click 'Run Simulation'
8. To clear the display, press Reset.

#### There are 3 different test cases:

- Sequential access pattern
- Random access pattern
- Mid-repeat pattern

Each of these test cases is designed to evaluate how well a cache algorithm or system performs under different scenarios of block access.

The specific patterns are defined based on the values of n(memory block size) and a in each case.

##### Sequential Sequence:

- Description: In this test case, sequentially accessing cache blocks up to 2n.
  The sequence is repeated four times.

##### Random Sequence:

- Description: This test case involves accessing a sequence of 4n cache blocks randomly.
  Example: If n is 4, the sequence could be something like 7, 2, 14, 0, ..., (random order)

##### Mid-Repeat Blocks:

- Description: This test case involves starting with block 0, repeating the sequence in the middle two times up to a-1 blocks (where a is an arbitrary position), then continuing from c up to 2n. The sequence is repeated four times.

### Key Takeaways:

- Sequential Sequence:
  The hit rate is always higher than the miss rate

- Random Sequence:
  The miss rate is always higher than the hit rate
  Slowest memory access time

- Mid-Repeat Blocks:
  The hit rate is higher than the miss rate
  Fastest memory access time
