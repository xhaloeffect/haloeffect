from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Stan aplikacji
claimed = False  # Czy nagroda została odebrana
winner_address = None  # Adres zwycięzcy

# Strona główna z formularzem HTML
@app.route('/')
def home():
    return '''
        <h1>Congrats!</h1>
        <p>(Use Solana wallet below) Use the form below to claim the reward. Here's your first prize - 25$. There's a very small incentive on it to continue working
         on puzzles. Stay tuned for more puzzles on Twitter. Good luck!</p>
        <form action="/claim" method="post">
            <input type="text" name="address" placeholder="Enter your wallet address" required>
            <button type="submit">Submit</button>
        </form>
        <p>Check reward status: <a href="/status">/status</a></p>
    '''

# Endpoint do zgłoszenia adresu
@app.route('/claim', methods=['POST'])
def claim():
    global claimed, winner_address

    # Sprawdzanie, czy nagroda została już odebrana
    if claimed:
        return '''
            <h1>Reward already claimed!</h1>
            <p>The reward has already been claimed. Check the status <a href="/status">here</a>.</p>
        ''', 400

    # Pobranie adresu portfela z formularza
    wallet_address = request.form.get('address')

    if not wallet_address:
        return '''
            <h1>Error!</h1>
            <p>No wallet address provided. Please go back and try again.</p>
        ''', 400

    # Zapisanie adresu jako zwycięzcy i oznaczenie nagrody jako odebranej
    winner_address = wallet_address
    claimed = True
    return f'''
        <h1>Success!</h1>
        <p>Congratulations! You've claimed the reward.</p>
        <p>Your wallet address: {winner_address}</p>
        <p>Check the status <a href="/status">here</a>.</p>
    '''

# Endpoint do sprawdzenia statusu
@app.route('/status', methods=['GET'])
def status():
    if claimed:
        return jsonify({"status": "claimed", "winner": winner_address}), 200
    return jsonify({"status": "available"}), 200

if __name__ == "__main__":
    # Dynamiczny port i adres hosta wymagany przez Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
