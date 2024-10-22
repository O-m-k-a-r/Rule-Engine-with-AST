from flask import Flask, request, jsonify
from flask_cors import CORS
from rule import create_rule, combine_rules_with_heuristic, evaluate_rule, evaluate_condition, parse_value, Node

app = Flask(__name__)
CORS(app)

rule_storage = {}
@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json['rule']
    rule_id = request.json.get('id')
    root_node = create_rule(rule_string)  # This is from rule.py
    print("ROOT TYPE:", type(root_node))
    rule_storage[rule_id] = root_node
    return jsonify({'message': 'Rule created successfully', 'rule_ast': str(root_node)})


@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    rules = request.json['rules']
    combined_ast = combine_rules_with_heuristic(rules)  
    return jsonify({'message': 'Rules combined successfully', 'combined_ast': str(combined_ast)})


@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    
    data = request.json.get('data', None)
    rule_id = request.json.get('rule_id')
    rule_ast = rule_storage.get(rule_id)
    
    
    if not rule_ast or not data:
        return jsonify({'error': 'Missing rule_ast or data'}), 400
    print(f"Data received for evaluation: {data}")  
    result = evaluate_rule(rule_ast, data)  
    print(f"Evaluation result: {result}")
    return jsonify({'result': result}),200

if __name__ == '__main__':
    app.run(debug=True)