def load_lists(file, my_list):
    for line in open(file):  # opened in text-mode; all EOLs are converted to '\n'
        for word in line.split():  # breaks up each line into words based on spaces
            my_list.append(word)  # appends keyword from text file to end of keyword list


# =====================================================================================
# Check functions. Checks what type of word each word from the input file is
# =====================================================================================

def check_number(word, output, parsed_values):  # Function checks whether a number is a float or an integer
    for x in range(1, len(word)):  # Checks if any characters in the word is not a digit or a '.'
        if not (word[x].isdigit() or word[x] == "."):
            return False
    count = 0
    for char in word:
        if char == '.':  # for each '.' the count is increased by one. A float would have one period, if a word
            count += 1  # has more than one '.' then it is invalid
            if count > 1:
                return False
            # allows a '-' to be present at the front of a number
        if not (char == "-" or char == "+" or char == "." or char.isdigit()):
            return False
    if count == 1:  # if the count is one then there is one '.' so it is a floating point
        # print_float(word, output, parsed_values)
        return True
    elif count == 0:  # if the count is zero there are no '.'s so it is an integer
        # print_integer(word, output, parsed_values)
        return True
    else:
        return False


def check_valid_identifier(word, identifiers, symbol_table, last_keyword, memory_loc):
    # If the first character isn't a letter it returns false
    for char in word:
        if not char.isalpha():
            return False
        else:
            # Checks if the remaining letters are any of the valid characters
            for char in word:
                if not (char.isalpha() or char.isdigit() or char == "$"):
                    return False
            identifiers.append(word)
            if last_keyword == "INVALID":
                print(word + " was not declared before being used")
            else:
                my_tuple = (word, memory_loc, last_keyword)
                symbol_table.append(my_tuple)
            return True


# =====================================================================================
# Print functions. Prints what type of word each word from the input file is
# =====================================================================================


def print_notvalid(word, output):
    print("INVALID 	=	 " + word)
    f = open(output, "a+")
    f.write("INVALID 	=	 " + word + "\n")
    f.close()


def print_valid(word, output, values):
    print("IDENTIFIER 	=	 " + word)
    f = open(output, "a+")
    f.write("IDENTIFIER 	=	 " + word + "\n")
    f.close()
    add_to_list("IDENTIFIER", word, values)


def print_style(output):
    print("TOKENS			 Lexemes")
    f = open(output, "a+")
    f.write("TOKENS			 Lexemes" + "\n")
    f.close()


def print_float(word, output, values):
    print("FLOAT   	=	 " + word)
    f = open(output, "a+")
    f.write("FLOAT   	=	 " + word + "\n")
    f.close()
    add_to_list("FLOAT", word, values)


def print_keyword(word, output, values):
    print("KEYWORD         =        " + word)
    f = open(output, "a+")
    f.write("KEYWORD         =        " + word + "\n")
    f.close()
    add_to_list("KEYWORD", word, values)


def print_separator(word, output, values):
    print("SEPARATOR 	=	 " + word)
    f = open(output, "a+")
    f.write("SEPARATOR 	=	 " + word + "\n")
    f.close()
    add_to_list("SEPARATOR", word, values)


def print_operator(word, output, values):
    print("OPERATOR 	=        " + word)
    f = open(output, "a+")
    f.write("OPERATOR 	=        " + word + "\n")
    f.close()
    add_to_list("OPERATOR", word, values)


def print_integer(word, output, values):
    print("INTEGER 	=	 " + word)
    f = open(output, "a+")
    f.write("INTEGER 	=	 " + word + "\n")
    f.close()
    add_to_list("INTEGER", word, values)


# =====================================================================================
# Clear_file function. Removes any existing content from the file so the output file
# stays clean and only holds information from one usage of the Lexical Analyzer
# =====================================================================================


def clear_file(file):
    with open(file, "w"):
        pass


# =====================================================================================
# Clear_file function. Removes any existing content from the file so the output file
# stays clean and only holds information from one usage of the Lexical Analyzer
# =====================================================================================


def add_to_list(token, lexeme, my_list):
    mytuple = (token, lexeme)
    my_list.append(mytuple)


# =====================================================================================
# Parse function. Iterates through the check functions then calls the corresponding
# print function to match the type of word.
# =====================================================================================


