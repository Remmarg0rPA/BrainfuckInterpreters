import sys

POINTER = [0,0]
sizeX=3000
sizeY=3000
CELLS = [[0 for i in range(sizeX)] for k in range(sizeY)]
VALID_CHARACTERS = ['+', '-', '<', '>', 'v', 'V', '^', ',', '.', '[', ']']


with open('bF++program.txt', 'r') as file:
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
		CELLS[POINTER[1]][POINTER[0]] += 1
		CELLS[POINTER[1]][POINTER[0]] %= 255


   	#Subtracts one from the current cell
	elif PROGRAM[PTR] == '-':
		CELLS[POINTER[1]][POINTER[0]] -=1
		CELLS[POINTER[1]][POINTER[0]] %= 255


	#Moves the pointer one cell to the right
	elif PROGRAM[PTR] == '>':
		POINTER[0] += 1
		POINTER[0] %= sizeX


    	#Moves the pointer one cell to the left
	elif PROGRAM[PTR] == '<':
		POINTER[0] -= 1
		POINTER[0] %= sizeX


	#Moves the pointer one cell down
	elif PROGRAM[PTR].lower() == 'v':
		POINTER[1] += 1
		POINTER[1] %= sizeY


	#Moves the pointer one cell up
	elif PROGRAM[PTR] == '^':
		POINTER[1] -= 1
		POINTER[1] %= sizeY


    #Prints the ASCII character of the current cell
	elif PROGRAM[PTR] == '.':
		print(chr(CELLS[POINTER[1]][POINTER[0]]), end='')


    #Changes the current cells value to the input characters ASCII value
	elif PROGRAM[PTR] == ',':
		CELLS[POINTER[1]][POINTER[0]] = ord(input('\n')[0])


    #Handles starts of loops
	elif PROGRAM[PTR] == '[':
		loop = 1
		if CELLS[POINTER[1]][POINTER[0]] == 0:
			while loop:
				PTR += 1
				if PROGRAM[PTR] == '[':
					loop += 1
				elif PROGRAM[PTR] == ']':
					loop -= 1


    #Handles ends of loops
	elif PROGRAM[PTR] == ']':
		if CELLS[POINTER[1]][POINTER[0]] == 0:
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
