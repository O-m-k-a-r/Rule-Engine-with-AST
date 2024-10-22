const apiBaseUrl = "http://localhost:5000"; // backend URL
let ruleAstRootNode = null;

function generateUniqueId() {
    return 'rule-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
}

// Create Rule
function createRule() {
    const rule = document.getElementById("rule").value;
    const ruleId = generateUniqueId();
    fetch(`${apiBaseUrl}/create_rule`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rule: rule, id: ruleId }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Rule created:', data);
        localStorage.setItem('ruleId', ruleId);
        ruleAstRootNode = data.rule_ast;
        document.getElementById("astOutput").textContent = JSON.stringify(data, null, 2);
    })
    .catch(err => {
        console.error("Error creating rule:", err);
    });
}


function evaluateRule() {
    const data = JSON.parse(document.getElementById("data").value);
    const ruleId = localStorage.getItem('ruleId');
    if (!ruleAstRootNode) {
        console.error("No rule AST found. Please create a rule first.");
        return;
    }
    console.log("Sending data to evaluate:", data);
    console.log("RootNode:",ruleAstRootNode);
    fetch(`${apiBaseUrl}/evaluate_rule`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data, rule_id: ruleId })
    })
    .then(response => response.json())
    .then(result => {
        console.log("Received result:", result);
        document.getElementById("resultOutput").textContent = result.result ? "Rule Passed!" : "Rule Failed.";
    })
    .catch(err => {
        console.error("Error evaluating rule:", err);
    });
}


function combineRules() {
    const rules = document.getElementById("rulesList").value.split("\n");

    fetch(`${apiBaseUrl}/combine_rules`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rules })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("combinedAstOutput").textContent = JSON.stringify(data, null, 2);
    })
    .catch(err => {
        console.error("Error combining rules:", err);
    });
}