def parse(file, keywords, separators, operators, identifiers, output, parsed_values, symbol_table, instructions):
    last_keyword = 'INVALID'
    memory_loc = 5000
    # print_style(output)
    clear_file(output)
    in_comment = 0
    for line in open(file):
        for word in line.split():
            # The comment_state variable is used to keep track of if the words being parsed are inside of a comment
            # If the comment_state is equal to zero then it is not inside of a comment, so every word is parsed
            # to identify what it is. If comment_state is equal to 1 then it is inside of a comment so it only checks
            # if the word is a '!' to see if we are exiting the comment. Any other input leaves us in the same
            # comment_state so we do not exit the comment.
            if not in_comment:
                if word in identifiers:
                    # print_valid(word, output, parsed_values)
                    identifiers.append(word)
                    instructions.append(word)
                elif word in keywords:
                    last_keyword = word
                    # print_keyword(word, output, parsed_values)
                    instructions.append(word)
                elif word in separators:
                    instructions.append(word)
                    if word == ";":
                        last_keyword = 'INVALID'
                        # print_separator(word, output, parsed_values)

                elif word in operators:
                    # print_operator(word, output, parsed_values)
                    instructions.append(word)
                elif check_number(word, output, parsed_values):
                    instructions.append(word)
                    pass
                elif check_valid_identifier(word, identifiers, symbol_table, last_keyword, memory_loc):
                    # print_valid(word, output, parsed_values)
                    instructions.append(word)
                    memory_loc += 1
                elif word == "!":
                    in_comment = 1
                else:
                    print_notvalid(word, output)
            elif word == "!":
                in_comment = 0


# =====================================================================================
# gen_assy function. Iterates through the tokens to generate logical lines.  On a logical line generated
# function will then parse the line through the rules in order to generate assembly instructions
# =====================================================================================

def gen_assy(instructions, symbol_table, assembly_instructions, identifiers):
    temp_line = []
    ins_line = []
    jump_stack = []
    while_loop = 0
    bracket_counter = 0
    label_spot = 0
    for x in range(0, len(instructions)):
        if instructions[x] == ')':
            temp_line.append(')')
        if not (instructions[x] == ';' or instructions[x] == ')'):
            temp_line.append(instructions[x])
        else:
            # print(temp_line)
            if temp_line.__contains__('}'):
                if while_loop == 1:
                    bracket_counter -= 1
                    if bracket_counter == 0:
                        assembly_instructions.append("Jump " + str(label_spot))
                        jumpz_modify(assembly_instructions)
                jumpz_modify(assembly_instructions)
            if temp_line.__contains__('input'):
                input_rule(temp_line, symbol_table, assembly_instructions, identifiers)

            if temp_line.__contains__('if'):
                condition_rule(temp_line, symbol_table, assembly_instructions, identifiers)
                assembly_instructions.append("Jumpz")
            if temp_line.__contains__('+') or temp_line.__contains__('-') \
                    or temp_line.__contains__('*') or temp_line.__contains__('/'):
                arithmetic_rule(temp_line, symbol_table, assembly_instructions, identifiers)
                if not (temp_line.__contains__('output')):
                    for y in range(0, len(temp_line)):
                        if temp_line[y] in identifiers:
                            assembly_instructions.append("Popm " + str(get_mem_loc(temp_line[y], symbol_table)))
                            break
            elif temp_line.__contains__('='):
                assign_rule(temp_line, symbol_table, assembly_instructions, identifiers)
            if temp_line.__contains__('output'):
                # arithmetic_rule(temp_line, symbol_table, assembly_instructions, identifiers)
                output_rule(temp_line, symbol_table, assembly_instructions, identifiers)
            if temp_line.__contains__("while"):
                while_loop = 1
                assembly_instructions.append("Label")
                label_spot = len(assembly_instructions)
                condition_rule(temp_line, symbol_table, assembly_instructions, identifiers)
                assembly_instructions.append("Jumpz")
            if temp_line.__contains__('('):
                pass
            if temp_line.__contains__(')'):
                pass
            if temp_line.__contains__('{'):
                if while_loop == 1:
                    bracket_counter += 1
            if temp_line.__contains__('<'):
                pass
            if temp_line.__contains__('>'):
                pass
            if temp_line.__contains__('else'):
                pass
            ins_line.append(temp_line)
            temp_line.clear()


# =====================================================================================
# condition_rule function.  Breaks up the logical line containing if ( ) in order to identify
# the relational set used.  Generates the Assembly instruction for relation
# =====================================================================================

def condition_rule(temp_line, symbol_table, assembly_instructions, identifiers):
    instruction = 0
    for word in temp_line:
        if word == 'if':
            pass
        elif word == '(':
            pass
        elif word.isnumeric():
            assembly_instructions.append("Pushi " + str(word))
        elif word == ')':
            break
        elif word == '<':
            instruction = 1
        elif word == '==':
            instruction = 2
        elif word == '>':
            instruction = 3
        elif word == '<=':
            instruction = 4
        elif word == '>=':
            instruction = 5
        elif word == '!=':
            instruction = 6
        elif word in identifiers:
            assembly_instructions.append("Pushm " + str(get_mem_loc(word, symbol_table)))
    if instruction == 1:
        assembly_instructions.append('LES')
    elif instruction == 2:
        assembly_instructions.append('EQU')
    elif instruction == 3:
        assembly_instructions.append('GRT')
    elif instruction == 4:
        assembly_instructions.append('LEQ')
    elif instruction == 5:
        assembly_instructions.append('GEQ')
    elif instruction == 6:
        assembly_instructions.append('NEQ')


# =====================================================================================
# get_mem_loc function.  returns a memory location value for a word that is matched
# =====================================================================================

def get_mem_loc(word, symbol_table):
    for x in range(0, len(symbol_table)):
        symbol, mem_loc, type = symbol_table[x]
        if word == symbol:
            return mem_loc


