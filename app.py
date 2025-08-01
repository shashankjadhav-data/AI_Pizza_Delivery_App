from flask import Flask, render_template, request, jsonify, session
import requests
import re
import json
import time

app = Flask(__name__)
app.secret_key = 'pizza_secret_123'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Enhanced pizza menu with sizes and prices
PIZZA_MENU = {
    "Margherita": {
        "Small": 9.99,
        "Medium": 12.99,
        "Large": 15.99
    },
    "Pepperoni": {
        "Small": 11.99,
        "Medium": 14.99,
        "Large": 17.99
    },
    "Vegetarian": {
        "Small": 10.99,
        "Medium": 13.99,
        "Large": 16.99
    },
    "Supreme": {
        "Small": 12.99,
        "Medium": 15.99,
        "Large": 18.99
    },
    "Hawaiian": {
        "Small": 11.49,
        "Medium": 14.49,
        "Large": 17.49
    }
}

# Define extra toppings
TOPPINGS = {
    "Extra cheese": 1.50,
    "Mushrooms": 1.00,
    "Olives": 0.75,
    "Peppers": 0.75,
    "Onions": 0.50,
    "Sausage": 1.25,
    "Bacon": 1.75
}

# Define special options
SPECIAL_OPTIONS = ["Vegan", "Gluten-free", "Halal", "Extra spicy", "Light sauce"]

SYSTEM_PROMPT = f"""
You are an AI assistant for Pizza Palace taking pizza orders. Follow this EXACT flow:

1. FIRST greet: "Welcome to Pizza Palace! What pizza would you like? Options: {', '.join(PIZZA_MENU.keys())}"

2. AFTER pizza is selected (must be one of {list(PIZZA_MENU.keys())}), ask: 
"What size for your [SELECTED_PIZZA]? (Small/Medium/Large)"

3. AFTER size is given, ask:
"Any toppings from: {', '.join(TOPPINGS.keys())}? (comma separated)"

4. AFTER toppings, ask:
"Any special requests? (e.g., {', '.join(SPECIAL_OPTIONS)}, allergies, etc.)"

5. AFTER requests, ask:
"Please provide delivery address"

6. AFTER address, summarize and ask:
"Confirm order? (yes/no)"

7. ONLY AFTER 'yes', output:
[ORDER_COMPLETE]
{{
    "pizzas": [{{"name": "[SELECTED_PIZZA]", "size": "[SIZE]", "quantity": 1}}],
    "toppings": ["SELECTED_TOPPINGS"],
    "special_requests": ["REQUESTS"],
    "address": "FULL_ADDRESS"
}}
[/ORDER_COMPLETE]

STRICT RULES:
- Ask ONE question at a time
- WAIT for response before next question
- Store ALL selections in session
- Validate toppings against menu
- Capture ALL special requests
"""

