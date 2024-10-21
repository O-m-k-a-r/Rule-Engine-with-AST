class Node:
    def __init__(self, type, value=None, left = None, right = None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

import re
def tokenize(rule_string):
    token_pattern = r'(\(|\)|AND|OR|=|>|<|\'[^\']*\'|\w+|\d+)'
    return re.findall(token_pattern, rule_string)

# def tokenize(rule_string):
#     token_pattern = r"(\b\w+\b|[><=!]=|['\"].*?['\"]|\(|\)|AND|OR)"
#     tokens = re.findall(token_pattern, rule_string)
#     return tokens

def build_ast(tokens):
    operators = []
    operands = []
    precedence = {'OR': 1, 'AND': 2}

    def apply_operator():
        operator = operators.pop()
        right = operands.pop()
        left = operands.pop()
        new_node = Node(type='operator', value=operator, left=left, right=right)
        operands.append(new_node)

    current_operand = ""  # To store combined operand

    for token in tokens:
        if token == '(':
            if current_operand:
                operands.append(Node(type='operand', value=current_operand.strip()))
                current_operand = ""
            operators.append(token)
        elif token == ')':
            if current_operand:
                operands.append(Node(type='operand', value=current_operand.strip()))
                current_operand = ""
            while operators and operators[-1] != '(':
                apply_operator()
            operators.pop()  # Pop the '(' from the stack
        elif token in precedence:
            if current_operand:
                operands.append(Node(type='operand', value=current_operand.strip()))
                current_operand = ""
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                apply_operator()
            operators.append(token)
        else:
            # This is part of an operand (e.g., age, >, 30, etc.)
            current_operand += token + " "

    # If there's any remaining operand, add it
    if current_operand:
        operands.append(Node(type='operand', value=current_operand.strip()))

    # Apply remaining operators
    while operators:
        apply_operator()

    # The root of the AST will be the last remaining node in operands
    return operands[-1] if operands else None



def create_rule(rule_string):
    tokens = tokenize(rule_string)
    print("Tokens", tokens)
    ast = build_ast(tokens)    
    return ast


sample_rule = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
ast = create_rule(sample_rule)
# def print_ast(node, indent=0):
#     if node:
#         print(' ' * indent + f'Node type: {node.node_type}, value: {node.value}')
#         print_ast(node.left, indent + 2)
#         print_ast(node.right, indent + 2)


# def print_ast(node, indent=0):
#     if node:
#         # Print the current node with indentation
#         print(' ' * indent + f"Node(type='{node.node_type}', value='{node.value}')")
        
#         # Recursively print the left and right children with increased indentation
#         if node.left:
#             print(' ' * (indent + 2) + "Left:")
#             print_ast(node.left, indent + 4)
#         if node.right:
#             print(' ' * (indent + 2) + "Right:")
#             print_ast(node.right, indent + 4)

# Print the AST for inspection
#print_ast(ast)
print("AST Structure:")
def print_ast(node, level=0):
    """Recursively print the AST in a structured format."""
    if node is not None:
        indent = '  ' * level
        print(f"{indent}{node.type}: {node.value}")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)


print_ast(ast)
