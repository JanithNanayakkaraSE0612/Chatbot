from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
#key improvements:
# Fixed chat_history_ids being undefined by initializing it globally.
#  Removed unnecessary loop (for step in range(5)).
#  Replaced request.form["msg"] with request.get_json() for better request handling.
#  Wrapped responses in jsonify() for proper API communication.
# Added debug=True for better debugging in development mode.
# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route("/")
def index():
    return render_template('index.html')

# Chatbot API route
@app.route("/get", methods=["POST"])
def chat():
    data = request.get_json()  # Expecting JSON input
    msg = data.get("msg", "")  # Get "msg" safely

    if not msg:
        return jsonify({"response": "Please enter a message."})

    response = get_Chat_response(msg)
    return jsonify({"response": response})

# Chatbot response function
from flask import session  # Import session for per-user data

def get_Chat_response(text):
    chat_history_ids = session.get('chat_history_ids', None)  # Retrieve per-session chat history

    # Encode user input
    new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')

    # Append to chat history or initialize it
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids  # First message

    # Generate response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    session['chat_history_ids'] = chat_history_ids  # Save chat history back to session

    # Decode response
    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
