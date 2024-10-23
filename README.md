# Rule Engine with Flask and Abstract Syntax Tree
This project is a simple 3-tier rule engine application that allows users to create, combine, and evaluate rules using an Abstract Syntax Tree (AST). It includes a frontend (HTML/CSS/JS), backend (Flask), and rule-processing logic. The rule engine supports rule creation, combination using heuristics, and efficient rule evaluation.

## Project Structure

```.
├── Frontend
│   ├── index.html
│   ├── style.css
│   └── script.js
├── Backend
│   ├── app.py           # Flask app (API backend)
│   ├── rule.py          # Rule engine implementation (AST creation, combination, evaluation)
│   ├── requirements.txt # Project dependencies
└── README.md
```

## Features
+ **Rule Creation:** Allows creating rules based on attributes (e.g., `age > 30`, `department = 'Sales'`, `salary = 50000` and `experience = 5`) using an AST and returns the `Root Node` of AST formed.
+ **Rule Combination:** Supports combining rules with a heuristic to minimize redundant checks and returns the `Root Node` of the combined AST.
+ **Rule Evaluation:** Evaluates the combined rule against provided data and states it as `True` or `False`.
+ **Frontend:** A basic HTML form to interact with the rule engine (create, combine, and evaluate rules).
+ **Backend:** Flask API that handles rule management and processing.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-CORS

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/O-m-k-a-r/Rule-Engine-with-AST.git
   cd Rule-Engine-with-AST
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
### Running the Application
1. Start the Flask server:

```
cd .\backend\
python app.py
```
2. Start the frontend:
```
cd .\frontend\
```
Click on `Go Live` to start frontend

## Example UI Workflow:
+ **Create Rule:** Input a rule and submit it to create an AST.
  ```
  ((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)
  ```
+ **Combine Rules:** Input multiple rules to combine them into one AST.
  ```
  ((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)
  ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
  ```
+ **Evaluate Rule:** Input data and select a rule to evaluate it.
  ```
  {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
  ```
