import re
from collections import deque

def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_operator(token):
    return token in "*/+-"

class Compiler:
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
    
    def tokenize(self, program):
        regex = re.compile(r'\s*([-+*/\(\)\[\]]|[A-Za-z]+|[0-9]+)\s*')
        tokens = regex.findall(program)
        return [int(tok) if tok.isdigit() else tok for tok in tokens]

    def pass1(self, program):
        tokens = self.tokenize(program)
        output_queue = deque()
        operator_stack = deque()
        args = []
        token_index = 0

        def get_next_token():
            nonlocal token_index
            if token_index < len(tokens):
                token = tokens[token_index]
                token_index += 1
                return token
            return None

        def precedence_is_not_greater(o1, o2):
            precedences = {'/': 3, '*': 3, '+': 2, '-': 2}
            return precedences[o1] <= precedences[o2]

        def build_ast(output_queue):
            output = output_queue.pop()
            node = {}

            if is_number(output):
                node['op'] = 'imm'
                node['n'] = output
            elif output in args:
                node['op'] = 'arg'
                node['n'] = args.index(output)
            elif is_operator(output):
                node['op'] = output
                b = build_ast(output_queue)
                a = build_ast(output_queue)
                node['a'] = a
                node['b'] = b

            return node

        while True:
            token = get_next_token()
            if token is None:
                break

            if token == '[':
                while (next_token := get_next_token()) != ']':
                    args.append(next_token)
            elif is_number(token) or token in args:
                output_queue.append(token)
            elif is_operator(token):
                while (operator_stack and is_operator(operator_stack[-1]) and
                       precedence_is_not_greater(token, operator_stack[-1])):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return build_ast(output_queue)

    def pass2(self, ast):
        def reduce_tree(ast):
            if ast['op'] in {'imm', 'arg'}:
                return ast
            ast['a'] = reduce_tree(ast['a'])
            ast['b'] = reduce_tree(ast['b'])
            if ast['a']['op'] == 'imm' and ast['b']['op'] == 'imm':
                n = eval(f"{ast['a']['n']} {ast['op']} {ast['b']['n']}")
                return {'op': 'imm', 'n': n}
            return ast
        
        return reduce_tree(ast)

    def pass3(self, ast):
        operator_map = {'+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}
        operation_depths = {}
        max_depth = float('-inf')

        def mark_depth(ast, depth=0):
            nonlocal max_depth
            if 'a' in ast and 'b' in ast:
                max_depth = max(max_depth, depth)
                if depth not in operation_depths:
                    operation_depths[depth] = []
                operation_depths[depth].append(ast)
                mark_depth(ast['a'], depth + 1)
                mark_depth(ast['b'], depth + 1)

        mark_depth(ast)
        asm = []

        current_depth = max_depth
        while current_depth >= 0:
            current_depth_operations = operation_depths.get(current_depth, [])
            while current_depth_operations:
                current_operation = current_depth_operations.pop(0)

                # Handle right branch
                if current_operation['b']['op'] == 'imm':
                    asm.append(f'IM {current_operation["b"]["n"]}')
                elif current_operation['b']['op'] == 'arg':
                    asm.append(f'AR {current_operation["b"]["n"]}')
                else:
                    asm.append('PO')

                asm.append('SW')

                # Handle left branch
                if current_operation['a']['op'] == 'imm':
                    asm.append(f'IM {current_operation["a"]["n"]}')
                elif current_operation['a']['op'] == 'arg':
                    asm.append(f'AR {current_operation["a"]["n"]}')
                else:
                    asm.append('PO')

                # Apply operation
                asm.append(operator_map[current_operation['op']])

                # Push result to stack
                asm.append('PU')

            current_depth -= 1

        return asm
