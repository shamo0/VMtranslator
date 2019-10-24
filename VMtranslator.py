#!/usr/bin/env python3
'''
Name: MIDN Shamugia Genadi
Course: SY303
Section: 4321
Description: Program takes a vm file as an input and translates it into hack assembly code (asm).
Usage:
  $ ./VMtranslator.py <program.vm>
'''
#Imported libraries
import sys
import random

def parser(inst):
    '''
    Description: Function parses the instruction and returns a tuple containing
                 instruction type and instuction arguments.
    Arguments:
        instruction
    Returns:
        tuple containing instruction type and instuction arguments
    '''
    items = (inst.strip()).split(" ")
    command = items[0]
    # Your code here
    if len(items)==1: #if only one item on line it is an arithmetic or logical command
        tup = ('C_ARITHMETIC',(command,None))
    elif len(items)==3: #Memory access command
        if command =="push": #Push command
            tup = ('C_PUSH',(command,(items[1],items[2])))
        else: #Pop Command
            tup = ('C_POP',(command,(items[1],items[2])))
    # Return a tuple containing the instruction type and the arguments (arg1, arg2)
    return tup

def code(instType, instArgs):
    '''
    Description: Based on the instruction type function calls either generateArithmetic() function or generateMemoryAccess() function.
    Arguments:
        instruction type and instruction arguments
    Returns:
        Assembly code which is going to be written to the output file
    '''
    # Determine the class of code that must be generated based on the type, then create it in an appropriate function
    if instType=="C_ARITHMETIC": # if arithmetic or logical operation
    # Need to generate Hack Assembly instructions to implement an Arithmetic or Logical VM instruction (suggested arguments included)
        assembly = generateArithmetic(instArgs[0])
        # print(instArgs[0])
    elif instType=="C_PUSH": #PUSH
        assembly = generateMemoryAccess(instArgs[0], (instArgs[1])[0], (instArgs[1])[1])
        # print(instArgs[0], (instArgs[1])[0], (instArgs[1])[1])
    else: #POP
    # Need to generate Hack Assembly instructions to implement a Memory Access VM instruction (push, pop) (suggested arguments included)
        assembly = generateMemoryAccess(instArgs[0], (instArgs[1])[0], (instArgs[1])[1])
        # print(instArgs[0], (instArgs[1])[0], (instArgs[1])[1])
    # Return the line(s) of Hack Assembly code which accomplish the requested VM instruction
    return assembly

def generateArithmetic(command):
    '''
    Description: Translates logical and arithmetic operations.
    Arguments:
        command
    Returns:
        The resulting sequence of assembly commands to perform the opperation
    '''
    counterJmp=str(random.randint(0,10000)) # get a random integer which we use to create unique conditional jump location
    # Your code here
    if command == "add": #Add top two items on the stack
        retStr= '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D+M'
    elif command =="sub": #Subtract top two items on the stack
        retStr= '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D-M'
    elif command =='neg': #Unary operation. Returns the negative of the item on the head of the stack
        retStr= '@SP\n'+"M=M-1\n"+'A=M\n'+'M=-M\n'+'@SP\n'+'M=M+1'
    elif command =='and': #And top two items on the head of the stack
        retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D&M'
    elif command =='or': #Or top two items on the head of the stack
        retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'M=D|M'
    elif command =='not': #Unary operation. returns !item from the head of the stack
        retStr= '@SP\n'+'M=M-1\n'+'A=M\n'+'M=!M\n'+'@SP\n'+'M=M+1'
    #For following conditional jumps we have have two locations JUMPTRUE and ENDJUMP. If The conditional is true the value RAM[@SP-2] is changed to 0, else it is replaced with -1.
    #Also by adding the 'counterJmp' to the label name we ensure that the locations are unique
    elif command =='eq': #Conditional jump checks for equality and jumps if equal. Handles stack pointer accordignly
        retStr='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JEQ'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    elif command =='gt': #Conditional jump checks for equality and jumps if greater than zero. Handles stack pointer accordignly
        retStr='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JGT'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    elif command =='lt': #Conditional jump checks for equality and jumps if less than zero. Handles stack pointer accordignly
        retStr='@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'A=A-1\n'+'D=M-D\n'+'@'+'JUMPTRUE'+counterJmp+'\n'+'D;'+'JLT'+'\n'+'@SP\n'+'A=M-1\n'+'M=0\n'+'@'+'ENDJUMP'+counterJmp+'\n'+'0;JMP\n'+'(JUMPTRUE'+counterJmp+')\n'+'@SP\n'+'A=M-1\n'+'M=-1\n'+'(ENDJUMP'+counterJmp+')'
    # Return a representation of Hack Assembly instruction(s) which implement the passed in command
    return retStr

