# Picobot-Genetic-Algorithm
A program which models a picobot machine as well as the square picobot maze. 

Picobot is seen here: https://www.cs.hmc.edu/picobot/

The program randomly produces instructions for 200 picobot programs. After that, the programs make it to the next generation if they are above a certain fitness. To keep each generation at a constant 200 programs, the remaining space is filled with programs that are products of two programs in the previous generation mating. This is done by mating a good program (a program over the required fitness threshold, thus it is already added to the next generation) with a random program from the same generation. Evolution is further modeled by introducing mutations to every fifteenth program produced by mating. 

The goal is to produce programs that can traverse the entire square picobot maze. This is achieved in 20 generations, as seen
in our experimental data.
