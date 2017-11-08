from getch import getche
from types import SimpleNamespace
import click

source =  '''
HELLO BRAINFUCK!
++++++[--+]
'''

ctx = SimpleNamespace(tokens=[], indent=0)
ctx.indent += 1

def pre_process():
    counter = 0
    previous_operation = ""
    pre_processed_operations = ""

    for operation in source:
        if(operation == "+"):
            if(previous_operation == "+"):
                counter += 1
            else:
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

            previous_operation = "+"
        
        elif(operation == "-"):
            if(previous_operation == "-"):
                counter += 1
            else:
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

            previous_operation = "-"

        elif(operation == ">"):
            if(previous_operation == ">"):
                counter += 1
            else:
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

            previous_operation = ">"

        elif(operation == "<"):
            if(previous_operation == "<"):
                counter += 1
            else:
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

            previous_operation = "<"

        elif(operation == "."):
            if(previous_operation == "."):
                counter += 1
            else:
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

            previous_operation = "."

        elif(operation == ","):
            if(previous_operation == ","):
                counter += 1
            else:
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

            previous_operation = ","

        else:
            pre_processed_operations += str(counter) + previous_operation
            counter = 1

            previous_operation = operation

    
    pre_processed_operations += str(counter) + previous_operation
    
    print(pre_processed_operations[1:])

def bf(ctx, source):
    data = [0]
    ptr = 0
    code_ptr = 0
    depth = 0
    breakpoints = []

    ctx.tokens.append('\tunsigned char character[42042];\n')
    ctx.tokens.append('\tunsigned int ptr;\n\n')

    while code_ptr < len(source):
        cmd = source[code_ptr]

        if cmd == '+':
            data[ptr] = (data[ptr] + 1) % 256
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'character[ptr]++;\n')
        elif cmd == '-':
            data[ptr] = (data[ptr] - 1) % 256
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'character[ptr]--;\n')
        elif cmd == '>':
            ptr += 1
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'ptr++;\n')
            if ptr == len(data):
                data.append(0)
        elif cmd == '<':
            ptr -= 1
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'ptr--;\n')
        elif cmd == '.':
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'putchar(character[ptr]);\n')
        elif cmd == ',':
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'character[ptr] = getchar();\n')
        elif cmd == '[':
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'while(character[ptr] != 0){\n')
            depth += 1 
        elif cmd == ']':
            depth -= 1
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + '}\n')
        code_ptr += 1

    ctx.tokens.append('\n\treturn 0;\n')
    ctx.tokens.append('}\n')

    return ''.join(ctx.tokens)

@click.command()
@click.argument('entry_file_name')
@click.option('-o', nargs=1)

def compiled_c(o, entry_file_name):
    input_file = open(entry_file_name, 'r')

    entry_arg = '%s' % o

    args = SimpleNamespace(tokens=[])

    for line in input_file:
        args.tokens.append(line)

    input_file.close()

    source = bf(ctx, ''.join(args.tokens))

    output_file = open(entry_arg, 'w')

    output_file.write('#include <stdio.h>\n')
    output_file.write('#include <stdlib.h>\n')
    output_file.write('\nint main() {\n')
    output_file.write(source)

    output_file.close()
    input_file.close()

compiled_c()
