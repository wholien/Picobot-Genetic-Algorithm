# Picobot-Genetic-Algorithm
A program which models a picobot machine as well as the square picobot maze. 

Picobot is seen here: https://www.cs.hmc.edu/picobot/

The program randomly produces instructions for 200 picobot programs. After that, the programs make it to the next generation if they are above a certain fitness. Fitness of a program is calculated as what percentage of the maze the picobot can traverse with the program's commands.

We chose the threshold of a good program that makes it to the next generation as any program that has a fitness that is above the average between the max fitness of this generation and the average fitness of this generation.

Since not every program can make it to the next generation, and we want each generation to have a constant 200 programs, the remaining space in the next generation is taken up by crossover programs and mutated programs.

Crossover is achieved by mating a good program with a random program, thus generating a "child" program. Every 15th crossover program will have some of its commands mutated, thus introducing extra variance into the gene pool.

The goal is to have programs that can traverse the entire square maze by generation 20. This is largely achieved, as the fittest program in generation 20 is able to traverse the entire square maze.
