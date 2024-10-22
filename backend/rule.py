class Node:
    def __init__(self, type, value=None, left = None, right = None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"

    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
    @classmethod
    def from_dict(cls, node_dict):
        if node_dict is None:
            return None
        return cls(
            type=node_dict['type'],
            value=node_dict['value'],
            left=cls.from_dict(node_dict['left']),
            right=cls.from_dict(node_dict['right'])
        )

import re
def tokenize(rule_string):
    token_pattern = r'(\(|\)|AND|OR|=|>|<|\'[^\']*\'|\w+|\d+)'
    return re.findall(token_pattern, rule_string)


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
    #print("Tokens", tokens)
    ast = build_ast(tokens)    
    return ast

#print("AST Structure:")
def print_ast(node, level=0):
    """Recursively print the AST in a structured format."""
    if node is not None:
        indent = '  ' * level
        print(f"{indent}{node.type}: {node.value}")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)


def evaluate_rule(node, data):
    """
    Recursively evaluate the AST based on the input data.
    
    Args:
    - node: The root node of the AST to evaluate.
    - data: A dictionary representing user attributes (e.g., {"age": 35, "department": "Sales", ...})
    
    Returns:
    - True if the rule evaluates to True for the given data, False otherwise.
    """
    if node.type == 'operand':
        # Evaluate the condition in the operand node
        print("Operand Node", node.value)
        return evaluate_condition(node.value, data)
    
    elif node.type == 'operator':
        # Recursively evaluate left and right nodes
        print("Root node", node, "Left Node", node.left)
        left_result = evaluate_rule(node.left, data)
        print("Left Result", left_result)
        print("Root node", node, "Right Node", node.right)
        right_result = evaluate_rule(node.right, data)
        print("Right Result", right_result)
        # Apply the operator (AND or OR)
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
    
    return False

def evaluate_condition(condition, data):
    """
    Evaluate a single condition (operand) like "age > 30" against the data dictionary.
    
    Args:
    - condition: A string representing the condition (e.g., "age > 30")
    - data: A dictionary containing user data (e.g., {"age": 35, "department": "Sales", ...})
    
    Returns:
    - True if the condition is satisfied, False otherwise.
    """
    # Split the condition into field, operator, and value
    # Example: "age > 30" -> field = "age", operator = ">", value = "30"
    
    tokens = condition.split()
    
    if len(tokens) != 3:
        raise ValueError(f"Invalid condition: {condition}")
    
    field, operator, value = tokens
    value = parse_value(value)  # Convert value to int/float if needed
    
    # Get the actual value from the data dictionary
    if field not in data:
        return False  # Field doesn't exist in data
    
    actual_value = data[field]
    print("JSON Value", actual_value)
    print("Code Value", value)
    
    # Compare based on the operator
    if operator == '>':
        return actual_value > value
    elif operator == '<':
        return actual_value < value
    elif operator == '>=':
        return actual_value >= value
    elif operator == '<=':
        return actual_value <= value
    elif operator == '=':
        return actual_value == value
    elif operator == '!=':
        return actual_value != value
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    
def parse_value(value):
    """
    Convert a string value into an appropriate type (int, float, or string).
    
    Args:
    - value: The string representation of the value.
    
    Returns:
    - The value converted to int, float, or string.
    """
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        # If it's not a number, return the string as-is (e.g., for department)
        return value


sample_rule = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
ast = create_rule(sample_rule)
#print_ast(ast)
print("AST", type(ast))
data = {
    "age": 35,
    "department": "Marketing",
    "salary": 10000,
    "experience": 6
}

result = evaluate_rule(ast, data)
print(result)

def count_operators(node, operator_count):
    """
    Recursively count the occurrences of AND/OR operators in the AST.
    
    Args:
    - node: The current AST node.
    - operator_count: Dictionary to keep track of the frequency of 'AND' and 'OR' operators.
    """
    if node is None:
        return
    
    if node.type == 'operator':
        operator_count[node.value] += 1
        count_operators(node.left, operator_count)
        count_operators(node.right, operator_count)


def merge_common_subtrees(ast1, ast2):
    """
    Merge two ASTs, ensuring common subtrees are only included once.
    
    Args:
    - ast1: The first AST.
    - ast2: The second AST.
    
    Returns:
    - The merged AST with common subtrees combined.
    """
    if ast1 is None:
        return ast2
    if ast2 is None:
        return ast1

    # If both nodes are identical (same type and value), we return one of them
    if ast1.type == ast2.type and ast1.value == ast2.value:
        return Node(type=ast1.type, value=ast1.value, left=merge_common_subtrees(ast1.left, ast2.left), right=merge_common_subtrees(ast1.right, ast2.right))
    
    # Otherwise, we return a new OR node combining both
    return Node(type='operator', value='OR', left=ast1, right=ast2)


def select_most_frequent_operator(operator_count):
    """
    Select the most frequent operator ('AND' or 'OR') based on their counts.
    
    Args:
    - operator_count: Dictionary with counts of 'AND' and 'OR'.
    
    Returns:
    - The operator that occurs most frequently.
    """
    return 'AND' if operator_count['AND'] > operator_count['OR'] else 'OR'


def combine_rules_with_heuristic(rules):
    """
    Combine a list of rule strings into a single AST, considering redundancy and operator frequencies.
    
    Args:
    - rules: A list of rule strings.
    
    Returns:
    - The root node of the combined AST.
    """
    if not rules:
        return None  # No rules to combine

    # Step 1: Build individual ASTs for each rule
    asts = [build_ast(tokenize(rule)) for rule in rules]

    # Step 2: Count operator frequencies in all rules
    operator_count = {'AND': 0, 'OR': 0}
    for ast in asts:
        count_operators(ast, operator_count)

    # Step 3: Select the most frequent operator (AND or OR)
    frequent_operator = select_most_frequent_operator(operator_count)
    
    # Step 4: Combine the ASTs with the selected operator and merge common subtrees
    combined_ast = asts[0]
    for ast in asts[1:]:
        combined_ast = Node(type='operator', value=frequent_operator, left=combined_ast, right=merge_common_subtrees(combined_ast, ast))
    
    return combined_ast


rules = [
    "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
    "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
]
combined_ast = combine_rules_with_heuristic(rules)
print_ast(combined_ast)