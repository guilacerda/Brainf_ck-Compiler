from getch import getche
from types import SimpleNamespace
import click

ctx = SimpleNamespace(tokens=[], indent=0)
ctx.indent += 1

def bf(ctx, source):
    data = [0]
    ptr = 0
    code_ptr = 0
    breakpoints = []

    ctx.tokens.append('\tunsigned char caracter[42042];\n')
    ctx.tokens.append('\tunsigned int ptr;\n\n')

    while code_ptr < len(source):
        cmd = source[code_ptr]

        if cmd == '+':
            data[ptr] = (data[ptr] + 1) % 256
            ctx.tokens.append(('\t' * ctx.indent) + 'caracter[ptr]++;\n')
        elif cmd == '-':
            data[ptr] = (data[ptr] - 1) % 256
            ctx.tokens.append(('\t' * ctx.indent) + 'caracter[ptr]--;\n')
        elif cmd == '>':
            ptr += 1
            ctx.tokens.append(('\t' * ctx.indent) + 'ptr++;\n')
            if ptr == len(data):
                data.append(0)
        elif cmd == '<':
            ptr -= 1
            ctx.tokens.append(('\t' * ctx.indent) + 'ptr--;\n')
        elif cmd == '.':
            ctx.tokens.append(('\t' * ctx.indent) + 'putchar(caracter[ptr]);\n')
        elif cmd == ',':
            ctx.tokens.append(('\t' * ctx.indent) + 'caracter[ptr] = getchar();\n')
        elif cmd == '[':
            if data[ptr] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    code_ptr += 1
                    if source[code_ptr] == '[':
                        open_brackets += 1
                    elif source[code_ptr] == ']':
                        open_brackets -= 1
            else:
                breakpoints.append(code_ptr)
        elif cmd == ']':
            # voltar para o colchete correspondente
            code_ptr = breakpoints.pop() - 1

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