# =====================================================================================
# assign_rule function.  Conducts the assign rule, sends true/false as 1/0,
# acquires the memory_loc of a value, and puts it in the assigned mem location
# =====================================================================================

def assign_rule(temp_line, symbol_table, assembly_instructions, identifiers):
    id_count = 0
    id_num = 0
    temp_string = 'hi'
    for word in temp_line:
        if word in identifiers:
            id_count += 1
    if id_count == 1:
        for word in temp_line:
            if word == '=':
                pass
            elif word == 'true':
                assembly_instructions.append("Pushi 1")
            elif word == 'false':
                assembly_instructions.append("Pushi 0")
            elif word.isnumeric():
                assembly_instructions.append("Pushi " + str(word))
            elif word in identifiers:
                temp_string = ("Popm " + str(get_mem_loc(word, symbol_table)))
        assembly_instructions.append(temp_string)
    if id_count == 2:
        for word in temp_line:
            if word in identifiers:
                id_num += 1
                if id_num == 1:
                    temp_string = ("Popm " + str(get_mem_loc(word, symbol_table)))
                if id_num == 2:
                    assembly_instructions.append("Pushm " + str(get_mem_loc(word, symbol_table)))
        assembly_instructions.append(temp_string)


# =====================================================================================
# arithmetic_rule function.  Conducts the arithmetic rules. Grabs the MUL/DIV values
# first, then ADD/SUB, will then push the 2 values, produce the appropriate assembly command
# and leave function to allow assign
# =====================================================================================
def arithmetic_rule(temp_line, symbol_table, assembly_instructions, identifiers):
    id_count = 0
    id_num = 0
    temp_string = 'hi'
    add_flag = False
    sub_flag = False
    mul_flag = False
    div_flag = False
    temp_ins = []
    temp_line.reverse()
    if temp_line.__contains__('*') or temp_line.__contains__('/'):
        for word in temp_line:
            if word.isnumeric():
                temp_string = ("Pushi " + str(word))
                temp_ins.append(temp_string)
                # assembly_instructions.append("Pushi " + str(word))
                if (mul_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('MUL')
                    mul_flag = False
                    # temp_ins.clear()
                if (div_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('DIV')
                    div_flag = False
                    # temp_ins.clear()
            elif word in identifiers:
                temp_string = ("Pushm " + str(get_mem_loc(word, symbol_table)))
                temp_ins.append(temp_string)
                # assembly_instructions.append(temp_string)
                if (mul_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('MUL')
                    mul_flag = False
                    # temp_ins.clear()
                if (div_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('DIV')
                    div_flag = False
                    # temp_ins.clear()
            elif word == '*':
                mul_flag = True
                # assembly_instructions.append('MUL')
            elif word == '/':
                div_flag = True
                # assembly_instructions.append('DIV')
    if temp_line.__contains__('+') or temp_line.__contains__('-'):
        for word in temp_line:
            if word.isnumeric():
                temp_string = ("Pushi " + str(word))
                temp_ins.append(temp_string)
                # assembly_instructions.append("Pushi " + str(word))
                if (add_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('ADD')
                    add_flag = False
                    # temp_ins.clear()
                if (sub_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('SUB')
                    sub_flag = False
                    # temp_ins.clear()
            elif word in identifiers:
                temp_string = ("Pushm " + str(get_mem_loc(word, symbol_table)))
                temp_ins.append(temp_string)
                # assembly_instructions.append(temp_string)
                if (add_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('ADD')
                    add_flag = False
                if (sub_flag):
                    assembly_instructions.append(temp_ins[1])
                    assembly_instructions.append(temp_ins[0])
                    assembly_instructions.append('SUB')
                    sub_flag = False
            elif word == '+':
                add_flag = True
            elif word == '-':
                sub_flag = True
    temp_line.reverse()


# =====================================================================================
# jumpz_modify function.  Allows for the last jumpz to be updated to the correct end of
# scope line.
# =====================================================================================
def jumpz_modify(assembly_instructions):
    my_value = len(assembly_instructions) + 1
    for y in range(0, len(assembly_instructions)):
        if assembly_instructions[y] == 'Jumpz':
            assembly_instructions[y] = ('Jumpz ' + str(my_value))


# =====================================================================================
# input_rule function. Conducts the STDIN rule, adds instruction to assembly list
# =====================================================================================
def input_rule(temp_line, symbol_table, assembly_instructions, identifiers):
    for word in temp_line:
        if word == 'input':
            assembly_instructions.append('STDIN')
        elif word == '(':
            pass
        elif word in identifiers:
            assembly_instructions.append("Popm " + str(get_mem_loc(word, symbol_table)))
        elif word == ')':
            pass


# =====================================================================================
# output_rule function. Conducts the STDOUT rule, adds instruction to assembly list
# =====================================================================================
def output_rule(temp_line, symbol_table, assembly_instructions, identifiers):
    for word in temp_line:
        if word == 'output':
            assembly_instructions.append('STDOUT')
            break
