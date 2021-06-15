#!/usr/bin/python3
import re, time, praw
import numpy as np
from decouple import RepositoryIni
from reddit_base_bot import RedditBotBase

class BrainFuckBot(RedditBotBase):
    # interpret_bf returns one of these values if it did not finish the execution of the program
    TIME_OUT = 1
    PARENTESIS_ERROR = 2

    def __init__(self, reddit_client_id, reddit_client_secret, reddit_user, reddit_password, user_agent):
        super(BrainFuckBot, self).__init__(reddit_client_id=reddit_client_id,
                                      reddit_client_secret=reddit_client_secret,
                                      reddit_user=reddit_user,
                                      reddit_password=reddit_password,
                                      user_agent=user_agent)

    def process_summon(self, comment):
        # Removes all invalid chars
        program = ''
        for c in comment.body:
            if c in ['+', '-', '<', '>', ',', '.', '[', ']']:
                program += str(c)

        out = self.interpret_bf(program)
        text = ''
        if out == BrainFuckBot.PARENTESIS_ERROR:
            text += "There was an error in your brainfuck code. You have to make sure the parentesis match."
        elif out == BrainFuckBot.TIME_OUT:
            text += "The execution time exceeded the maximum limit."
            text += "This could be because of an infinite loop or because the program was too long."
        else:
            text += "Your brainfuck code produced the following output:\n\n"
            for i in out.split('\n'):
                text += '\t' + i + '\n'
        return text

    @staticmethod
    def interpret_bf(PROGRAM, MAX_EXEC_TIME=120):
        # Creates a 30 000 int array
        CELLS = np.zeros((1, 30000))[0]
        CELLS = CELLS.astype('i')
        POINTER = 0
        PROG_PTR = 0
        #The string with the output to return
        OUTPUT_BUF = ''

        #Will make sure that all Parentheses match
        r1 = re.compile('\[')
        r2 = re.compile('\]')
        if len(r1.findall(PROGRAM)) != len(r2.findall(PROGRAM)):
            return BrainFuckBot.PARENTESIS_ERROR

        time_start = time.time()
        #Executes the program
        while PROG_PTR < len(PROGRAM):
            #Adds one to the current cell
            if PROGRAM[PROG_PTR] == '+':
                CELLS[POINTER] = (CELLS[POINTER] + 1) % 256
            #Subtracts one from the current cell
            elif PROGRAM[PROG_PTR] == '-':
                CELLS[POINTER] = (CELLS[POINTER] - 1) % 256
            #Moves the pointer one cell to the right and wraps around
            elif PROGRAM[PROG_PTR] == '>':
                POINTER = (POINTER + 1)  % 30000
            #Moves the pointer one cell to the left and wraps around
            elif PROGRAM[PROG_PTR] == '<':
                POINTER = (POINTER - 1)  % 30000
            #Prints the ASCII character of the current cell
            elif PROGRAM[PROG_PTR] == '.':
                OUTPUT_BUF += chr(CELLS[POINTER])
            #Cannot take usr input and will therefore default it to 0
            elif PROGRAM[PROG_PTR] == ',':
                CELLS[POINTER] = 0
            #Handles starts of loops
            elif PROGRAM[PROG_PTR] == '[':
                loop = 1
                if CELLS[POINTER] == 0:
                    while loop:
                        PROG_PTR += 1
                        if PROGRAM[PROG_PTR] == '[':
                            loop += 1
                        elif PROGRAM[PROG_PTR] == ']':
                            loop -= 1
            #Handles ends of loops
            elif PROGRAM[PROG_PTR] == ']':
                if CELLS[POINTER] == 0:
                    #Will skip while-loop and thus terminate loop
                    loop = 0
                else:
                    loop = 1
                while loop:
                    PROG_PTR -= 1
                    if PROGRAM[PROG_PTR] == '[':
                        loop -= 1
                    elif PROGRAM[PROG_PTR] == ']':
                        loop += 1
            if (time.time() - time_start) > MAX_EXEC_TIME:
                return BrainFuckBot.TIME_OUT
            PROG_PTR += 1

        if POINTER >= 5 and POINTER <= 29994:
        	Fr = POINTER - 5
        elif POINTER > 29994:
        	Fr = 29990
        elif POINTER < 5:
        	Fr = 0
        OUTPUT_BUF += '\nCell  '
        center_val = []
        for i in range(9):
            center_vals.append(len(str(Fr+i)) + 2)
            OUTPUT_BUF += str(Fr + i).center(center_val[-1])
        OUTPUT_BUF += '\nValue '
        for i in range(9):
        	if i + Fr == POINTER:
        		OUTPUT_BUF += ('[' + str(CELLS[Fr + i]) + ']').center(center_val[i])
        	else:
        		OUTPUT_BUF += str(CELLS[i + Fr]).center(center_val[i])
        return OUTPUT_BUF



if __name__ == "__main__":
    getItem = lambda key: RepositoryIni('.settings.ini').__getitem__(key)
    b = BrainFuckBot(reddit_client_id = getItem('client_id'),
                reddit_client_secret = getItem('client_secret'),
                reddit_user = getItem('username'),
                reddit_password = getItem('password'),
                user_agent = getItem('user_agent'))
    b.dry_run = False
    b.debug = False
    b.include_old_mentions = False
    b()
