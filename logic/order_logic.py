import json
import os

# Load menu.json once at module load
MENU_PATH = os.path.join(os.path.dirname(__file__), '..', 'menu.json')
with open(MENU_PATH, 'r') as f:
    MENU = json.load(f)['menu']

def handle_order(intent, parameters):
    if intent == "OrderBurger":
        burger_type = parameters.get("burger_type")
        quantity = parameters.get("number")
        burgers = [item['name'] for item in MENU.get('Juniors', [])]
        if burger_type and quantity:
            if burger_type in burgers:
                price = next(item['price'] for item in MENU['Juniors'] if item['name'] == burger_type)
                total = int(quantity) * price
                return f"Okay, {int(quantity)} {burger_type} burgers coming right up! Your total is ${total:.2f}."
            else:
                return f"Sorry, we don't have {burger_type}. Our burgers are: {', '.join(burgers)}."
        else:
            return f"What kind of burger and how many would you like? Our burgers are: {', '.join(burgers)}."
    elif intent == "RequestMenu":
        burgers = [item['name'] for item in MENU.get('Juniors', [])]
        return f"Our burger menu: {', '.join(burgers)}. What would you like to order?"
    elif intent == "AddSide":
        side_dish = parameters.get("side_dish")
        if side_dish:
            return f"Adding a {side_dish} to your order."
        else:
            return "What side would you like to add?"
    elif intent == "CompleteOrder":
        return "Your total is $12.50. Please proceed to the window."
    elif intent == "DefaultWelcomeIntent":
        return "Welcome to the Drive-Thru"
    else:
        return "Sorry, I didn't understand that.  Can you please repeat?" 