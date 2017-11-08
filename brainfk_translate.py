from getch import getche
from types import SimpleNamespace
import click

ctx = SimpleNamespace(tokens=[], indent=0)
ctx.indent += 1

def pre_process_source(source):
    counter = 0
    previous_operation = ""
    pre_processed_operations = ""
    valid_operations = "+-<>.,[]"

    for operation in source:
        if(valid_operations.find(operation) != -1):

            if(operation == "[" or operation == "]"):
                pre_processed_operations += str(counter) + previous_operation
                counter = 1

                previous_operation = operation
            else:
                if(operation == previous_operation):
                    counter += 1
                else:
                    pre_processed_operations += str(counter) + previous_operation
                    counter = 1

                previous_operation = operation
    
    pre_processed_operations += str(counter) + previous_operation

    pre_processed_operations = pre_processed_operations[1:]
    return pre_processed_operations

def bf(ctx, source):
    data = [0]
    ptr = 0
    code_ptr = 0
    depth = 0
    breakpoints = []

    ctx.tokens.append('\tunsigned char character[42042];\n')
    ctx.tokens.append('\tunsigned int ptr;\n\n')

    pre_processed_operations = pre_process_source(source)

    while code_ptr < len(pre_processed_operations):
        number_of_ocurrences = ""
        while(pre_processed_operations[code_ptr].isdigit()):
            number_of_ocurrences += pre_processed_operations[code_ptr]
            code_ptr+=1

        cmd = pre_processed_operations[code_ptr]

        if cmd == '+':
            data[ptr] = (data[ptr] + 1) % 256
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'character[ptr]+={};\n'.format(number_of_ocurrences))
        elif cmd == '-':
            data[ptr] = (data[ptr] - 1) % 256
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'character[ptr]-={};\n'.format(number_of_ocurrences))
        elif cmd == '>':
            ptr += 1
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'ptr+={};\n'.format(number_of_ocurrences))
            if ptr == len(data):
                data.append(0)
        elif cmd == '<':
            ptr -= 1
            ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'ptr-={};\n'.format(number_of_ocurrences))
        elif cmd == '.':
            if(number_of_ocurrences == "1"):
                ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'putchar(character[ptr]);\n')
            else:
                ctx.tokens.append(('\t' * (ctx.indent + depth)) + 
                'for(int i = 0;i < {};++i)'.format(number_of_ocurrences) + '{' + '\n')
                ctx.tokens.append(('\t' * (ctx.indent + (depth + 1))) + 'putchar(character[ptr]);\n')
                ctx.tokens.append(('\t' * (ctx.indent + depth)) + '}\n')
        elif cmd == ',':
            if(number_of_ocurrences == "1"):
                ctx.tokens.append(('\t' * (ctx.indent + depth)) + 'character[ptr] = getchar();\n')
            else:
                ctx.tokens.append(('\t' * (ctx.indent + depth)) + 
                'for(int i = 0;i < {};++i)'.format(number_of_ocurrences) + '{' + '\n')
                ctx.tokens.append(('\t' * (ctx.indent + (depth + 1))) + 'character[ptr] = getchar();\n')
                ctx.tokens.append(('\t' * (ctx.indent + depth)) + '}\n')
                
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
