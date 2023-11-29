# CSARCH2 Cache Simulation Project S12

## Type of cache memory: 4-way BSA + LRU

### PG5:

- AMBRAY, ALEXIS SOFIA BUGIA
- MALIA, GIDEON ANDREW LIMPIADA
- MARTINEZ, MICHELLLE ANDREA HERVAS
- RACELA, MEL GEOFFREY FRANCISCO

- Link to the walkthrough vide: https://drive.google.com/file/d/1IBvfmw3l8LmQRca3sYFN-XVClvCdcnfz/view?usp=sharing

#### There are 3 different test cases:

- Sequential access pattern
- Random access pattern
- Mid-repeat pattern

Each of these test cases is designed to evaluate how well a cache algorithm or system performs under different scenarios of block access.

The specific patterns are defined based on the values of n(memory block size) and a in each case.

##### Sequential Sequence:

- Description: In this test case, sequentially accessing cache blocks up to 2n.
  The sequence is repeated four times.
- Example: If n is 4, the sequence would be 0, 1, 2, 3, ..., 14, 15, 0, 1, 2, 3, ..., 14, 15, 0, 1, 2, 3, ...,14, 15, 0, 1, 2, 3, ..., 14, 15.

##### Random Sequence:

- Description: This test case involves accessing a sequence of 4n cache blocks randomly.
- Example: If n is 4, the sequence could be something like 7, 2, 14, 0, ..., (random order)

##### Mid-Repeat Blocks:

- Description: This test case involves starting with block 0, repeating the sequence in the
  middle two times up to a-1 blocks (where a is an arbitrary position), then continuing from c
  up to 2n. The sequence is repeated four times.
- Example: If n is 8 and a is 6, the sequence would be 0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 (repeated four times).