def get_ollama_response(messages):
    payload = {
        "model": "mistral:7b",
        "messages": messages,
        "stream": False
    }
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def extract_order_data(response_text):
    """Extract structured order from AI response"""
    match = re.search(r'\[ORDER_COMPLETE\](.*?)\[\/ORDER_COMPLETE\]', response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    return None

def calculate_total(order_data):
    """Calculate order total based on menu prices"""
    if not order_data:
        return 0.0
    
    total = 0.0
    for pizza in order_data.get("pizzas", []):
        if pizza["name"] in PIZZA_MENU and pizza["size"] in PIZZA_MENU[pizza["name"]]:
            total += PIZZA_MENU[pizza["name"]][pizza["size"]] * pizza.get("quantity", 1)
    
    for topping in order_data.get("toppings", []):
        if topping in TOPPINGS:
            total += TOPPINGS[topping]
    
    return round(total, 2)

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip().lower()
    
    if 'history' not in session:
        session['history'] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": f"Welcome to Pizza Palace! What pizza would you like? Options: {', '.join(PIZZA_MENU.keys())}"}
        ]
        session['current_step'] = 'pizza_selection'
        session['toppings'] = []
        session['special_requests'] = []
        session.modified = True
        return jsonify({
            "response": session['history'][-1]['content'],
            "order": None
        })
    
    session['history'].append({"role": "user", "content": user_input})
    
    current_step = session.get('current_step', 'pizza_selection')
    response = ""
    
    if current_step == 'pizza_selection':
        selected_pizza = next((pizza for pizza in PIZZA_MENU.keys() 
                             if pizza.lower() in user_input), None)
        if not selected_pizza:
            response = f"Please select a pizza from: {', '.join(PIZZA_MENU.keys())}"
        else:
            session['selected_pizza'] = selected_pizza
            session['current_step'] = 'size_selection'
            response = f"What size for your {selected_pizza}? (Small/Medium/Large)"
    
    elif current_step == 'size_selection':
        size = next((s for s in ['small', 'medium', 'large'] 
                    if s in user_input), None)
        if not size:
            response = "Please choose: Small, Medium, or Large"
        else:
            session['selected_size'] = size.capitalize()
            session['current_step'] = 'toppings'
            response = f"Add toppings (comma separated): {', '.join(TOPPINGS.keys())}"
    
    elif current_step == 'toppings':
        selected_toppings = []
        for topping in TOPPINGS.keys():
            if topping.lower() in user_input:
                selected_toppings.append(topping)
        
        session['toppings'] = selected_toppings
        session['current_step'] = 'special_requests'
        response = f"Any special requests? (e.g., {', '.join(SPECIAL_OPTIONS)}, allergies)"
    
    elif current_step == 'special_requests':
        selected_requests = []
        for req in SPECIAL_OPTIONS:
            if req.lower() in user_input:
                selected_requests.append(req)
        
        if 'allerg' in user_input:
            selected_requests.append(f"Allergy note: {user_input}")
            
        session['special_requests'] = selected_requests
        session['current_step'] = 'address'
        response = "Please provide your delivery address"
    
    elif current_step == 'address':
        if len(user_input) < 10:
            response = "Please provide a complete address"
        else:
            session['address'] = user_input
            session['current_step'] = 'confirmation'
            
            summary = f"""Your Order:
- Pizza: {session['selected_pizza']} ({session['selected_size']})
- Toppings: {', '.join(session['toppings']) or 'None'}
- Special Requests: {', '.join(session['special_requests']) or 'None'}
- Address: {session['address']}

Total: ${calculate_total({
                'pizzas': [{'name': session['selected_pizza'], 'size': session['selected_size'], 'quantity': 1}],
                'toppings': session['toppings'],
                'special_requests': session['special_requests']
            })}

Confirm (yes/no)?"""
            response = summary
    
    elif current_step == 'confirmation':
        if 'yes' in user_input:
            order_data = {
                "pizzas": [{
                    "name": session['selected_pizza'],
                    "size": session['selected_size'],
                    "quantity": 1
                }],
                "toppings": session['toppings'],
                "special_requests": session['special_requests'],
                "address": session['address']
            }
            order_data["total"] = calculate_total(order_data)
            response = f"[ORDER_COMPLETE]\n{json.dumps(order_data, indent=2)}\n[/ORDER_COMPLETE]"
            session['current_order'] = order_data
        else:
            response = "What would you like to change?"
            session['current_step'] = 'pizza_selection'
    
    session['history'].append({"role": "assistant", "content": response})
    session.modified = True
    
    order_data = extract_order_data(response)
    if order_data:
        order_data["total"] = calculate_total(order_data)
        return jsonify({
            "response": response,
            "order": order_data
        })
    
    return jsonify({
        "response": response,
        "order": None
    })

@app.route('/confirm', methods=['POST'])
def confirm_order():
    order_data = request.json
    print("Confirmed Order:", json.dumps(order_data, indent=2))
    return jsonify({
        "status": "success",
        "message": "Order confirmed! Your pizza will arrive in 30 minutes."
    })

@app.route('/manual-confirm', methods=['POST'])
def manual_confirm():
    if 'current_order' not in session:
        return jsonify({"status": "error", "message": "No order to confirm"})
    
    order_data = session['current_order']
    print("Manually Confirmed Order:", json.dumps(order_data, indent=2))
    return jsonify({
        "status": "success",
        "message": "Order manually confirmed! Your pizza will arrive in 30 minutes."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
