#include <iostream>
#include <fstream>

int parity(std::string);

//argc is number of cmnd line args. *argv[] is a list with the command line argments
int main(int argc, char *argv[]) {

    std::string program;
    std::ifstream brainFile;
    int rep = 0;
    while (!(brainFile.is_open()) && rep < 5) {
        //Opens the brainf.txt if no second arg is given
        if (argc < 2){
            brainFile.open("brainf.txt", std::ios::out);
        } 
        //Opens the second argument if given 
        else {
            brainFile.open(argv[1], std::ios::out);
        }
        //Reads the file if it has opened
        if (brainFile.is_open()){
            std::string line;
            //Reads the file line by line and appeds it to program string
            while (getline(brainFile, line)){
                program += line;
            }
        }
        rep++;
        //If the file has not opened within five repetitions
        if (rep == 5){
            if (argc < 2){
                 std::cout << "Could not open or find brainf.txt" << std::endl;
                 return 1;
            } else {
                std::cout << "Could not find or open "<< argv[1] << std::endl;
                return 1;
            }
        }
    }


    //Will check if the parenthesis match before the program starts
    if (parity(program)){
        return 2;
    }


    int array_length = 3000;
    int array[array_length] = {0}; //The array with all of the cells
    unsigned short int ptr = 0; //The "pointer" that points to a cell in the array
    //A pointer was not used because it could move past the beginning or end of the array easily

    int loop_counter = 0;
    int program_length = program.length();

    int i = 0;
    while (i < program_length){
        
        //Increments current cell by 1
        if(program[i] == '+'){
            array[ptr]++;
            array[ptr] %= 256;
            i++;
            continue;
        }
        
        //Decrements current cell by 1
        else if(program[i] == '-'){
            array[ptr]--;
            array[ptr] %= 256;
            i++;
            continue;
        }

        //Moves the array pointer one step to the right
        else if(program[i] == '>'){
            ptr++;
            ptr %= array_length;
            i++;
            continue;
        }

        //Moves the array pointer one step t othe left
        else if(program[i] == '<'){
            ptr--;
            ptr %= array_length;
            i++;
            continue;
        }

        //Outputs the ASCII value of the current cell
        else if(program[i] == '.'){
            unsigned char c = array[ptr];
            std::cout << c ;//<< array[ptr];
            i++;
            continue;
        }

        //Assigns the ASCII value of input to the current cell
        else if(program[i] == ','){
            unsigned char in;
            std::cin >> in;
            array[ptr] = int(in);
            i++;
            continue;
        }

        //Handles the start of loops
        else if (program[i] == '['){

            loop_counter = 1;
            //Skips the loop
            if (array[ptr] == 0){
                
                while (loop_counter){
                    i++;
                    if (program[i] == '['){
                        loop_counter++;
                        
                    }
                    else if (program[i] == ']'){
                        loop_counter--;
                        
                    }
                }
            }

            //Enters the loop
            i++;
            continue;
        }

        //Handles the end of loops
        else if (program[i] == ']'){

            if (array[ptr] == 0){
                i++;
                continue;
            }
            else{
                loop_counter = 1;
                
                while (loop_counter != 0){
                    i--;
                    if (program[i] == '['){
                        loop_counter--;
                        
                    }
                    else if (program[i] == ']'){
                        loop_counter++;
                        
                    }
                }
            }
        }

        //If it was not a valid character
        else {
            i++;
            continue;
        }

    }

    return 0;
}


int parity(std::string str){
    int p = 0;
    char c;
    for (int i; i < str.length(); i++){
        c = str[i];
        if ( c == '['){p++;}
        else if (c == ']'){p--;}
        }

    if (p != 0){
        std::cout << "Error! The '[' and ']' do not match" << std::endl;
        return 1;
    }
    return 0;
}