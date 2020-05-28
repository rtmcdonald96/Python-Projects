#  Ryan McDonald, Alexander Frederick
#  05/13/2020
#  Assignment 3
#  Requires the input file to have spaces between every single "word"
#  Identifies differences between floats and integers as well as recognizing positive and negative numbers
#  Ignores all block comments from input file. Whether in the middle of the line or at the end of the line
#  Identifiers, keywords, and separators lists can be easily modified by modifying the corresponding files
#  to add or remove symbols. Mutli-symbol operators are also able to read with this iteration
#  This assignment generates a symbol table as well as has error handling built in place to detect whether an identifier
#  is being used before it has been declared.  Our project 2 was originally built in C++
#  so for assignment 3 we rebuilt the entire process from the ground up. Assembly code and symbol tables are outputted
#  to the console as well as our output.txt file

import functions

keywords = []
separators = []
operators = []
identifiers = []
parsed_values = []
symbol_table = []
instructions = []
assembly_instructions = []

functions.load_lists("keyword.txt", keywords)
functions.load_lists("operator.txt", operators)
functions.load_lists("separator.txt", separators)

functions.parse("input.txt", keywords, separators, operators, identifiers, "output.txt", parsed_values, symbol_table,
                instructions)
functions.gen_assy(instructions, symbol_table, assembly_instructions, identifiers)

open('output.txt', 'w').close()

output_file = open("output.txt", "a")
print("=== Start of Symbol Table ===")
output_file.write("=== Start of Symbol Table ===\n")
for x in range(0, len(symbol_table)):
    print(symbol_table[x])
    output_file.write(str(symbol_table[x]) + '\n')

print("=== Start of Assembly Code ===")
output_file.write("=== Start of Assembly Table ===\n")
for x in range(0, len(assembly_instructions)):
    print(str(x+1) + ' ' + assembly_instructions[x])
    output_file.write(str(x+1) + ' ' + assembly_instructions[x] + '\n')
output_file.close()