def generateMemoryAccess(command, segment, index):
    '''
    Description: Function handles memory access commands. Push and Pop commands are being translated to appropriate assembly assembly code.
                 For each of push and pop command a different memory segment is used to translate the instrucions. returns a string of assembly code.
    Arguments:
        command, segment, index
    Returns:
        A string which is a translation of a specific push or pop command
    '''
    # Your code here
    if command =="push": #Push opperation adds an element to the top of the stack.
        if segment =="constant":
            retStr = '@'+str(index)+'\n'+'D=A\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='local': #points at the base of current VM function's local segment. We save the value at @LCL+offset and then push it on the stack.
            retStr = '@LCL\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='argument': #We save the value at @ARG+offset and push it on the stack
            retStr = '@ARG\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='this': #Get the value at @THIS+offset and push it on top of the stack
            retStr = '@THIS\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='that': #Get the value at @THAT+offset and push it on top of the stack
            retStr = '@THAT\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='pointer': #pointer is mapped to locations 3-4 on RAM. Therefore 'push pointer i' is translated to assembly code that accesses RAM location 3+i.
            retStr = '@R3\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='temp': #temp is mapped to locations 5-12 on RAM. Therefore 'push temp i' is translated to assembly code that accesses RAM location 5+i.
            retStr = '@R5\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'A=D\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'
        elif segment =='static': #We represent each variable J in file F as a symbol F.J. We store the value at that address in D register and then push it on stack.
            retStr = '@'+str((sys.argv[1].split('.'))[0])+'.'+str(index)+'\n'+'D=M\n'+'@SP\n'+'A=M\n'+'M=D\n'+'@SP\n'+'M=M+1'

    elif command =="pop": #Pop opperation removes the top element from the stack.
        if segment =="local": # Store the value of the @LCL+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@LCL\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='argument': #Store the value of the @ARG+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@ARG\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='this': #Store the value of the @THIS+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@THIS\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='that': #Store the value of the @THAT+offset in R13 register. Go to get the value at @SP-1 and set the RAM[@R13] to the value.
            retStr='@SP\n'+'M=M-1\n'+'@THAT\n'+'D=M\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='pointer': #Store the address of the desired offset in R13 register. Retrieve the value from top of the stack and put it inside the saved address location.
            retStr='@SP\n'+'M=M-1\n'+'@R3\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='temp':  #Store the address of the desired offset in R13 register. Retrieve the value from top of the stack and put it inside the saved address location.
            retStr='@SP\n'+'M=M-1\n'+'@R5\n'+'D=A\n'+'@'+str(index)+'\n'+'D=D+A\n'+'@R13\n'+'M=D\n'+'@SP\n'+'A=M\n'+'D=M\n'+'@R13\n'+'A=M\n'+'M=D'
        elif segment =='static': #Take the top element from the stack and put it inside the location of @F.J
            retStr = '@SP\n'+'M=M-1\n'+'A=M\n'+'D=M\n'+'@'+str((sys.argv[1].split('.'))[0])+'.'+str(index)+'\n'+'M=D'
    # Return a representation of Hack Assembly instruction(s) which implement the passed in command
    return retStr
######################################################################################################
# Define any additional helper functions here (include function descriptions)
def removeComments(lineList):
    '''
    Description: Function takes a list of all the lines from VM file and removes the comments
    Arguments:
        lineList
    Returns:
        A list of lines without the comments
    '''
    newList = [] #Initializiing an empty list for commands with comments removed.
    for line in lineList:
        if (line.strip()).startswith("//"): #Check if line startswith '//'. If yes, ignore.
            continue
        elif "//" in line: #If '//' in line together with command, only leave command part and remove comment.
            removedComms=line.split('//')[0].strip()
            newList.append(removedComms)
        elif line=="\n": #Ignore newlines (Empty lines)
            continue
        else:
            newList.append(line.strip()) #If not newline or comment append to command list.
    return newList #Return the list of only commands.
######################################################################################################

def main():
    '''
    Description: Open the input and output files. Remove comments from the input file and for each line
                 of VM code provide appropriate asm instrucions and write them to the output file.
    '''
    # Read filename from command line argument
    # Open the input .vm file with that filename
    fdIn = open(sys.argv[1],'r')
    # Create and open the output .asm file with the same basename
    outputFilename = (sys.argv[1].split("."))[0] + ".asm"
    fdOut = open(outputFilename,'w')
    # Read each VM instruction in the input file
    inFileRead = fdIn.readlines()
    #Remove comments from the input file
    inFileRead = removeComments(inFileRead)
    # print(inFileRead)
    # For each instruction:
    for instruction in inFileRead:
        # Parse the instruction into its type (eg. Arithmetic, Push, Pop) and arguments and return them in a tuple
        # print(parser(instruction))
        instruction_type, instruction_arguments = parser(instruction)
        # Generate the corresponding Hack Assembly code of that parsed instruction as a string
        assembly_code = code(instruction_type, instruction_arguments)
        # Write that binary string to the output file
        fdOut.write(assembly_code+'\n')
    # Be nice and close the files when you are done!
    fdIn.close()
    fdOut.close()
# Include code below to ONLY call the main function when the program is run from the command line; i.e. a standalone program
if __name__ =="__main__":
    main()
