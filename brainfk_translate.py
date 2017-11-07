from getch import getche
from types import SimpleNamespace

source =  '''
HELLO BRAINFUCK!
+
-
-
+
+++++++,
.
'''

ctx = SimpleNamespace(tokens=[], indent=0)

ctx.tokens.append('#include "stdio.h"\n')
ctx.tokens.append('#include "stdlib.h"\n')
ctx.tokens.append('\nint main() {\n')

ctx.indent += 1

def bf(source):
    """
    Executa uma string de código brainf*ck e retorna
    o estado final da fita de memória.
    """

    data = [0]
    ptr = 0
    code_ptr = 0
    breakpoints = []

    while code_ptr < len(source):
        cmd = source[code_ptr]

        if cmd == '+':
            data[ptr] = (data[ptr] + 1) % 256
            ctx.tokens.append(('    ' * ctx.indent) + 'caracter[ptr]++;\n')
        elif cmd == '-':
            data[ptr] = (data[ptr] - 1) % 256
            ctx.tokens.append(('    ' * ctx.indent) + 'caracter[ptr]--;\n')
        elif cmd == '>':
            ptr += 1
            ctx.tokens.append(('    ' * ctx.indent) + 'ptr++;\n')
            if ptr == len(data):
                data.append(0)
        elif cmd == '<':
            ptr -= 1
            ctx.tokens.append(('    ' * ctx.indent) + 'ptr--;\n')
        elif cmd == '.':
            ctx.tokens.append(('    ' * ctx.indent) + 'putchar(data[ptr]);\n')
        elif cmd == ',':
            data[ptr] = ord(getche())
            ctx.tokens.append(('    ' * ctx.indent) + 'data[ptr] = getchar(data[ptr]);\n')
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


    ctx.tokens.append('\n' + '    ' + 'return 0;\n')
    ctx.tokens.append('}\n')

    print(''.join(ctx.tokens))

    return data

bf(source)
