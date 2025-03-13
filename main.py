from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage (no database)
messages = []
gigs = [{"title": "Web Development", "price": 50}]  # Sample gig
balance = 500  # Sample balance

@app.route('/')
def index():
    return render_template('index.html', gigs=gigs, balance=balance, messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get("message")

    if message:
        messages.append({"text": message, "type": "sent"})
        return jsonify({"status": "success", "message": message})
    
    return jsonify({"status": "error", "message": "No message provided"}), 400

@app.route('/create_gig', methods=['POST'])
def create_gig():
    data = request.json
    title = data.get("title")
    price = data.get("price")

    if title and price:
        gigs.append({"title": title, "price": float(price)})
        return jsonify({"status": "success", "gig": {"title": title, "price": price}})
    
    return jsonify({"status": "error", "message": "Invalid gig details"}), 400

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global balance
    data = request.json
    amount = float(data.get("amount", 0))

    if amount <= 0:
        return jsonify({"status": "error", "message": "Enter a valid amount"}), 400
    if amount > balance:
        return jsonify({"status": "error", "message": "Insufficient balance"}), 400

    balance -= amount
    return jsonify({"status": "success", "new_balance": balance})

if __name__ == '__main__':
    app.run(debug=True)
