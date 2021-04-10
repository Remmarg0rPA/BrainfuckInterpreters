#!/usr/bin/python3
import sys
import numpy as np

POINTER = 0
CELLS = np.random.uniform(0, 0, 30000)
CELLS = CELLS.astype('i')

VALID_CHARACTERS = ['+', '-', '<', '>', ',', '.', '[', ']']

with open('bFprogram.txt', 'r') as file:
	PROGRAM = file.read()


#Will make sure that all Parentheses match
PTR = 0
for character in PROGRAM:
	if character == '[':
		PTR += 1
	elif character == ']':
		PTR -= 1
if PTR !=0:
	sys.exit('BracketError: brackets do not match')


PTR = 0

#Executes the program
while PTR < len(PROGRAM):

    if PROGRAM[PTR] not in VALID_CHARACTERS:
        pass

    #Adds one to the current cell
    elif PROGRAM[PTR] == '+':
        CELLS[POINTER] += 1
        CELLS[POINTER] %= 256

    #Subtracts one from the current cell
    elif PROGRAM[PTR] == '-':
        CELLS[POINTER] -= 1
        CELLS[POINTER] %= 256

    #Moves the pointer one cell to the right
    elif PROGRAM[PTR] == '>':
        POINTER += 1
        POINTER %= 30000

    #Moves the pointer one cell to the left
    elif PROGRAM[PTR] == '<':
        POINTER -= 1
        POINTER %= 30000

    #Prints the ASCII character of the current cell
    elif PROGRAM[PTR] == '.':
        print(chr(CELLS[POINTER]), end='')

    #Changes the current cells value to the input characters ASCII value
    elif PROGRAM[PTR] == ',':
        CELLS[POINTER] = ord(input('\n')[0])

    #Handles starts of loops
    elif PROGRAM[PTR] == '[':
        loop = 1
        if CELLS[POINTER] == 0:
            while loop:
                PTR += 1
                if PROGRAM[PTR] == '[':
                    loop += 1
                elif PROGRAM[PTR] == ']':
                    loop -= 1

    #Handles ends of loops
    elif PROGRAM[PTR] == ']':
        if CELLS[POINTER] == 0:
            loop = 0
        else:
            loop = 1

        while loop:
            PTR -= 1

            if PROGRAM[PTR] == '[':
                loop -= 1

            elif PROGRAM[PTR] == ']':
                loop += 1

    PTR += 1


if POINTER >= 5 and POINTER <= 29994:
	Fr = (POINTER - 5)
	To = (POINTER + 4)

elif POINTER > 29994:
	Fr = 29990
	To = 29999

elif POINTER < 5:
	Fr = 0
	To = 9

print('\n',Fr, Fr + 1, Fr + 2, Fr + 3, Fr + 4, Fr + 5, Fr + 6, Fr + 7, Fr + 8, Fr + 9, sep='\t')

for i in range(len(CELLS[Fr:To]) + 1):
	if i + Fr == POINTER:
		print('\t[' + str(CELLS[i + Fr]) + ']', end='')
	else:
		print('\t' + str(CELLS[i]), end='')
